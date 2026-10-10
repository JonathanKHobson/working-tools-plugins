# Staged validation, 2026-09-23

- Existing `mac-ops-toolkit@local-skill-plugins` is installed but disabled in the pre-consolidation snapshot. This staged source reuses its identity; no installation or live-routing claim is made.
- Plugin validator passed. Both selected skill entrypoints passed `quick_validate.py`.
- Internal Markdown/resource paths checked: 8 references, 0 missing. External sibling routes now use installed skill names rather than unresolved relative package paths.
- `bash -n` passed for both bundled shell scripts. `app_window_state.sh Finder` returned process, System Events and app window counts without changing app state; this checks the staged AppleScript argument route. `support_state_backup.sh` was **not** run, because it writes backups under Application Support and no user data reset was requested.
- Of 11 selected skill files, 8 are byte-identical to standalone sources. The two SKILL.md files have package-relative route repairs; `app_window_state.sh` has argument quoting/literal-match repair. No hidden Git, cache or archive files were copied.
- This remains a private receiving-Mac package. The actual drive mounts, app state and permissions must be checked on each task; a validator or Finder smoke test is not evidence for another app or host.
