## Codex Desktop Launch and Window Recovery

Use when Codex Desktop has blank conversations, appears to open and immediately
close, stays active without a visible window, or stops restoring its task list.

1. Define success before repair: the app remains running, its main window is
   visible, the task list populates, and one existing conversation renders.
2. Distinguish a real process exit from an invisible window. After one launch,
   check whether the menu bar still says `ChatGPT` and whether the process
   persists for at least ten seconds. If it does, inspect the `Window` menu.
   An enabled generic window menu means a window exists even if none is visible.
3. Recover an off-screen window with `Window -> Zoom`. In the verified July 24,
   2026 incident, `Center` and `Bring All to Front` did not reveal the window,
   while `Zoom` restored it immediately.
4. Do not repeat launches without a new hypothesis. Reproduce once per layer:
   process lifecycle, app-only state, reboot, and window placement.
5. Preserve history before changing state. Do not delete
   `~/.codex/sessions/`, `~/.codex/state_5.sqlite`, or its WAL/SHM files.
   Copy the database with WAL/SHM to a local path and run
   `PRAGMA quick_check`; verify thread counts, titles, and recent rows.
6. Treat `~/.codex/process_manager/chat_processes.json` as resumable process
   state, not conversation history. If it contains dead PIDs or stale commands,
   make a timestamped backup and replace only that registry with `[]`.
7. If the app still exits, back up and reset only app UI/session state:
   `~/Library/Application Support/com.openai.codex`,
   `~/Library/Caches/com.openai.codex`, and
   `~/Library/Preferences/com.openai.codex.plist`. Then perform a normal reboot
   before another launch.
8. Verify the app bundle and host before reinstalling: check code signing,
   macOS build, and executable architecture. A valid current Intel `x86_64`
   build on an Intel Mac is not an architecture mismatch.
9. Interpret the July 24 incident as a compound stale process/UI restore-state
   failure. Evidence: the thread database passed integrity checks with 170
   indexed conversations; stale process records were present; clearing
   process/UI state plus reboot stopped the immediate exit; the surviving
   window then had to be recovered from off-screen with `Window -> Zoom`.
   No macOS ChatGPT crash report existed, so do not claim a more precise
   internal abort mechanism without new logs.
10. Prefer Screen Sharing and small targeted reads over recursive SMB scans.
    SMB can stall on many small files. If Screen Sharing keyboard automation
    maps `_` to `-`, `|` to `\`, or modifiers to literal letters, use simple
    commands, separate typing from Return, and visually verify the command
    before executing it.
11. Before signoff, confirm the changed visual anchors: visible main window,
    populated task list, and rendered prior conversation. Disconnect Screen
    Sharing and leave the repaired Codex window open for the user.
