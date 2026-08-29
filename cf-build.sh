#!/usr/bin/env bash
# What Cloudflare Workers Builds runs. The dashboard's build command is
# `bash cf-build.sh` and nothing else, so the steps live here, in git, where
# they are reviewable in a diff and cannot drift from the code they build.
#
# They used to live in the dashboard field itself. On 2026-08-28 that field
# still held the pre-R2 command after the dataset left git, and three builds
# failed against a repository that no longer carried data/wines.json — a
# mismatch invisible from the code and from any diff.
#
# It sits at the repository root rather than in deploy/ because the build's
# watch paths exclude /deploy, and a fix to this file must trigger the build
# that tests it.
set -euo pipefail

# A Worker rejects a deployment over 20 000 static assets on the free plan, and
# the build grows with the assortment. Failing here with the number is cheaper
# than a rejected upload with a generic message. This counts files; wrangler
# counts registered paths, roughly twice as many, because every index.html is
# also reachable at its pretty URL — see issue #17. Treat it as a conservative
# tripwire, not as the real ceiling.
ASSET_LIMIT="${ASSET_LIMIT:-19000}"

# The dataset is not in git. The site's own bucket serves it; the rolling
# release is the fallback for when the bucket is unreachable. Overridable so a
# fork, or a local run, can build against its own copy.
DATA_URL="${DATA_URL:-https://vindeklaration.se/data/wines.json.gz}"
RELEASE_URL="${RELEASE_URL:-https://github.com/matalve/vindeklaration/releases/download/dataset-latest/wines.json.gz}"

# Decompress to a temporary file and move it into place only on success: a
# truncated transfer must not leave a half-written dataset that the build then
# renders 15 000 pages from.
fetch_dataset() {
  local url="$1" tmp
  tmp="$(mktemp)"
  if curl -fsSL --retry 3 "$url" | gunzip > "$tmp"; then
    mv "$tmp" data/wines.json
    return 0
  fi
  rm -f "$tmp"
  return 1
}

echo "== fetching the dataset"
mkdir -p data
if fetch_dataset "$DATA_URL"; then
  echo "   from $DATA_URL"
elif fetch_dataset "$RELEASE_URL"; then
  echo "   bucket unreachable; fell back to the rolling release"
else
  echo "::error::could not fetch the dataset from either source" >&2
  exit 1
fi

# Cloudflare's image has no uv; a GitHub runner installs it as an action, and a
# laptop already has it. Only pay for the install where it is actually missing.
if command -v uv >/dev/null 2>&1; then
  echo "== uv already present"
else
  echo "== installing uv"
  pip install uv
fi

echo "== building the site"
uv run python -m src.site

count="$(find site -type f | wc -l)"
echo "== $count files in site/"
if [ "$count" -gt "$ASSET_LIMIT" ]; then
  echo "::error::$count files exceeds the $ASSET_LIMIT guard — a Worker allows" >&2
  echo "  20 000 static assets. See \"Bilingual\" in docs/site-plan.md for what" >&2
  echo "  to do when this trips, and issue #17 on what the limit really counts." >&2
  exit 1
fi
