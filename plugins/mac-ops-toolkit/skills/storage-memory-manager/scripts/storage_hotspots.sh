#!/usr/bin/env bash
set -euo pipefail

scan_root="${STORAGE_SCAN_HOME:-$HOME}"
if [[ ! -d "$scan_root/Library" ]]; then
  echo "Storage scan requires an existing Library directory beneath STORAGE_SCAN_HOME (or HOME): $scan_root/Library" >&2
  exit 2
fi

echo "== Disk overview =="
# Optional positional arguments are explicit recipient volumes; none are assumed.
df -h /
for volume in "$@"; do
  if [[ -d "$volume" ]]; then
    df -h "$volume"
  fi
done

echo
echo "== Top folders in \$HOME/Library =="
du -hd 1 "${STORAGE_SCAN_HOME:-$HOME}/Library" 2>/dev/null | sort -hr | head -n 20

echo
echo "== Top folders in \$HOME/Downloads =="
if [[ -d "${STORAGE_SCAN_HOME:-$HOME}/Downloads" ]]; then
  du -hd 1 "${STORAGE_SCAN_HOME:-$HOME}/Downloads" 2>/dev/null | sort -hr | head -n 20
fi

echo
echo "== Largest Application Support roots =="
if [[ -d "${STORAGE_SCAN_HOME:-$HOME}/Library/Application Support" ]]; then
  du -hd 1 "${STORAGE_SCAN_HOME:-$HOME}/Library/Application Support" 2>/dev/null | sort -hr | head -n 20
fi
