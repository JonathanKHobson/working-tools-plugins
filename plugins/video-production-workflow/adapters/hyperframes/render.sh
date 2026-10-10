#!/usr/bin/env bash
set -euo pipefail
command -v npx >/dev/null || { echo 'Node/npx is required' >&2; exit 2; }
[[ $# -ge 2 ]] || { echo 'usage: render.sh <project-dir> <output>' >&2; exit 2; }
PROJECT="$1"; OUTPUT="$2"
cd "$PROJECT"
# Adapt this command to the current HyperFrames project API after reviewing its live documentation.
npx hyperframes render --output "$OUTPUT"
