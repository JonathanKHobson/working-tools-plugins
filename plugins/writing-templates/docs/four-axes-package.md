# Four-axis package integration

`library/voice-library/axes/four-axes.json` is the authored source. It covers each registered ID with voice, tone, style and format summaries, term selections, editorial prominence levels, source evidence, constraints and a format policy. The levels are ordinal editorial descriptions, not numeric QA thresholds. Complete selected, base and routed module guides remain authoritative.

Generate or verify the library reading views:

```sh
python3 scripts/build_axis_references.py --write
python3 scripts/build_style_entries.py
python3 scripts/build_axis_references.py --check
python3 scripts/build_style_entries.py --check
python3 -m unittest discover -s tests -p 'test_four_axes.py'
```

`--write` creates `styles/{ID}/axes/README.md`, four Markdown pages and `profile.json`, then records their hashes and the source JSON hash in the runtime approved-source manifest. `STYLE.md` stays the entrypoint. The native handoff reads the actual selected/base/module route, includes its scoped profiles and checked reference files, and directs the writer to read these after guide authority and before drafting. The full plugin builder includes the source JSON and generated references through its existing library allowlist.

To prepare new portable archives from an existing public downloads tree, supply a **separate** empty staging directory:

```sh
python3 scripts/build_axis_references.py --check \
  --zip-input-dir /path/to/current-public/writing-library/downloads \
  --zip-output-dir /path/to/staging/writing-axes-v1
```

Each source may be `downloads/{ID}/bundle.zip` or a flat `writing-resource-{id}.zip` release asset. For an additive bundle held elsewhere, pass `--zip-override P49=/absolute/path/to/bundle.zip`. The script writes `writing-resource-{id}-axes-v1.zip` into staging, preserving each archive's existing guides, examples, selected/base/module route, QA files and other members. It adds `axes/` pages and a scoped `axes/profile.json`, closes links to cited evidence under `references/`, updates `agent-manifest.json`, and appends an explicit SKILL.md reading instruction. Existing evidence files must match the canonical source bytes. It refuses to write over a staged archive or into the source downloads directory. Uploading, catalog URL changes and Site publication are separate release steps. Do not run `build_voice_public.py` for this addition; it predates the additive P49 projection.

The additive P49 source archive also carries an older 48-profile `axes/four-axes.json`. The new P49 archive replaces that member with the current 49-profile canonical source and replaces its old general axes README with the scoped P49 reading guide. Its `P49-authoring.json` remains for provenance. The original source ZIP is unchanged.

For a reviewed subset while another resource profile is still being authored, omit `--check` and pass `--ids V01,V02` with the ZIP input/output pair. Full `--write`, `--check` and plugin build require all registered profiles.


Collection-dependent history and commands describe the maintained source-owner collection. Its bodies and private integrity pins are excluded from public distribution. Bind your own authorized collection before running those commands; the fresh public runtime uses its documented fixture or included eligible kits.
