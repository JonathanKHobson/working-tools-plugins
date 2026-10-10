#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python -m video_workflow.cli render examples/music-slideshow/project.json --output examples/music-slideshow/output/preview.mp4 --work-dir examples/music-slideshow/work
python -m video_workflow.cli qa examples/music-slideshow/output/preview.mp4 --width 640 --height 360 --duration 8 --output examples/music-slideshow/output/qa-report.json --deep
python -m video_workflow.cli contact-sheet examples/music-slideshow/output/preview.mp4 --output examples/music-slideshow/output/contact-sheet.png --count 8 --width 320
python -m video_workflow.cli waveform examples/music-slideshow/assets/music.wav --output examples/music-slideshow/output/waveform.png
