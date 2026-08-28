#!/usr/bin/env bash
# One full update cycle. Called by the systemd timer, and safe to run by hand.
#
# Sunday re-fetches every declaration; other days only fetch wines that are not
# cached yet. The fetch is resumable, so an interrupted run loses nothing.
set -euo pipefail

cd "$(dirname "$0")/.."
UV="${UV:-$(command -v uv)}"

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
wrangler r2 object put vindeklaration-data/wines.json.gz \
  --file data/wines.json.gz --content-type application/gzip
wrangler r2 object put vindeklaration-data/catalog.json.gz \
  --file data/catalog.json.gz --content-type application/gzip
echo "=== published to R2"

# Rolling release: same asset names, overwritten nightly, so the download URL
# is stable. --clobber is the point. Needs `gh auth login` on the runner.
gh release view dataset-latest >/dev/null 2>&1 \
  || gh release create dataset-latest \
       --title "Latest dataset" \
       --notes "Nightly build, overwritten every night. Monthly snapshots live in their own releases."
gh release upload dataset-latest data/wines.json.gz data/catalog.json.gz --clobber
echo "=== published to the dataset-latest release"

# Frozen snapshot on the first Sunday of the month, for reproducibility —
# with the dataset out of git, history no longer answers "what did the
# assortment look like in spring".
if [ "$(date +%u)" = "7" ] && [ "$(date +%d)" -le 7 ]; then
  tag="dataset-$(date -u +%Y-%m)"
  gh release view "$tag" >/dev/null 2>&1 \
    || gh release create "$tag" data/wines.json.gz data/catalog.json.gz \
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
