#!/usr/bin/env bash
set -euo pipefail
command -v blender >/dev/null || { echo 'Blender is required' >&2; exit 2; }
[[ $# -ge 1 ]] || { echo 'usage: render.sh <scene.blend> [python-script]' >&2; exit 2; }
SCENE="$1"; SCRIPT="${2:-}"
if [[ -n "$SCRIPT" ]]; then blender -b "$SCENE" -P "$SCRIPT" -a; else blender -b "$SCENE" -a; fi
