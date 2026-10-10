# Installation and runtime

Install this complete directory through the supported host plugin flow. See the [shared public installation guide](https://github.com/JonathanKHobson/working-tools-plugins/blob/main/docs/install.md). Methods can be used without the MCP dependencies.

Prepare Python 3.10+ for the local MCP App from the plugin root:

```sh
python3 -m venv .runtime/venv
.runtime/venv/bin/python -m pip install -r runtime/data-explorer/requirements.txt
```

The launcher uses `.runtime/venv/bin/python` by default. Set `DATA_EXPLORER_PYTHON` to an absolute Python path for an environment outside the plugin. Set `DATA_EXPLORER_DATA_DIR` for recipient-owned storage; otherwise it uses the XDG data directory or the user's local share directory. No dependency installation or repair occurs during MCP startup. The manifest uses the supported plugin-root expansion; hosts with another configuration contract should invoke `python3 /absolute/plugin/scripts/data_explorer_mcp.py` using their documented stdio setup.

The checked-in self-contained app resource can run without Node. To rebuild, install Node 22+ and run from `runtime/data-explorer`:

```sh
npm ci --ignore-scripts
npm run build
```

Run behavior and calculation parity tests from the plugin root:

```sh
.runtime/venv/bin/python -B -m unittest discover -s runtime/data-explorer/tests -v
```

`runtime/data-explorer/preview.py --data-dir /recipient/temporary/directory` is a loopback-only QA harness, not native host acceptance. Close the task-owned preview server after inspection. The package contains no data/state, environment, node_modules, private config or proprietary Visualize bytes. Native MCP Apps support and host discussion delivery must be observed in the recipient host before claiming them.

Agent Plugins clients discover schema-valid `mcp.json` using `${PLUGIN_ROOT}`. Codex/Claude native identities use `.mcp.json` with their supported native plugin-root expansion. Exercise either transport after preparing Python: `python examples/sample_stdio.py` for native configuration, or add `--portable` for portable configuration. Use the prepared environment Python for the sample.
