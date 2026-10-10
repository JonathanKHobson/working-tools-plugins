## Browser Handoff

Use when browser automation, Playwright, Chrome control, or browser MCPs were used.
For task/session boundaries, uncertain writes and repeat navigation, load
[browser workflow reliability](browser-workflow-reliability.md).

1. Record the selected provider and exact task-owned session/tab identifiers as
   they are created. A profile holds authentication; a session or tab is a work
   surface. Separate sessions do not necessarily isolate shared cookies.
2. Verify the requested outcome in the live surface. If a write timed out,
   inspect its resulting state before any retry. A click or attempted save is
   not a receipt. Save only the redacted evidence the owning project needs.
3. Finish any active human login/challenge handoff before cleanup. Preserve the
   user's normal browser, pre-existing tabs, other tasks' sessions and accounts.
4. Close only task-owned automation windows, tabs and sessions with the current
   provider's documented API. For a borrowed human tab, detach or leave it open
   as the provider/user requires; do not force-close it.
5. Where the selected route creates a dedicated automation Chrome process, close
   its owned parent daemon too and check for that session's automation-only
   arguments (headless, temporary user-data-dir, debugging port, Playwright
   profile). Do not terminate a shared provider or a process based on name alone.
6. Verify no task-owned automation Chrome remains, or that normal Chrome is
   visible without automation-only arguments. A shared native browser service
   may remain because other tasks use it; report cleanup limits accurately.
7. Treat this readback as completion evidence. Use existing project records for
   a useful resume pointer, not a new browser history catalog.
