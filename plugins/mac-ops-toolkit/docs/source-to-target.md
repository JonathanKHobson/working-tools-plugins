# Mac operations package map

This staged package reuses the existing disabled `mac-ops-toolkit` identity rather than creating a second Mac plugin. The canonical generated source is `$USER_HOME/.codex/local-plugin-workspace/source/plugins/mac-ops-toolkit/`; this focused candidate is staged at `$USER_HOME/Documents/Codex/2026-09-22/i-x20/work/consolidation/mac-ops-toolkit/`. The installed snapshot recorded `mac-ops-toolkit@local-skill-plugins` as installed but disabled. No marketplace, installed cache, global route, or original skill was changed.

| Original source | Staged target | Retained capability |
| --- | --- | --- |
| `$USER_HOME/.codex/skills/mac-environment-conventions/` | `skills/mac-environment-conventions/` | the configured drive roles, symlink and install targets, Codex storage/update notes, machine-state inspection. All four conditional references copied. |
| `$USER_HOME/.codex/skills/mac-troubleshooter/` | `skills/mac-troubleshooter/` | Reversible app/window/process recovery, recovery playbook, window-state inspection and timestamped support-state backup scripts. The staged entrypoint includes the newer Codex update reference absent in the generated 2026-06-20 plugin copy. |

The legacy standalone paths above must remain available as compatibility paths while global callers still name them. Internal sibling links resolve within this package. Other local workflows (`storage-memory-manager`, `local-mcp-debugging`, `local-storage-mcp`, `focus-ops-manager`, `native-macos-app-builder`, and security checks) remain separately owned; the staged entrypoints reference them by installed skill name instead of broken package-relative paths. The `app_window_state.sh` copy passes the app name as AppleScript data rather than interpolating it into script text, and uses literal `rg` matching. It was not run against a live app in this packaging pass.

This is **private Mac-specific guidance**, portable as a grouped Codex package on the receiving Mac. Its `$ARCHIVE_VOLUME`, `$RUNTIME_VOLUME`, username, Claude profile, and app-placement facts must be rebound and checked before use on another machine. A copied skill is not evidence that a drive is currently mounted or an app is running. No license/notice file was present in the selected original skill folders; the existing generated plugin manifest marked the package `Private`.
