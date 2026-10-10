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
