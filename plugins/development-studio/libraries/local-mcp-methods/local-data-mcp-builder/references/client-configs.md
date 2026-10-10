# Client Configs

## Codex

Config file:

```text
~/.codex/config.toml
```

Pattern:

```toml
[mcp_servers.example_server]
command = "/absolute/path/to/python"
args = ["/absolute/path/to/server.py", "--root", "/absolute/path/to/data"]
```

Important:

- Existing Codex sessions usually do not hot-load newly added MCPs.
- Start a fresh Codex session after editing the config.
- Before any batch edit, run `back up the active Codex config with the host-approved config workflow`.
- After editing, run `validate a scratch copy with the host-approved Codex config validator` and do not restart until it prints `OK`.
- If the same server should exist in multiple clients, compare the final config files instead of assuming earlier edits propagated.
- Prefer direct interpreter launchers over shell wrappers; they are more portable across clients on some macOS hosts.
- If `uvx` is not on PATH, use the explicit launcher that is available on some macOS hosts, for example:

```toml
command = "/Applications/Xcode.app/Contents/Developer/usr/bin/python3"
args = ["-m", "uv", "tool", "run", "--from", "idea-reality-mcp", "idea-reality-mcp"]
```
- For npm packages with multiple published bins, use the actual binary name from `npm view <package> bin` rather than the package name itself.

## Claude Desktop

Config file:

```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

Pattern:

```json
{
  "mcpServers": {
    "example-server": {
      "command": "/absolute/path/to/python",
      "args": [
        "/absolute/path/to/server.py",
        "--root",
        "/absolute/path/to/data"
      ]
    }
  }
}
```

Important:

- Claude Desktop usually needs a full quit/reopen after config changes.
- If the JSON file already contains user preferences, merge carefully instead of replacing it.
- A server appearing in Codex does not imply it is present in Claude Desktop; the JSON must contain its own matching entry.
- Default daily Claude Desktop profile on some macOS hosts is `claude_desktop_config.minimal-profile.json`.
- Keep named profile files alongside the live config:
  - `claude_desktop_config.minimal-profile.json`
  - `claude_desktop_config.task-profile-a.json`
  - `claude_desktop_config.task-profile-b.json`
  - `claude_desktop_config.quarantine-profile.json`
  - `claude_desktop_config.full-fleet.json`
- When the fleet is unstable, switch profiles instead of adding more servers to the active config.
- Prefer a direct interpreter command here. Avoid `/bin/bash <external-volume>/run_server.sh` launchers on external drives; Claude Desktop has rejected that pattern with `Operation not permitted` on some macOS hosts.
- For remote OAuth MCPs, prefer a stable loopback callback host and fixed port instead of relying on a fragile default browser handoff.
- If a package installer rewrites the Claude config, re-check the final file before assuming the server itself is broken.
- For package-based Python MCPs, prefer a launcher that resolves the tool explicitly rather than assuming `uvx` is on PATH.
- If an MCP does heavy first-run data ingestion, raise the startup timeout in both Codex and Claude Desktop so the client does not cancel a server that is still warming its cache.
- If an npm MCP depends on a native addon and the local install can land on the wrong architecture, wrap the command in an explicit architecture selector such as `arch -arm64` so Claude and Codex launch the same CPU slice you tested.
- For .NET MCPs on external drives, prefer `dotnet /absolute/path/to/ToolBox.dll --stdio` over `dotnet run --project ...` once the project has already been built. The DLL launch avoids project-file lookup during client attach and is usually more stable in Claude.
- Run `python3 <development-studio-plugin>/libraries/local-mcp-methods/local-data-mcp-builder/scripts/check_claude_mcp_fleet.py` before trusting a newly edited active Claude config.
- Run `<mcp-enabled-python> <development-studio-plugin>/libraries/local-mcp-methods/local-data-mcp-builder/scripts/smoke_claude_profile.py --config <profile-json>` after launcher changes.

## Claude Code

Project config file:

```text
.mcp.json
```

Pattern:

```json
{
  "mcpServers": {
    "example-server": {
      "command": "/absolute/path/to/python",
      "args": [
        "/absolute/path/to/server.py",
        "--root",
        "/absolute/path/to/data"
      ]
    }
  }
}
```

Important:

- Claude Code expects the workspace root to contain the `.mcp.json`.
- If the user opens the wrong parent folder, the MCP may not appear even though the config is correct.
- Use [scripts/compare_client_mcp_configs.py](../scripts/compare_client_mcp_configs.py) after setup if multiple clients should expose the same server names.
- Reuse the same direct interpreter pattern here unless there is a strong reason not to.
