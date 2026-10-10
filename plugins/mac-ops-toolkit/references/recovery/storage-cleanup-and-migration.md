# Storage cleanup and migration verification

Use for low disk space, cache or unused-runtime removal, and external moves
that cross filesystems or affect active projects. These procedures were learned
from the September 2026 Mac cleanup; current volume and app evidence takes
precedence over that session's paths, sizes and version numbers.

## Establish what occupies the internal disk

1. Record time and `df -k $SYSTEM_DATA_ROOT`. Inspect `df`, `mount` and
   `diskutil info` for each large source and proposed destination before counting
   it as internal. A real directory under Documents may be an external mount;
   `test -L` alone cannot determine placement. Use `du -x` for bounded scans.
2. Confirm the external volume's UUID, filesystem, available space and existing
   destination layout. Historical labels and catalogs guide placement but do
   not prove identity. Never create a directory under `/Volumes` to compensate
   for a missing drive. Preserve existing Spotlight exclusions.
3. Rank measured contributors. Plugins, templates or skills are not inherently
   large; avoid relocating small, active infrastructure without a useful gain.
   Keep personal data, credentials and app databases distinct from caches.

## Choose a disposition from evidence

- Delete authorized, regenerable material only after identifying its producer,
  regeneration path and exact scope. Check the owning app and open handles.
  A temporary-looking name, old timestamp or folder called cache is insufficient.
- An obsolete rollback copy needs an intact replacement at the live lookup path,
  verified contents/function and no remaining consumer. A newer date alone does
  not prove a backup supersedes an older one.
- Use narrow producer-specific sets: for example, Adobe generated `.cfa`, `.pek`
  and `.ims` files after confirming no editor or handle uses them. Preserve source
  media, project files and unfamiliar cache databases. For a duplicate downloaded
  app, compare contents with the working installation before deletion.
- For app-created temporary clones, retain current-launch, recently created and
  open instances. Never sweep a whole system temporary root by age or filename.
- Archive valuable inactive material to the established destination. If uncertain,
  record the question and retain or quarantine it with original-path provenance.
  Moving into Trash on the same volume does not itself reclaim space. Avoid
  consuming archive capacity with easily downloaded or regenerated data.

## Copy, verify, then redirect

1. Check open file handles and process working directories separately. An idle
   chat can still have helpers holding the project root as `cwd`. Do not move
   that root or kill unrelated helpers to clear it. If authorized and quiescent,
   move selected child trees and leave the root real; defer the root switch until
   consumers close. New root-level files remain local until that switch.
2. Copy to a unique destination with required metadata (`ditto --rsrc --extattr
   --acl` on compatible Mac filesystems). Check destination filesystem support
   before depending on Mac permissions, symlinks, resource forks or extended
   attributes. Do not merge into an unexplained existing destination.
3. Compare path inventory, regular-file hashes, symlink targets, modes and relevant
   metadata. Record source signatures before and after the copy to detect writes;
   resolve changes before cutover. Recheck consumers before retiring the source.
4. `ditto` can absorb `._` AppleDouble files into metadata. A manifest mismatch
   is a real stop condition: preserve the source and investigate. If literal
   sidecars are part of the source, preserve those bytes and verify again; never
   weaken the check merely to make the migration pass.
5. Rename the source to a temporary rollback location, create the authorized
   redirect, and verify reads and a disposable write through the original path.
   Retire the rollback only after integrity and access checks pass. For app-owned
   data, also verify the actual app's reopen/use before removing its rollback;
   if it cannot reopen now, retain that rollback and report the verification gap.
   Continue to preserve roots the app requires to be real directories.

## Xcode and other managed components

- For unused, downloadable simulator runtimes, prefer the owning component
  manager's uninstall and a later download from Xcode Settings > Components
  (called Platforms in some releases). Record version/build if reproducibility
  matters; do not promise that an old release will remain available. Do not
  symlink Apple-managed runtime or MobileAsset directories as an archive tactic.
- Before launching a newly updated tool to clean storage, inspect available CLI
  capabilities and first-run state. Setup can download optional platforms,
  documentation and predictive models, consuming the space being recovered.
  Deselect offered downloads unrelated to the task. If an automatic download
  starts, use the supported cancel/remove control if available and record the
  outcome; avoid repeated blind clicks or force-killing system download services.
- A new license agreement needs explicit user authorization to accept; reuse it
  once granted. Administrator authentication is a separate local prerequisite.
  Never collect a password, bypass protections or claim an unauthenticated
  privileged operation ran. Fresh UI state is required after setup changes;
  once the CLI works, use it to verify instead of repeatedly navigating settings.
- Verify three independent facts: component-manager state, remaining storage,
  and free space. For Xcode, a successful `xcrun simctl runtime list -j` with no
  registered runtimes proves uninstallation, not absence of installer DMGs or
  caches. A timeout or service error is not an empty inventory. A UI changing
  to Get may only mark a model purgeable, not physically remove its bytes.
- If an installer remains, identify the exact asset from its metadata, verify
  its build is unregistered, its image is unmounted, and no process uses it.
  Prefer supported cleanup. Any residual manual deletion must be narrowly
  authorized and pass those checks with sufficient access; incomplete `lsof`
  visibility is not evidence of no handles. Never generalize one asset's removal
  into deleting the parent MobileAsset store or disabling system protections.

## Deferred steps and honest accounting

- When app shutdown or local administrator authentication is still required,
  finish independent authorized work and provide a narrowly scoped finalizer
  only when it helps. Include a read-only check mode; revalidate volume UUID,
  current paths, symlinks, unexpected new files, runtime registration and open
  handles as applicable at execution time. Fail closed if assumptions changed.
  Record completion only after the actual mutation and readback, not on script
  creation or a successful dry run. Never embed credentials or disable safeguards.
- Record deletions, verified migrations and pending steps separately. APFS clones,
  snapshots and purgeable files mean `du` totals cannot be summed as reclaimed
  physical space. Active writes and swap can also obscure the change. Compare
  timestamped `df` readings and disclose those limits; never delete live swap.
- Keep task receipts and specific asset paths in the owning project. Report app
  registration, filesystem access, app reopen verification and remaining physical
  data separately. Do not turn a one-run receipt into a universal host rule.
