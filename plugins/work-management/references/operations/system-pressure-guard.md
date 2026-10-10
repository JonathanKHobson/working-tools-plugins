## System Pressure Guard

Use when Kyle reports freezing, Finder/Chrome/Codex slowness, hard resets,
power failure recovery, missing Codex project folders, memory pressure, or when
starting a broad/resource-heavy lane.

1. Run
   `python3 ~/.codex/scripts/codex_pressure_guard.py check --json`.
2. Treat `warn` and `critical` as advisory only. Never refuse, pause, delay, or
   abandon requested work solely because of memory or process pressure. Name
   the source briefly when useful, then continue the requested lane.
3. Prefer the centralized guard for cleanup:
   `python3 ~/.codex/scripts/codex_pressure_guard.py cleanup-stale`.
   It may close confirmed Codex-owned stale duplicates, but the task continues
   even when nothing is eligible. Do not hand-kill generic Node/Python processes
   unless ownership is clear.
4. Check the four recurring overload vectors: Codex duplicate helpers,
   Spotlight/`mds*`, network mounts, and background app clutter.
5. Keep `$PROJECT_VOLUME`, `$RUNTIME_VOLUME`, and
   `$PROJECT_VOLUME III` guarded with `.metadata_never_index` and
   `mdutil -i off`.
6. Keep Codex on the automation-safe MCP baseline unless Kyle explicitly asks
   to keep a temporary MCP enabled.
7. Do not disable Malwarebytes, GhostPepper, KSB, or Claude-owned KSB
   processes from generic cleanup.
8. Throttle identical prompt-time warnings to at most once per hour unless the
   pressure category changes or new safe cleanup targets appear.
