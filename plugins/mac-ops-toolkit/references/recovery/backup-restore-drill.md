# Bounded backup restore drill

Use for an explicitly requested recoverability check of selected Mac files or narrow app-state backup. This is a file-level drill into an isolated destination. It does not erase, repartition, replace a live profile, restore a disk, change Time Machine associations, or authorize a whole-system recovery. Preserve the full [storage verification method](storage-cleanup-and-migration.md) for volume identity, copy/metadata checks and rollback.

## Select the actual backup

Record the requested recovery question, sample files, expected backup date/version, owning app, backup producer and actual artifact/volume. Confirm current macOS, mounted volume UUID/filesystem, available space and read access. A label, catalog entry, newest timestamp or successful backup command does not prove the intended item exists in a usable backup.

For Time Machine, inspect current supported `tmutil` help/manual and Time Machine settings. Read-only `destinationinfo`, `listbackups` and `latestbackup` can help identify a destination/snapshot where available; record failures instead of treating empty/error output as no backups. Browse the selected dated backup and find the actual sample item. Distinguish an external/network backup from a same-disk local snapshot; local recovery alone does not test loss of the internal disk. For an app-state copy, inspect its path inventory and recorded manifest/hash; a ZIP suffix alone does not prove a coherent backup. Quiesce live writes before creating a new app-state copy, using the existing backup helper only within its authorized scope.

Choose a small meaningful sample: one ordinary file plus a format the recovery needs (e.g. media, package, symlink or metadata-bearing file). For an existing historical backup, compare to its saved version/manifest, not today's changed live file. If no historical hash exists, disclose the weaker comparison and verify content/readability; do not invent a baseline.

## Restore to an isolated destination

Use a new empty, uniquely named directory under the established authorized test location. Resolve its real path, reject symlinks/aliases and existing contents, verify it is neither the live source nor the backup source (nor nested inside either), and verify its mounted volume and capacity. Revalidate these facts immediately before writing. Do not invent a path under `/Volumes` for an absent drive. Preserve backup contents and current Spotlight/storage conventions.

Apple's normal Time Machine Restore action returns items to their original location. Therefore do not click it over live data as a drill. [Apple file restore](https://support.apple.com/guide/mac-help/restore-files-mh11422/mac)

Use a supported restore-to-destination path verified for the current host. The local `tmutil` manual documents `restore [-v] src ... dst`, with the last argument the destination and copy-like path semantics. Inspect those semantics and confirm the exact planned source and fresh destination before execution; quote each verified path. If permissions or backup format prevent a separate destination, report the limitation and hold this write. Do not silently elevate, collect passwords or substitute a disk-level restore. A narrow copied app-state backup may use the existing copy procedure into the fresh test directory; keep archive extraction bounded to that directory and inspect paths before extracting.

## Verify recoverability

Compare restored path inventory, file sizes and regular-file SHA-256 values to the selected backed-up version or trusted recorded manifest. Read the selected backup before/after where needed to detect changes; stop on a mismatch. Check symlink targets, permissions and relevant extended attributes/resource forks using the existing storage method. Byte hashes do not establish metadata or app behavior.

Open/read the restored sample in the appropriate viewer or isolated app profile when safe, and verify the expected content/version. Never launch restored executables, import a live credential database or connect a recovered profile merely to demonstrate recovery. For app state that cannot safely be opened in isolation, report byte/metadata checks separately from untested app reopening. Preserve source and backup if the drill fails.

Apple's Verify Backups guidance concerns network Time Machine destinations; its result is useful backup-integrity evidence, separate from a selected-file restore and readback. Do not promise that command/UI for every local disk. [Apple backup verification](https://support.apple.com/guide/mac-help/verify-your-backup-disk-mh26840/mac)

## Receipt and closeout

Keep in the task record: backup producer/artifact and selected date, volume identity, sample/version, destination, restore action/result, comparison basis, hashes/readback, metadata check, elapsed time, pass/fail/unverified and exact limits. A pass establishes recovery of those samples under that tested configuration; it does not certify every file or disaster recovery. Keep restored samples until the user-requested retention/cleanup point. Remove only identified task-owned drill files when authorized; never sweep backups or delete a source to prove the drill. No scheduled drill is created without a request.
