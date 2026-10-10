# Storage Layout

## Verify historical names before use

The paths below record established roles, not guaranteed current mount names.
For every move, use `diskutil info`, `mount` and `df` to identify the current
volume UUID, filesystem and free space, then inspect the actual target layout.
For example, `runtime-volume label` and `alternate runtime-volume label` must not be treated as interchangeable
without verifying identity. A native Documents path may itself be an external
mount. Never create a missing mountpoint or infer internal usage from its name.
Live evidence takes precedence over an older `_Catalog` report.

## Two-drive model

- `$ARCHIVE_VOLUME`
  Primary archive and file drive. Use for documents, downloads moved off the
  Mac, reusable assets, long-lived project files, media libraries, websites,
  and archive-style storage.
- `$RUNTIME_VOLUME`
  Primary apps/runtime drive. Use for externally stored app bundles, game
  libraries, backups, stream assets, Windows compatibility/runtime material,
  and mirrored user-library storage used by symlink redirects.

## High-confidence role boundaries

Use `$ARCHIVE_VOLUME` for:

- Archived downloads and dated offloads
- Dated archive folders containing the former contents of `~/Downloads`
- Documents and project artifacts
- Reusable assets and media libraries
- Website and code project storage

Use `$RUNTIME_VOLUME` for:

- `ExternalApplications`
- `Users/<user>/Library/...` mirror content
- `Backup`
- `SteamLibrary`, `Epicgames`, `Emulator`
- `Stream Assets`, `GameRecorderings`, `GameClips`
- `Windows`

## Internal disk defaults

Keep local by default when there is no clear redirect pattern:

- System applications and macOS-managed components
- `~/Downloads` itself. The folder stays local and real;
  only its contents should be moved to dated archive folders on `$ARCHIVE_VOLUME`.
- Standard Apple paths that have no existing external mirror
- Small or clearly ephemeral items where externalization adds complexity without
  payoff

## Operational rule

When a task could belong to either external drive:

1. Ask whether it is archive-oriented or runtime-oriented.
2. If it is archive-oriented, prefer `$ARCHIVE_VOLUME`.
3. If it is runtime-oriented, prefer `$RUNTIME_VOLUME`.
4. Verify current placement with the drive `_Catalog/reports` outputs before
   changing anything.
