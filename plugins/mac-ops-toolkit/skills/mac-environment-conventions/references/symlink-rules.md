# Symlink Rules

## Observed pattern

Jonathan already uses native-path symlinks to keep selected app data on
`$RUNTIME_VOLUME`.

Common example:

- `~/Library/Application Support/<App>`
- points to
- `$RUNTIME_VOLUME/UserMirror/Library/Application Support/<App>`

Observed app-support examples include:

- `Adobe`
- `BBEdit`
- `Steam`
- `OpenAI`
- `obs-studio`
- `Slack`
- `Loom`
- `Arc`
- `Plex Media Server`

Observed app-bundle examples include:

- `/Applications/BBEdit.app`
- `/Applications/Steam.app`
- `/Applications/VLC.app`
- `/Applications/Firefox.app`
- `/Applications/Signal.app`
- all pointing into `$RUNTIME_VOLUME/ExternalApplications/...`

Current baseline reports show:

- 20 inbound native app symlinks into `ExternalApplications`
- 28 inbound native symlinks into the mirrored
  `$RUNTIME_VOLUME/UserMirror/Library` tree

## Preferred rule

When externalizing a supported app family:

1. Keep the native path in place as the launch or lookup location.
2. Put the actual storage on `$RUNTIME_VOLUME`.
3. Mirror the native subpath structure under:
   `$RUNTIME_VOLUME/UserMirror/Library/...`
4. Use a symlink from the native path to the external mirror target.

## Preferred targets

- Application Support:
  `$RUNTIME_VOLUME/UserMirror/Library/Application Support/<App>`
- Caches:
  `$RUNTIME_VOLUME/UserMirror/Library/Caches/<App or tool>`
- App bundle:
  `$RUNTIME_VOLUME/ExternalApplications/<App>.app`

## Safety rules

- Inspect the current symlink state before creating a new redirect.
- Never replace `~/Downloads` with a symlink, alias, moved
  folder, or external redirect. The Downloads folder is the permanent local
  scratch/download location for Chrome and temporary work. To clear it, move
  its contents into a dated archive folder under `$ARCHIVE_VOLUME/Downloads/`
  and recreate nothing; the local folder itself stays put.
- Do not replace system apps or Apple-managed paths with external symlinks
  unless that exact path already follows the pattern.
- Do not assume every nested symlink is storage policy; some singleton lock and
  socket links are just runtime implementation details.
- Prefer matching an existing app family pattern over generalizing from a single
  one-off example.

## Reports to consult

- `$RUNTIME_VOLUME/_Catalog/reports/symlink_map.csv`
- `$RUNTIME_VOLUME/_Catalog/reports/library_redirect_candidates.csv`

When using `symlink_map.csv`, prioritize rows where `drive_classification` is
`kyle_ssd_ii`. The report also includes normal runtime singleton links and
temporary internal links that are not storage-policy signals.
