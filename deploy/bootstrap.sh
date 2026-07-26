#!/usr/bin/env bash
# Prepare a Raspberry Pi (or any Linux box) to run the pipeline unattended.
# Run this ON the Pi, from the repository root:
#
#   ./deploy/bootstrap.sh
#
# It installs uv, sets up the virtualenv, installs the timer, and reports
# anything it could not do. It does not fetch any data.
set -euo pipefail

cd "$(dirname "$0")/.."
REPO="$PWD"

echo "== Host"
uname -srm
if [ -r /etc/os-release ]; then . /etc/os-release; echo "$PRETTY_NAME"; fi

case "$(uname -m)" in
  aarch64|x86_64) ;;
  armv7l|armv6l)
    echo
    echo "NOTE: this is a 32-bit userland. There are no prebuilt wheels for"
    echo "rapidfuzz on armv7, so 'uv sync' will compile it — expect several"
    echo "minutes and make sure you have swap. Everything else works."
    echo "If the Pi is 64-bit capable, reinstalling with the 64-bit image is"
    echo "the easier path."
    echo ;;
  *) echo "Unrecognised architecture; continuing anyway." ;;
esac

echo
echo "== uv"
if ! command -v uv >/dev/null; then
  echo "Installing uv..."
  curl -fsSL https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi
uv --version

echo
echo "== Dependencies"
uv sync
uv run python -c "import httpx, yaml, rapidfuzz; print('imports ok')"

echo
echo "== Tests"
uv run pytest -q

echo
echo "== Timer"
mkdir -p "$HOME/.config/systemd/user"
for unit in wine-additives.service wine-additives.timer; do
  sed "s|__REPO__|$REPO|g; s|__UV__|$(command -v uv)|g" "deploy/$unit" \
    > "$HOME/.config/systemd/user/$unit"
  echo "installed ~/.config/systemd/user/$unit"
done
systemctl --user daemon-reload
systemctl --user enable --now wine-additives.timer
systemctl --user list-timers wine-additives.timer --no-pager || true

echo
if [ "$(loginctl show-user "$USER" -p Linger --value 2>/dev/null || echo no)" != "yes" ]; then
  cat <<'EOF'
== One step left, and it needs sudo

User services normally stop when you log out, which would stop the nightly
update on a headless Pi. "Lingering" keeps them running. Run:

    sudo loginctl enable-linger $USER

That is the only privileged change this deployment needs.
EOF
else
  echo "== Lingering already enabled — the timer survives logout."
fi

echo
echo "Done. Run one update by hand with:  systemctl --user start wine-additives.service"
echo "Follow it with:                     journalctl --user -u wine-additives -f"
