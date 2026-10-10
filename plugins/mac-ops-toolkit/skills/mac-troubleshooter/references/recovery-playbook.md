# Recovery Playbook

## Invisible Window or "App Open With No Window"

1. Confirm whether the app has real windows.
   Compare:
   - `osascript` window counts from the app
   - `System Events` window counts from the process
   - raw process arguments from `ps`
2. Check whether the tracked app process is actually:
   - a headless browser process
   - a helper or renderer
   - an updater or login item
3. Try the least-destructive recovery:
   - activate the app
   - request a new window explicitly
   - relaunch the app normally
4. If stale helper or headless processes are holding the app open, clear those
   first and retry a normal launch.
5. Only if the symptom persists, back up the smallest relevant support files and
   reset crash/session/window-placement state.

## Process Will Not Quit

1. Attempt a normal app quit.
2. Re-check for remaining processes by exact command line, not just app name.
3. Identify helper/background processes separately from the main app.
4. Kill only the stale or blocking processes needed to unblock relaunch.
5. Re-test launch before editing any files.

## Login-Item Launch Race

If a desktop app starts too early at login and depends on external-drive MCPs:

1. Remove it from Login Items first.
2. Reboot with the app closed.
3. Mount the external drives.
4. Launch the app manually and confirm the MCPs attach.
5. If the app still fails after manual launch, inspect the MCP logs before
   changing the server config.

## Narrow Reset Pattern

When a reset is necessary:

1. Back up the exact files to a timestamped folder first.
2. Reset the smallest state that matches the failure:
   - crash flags
   - session restore files
   - window placement
   - one app-specific preference subtree
3. Relaunch and verify windows, interaction, and preserved user state.
4. If the app still fails, test with a fresh profile or temp data directory to
   separate app-binary issues from profile corruption.

## Evidence To Collect

- App/process visibility and frontmost state
- Window counts from both the app and `System Events`
- Exact process arguments
- Relevant preference keys
- Backup path for any touched state

## Storage Notes

- Backups for runtime/app-support recovery belong on `$RUNTIME_VOLUME` if
  they are being externalized or mirrored by an existing pattern.
- Do not invent new storage paths. Check the receiving operator's Mac conventions first.
