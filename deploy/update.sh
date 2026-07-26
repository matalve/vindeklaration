#!/usr/bin/env bash
# One full update cycle. Called by the systemd timer, and safe to run by hand.
#
# Sunday re-fetches every declaration; other days only fetch wines that are not
# cached yet. The fetch is resumable, so an interrupted run loses nothing.
set -euo pipefail

cd "$(dirname "$0")/.."
UV="${UV:-$(command -v uv)}"

echo "=== $(date -Is) starting update"

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
  git add data/wines.json data/wines.sqlite data/catalog.json data/unknown.json
  if git diff --staged --quiet; then
    echo "=== dataset unchanged"
  else
    git -c user.name="vindeklaration-bot" \
        -c user.email="vindeklaration-bot@localhost" \
        commit -q -m "Update dataset $(date -u +%Y-%m-%d)"
    echo "=== committed $(git rev-parse --short HEAD)"
  fi
fi

echo "=== $(date -Is) finished"
