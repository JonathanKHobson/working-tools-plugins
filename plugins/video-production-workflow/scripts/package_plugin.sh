#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"
if [[ "${SKIP_VERIFY:-0}" != "1" ]]; then
  "$PYTHON" "$ROOT/scripts/verify_release.py"
fi
VERSION="$("$PYTHON" -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$ROOT/.codex-plugin/plugin.json")"
"$PYTHON" "$ROOT/scripts/package_public.py" "${1:-$ROOT/../video-production-workflow-$VERSION.zip}"
