#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

render_variant() {
  local name="$1" width="$2" height="$3"
  local base="examples/multi-aspect-variants"
  mkdir -p "$base/output/$name" "$base/work/$name"
  python -m video_workflow.cli render "$base/$name.json" \
    --output "$base/output/$name/preview.mp4" \
    --work-dir "$base/work/$name"
  python -m video_workflow.cli qa "$base/output/$name/preview.mp4" \
    --width "$width" --height "$height" --duration 8 \
    --output "$base/output/$name/qa-report.json" --deep
  python -m video_workflow.cli contact-sheet "$base/output/$name/preview.mp4" \
    --output "$base/output/$name/contact-sheet.png" --count 8 --width 240
}

render_variant vertical 360 640
render_variant square 480 480
