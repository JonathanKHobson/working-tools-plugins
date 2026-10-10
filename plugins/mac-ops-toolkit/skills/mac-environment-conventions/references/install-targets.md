# Install Targets

## App bundles

Preferred target for relocatable user-installed apps:

- `$RUNTIME_VOLUME/ExternalApplications/<App>.app`

Native launch path may remain:

- `/Applications/<App>.app`

When the existing pattern is already in use, the native path is a symlink to the
external bundle.

## User library mirrors

Preferred external mirror root:

- `$RUNTIME_VOLUME/UserMirror/Library`

Important subroots already in use:

- `Application Support`
- `Caches`

Use this mirror for large app support, caches, and runtime data that already
fits the receiving operator's externalized-library pattern.

Current review candidates that remain local and should be evaluated case by case
include:

- `Claude`
- `Google`
- `discord`
- `Figma`
- `com.PolyDemons.The-RPG-Engine`

Claude Desktop is a special-case app on this Mac: if its configured MCPs rely
on external-drive runtimes, keep it out of Login Items and launch it manually
after `$ARCHIVE_VOLUME` and `$RUNTIME_VOLUME` are mounted.

## Runtime and backup targets

- Backups and save data:
  `$RUNTIME_VOLUME/Backup`
- Steam games and related runtime content:
  `$RUNTIME_VOLUME/SteamLibrary`
- Epic runtime content:
  `$RUNTIME_VOLUME/Epicgames`
- Emulator-related storage:
  `$RUNTIME_VOLUME/Emulator`
- Windows compatibility/runtime material:
  `$RUNTIME_VOLUME/Windows`
- Stream and creator assets:
  `$RUNTIME_VOLUME/Stream Assets`
- Recordings and captured creator output:
  `$RUNTIME_VOLUME/GameRecorderings`
  and `$RUNTIME_VOLUME/GameClips`

## Archive and project targets

Do not place archive-style files here by default. Use `$ARCHIVE_VOLUME` for:

- document archives
- dated downloads offloaded from the Mac
- reusable project assets
- media libraries
- websites and long-lived project storage

## Decision rule

Before placing something:

1. Determine if it is runtime-oriented or archive-oriented.
2. If runtime-oriented, inspect `$RUNTIME_VOLUME/_Catalog/reports/install_roots_summary.csv`.
3. If archive-oriented, switch to the archive-volume label conventions instead of forcing it
   onto the runtime drive.
