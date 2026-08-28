#!/usr/bin/env bash
# One full update cycle. Called by the systemd timer, and safe to run by hand.
#
# Sunday re-fetches every declaration; other days only fetch wines that are not
# cached yet. The fetch is resumable, so an interrupted run loses nothing.
set -euo pipefail

cd "$(dirname "$0")/.."
UV="${UV:-$(command -v uv)}"

# Publishing happens at the very end, after roughly three and a half hours of
# crawling. Resolve everything it needs now, so a missing tool costs a second
# instead of a night's work that is then thrown away undelivered.
#
# systemd's PATH is minimal — that is why UV is an absolute path above — so
# bare `wrangler` and `gh` are not enough. Wrangler falls back to npx because
# the crawler has no global install; the major version is pinned so a release
# cannot change the upload behaviour unannounced.
WRANGLER="${WRANGLER:-$(command -v wrangler || echo "npx --yes wrangler@4")}"
GH="${GH:-$(command -v gh || true)}"

if [ -z "$GH" ]; then
  echo "=== gh not found — it uploads the dataset release. Install it, or set GH." >&2
  exit 1
fi
if ! $GH auth status >/dev/null 2>&1; then
  echo "=== gh is not logged in — run 'gh auth login' on this machine." >&2
  exit 1
fi
if [ -z "${CLOUDFLARE_API_TOKEN:-}" ] || [ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]; then
  echo "=== CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID must be set for the" >&2
  echo "    R2 upload; see \"The dataset lives in R2, not git\" in" >&2
  echo "    docs/deploy-site.md for where the timer reads them from." >&2
  exit 1
fi

echo "=== $(date -Is) starting update"

# Code arrives from GitHub, data leaves for R2 and Releases. Pull before
# crawling: a machine left behind on an old additives.yaml spends the whole
# night producing declarations it cannot read, which is exactly what happened
# on 2026-07-26.
if git rev-parse --git-dir >/dev/null 2>&1; then
  if git pull --ff-only --quiet 2>/dev/null; then
    echo "=== pulled, now at $(git rev-parse --short HEAD)"
  elif git pull --rebase --autostash --quiet 2>/dev/null; then
    echo "=== pulled and rebased local commits, now at $(git rev-parse --short HEAD)"
  else
    echo "=== pull failed — running with the code that is already here"
  fi
fi

"$UV" run python -m src.catalog

# How much of the catalog has ever been fetched? A full refresh is pointless
# before the first pass has finished — finish it instead.
CATALOG=$("$UV" run python -c "import json;print(len(json.load(open('data/catalog.json'))))")
CACHED=$(find data/cache -name '*.json' | wc -l | tr -d ' ')
echo "=== $CACHED of $CATALOG declarations already fetched"

if { [ "$(date +%u)" = "7" ] || [ "${FULL:-}" = "1" ]; } \
   && [ "$CACHED" -ge $((CATALOG * 95 / 100)) ]; then
  echo "=== weekly full refresh"
  "$UV" run python -m src.details --refresh
else
  "$UV" run python -m src.details
fi

"$UV" run python -m src.build
"$UV" run pytest -q

# The report exits non-zero when the share of unread declarations jumped since
# the last run. That is information, not a reason to throw away the dataset we
# just built, so the exit code is recorded rather than propagated. --record is
# passed here and nowhere else: this is the run the baseline should come from.
if "$UV" run python -m src.report --record; then
  echo "=== quality gate passed"
else
  echo "=== quality gate FAILED — the unread share rose; see data/unknown.json"
fi

# The dataset no longer travels through git: a 16 MB JSON committed nightly
# costs its near-full size in history, forever. It is published as build
# output instead — to the site's R2 bucket, and to a rolling GitHub release
# for everyone else. Publish BEFORE pushing: the push is what triggers the
# site rebuild, and the rebuild downloads the dataset from the bucket.
gzip -kf data/wines.json data/catalog.json

# Needs CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID in the timer's
# environment; see "The dataset lives in R2, not git" in docs/deploy-site.md.
#
# --remote is load-bearing: without it wrangler writes to the local simulator,
# prints "Resource location: local" and exits 0, so the bucket would stay
# empty while every run reported success. On this machine it fails louder —
# the local path starts workerd, which cannot allocate against ARM64's address
# space and dies with EPIPE — but do not rely on the crash to catch it.
$WRANGLER r2 object put vindeklaration-data/wines.json.gz --remote \
  --file data/wines.json.gz --content-type application/gzip
$WRANGLER r2 object put vindeklaration-data/catalog.json.gz --remote \
  --file data/catalog.json.gz --content-type application/gzip
echo "=== published to R2"

# Rolling release: same asset names, overwritten nightly, so the download URL
# is stable. --clobber is the point. Needs `gh auth login` on the runner.
$GH release view dataset-latest >/dev/null 2>&1 \
  || $GH release create dataset-latest \
       --title "Latest dataset" \
       --notes "Nightly build, overwritten every night. Monthly snapshots live in their own releases."
$GH release upload dataset-latest data/wines.json.gz data/catalog.json.gz --clobber
echo "=== published to the dataset-latest release"

# Frozen snapshot on the first Sunday of the month, for reproducibility —
# with the dataset out of git, history no longer answers "what did the
# assortment look like in spring".
if [ "$(date +%u)" = "7" ] && [ "$(date +%d)" -le 7 ]; then
  tag="dataset-$(date -u +%Y-%m)"
  $GH release view "$tag" >/dev/null 2>&1 \
    || $GH release create "$tag" data/wines.json.gz data/catalog.json.gz \
         --title "Dataset $(date -u +%Y-%m)" --notes "Monthly snapshot."
fi

# quality-history.json stays in git because the gate compares against it:
# lose it and the next run has no baseline and silently passes. unknown.json
# is small and worth reading in diffs. quality-history.json changes on every
# recorded run, so this commit is also what triggers the nightly site rebuild
# — which is why it must come after the R2 upload above.
if git rev-parse --git-dir >/dev/null 2>&1; then
  git add data/unknown.json data/quality-history.json
  if git diff --staged --quiet; then
    echo "=== nothing to commit"
  else
    git -c user.name="vindeklaration-bot" \
        -c user.email="vindeklaration-bot@localhost" \
        commit -q -m "Update quality history $(date -u +%Y-%m-%d)"
    echo "=== committed $(git rev-parse --short HEAD)"

    # A rejected push means code was pushed while we were fetching. Rebase this
    # commit on top and try once more. Never force: the remote is shared, and a
    # commit that stays here is picked up by the next run anyway.
    if git push --quiet origin HEAD:main 2>/dev/null; then
      echo "=== pushed to origin"
    elif git pull --rebase --quiet && git push --quiet origin HEAD:main 2>/dev/null; then
      echo "=== pushed to origin after rebase"
    else
      echo "=== push failed — the commit is safe here and goes with the next run"
    fi
  fi
fi

echo "=== $(date -Is) finished"
