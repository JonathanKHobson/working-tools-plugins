#!/usr/bin/env bash
set -euo pipefail
command -v npx >/dev/null || { echo 'Node/npx is required' >&2; exit 2; }
[[ $# -ge 3 ]] || { echo 'usage: render.sh <project-dir> <composition-id> <output>' >&2; exit 2; }
PROJECT="$1"; COMPOSITION="$2"; OUTPUT="$3"
cd "$PROJECT"
echo 'Verify the current Remotion license for this organization/use before rendering.' >&2
npx remotion render "$COMPOSITION" "$OUTPUT"
