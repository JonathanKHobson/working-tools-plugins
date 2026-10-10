#!/usr/bin/env bash
set -euo pipefail
# Optionally clones research candidates into a NON-RUNTIME research directory.
# It never imports, installs, resets, or updates an existing checkout.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${1:-$ROOT/research/vendor}"
mkdir -p "$DEST"
clone_if_missing() {
  local url="$1" name="$2"
  if [[ -d "$DEST/$name/.git" ]]; then
    printf 'Preserving existing research checkout: %s\n' "$DEST/$name"
  elif [[ -e "$DEST/$name" ]]; then
    printf 'Refusing to overwrite non-repository path: %s\n' "$DEST/$name" >&2
    exit 2
  else
    git clone --depth 1 "$url" "$DEST/$name"
  fi
}
clone_if_missing https://github.com/browser-use/video-use.git video-use
clone_if_missing https://github.com/bradautomates/claude-video.git claude-video
clone_if_missing https://github.com/AgriciDaniel/claude-shorts.git claude-shorts
clone_if_missing https://github.com/DojoCodingLabs/remotion-superpowers.git remotion-superpowers
clone_if_missing https://github.com/openai/skills.git openai-skills
python3 -c 'from pathlib import Path; import json, subprocess, sys; root=Path(sys.argv[1]); items=[{"name":p.name,"commit":subprocess.check_output(["git","-C",str(p),"rev-parse","HEAD"],text=True).strip()} for p in sorted(root.iterdir()) if (p/".git").exists()]; (root/"FETCHED_SOURCES.json").write_text(json.dumps({"sources":items},indent=2)+"\n")' "$DEST"
printf 'Reference repositories inventoried in %s\n' "$DEST"
