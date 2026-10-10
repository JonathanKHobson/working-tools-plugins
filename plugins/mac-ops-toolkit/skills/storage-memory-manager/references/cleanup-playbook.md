# Cleanup Playbook

## Priority Order

1. Measure available disk, memory pressure, and swap.
2. Identify the biggest folders in:
   - `~/Library`
   - `~/Downloads`
   - app-specific support or cache roots
   - external SSD backup and mirror roots
3. Ask the user before deleting anything.
4. Back up anything that may be deleted unless it is clearly disposable cache or
   temp data and the user has approved removing it.
5. Reclaim safe-to-rebuild data first.
6. Re-check free space and performance.
7. Only then consider moves, symlinks, or archival offloads.

## Usually Safe First Pass

Even for items in this section, ask first before deleting. These are lower-risk,
not auto-delete targets.

- Browser caches
- App shader caches
- Temporary export/render folders
- Crash dumps and stale logs
- Old installer packages and duplicate downloads
- Rebuildable derived data

## Use More Caution With

Back these up before any deletion or relocation.

- `~/Library/Application Support/...`
- browser profiles
- mail stores
- chat histories
- sync roots
- databases
- anything already mirrored to `${RUNTIME_VOLUME}`

## Drive Decision Rule

- Archive-oriented: prefer `${ARCHIVE_VOLUME}`
- Runtime-oriented: prefer `${RUNTIME_VOLUME}`
- Small system-managed items: usually keep local unless a redirect pattern
  already exists

## Memory Pressure Triage

1. Capture `memory_pressure`, `vm_stat`, and top resident-memory processes.
2. Look for runaway apps, browser tabs, VMs, Electron apps, or indexing tasks.
3. Prefer closing or restarting the biggest offenders before suggesting deeper
   OS-level changes.
4. If swap is high and repeated, check whether disk pressure and login items are
   also contributing.
