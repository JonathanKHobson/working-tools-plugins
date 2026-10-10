# Native design runtime adapter

`scripts/design_runtime.py` is the owned entrypoint for the pinned Impeccable engine. It reads `runtime/impeccable/manifest.json`, checks the executable SHA-256 and Mach-O architecture, and loads assets only from the packaged `skillDir`. The public Git source includes the complete pinned reference assets and adapter, while the macOS arm64 executable is a separate release-only runtime archive. A missing or changed executable fails with exit 1. The adapter never searches PATH, runs `npx`, downloads a release, or updates the engine. Its child environment contains no inherited API/cloud keys or browser override and sets `IMPECCABLE_NO_UPDATE_CHECK=1`, `IMPECCABLE_SKILL_DIR`, and `IMPECCABLE_SELF`.

The runtime dependency is pinned to upstream commit `114ea1d3838fca73b253af45f873b9c4f5f213c8`; see its packaged manifest, license, notice, and `SOURCE-PATCHES.diff` for build provenance. `ASSET-PATCHES.diff` separately records the reviewed local control-state reference amendment; `BUILD.md` explains the upstream and amended asset digests. Asset changes require a comparison against the verified pinned source and an explicit patch record before changing the manifest. Rehashing unreviewed drift is not a repair. These commands are an integration surface, not a claim that deterministic findings prove visual quality. Review findings against the rendered interface and the project's actual brief.

## Recipient runtime acquisition

On macOS arm64, obtain the separately reviewed `ux-design-toolkit-impeccable-macos-arm64-4.0.0.zip` release asset from the package's release. Its ZIP paths begin with `runtime/impeccable/`; extract into the installed plugin root so the executable is exactly `runtime/impeccable/bin/impeccable`. Preserve the ZIP's `LICENSE`, `NOTICE.md`, `BUILD.md`, source and asset patches, manifest and reference assets. The matching upstream source archive `impeccable-114ea1d.tar.gz` is a separate source asset, SHA-256 `f12d358c640c33c90ad198d09b1dbe77ddc37286c72c74fc4e5b16ae70816b3d`. Verify the runtime ZIP checksum from its release receipt, then run `verify` below. If the extraction tool did not preserve executable mode, set `chmod 755 "$PLUGIN/runtime/impeccable/bin/impeccable"`. The executable must hash to `46df08a23d806599660b8ccf588a5562e11d7b37c3ff2ed199fd686ed1acddc5`. Source-only installation intentionally reports a missing engine until this overlay is present. Other operating systems and architectures need a separately reviewed build and matching manifest; do not substitute an arbitrary binary.

## Explicit commands

Use a recipient-installed Python 3.9 or newer interpreter. For project-local hooks, the installer records the interpreter that runs it, preserving a virtual environment's executable path.

```sh
PLUGIN=/absolute/path/to/ux-design-toolkit
UX_DESIGN_PLUGIN_ROOT="$PLUGIN"
PY=python3
"$PY" "$PLUGIN/scripts/design_runtime.py" verify
"$PY" "$PLUGIN/scripts/design_runtime.py" detect --project /absolute/project /absolute/project/src/App.tsx
"$PY" "$PLUGIN/scripts/design_runtime.py" detect --project /absolute/project --url http://127.0.0.1:3000
"$PY" "$PLUGIN/scripts/design_runtime.py" context --project /absolute/project
"$PY" "$PLUGIN/scripts/design_runtime.py" native --project /absolute/project palette -- --help
"$PY" "$PLUGIN/scripts/design_runtime.py" live --project /absolute/project --dev-url http://127.0.0.1:3000 live
"$PY" "$PLUGIN/scripts/design_runtime.py" live --project /absolute/project --dev-url http://127.0.0.1:3000 live-generate -- --selector '.card'
"$PY" "$PLUGIN/scripts/design_runtime.py" live --project /absolute/project --dev-url http://127.0.0.1:3000 live-server -- stop
```

`detect` accepts named, existing frontend files inside the project. URL scans require `--url` and explicit `http(s)` targets; they open an isolated browser profile and may fetch that page's subresources. No directory-wide target is inferred. Detector stdout stays a JSON array. Exit 0 means clean or advisory only, 2 means primary findings, and 1 means an operational failure. The adapter also permits the reviewed native utility verbs shown by `native --help`; installer/update, `generate-image`, raw hook administration, and unlisted verbs are unavailable. Image creation belongs to the host's native image tool.

Live and variant commands require a named project and loopback dev URL. The adapter passes that URL to native live discovery and `live-generate`, redacts token-bearing fields from JSON output, and refuses caller-supplied tokens or retained injection. Unstructured live output is withheld because it can contain a session token. The patched engine denies sensitive source paths and non-loopback live targets. Work only in a scoped local development checkout; inspect any source diff before accepting a variant, stop the live server, remove its injection, and verify the owned browser/helper has ended. This adapter does not alter production CSP or inject into a production build by itself.

## Project opt-in hooks

The preferred installed Codex/Claude integration owns its `PostToolUse` and `Stop` declarations in the UX Design Studio plugin. With that plugin installed and its reviewed definitions trusted by the host, opt in one project with the marker only:

