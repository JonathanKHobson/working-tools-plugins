#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"
"$PYTHON" -m venv "$ROOT/.venv"
# shellcheck disable=SC1091
source "$ROOT/.venv/bin/activate"
python -m pip install --upgrade pip
python -m pip install -e "$ROOT[audio,dev]"
video-workflow check
cat <<'EOF'
Baseline installation complete.
Required external tools: ffmpeg and ffprobe.
Optional extras are documented in skills/install-video-toolchain/references/.
EOF
