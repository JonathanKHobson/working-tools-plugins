# Codex Storage and Update Recovery

Use this reference when Codex or the ChatGPT desktop app reports an update
download error, `No space left on device`, unexpectedly large local storage,
or when deciding what Codex data can safely live externally.

## Known Mac Layout

- The desktop app bundle is `/Applications/ChatGPT.app`, while its bundle ID is
  `com.openai.codex` and its user data is commonly under
  `~/Library/Application Support/Codex` and `~/.codex`.
- Projectless workspaces require `~/Documents/Codex` to be a real directory.
  On this Mac it is an external APFS volume (`CodexWorkspaces`) mounted at that
  native path. Do not replace it with a symlink: the app rejects that layout.
- Workspace externalization does not externalize application support, crash
  reporting, update staging, caches, plugins, or `~/.codex/sessions`.

## Diagnose Before Moving Data

1. Confirm internal free space with `df -h $SYSTEM_DATA_ROOT`.
2. Measure the likely roots separately:

   ```bash
   du -sh "$HOME/Library/Application Support/Codex" "$HOME/.codex"
   du -x -h -d 1 "$HOME/Library/Application Support/Codex"
   du -x -h -d 2 "$HOME/.codex/sessions"
   ```

3. For update failures, inspect Sparkle evidence rather than guessing:

   ```bash
   /usr/bin/log show --last 4h --style compact \
     --predicate 'process == "ChatGPT" AND eventMessage CONTAINS[c] "space"'
   ```

   `No space left on device` during a download establishes an internal-volume
   capacity failure, not a network or account problem.

## Safe Codex Targets

- `~/Library/Application Support/Codex/Crashpad/pending` is a crash-report
  queue. It is regenerable. Verify no open handle, then archive or move it to
  external storage; a nested symlink to an external live queue is appropriate
  when its target remains mounted whenever Codex runs.
- Closed historical month folders under `~/.codex/sessions/YYYY/MM` can be
  moved externally and replaced with a symlink after verifying the copy and
  readability at the original path.
- Keep the active month and current task session local while Codex is running.
  Do not replace the entire `~/.codex/sessions` root during an active session.

## Do Not Relocate Blindly

- Do not mass-move `~/Library/Application Support/Codex`, `~/.codex`,
  credentials, databases, plugins, skills, memories, or the active session.
- Do not rely on an external volume that may be disconnected while Codex is
  running. Verify its mount device, free space, target directory, symlink, and
  a representative historical session read before declaring success.
- Preserve old crash reports externally when deletion is not explicitly
  authorized. They are safe to remove later, but are not needed for Codex to
  function.

## Verification and Closeout

1. Verify `test -L`, `readlink`, `test -r` for a moved session, and `test -w`
   for a redirected crash queue.
2. Recheck `df -h $SYSTEM_DATA_ROOT` and the two Codex root sizes.
3. Quit and reopen Codex, then retry the update once. Do not claim the update
   itself succeeded until the new build is running or Sparkle reports success.
