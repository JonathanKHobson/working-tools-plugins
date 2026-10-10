#!/usr/bin/env python3
"""Task-scoped MCP client for Critical Compass's full tool profile.

The ordinary plugin MCP registration stays on its compact routine profile.
This client starts one full-profile backend subprocess for one explicit request,
writes the complete response to a caller-owned file, then exits.
"""

import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
import sys



def binding(path: Path) -> tuple[str, list[str], dict[str, str]]:
    config = json.loads(path.read_text())["critical-compass"]
    interpreter = Path(config["interpreter"]).expanduser().absolute()
    server = Path(config["server"]).expanduser().resolve(strict=True)
    if not interpreter.is_file() or not os.access(interpreter, os.X_OK) or not server.is_file():
        raise ValueError("Critical Compass selected binding points to an unavailable runtime")
    extra = config.get("args", [])
    if not isinstance(extra, list) or not all(isinstance(v, str) for v in extra):
        raise ValueError("Invalid Critical Compass launch arguments")
    # Replace the binding's profile in this child only; leave other paths and
    # options (including the canonical writable state path) intact.
    args = []
    index = 0
    while index < len(extra):
        item = extra[index]
        if item == "--tool-profile":
            if index + 1 >= len(extra):
                raise ValueError("--tool-profile lacks a value")
            index += 2
            continue
        if item.startswith("--tool-profile="):
            index += 1
            continue
        args.append(item)
        index += 1
    additions = config.get("env", {})
    if not isinstance(additions, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in additions.items()):
        raise ValueError("Invalid Critical Compass environment settings")
    return str(interpreter), [str(server), *args, "--tool-profile", "full"], additions


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    tmp.replace(path)


async def run(options: argparse.Namespace) -> dict:
    interpreter, server_args, additions = binding(options.binding.expanduser())
    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
    except ModuleNotFoundError as exc:
        # Preserve the original venv re-exec lane only for the missing MCP SDK.
        if exc.name != "mcp" or os.environ.get("REASONING_FULL_CLIENT_REEXEC") == "1":
            raise ValueError("Selected environment lacks the MCP SDK; install it in the reviewed provider environment") from exc
        os.execve(interpreter, [interpreter, __file__, *sys.argv[1:]], dict(os.environ, REASONING_FULL_CLIENT_REEXEC="1"))
    if options.state_db_path:
        server_args += ["--state-db-path", str(options.state_db_path.expanduser().absolute())]
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.update(additions)
    params = StdioServerParameters(command=interpreter, args=server_args, env=env)
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            names = {item.name for item in tools}
            if options.action == "discover":
                payload = {"profile": "full", "tool_count": len(tools), "tools": sorted(names)}
            elif options.action == "schema":
                match = next((item for item in tools if item.name == options.tool), None)
                if match is None:
                    raise ValueError(f"Unknown full-profile tool: {options.tool}")
                payload = match.model_dump(mode="json")
            else:
                request = json.loads(options.request.read_text())
                if not isinstance(request, dict) or not isinstance(request.get("tool"), str) or not isinstance(request.get("arguments", {}), dict):
                    raise ValueError("Request must contain a tool name and an arguments object")
                name = request["tool"]
                if name not in names:
                    raise ValueError(f"Unknown full-profile tool: {name}")
                result = await session.call_tool(name, request.get("arguments", {}))
                payload = {"tool": name, "result": result.model_dump(mode="json")}
    write_json(options.output, payload)
    digest = hashlib.sha256(options.output.read_bytes()).hexdigest()
    receipt = {"action": options.action, "output": str(options.output), "sha256": digest}
    if options.action == "discover":
        receipt["tool_count"] = payload["tool_count"]
    elif options.action == "schema":
        receipt["tool"] = options.tool
    else:
        result = payload["result"]
        data = result.get("structuredContent") or {}
        receipt.update(tool=payload["tool"], is_error=result.get("isError", False),
                       status=data.get("status"), pause_required=data.get("PAUSE_REQUIRED"),
                       host_must_pause=(data.get("human_loop_host_action") or {}).get("must_pause"))
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binding", type=Path, required=True, help="Operator-selected Compass JSON binding; no personal default")
    parser.add_argument("action", choices=("discover", "schema", "call"))
    parser.add_argument("output", type=Path, help="File for complete JSON response")
    parser.add_argument("--tool", help="Exact tool name for schema")
    parser.add_argument("--request", type=Path, help="JSON file with tool and arguments for call")
    parser.add_argument("--state-db-path", type=Path, help="Explicit isolated state DB for testing")
    options = parser.parse_args()
    if (options.action == "schema" and not options.tool) or (options.action == "call" and not options.request):
        parser.error("schema requires --tool; call requires --request")
    try:
        receipt = asyncio.run(run(options))
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(f"Critical Compass full-profile client failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(receipt, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
