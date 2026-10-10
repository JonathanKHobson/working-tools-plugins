# Installation and runtime

Install this complete directory through the supported host plugin flow. See the [shared public installation guide](https://github.com/JonathanKHobson/working-tools-plugins/blob/main/docs/install.md). Methods can be used without the MCP dependencies.

Prepare Python 3.10+ for the local MCP App from the plugin root:

```sh
python3 -m venv .runtime/venv
.runtime/venv/bin/python -m pip install -r runtime/data-explorer/requirements.txt
```

The launcher always runs this package's `runtime/data-explorer/server.py`. It chooses the interpreter and saved-data location independently:

| Setting | First choice | Existing private binding | Default |
| --- | --- | --- | --- |
| Interpreter | `DATA_EXPLORER_PYTHON` | `interpreter` | `.runtime/venv/bin/python` (or `Scripts/python.exe` on Windows) |
| Saved data | `DATA_EXPLORER_DATA_DIR` | `data_dir` | `$XDG_DATA_HOME/working-tools/data-explorer` or `~/.local/share/working-tools/data-explorer` |

The optional binding is `~/.config/studio-tools/data-explorer.json`. `DATA_EXPLORER_BINDING` selects another absolute JSON file path. Configured paths must be absolute; a leading `~` is expanded. Complete interpreter and data-directory environment overrides bypass the default binding. An explicitly selected binding is always validated. A missing explicit file, malformed required binding or empty configured path fails with an actionable error. The launcher does not install dependencies, edit bindings, inspect saved datasets or repair configuration.

Existing `interpreter` and `data_dir` values continue to work. A legacy `server` field can remain for rollback but does not override this package's bundled server. Back up an existing binding before changing it; do not commit personal paths or data. These settings control runtime location, not optional provider procedures, which use the separate [provider-source binding](../references/provider-methods.md).

The manifest uses the supported plugin-root expansion; hosts with another configuration contract should invoke `python3 /absolute/plugin/scripts/data_explorer_mcp.py` using their documented stdio setup.

The checked-in self-contained app resource can run without Node. To rebuild, install Node 22+ and run from `runtime/data-explorer`:

```sh
npm ci --ignore-scripts
npm run build
```

Run behavior and calculation parity tests from the plugin root:

```sh
.runtime/venv/bin/python -B -m unittest discover -s runtime/data-explorer/tests -v
python3 -B -m unittest discover -s tests -v
```

`runtime/data-explorer/preview.py --data-dir /recipient/temporary/directory` is a loopback-only QA harness, not native host acceptance. Close the task-owned preview server after inspection. The package contains no data/state, environment, node_modules, private config or proprietary Visualize bytes. Native MCP Apps support and host discussion delivery must be observed in the recipient host before claiming them.

Agent Plugins clients discover schema-valid `mcp.json` using `${PLUGIN_ROOT}`. Codex/Claude native identities use `.mcp.json` with their supported native plugin-root expansion. Exercise either transport after preparing Python: `python examples/sample_stdio.py` for native configuration, or add `--portable` for portable configuration. Use the prepared environment Python for the sample.
