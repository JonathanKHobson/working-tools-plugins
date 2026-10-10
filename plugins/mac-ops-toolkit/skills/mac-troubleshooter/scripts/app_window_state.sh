#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"App Name\"" >&2
  exit 1
fi

app_name="$1"

echo "== App window state for: $app_name =="

echo "-- System Events --"
osascript - "$app_name" <<'APPLESCRIPT'
on run argv
set app_name to item 1 of argv
tell application "System Events"
  if exists process app_name then
    tell process app_name
      return {name, visible, frontmost, background only, unix id, (count windows)}
    end tell
  else
    return {app_name, false, false, false, -1, -1}
  end if
end tell
end run
APPLESCRIPT

echo "-- App window count --"
osascript - "$app_name" <<'APPLESCRIPT'
on run argv
set app_name to item 1 of argv
tell application app_name
  if it is running then
    return count every window
  else
    return 0
  end if
end tell
end run
APPLESCRIPT

echo "-- Matching processes --"
ps -axww -o pid,ppid,stat,etime,command | rg -i -F -- "$app_name" || true
