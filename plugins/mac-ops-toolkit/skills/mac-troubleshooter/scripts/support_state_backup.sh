#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <path> [more-paths...]" >&2
  exit 1
fi

timestamp="$(date +%Y%m%d-%H%M%S)"
backup_root="${HOME}/Library/Application Support/CodexTroubleshootingBackups/${timestamp}"

mkdir -p "$backup_root"

for src in "$@"; do
  if [[ ! -e "$src" ]]; then
    echo "SKIP missing: $src" >&2
    continue
  fi

  base_name="$(basename "$src")"
  dest="${backup_root}/${base_name}"

  if [[ -d "$src" ]]; then
    cp -R "$src" "$dest"
  else
    cp "$src" "$dest"
  fi

  echo "BACKED_UP $src -> $dest"
done

echo "BACKUP_ROOT $backup_root"
