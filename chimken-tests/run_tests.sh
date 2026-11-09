#!/usr/bin/env bash
# Runs the ChimkenMuziks tests on a private D-Bus session bus.
#   ./run_tests.sh                 everything
#   ./run_tests.sh -k pause -vv    filter / verbose
#   APP_REPO=Project/ChimkenMuziks APP_START_ARGS="--song {song}" ./run_tests.sh
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d .venv ]; then
    echo "No .venv here. Creating it first:" >&2
    python -m venv .venv && .venv/bin/pip install -r requirements-test.txt
fi
source .venv/bin/activate

Here="$(pwd)"

export DEBUG_OBJECT_PATH="/org/ChimkenMuziks"
export APP_REPO=$Here/../

echo "$@"
# Everything runs on a private session bus. The variable is set inside the session (after
# the bus exists) so the app's sdbus connects to it, not to the system bus.
exec dbus-run-session -- env DBUS_STARTER_BUS_TYPE=session python -m pytest "$@"
