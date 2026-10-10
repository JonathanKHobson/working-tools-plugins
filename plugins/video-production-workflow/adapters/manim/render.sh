#!/usr/bin/env bash
set -euo pipefail
command -v manim >/dev/null || { echo 'Manim is required in the active environment' >&2; exit 2; }
[[ $# -ge 2 ]] || { echo 'usage: render.sh <scene.py> <SceneName> [quality]' >&2; exit 2; }
SCENE="$1"; NAME="$2"; QUALITY="${3:--qh}"
manim "$QUALITY" "$SCENE" "$NAME"
