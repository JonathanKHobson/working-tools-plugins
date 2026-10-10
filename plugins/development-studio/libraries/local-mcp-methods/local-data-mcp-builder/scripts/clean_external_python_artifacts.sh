#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /path/to/runtime-or-venv" >&2
  exit 1
fi

target="$1"

if [[ ! -d "$target" ]]; then
  echo "Path is not a directory: $target" >&2
  exit 1
fi

find "$target" -name '._*' -print -delete
