# Troubleshooting

## MCP exists on disk but is not visible

Check in this order:

1. The server command exists.
2. The config entry exists in the right client config file.
3. If the server should exist in multiple clients, compare the config files for drift.
4. The project root is correct for `.mcp.json` setups.
5. The Python/runtime path is still valid.
6. The server can list tools via a real MCP client.
7. The client has been restarted or reopened as needed.

Do not jump straight into editing server code.

## Common causes

### Codex

- Config added after the current session started.
- Wrong server key or malformed TOML.
- Command path moved or venv deleted.

### Claude Desktop

- Desktop app not fully restarted after config edit.
- Config JSON overwritten incorrectly.
- Server path contains stale or deleted runtime paths.
- Another client was updated, but Claude Desktop was not.
- Too many Claude MCPs were asked to initialize at once, so the client cancelled a whole startup wave instead of one truly missing server.
- Shell launcher points at a script on `<external-volume>`; Claude Desktop on some macOS hosts has failed that pattern with `Operation not permitted`.
- Claude log already contains the real stderr, but it was not checked.
- Remote OAuth MCPs can keep re-opening a browser if the callback host/port is unstable or the auth cache never completes.
- If the browser lands on a dead-end `cannot reach server` screen after login, check the callback host/port first before blaming the upstream server.
- If the launcher is a Python package tool and `uvx` is missing from PATH, try the explicit interpreter form before assuming the repo is broken.
- If an npm package refuses to start with `could not determine executable to run`, inspect `npm view <package> bin` and launch the published bin name explicitly.
- If an npm package loads a native addon with the wrong CPU slice, force the correct architecture explicitly (for example `arch -arm64` on Apple Silicon) before assuming the package is broken.
- If a .NET MCP works from Terminal but Claude fails on `dotnet run --project`, switch Claude to `dotnet /absolute/path/to/ToolBox.dll --stdio` after a successful build. This avoids project-path resolution during attach and is often the difference between "works in Terminal" and "works in Claude."

### Claude Code

- `.mcp.json` is in the wrong directory.
- The user opened the wrong workspace root.
- The file exists but the server command is invalid.

## Cross-client drift

If Codex sees a server but Claude Desktop or Claude Code does not:

- Compare the final config files directly.
- Do not assume “it works in one client” means the other clients were updated.
- Use [scripts/compare_client_mcp_configs.py](../scripts/compare_client_mcp_configs.py) to check for missing server names across clients.

## Claude Desktop fleet overload / shared timeout wave

If several Claude MCPs fail together, do not assume you have several broken repos.

Evidence pattern:

- multiple servers fail in one Claude boot window
- `~/Library/Logs/Claude/mcp.log` shows repeated `notifications/cancelled`
- the reason is `McpError: MCP error -32001: Request timed out`
- one or more of the same servers can still initialize when isolated

Fix in this order:

1. Switch the active Claude config to the smallest named profile that fits the current task. Default daily profile is `minimal-profile`.
2. Run [scripts/check_claude_mcp_fleet.py](../scripts/check_claude_mcp_fleet.py) against the active config.
3. Remove or quarantine any server with recent `Invalid JSON` or parse-error evidence before re-expanding the profile.
4. Run [scripts/smoke_claude_profile.py](../scripts/smoke_claude_profile.py) against the target profile.
5. Only after the smaller profile still fails should you debug one server's code or launcher.

## Runtime failures

If the server does not even start:

- Verify the interpreter path.
- Verify required packages are installed in that interpreter.
- Run the server command directly in a terminal.
- If needed, use [scripts/check_local_mcp.py](../scripts/check_local_mcp.py).
- If Claude Desktop is the failing client, rerun the checker with `--client claude-desktop`.
- If the command points at a virtualenv Python, preserve that exact launcher path.
- Do not resolve the venv shim all the way to the base interpreter or you may lose the venv packages.
- Check `~/Library/Logs/Claude/mcp-server-<name>.log` for stderr before editing server code.
- If an ESM Node MCP is guarded by `process.argv[1] === new URL(import.meta.url).pathname`, watch for encoded spaces in the file path. Use `fileURLToPath(import.meta.url)` or another decoded comparison when the script lives on a volume path with spaces.

## Claude Desktop shell-launcher failure on external drives

On some macOS hosts, Claude Desktop has failed commands shaped like:

- `/bin/bash <external-volume>/run_server.sh`
- `/bin/sh <external-volume>/launcher.sh`

with:

- `Operation not permitted`

even when the same command works in Terminal.

Safer pattern:

1. Keep the runtime in a home-directory location.
2. Launch the interpreter directly in Claude Desktop.
3. Pass the server script on the external drive as an argument.

Example:

```json
{
  "mcpServers": {
    "example-server": {
      "command": "<home>/.local/share/example-mcp/venv/bin/python",
      "args": [
        "<external-ssd>/Path/To/server.py",
        "--root",
        "<external-ssd>/Path/To/data"
      ]
    }
  }
}
```

## Remote OAuth MCPs

If a remote MCP opens a browser for OAuth every time:

1. Check whether the client config uses a stable callback host and port.
2. Prefer `127.0.0.1` over relying on whatever hostname the wrapper chooses.
3. Confirm the auth flow actually returns to the wrapper instead of stopping on an error page.
4. If the client was rewritten by a package manager or installer, compare the final config file again.
5. If the issue only happens in Codex but not in Terminal, treat it as an MCP wrapper/auth persistence problem rather than a server bug.

## External-drive Python problems

If a Python runtime or virtualenv behaves strangely on an external SSD:

- Look for AppleDouble sidecar files like `._distutils-precedence.pth`.
- These can corrupt Python startup on some setups.
- Prefer keeping the heavy data on the external SSD and the Python runtime in a stable home-directory path.
- Use [scripts/clean_external_python_artifacts.sh](../scripts/clean_external_python_artifacts.sh) if needed.
- If a server does a heavy initial download or build, raise `startup_timeout_sec`/`tool_timeout_sec` and prewarm the cache once in a terminal before relying on Claude Desktop.
- If the failing server is one of the current external-drive-aware MCPs on some macOS hosts, confirm the launcher shape before chasing server code:
  - `chatgpt-history`
- For critical daily MCPs such as Prompt Compass and Critical Compass, keep the runtime in a home-directory path even if the code or DB lives on an external drive.

## External-drive git/npm sidecars

If a clone or build on an external SSD starts failing with weird index or pack errors:

- Check for AppleDouble sidecars like `._pack-*.idx`, `._package-lock.json`, or `._node_modules`.
- These files can confuse git, npm, and some package managers on macOS.
- Clean the sidecars before retrying the install or move the clone to a cleaner directory on the same volume.

## External-drive .NET source sidecars

If a .NET MCP build starts failing on an external SSD with compiler errors against files like `._Program.cs`:

- Treat the problem as a sidecar contamination issue, not a code syntax issue.
- AppleDouble files can be globbed as fake source files by the C# compiler.
- Remove `._*` and `.__*` files from the repo before rebuilding.
- Re-run the build after cleanup and confirm the real source tree no longer contains sidecars.
