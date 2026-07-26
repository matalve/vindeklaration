#!/usr/bin/env bash
# Copy this working tree to the Pi. Run from the Mac, in the repository root:
#
#   ./deploy/push-to-pi.sh [user@host] [remote-path]
#
# The already-fetched declarations in data/cache go along, so the Pi resumes the
# fetch instead of starting over. Nothing is deleted on either side except stale
# copies of files this repo owns.
set -euo pipefail

cd "$(dirname "$0")/.."
TARGET="${1:-pi@raspberrypi}"
REMOTE="${2:-wine-additives}"

echo "== Sending $(ls data/cache 2>/dev/null | wc -l | tr -d ' ') cached declarations to $TARGET:$REMOTE"

# Two passes on purpose.
#
# The first replaces code and configuration, --delete included, so a file
# removed here is removed there. It must never touch data/: the remote is the
# machine that does the fetching, so its cache is almost always ahead of this
# one, and --delete once destroyed eleven thousand fetched declarations here.
#
# --progress, not --info=progress2: macOS ships openrsync, which speaks the
# rsync 2.6.9 flag set and does not know the newer option.
rsync -az --progress --delete \
  --exclude '.venv/' \
  --exclude '__pycache__/' \
  --exclude '.pytest_cache/' \
  --exclude 'data/' \
  ./ "$TARGET:$REMOTE/"

# The second adds data, never deleting. Entries the remote has and we do not
# are exactly the work it has done since the last push.
rsync -az --progress \
  ./data/ "$TARGET:$REMOTE/data/"

cat <<EOF

Sent. Next, on the Pi:

    ssh $TARGET
    cd $REMOTE
    ./deploy/bootstrap.sh

To pull the finished dataset back here later:

    rsync -az $TARGET:$REMOTE/data/{wines.json,wines.sqlite,unknown.json} data/
EOF
