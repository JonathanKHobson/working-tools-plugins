#!/usr/bin/env bash
set -euo pipefail

echo "== Memory pressure =="
memory_pressure

echo
echo "== VM stats =="
vm_stat

echo
echo "== Top memory consumers =="
top -l 1 -o mem -n 15 | sed -n '1,25p'
