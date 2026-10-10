#!/usr/bin/env bash
set -euo pipefail
command -v npm >/dev/null || { echo 'Node/npm is required' >&2; exit 2; }
[[ $# -ge 1 ]] || { echo 'usage: render.sh <project-dir>' >&2; exit 2; }
cd "$1"
npm run render
