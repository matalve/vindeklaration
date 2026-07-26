#!/usr/bin/env bash
# One full update cycle. Called by the systemd timer, and safe to run by hand.
#
# Sunday re-fetches every declaration; other days only fetch wines that are not
# cached yet. The fetch is resumable, so an interrupted run loses nothing.
set -euo pipefail

cd "$(dirname "$0")/.."
UV="${UV:-$(command -v uv)}"

echo "=== $(date -Is) starting update"

# Code arrives from GitHub, data leaves for it. Pull before crawling: a machine
# left behind on an old additives.yaml spends the whole night producing
# declarations it cannot read, which is exactly what happened on 2026-07-26.
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

# The report exits non-zero when too many declarations went unread. That is
# information, not a reason to throw away the dataset we just built, so the
# exit code is recorded rather than propagated.
if "$UV" run python -m src.report; then
  echo "=== quality gate passed"
else
  echo "=== quality gate FAILED — see the unknown tokens above and data/unknown.json"
fi

if git rev-parse --git-dir >/dev/null 2>&1; then
  # wines.sqlite is deliberately absent: it is a binary that git cannot delta,
  # and src/build.py regenerates it from wines.json in seconds.
  git add data/wines.json data/catalog.json data/unknown.json
  if git diff --staged --quiet; then
    echo "=== dataset unchanged"
  else
    git -c user.name="vindeklaration-bot" \
        -c user.email="vindeklaration-bot@localhost" \
        commit -q -m "Update dataset $(date -u +%Y-%m-%d)"
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
