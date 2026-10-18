# Local plugin change tracking

`scripts/plugin_change_record.py` records byte-level changes in canonical plugin
sources. It is a local observation tool. It does not install, package, publish,
deploy, or authorize any release. A first run creates a baseline without
claiming historical changes.

Call `record(config, origin='manual')` or run the CLI with `--config PATH`.
The default config is `~/.config/studio-tools/plugin-change-tracking.json`.
Required JSON keys are `canonical_root` and `state_dir`. Optional
`canonical_sources` maps product IDs to other canonical directories, and
`release_config` points to the existing local release configuration. The
`--quiet` option emits no output and exits zero for hook use, recording errors
in `state_dir/errors.log`. If the config cannot be read, it uses the private
host fallback at `~/.local/state/plugin-change-tracking/errors.log`. Ordinary
CLI mode returns JSON or a nonzero error.

The state directory contains a mode-0600 `journal.json` and `journal.lock`.
Journal schema version 1 has `revision`, `initialized_at`, `observed_at`,
`products`, `events`, and `pending_refresh_ids`. Each product has a relative
path-to-file map with SHA-256 and stat cache. Each material event has an ID,
time, origin, and added/edited/deleted file changes with before and after
hashes. A timestamp-only change refreshes the stat cache without advancing
the revision or `observed_at`. Nested links store their target string and link
hash; their external contents are not read.

Unavailable roots and missing mounted overrides preserve prior observations.
Malformed journals are never overwritten. An optional release queue refresh
uses only `release_manager.pending.refresh` under the existing nonblocking
`completion.lock`; outstanding product IDs remain in the journal for retry if
the public source, queue, or lock is unavailable. The queue's separate semantic
notes and publication decision stay with the release owner.

Verify with `python3 -B -m unittest tests/test_plugin_change_record.py -v`.


## Event wiring

Use one explicitly adopted Stop command hook for the configured recorder with
`--quiet` and a fixed origin label. A private companion plugin may own the
registration and local binding while this plugin retains the portable engine.
Codex supports plugin-owned hooks; a host-user registration is another option.
Claude Code can use its current plugin or user settings hook surface. Preserve every existing
registration and enable/trust this exact command through the supported host
configuration. Bind the command to the maintained script and local Python
interpreter. No model continuation, timer, polling loop or publication command
belongs in this hook. Existing chats may need a new session to discover a new
registration. A native host readback verifies discovery/trust; invoking the
handler verifies recording, not a model-driven session's dispatch.

The existing Obsidian filesystem listener can call the same recorder, then
render recent journal events into one generated **Local changes** note. Link
observations to the existing plugin notes. Preserve user-edited notes using the
vault's conflict-safe merge, and leave graph settings, canvases and custom notes
alone. For supporting-file events, reuse the cached inventory; metadata changes
and vault opening use the existing inventory collector.

This is batch observation, not an editor history or attribution system. Reverted
intermediate saves between observations may not be recorded. If both the host
and vault are closed, the next completion/open reconciles the current state.
The pending release queue remains authoritative for differences from public
packages; the observation journal retains history even after publication.
