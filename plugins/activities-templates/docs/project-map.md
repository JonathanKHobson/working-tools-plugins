# Activities Templates project map

- `plugin.json`/`mcp.json` and the native `.codex-plugin/plugin.json`/`.mcp.json`: one discovery skill and twelve preserved fixed-domain registrations.
- `scripts/atlas_library_mcp.py`: stdlib bootstrap, operator binding and fixed-domain process startup.
- `runtime/studio_library/`: canonical server, scoped catalog/index builder, domain registry, narrow Atlas ID helpers and explicit private search-feedback code. Private databases and vaults stay external.
- `runtime/studio_library/ui/`: preserved Activities chooser adapter and shared chooser presentation. Design Templates owns shared visual conventions; no private corpus is packaged here.
- `skills/activity-library/` and `references/catalog-use.md`: discovery and complete selected-source workflow. `references/setup.md`: Python/data requirements, binding and unavailable states.
- `library/public-edition.json` and `SOURCE-NOTES.md`: inspected public-edition metadata and source/rights boundary. No guide bodies or source notes are included.
- `tests/test_runtime.py`: isolated synthetic-catalog tests including actual stdio tool/resource contracts. `scripts/export_fixture.py`: synthetic private-export rendering fixture with no real notes.

Safe verification: run the tests with a Python environment containing `mcp` and `PyYAML`: `python -B -m unittest discover -s tests -v`. Run `python -B scripts/export_fixture.py --output <external-evidence-directory>` for the synthetic chooser HTML. Source/installation parity and native-host rendering are separate checks. Edit domain rules in `domains.json`, binding behavior in `binding.py`, retrieval in `catalog.py`, and host contracts in `server.py`.