```sh
python3 "$PLUGIN/scripts/design_runtime.py" install-hooks --project /absolute/project --marker-only
```

This verifies the pinned engine and writes only the exact canonical-root `.ux-design-toolkit/design-runtime.json` marker. It refuses marker-only setup when it finds owned project-local hook entries, avoiding duplicate scans. It does not create `.codex/hooks.json` or `.claude/settings.json`, and the success message means the marker is ready, not that the host loaded, trusted, or executed plugin hooks. Confirm those states through the host's hook UI and a disposable frontend edit. The event must declare a `cwd` inside the marked root and a `session_id`; missing fields produce a quiet skip. The marker is never inferred from a parent directory, so a nested shell cwd may skip rather than scan a broader project.

For a host without plugin hook loading, the optional project-local fallback remains `install-hooks --project /absolute/project --host codex|claude|both`. It merges only owned commands into `.codex/hooks.json` and/or `.claude/settings.json`, backs up changed configs, preserves unrelated entries, and writes the marker last. Repeating installation is idempotent. It recognizes older entries for this exact launcher, hook verb, and project even when their interpreter differs, while preserving unrelated commands. Do not combine plugin and project-local entries for the same host/project. To migrate an older project registration, run `remove-hooks --project /absolute/project --host both` first, then the marker-only install above. The lower-level `enable-hooks`/`disable-hooks` aliases toggle only the marker and do not verify the engine.

Example project-local `.codex/hooks.json` entries for a project at `/absolute/project` (the installer uses the real canonical path and shell quotes it; the host may still require trust approval):

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write|apply_patch",
      "hooks": [{
        "type": "command",
        "command": "/absolute/path/to/python3 /absolute/path/to/ux-design-toolkit/scripts/design_runtime.py hook post --project /absolute/project",
        "timeout": 5,
        "statusMessage": "Checking edited UI files"
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "/absolute/path/to/python3 /absolute/path/to/ux-design-toolkit/scripts/design_runtime.py hook stop --project /absolute/project",
        "timeout": 30,
        "statusMessage": "Checking queued UI files"
      }]
    }]
  }
}
```

The installer writes analogous entries to Claude's project `.claude/settings.json`. The handlers accept the host's stdin JSON, known edit payload paths, and `apply_patch` filename headers. They canonicalize paths and skip credential names, dependencies, generated output, symlink escapes, nonfrontend files, disabled projects, reentry, and recursive Stop. State is private file-path metadata under `~/Library/Caches/ux-design-toolkit/design-runtime/` on macOS, or `${XDG_CACHE_HOME:-~/.cache}/ux-design-toolkit/design-runtime/` elsewhere, keyed by project and session; no source text is stored. A debounced PostToolUse scan and one Stop scan each process at most 12 queued files. PostToolUse findings return additional context. Codex Stop findings return a nonblocking `systemMessage`; Claude Stop findings return additional context. Findings never hard block or automatically edit. Host schemas and timeout handling should be verified on a disposable project before enabling a real checkout. The host formats follow [Codex hooks](https://learn.chatgpt.com/docs/hooks) and [Claude hooks](https://code.claude.com/docs/en/hooks).

`hooks/hooks.json` is the default plugin declaration loaded by Codex and Claude. Its `python3` command uses Codex's `${PLUGIN_ROOT}` or falls back to Claude's `${CLAUDE_PLUGIN_ROOT}` to reach the installed script. `hooks/claude-hooks.json` remains as a Claude-specific compatibility copy but is not referenced by the public manifest, so Claude runs the default hook once. The handlers inspect only explicitly marked projects. Their presence in source alone is not proof a host loaded, trusted, or executed them. Do not combine them with project-local entries in the same project.

The Compass MCP launcher reads `~/.config/studio-tools/compass.json` by default. A recipient may set `UX_COMPASS_BINDING` to another existing binding file with the named backend's `interpreter` and `server` paths. The configured interpreter path is kept intact for virtual environments. The Design Library launcher requires a separately installed `design-templates` owner at the adjacent `design-templates` directory, or at `DESIGN_TEMPLATES_ROOT`; it does not provide a substitute private gallery. Atlas access is owned by Activities Templates and is not bound or launched by this package. These external owners and bindings are installation requirements, not bundled data.

To disable a marker-only project, run `remove-hooks --project /absolute/project --marker-only`. For a project-local fallback, use `remove-hooks --project /absolute/project --host both` to remove only owned entries and the marker. Removing the marker makes any stale host entry skip immediately.

## Verification

```sh
python3 -m unittest discover -s "$PLUGIN/tests/design_runtime" -v
python3 "$PLUGIN/scripts/design_runtime.py" verify
```

The tests exercise manifest refusal, environment stripping, timeout, detector exit propagation, explicit target boundaries, event parsing, secret/generated paths, symlink escape, debounce, Stop once, recursion guards, and host-config preservation with a mock engine. The separate pinned native runtime was tested with a clean sample, a doctor run and a disposable project hook edit. Browser and live acceptance require a disposable local site and process cleanup evidence on each receiving host; these tests do not establish those outcomes.
