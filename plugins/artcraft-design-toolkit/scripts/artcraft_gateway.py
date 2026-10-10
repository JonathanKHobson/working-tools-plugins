#!/usr/bin/env python3
"""One on-demand ArtCraft MCP gateway. Python standard library only."""

from __future__ import annotations

import collections
import json
import os
from pathlib import Path
import queue
import signal
import subprocess
import sys
import threading
import tempfile
from typing import Any

APPS = ("photocraft", "vectorcraft", "filmcraft", "lightcraft", "pdfcraft", "effectcraft", "designcraft")
CLI_COMMANDS = {
    "photocraft": {"convert", "info", "run", "batch", "droplet", "commands"},
    "vectorcraft": {"commands", "run", "convert", "info"},
    "filmcraft": {"commands", "describe", "inspect", "exec", "import", "export", "run", "help"},
    "lightcraft": {"commands", "controls", "run", "render", "calibrate"},
    "pdfcraft": {"info", "render", "text", "edit", "combine", "extract", "split", "check", "tools", "run", "ui", "help"},
    "effectcraft": {"info", "commands", "exec", "props", "set", "get", "run", "render-frame", "script"},
    "designcraft": {"commands", "describe", "script", "run", "app"},
}
MAX_LINE = 8 * 1024 * 1024
MAX_CLI_OUTPUT = 2 * 1024 * 1024
NATIVE_TIMEOUT = 45


def home_path() -> Path:
    value = os.environ.get("ARTCRAFT_HOME")
    if not value:
        config = Path.home() / ".config/artcraft-toolkit/host.json"
        try:
            data = json.loads(config.read_text())
            value = data.get("artcraft_home")
        except (FileNotFoundError, OSError, ValueError, TypeError):
            pass
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Set ARTCRAFT_HOME or ~/.config/artcraft-toolkit/host.json artcraft_home")
    root = Path(value).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("ArtCraft home is not a directory")
    return root


def cli_path(app: str) -> Path:
    if app not in APPS:
        raise ValueError(f"Unknown app: {app}")
    root = home_path()
    candidate = root / "cli" / app / f"{app}-cli"
    path = candidate.resolve(strict=True)
    if not path.is_relative_to(root) or not path.is_file() or not os.access(path, os.X_OK):
        raise ValueError(f"CLI is missing, outside ArtCraft home, or not executable: {candidate}")
    return path


def project_path(raw: str) -> Path:
    path = Path(raw).expanduser().resolve(strict=True)
    if not path.is_dir() or not os.access(path, os.W_OK):
        raise ValueError("project_root must be an existing writable directory")
    return path


def native_args(app: str, mode: str, root: Path, options: dict[str, Any]) -> list[str]:
    if mode not in ("headless", "live"):
        raise ValueError("mode must be headless or live")
    args = ["mcp"]
    if mode == "live":
        if app == "pdfcraft":
            raise ValueError("PdfCraft has no documented live MCP mode; use its CLI ui command")
        port = options.get("port", {"photocraft": 7878, "vectorcraft": 7979, "filmcraft": 9876, "lightcraft": 7980, "effectcraft": 9877, "designcraft": 7979}[app])
        if type(port) is not int or not 1024 <= port <= 65535:
            raise ValueError("port must be an integer from 1024 to 65535")
        if app == "photocraft":
            token = options.get("token_file")
            if not isinstance(token, str) or not Path(token).is_file():
                raise ValueError("PhotoCraft live mode requires an existing token_file")
            args += ["--bridge", f"127.0.0.1:{port}", "--control-token-file", token]
        elif app == "designcraft":
            args += ["--connect", str(port)]
        elif app in ("vectorcraft", "lightcraft"):
            args += ["--connect", f"127.0.0.1:{port}"]
        else:
            args += ["--bridge", f"127.0.0.1:{port}" if app == "filmcraft" else str(port)]
        return args
    if app == "photocraft":
        args += ["--automation-read-root", str(root), "--automation-write-root", str(root)]
    elif app == "vectorcraft":
        args += ["--headless"]
    elif app == "filmcraft":
        project = options.get("project")
        if project:
            p = Path(project).expanduser().resolve(strict=True)
            if not p.is_file() or not p.is_relative_to(root):
                raise ValueError("FilmCraft project must be an existing file under project_root")
            args += ["--project", str(p)]
        else:
            args += ["--demo"]
    elif app == "lightcraft":
        library = root / ".artcraft-library" / "lightcraft"
        library.mkdir(parents=True, exist_ok=True)
        args += ["--library", str(library)]
    elif app == "pdfcraft":
        args += ["--root", str(root), "--compact"]
    elif app == "effectcraft" and options.get("autosave", True):
        args += ["--autosave"]
    return args


class NativeSession:
    def __init__(self, app: str, mode: str, root: Path, options: dict[str, Any]):
        self.app, self.mode, self.root = app, mode, root
        self.args = native_args(app, mode, root, options)
        env = os.environ.copy()
        tmp = root / ".artcraft-tmp"
        tmp.mkdir(exist_ok=True)
        env["TMPDIR"] = str(tmp)
        if app == "effectcraft":
            config = root / ".artcraft-config" / "effectcraft"
            config.mkdir(parents=True, exist_ok=True)
            env["EFFECTCRAFT_CONFIG_DIR"] = str(config)
        self.proc = subprocess.Popen([str(cli_path(app)), *self.args], cwd=root, env=env,
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     bufsize=0, start_new_session=True)
        self.pending: dict[int, queue.Queue[dict[str, Any]]] = {}
        self.pending_lock = threading.Lock()
        self.write_lock = threading.Lock()
        self.next_id = 1
        self.stderr_tail: collections.deque[str] = collections.deque(maxlen=80)
        threading.Thread(target=self._read_stdout, daemon=True).start()
        threading.Thread(target=self._read_stderr, daemon=True).start()
        try:
            result = self.request("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                                                  "clientInfo": {"name": "artcraft-toolkit", "version": "0.2.1"}}, 20)
            if "result" not in result:
                raise RuntimeError(f"Native initialize failed: {result.get('error', result)}")
            self.notify("notifications/initialized")
        except BaseException:
            self.close()
            raise

    def _read_stdout(self) -> None:
        assert self.proc.stdout is not None
        while True:
            line = self.proc.stdout.readline(MAX_LINE + 1)
            if not line:
                break
            if len(line) > MAX_LINE or not line.endswith(b"\n"):
                self.close()
                break
            try:
                message = json.loads(line)
            except ValueError:
                continue
            if isinstance(message, dict) and isinstance(message.get("id"), int):
                with self.pending_lock:
                    waiter = self.pending.pop(message["id"], None)
                if waiter is not None:
                    waiter.put(message)
        with self.pending_lock:
            for waiter in self.pending.values():
                waiter.put({"error": {"message": "Native MCP server closed"}})
            self.pending.clear()

    def _read_stderr(self) -> None:
        assert self.proc.stderr is not None
        while chunk := self.proc.stderr.read(4096):
            self.stderr_tail.append(chunk.decode("utf-8", errors="replace")[-4096:])

    def _send(self, message: dict[str, Any]) -> None:
        raw = (json.dumps(message, separators=(",", ":")) + "\n").encode()
        if len(raw) > MAX_LINE:
            raise ValueError("Native request exceeds 8 MiB")
        with self.write_lock:
            if self.proc.poll() is not None or self.proc.stdin is None:
                raise RuntimeError("Native MCP server is closed")
            self.proc.stdin.write(raw)
            self.proc.stdin.flush()

    def notify(self, method: str) -> None:
        self._send({"jsonrpc": "2.0", "method": method})

    def request(self, method: str, params: dict[str, Any], timeout: int = NATIVE_TIMEOUT) -> dict[str, Any]:
        waiter: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=1)
        with self.pending_lock:
            ident = self.next_id
            self.next_id += 1
            self.pending[ident] = waiter
        try:
            self._send({"jsonrpc": "2.0", "id": ident, "method": method, "params": params})
            return waiter.get(timeout=timeout)
        except queue.Empty as exc:
            raise TimeoutError(f"Native {method} timed out after {timeout}s; operation may have completed") from exc
        finally:
            with self.pending_lock:
                self.pending.pop(ident, None)

    def close(self) -> None:
        if self.proc.poll() is None:
            try:
                if self.proc.stdin:
                    self.proc.stdin.close()
                self.proc.wait(timeout=3)
            except (OSError, subprocess.TimeoutExpired):
                self.proc.terminate()
                try:
                    self.proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self.proc.kill()
                    self.proc.wait(timeout=3)


def tool_schema(name: str, description: str, properties: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
    return {"name": name, "description": description,
            "inputSchema": {"type": "object", "properties": properties, "required": required or []}}


TOOLS = [
    tool_schema("installed_status", "Report installed CLI paths and the active session without launching apps.", {}),
    tool_schema("open_session", "Start one selected native ArtCraft MCP server. Live mode needs an already-running desktop app.",
                {"app": {"type": "string", "enum": list(APPS)}, "mode": {"type": "string", "enum": ["headless", "live"]},
                 "project_root": {"type": "string"}, "options": {"type": "object"}}, ["app", "mode", "project_root"]),
    tool_schema("native_tools", "Return the selected app's actual native MCP tools and input schemas.", {}),
    tool_schema("native_call", "Call a discovered tool on the selected native MCP server; preserves native content and images.",
                {"name": {"type": "string"}, "arguments": {"type": "object"}}, ["name"]),
    tool_schema("close_session", "Close the active native MCP server and its child process.", {}),
    tool_schema("cli_run", "Run one allowlisted CLI command on a selected installed ArtCraft app, without a shell.",
                {"app": {"type": "string", "enum": list(APPS)}, "argv": {"type": "array", "items": {"type": "string"}},
                 "project_root": {"type": "string"}, "timeout_seconds": {"type": "integer", "minimum": 1, "maximum": 120}},
                ["app", "argv", "project_root"]),
]


class Gateway:
    def __init__(self):
        self.session: NativeSession | None = None
        self.lock = threading.RLock()
        self.output_lock = threading.Lock()
        self.workers: set[threading.Thread] = set()
        self.worker_slots = threading.BoundedSemaphore(8)

    def emit(self, data: dict[str, Any]) -> None:
        raw = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        with self.output_lock:
            sys.stdout.write(raw + "\n")
            sys.stdout.flush()

    @staticmethod
    def result(value: Any) -> dict[str, Any]:
        return {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}]}

    def tool_call(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        with self.lock:
            if name == "installed_status":
                found = {}
                for app in APPS:
                    try:
                        found[app] = str(cli_path(app))
                    except (OSError, ValueError) as exc:
                        found[app] = {"error": str(exc)}
                return self.result({"installed": found, "active": self.session.app if self.session else None})
            if name == "open_session":
                if self.session:
                    raise ValueError(f"{self.session.app} session is active; save its work and close_session explicitly")
                app, mode = args["app"], args["mode"]
                root = project_path(args["project_root"])
                options = args.get("options", {})
                if not isinstance(options, dict):
                    raise ValueError("options must be an object")
                self.session = NativeSession(app, mode, root, options)
                return self.result({"app": app, "mode": mode, "pid": self.session.proc.pid,
                                    "project_root": str(root), "native_args": self.session.args})
            if name == "close_session":
                if self.session:
                    app = self.session.app
                    self.session.close()
                    self.session = None
                    return self.result({"closed": app})
                return self.result({"closed": None})
            if name == "native_tools":
                if not self.session:
                    raise ValueError("Open a session first")
                response = self.session.request("tools/list", {})
                if "error" in response:
                    raise RuntimeError(response["error"])
                return self.result(response["result"])
            if name == "native_call":
                if not self.session:
                    raise ValueError("Open a session first")
                native_name = args["name"]
                if not isinstance(native_name, str) or not native_name:
                    raise ValueError("name must be a nonempty string")
                native_args = args.get("arguments", {})
                if not isinstance(native_args, dict):
                    raise ValueError("arguments must be an object")
                response = self.session.request("tools/call", {"name": native_name, "arguments": native_args})
                if "error" in response:
                    return {"isError": True, "content": [{"type": "text", "text": json.dumps(response["error"])}]}
                native_result = response.get("result")
                if not isinstance(native_result, dict) or "content" not in native_result:
                    raise RuntimeError("Native tools/call returned no content")
                return native_result
            if name == "cli_run":
                if self.session:
                    raise ValueError("Close the active session before starting a separate CLI process")
                app = args["app"]
                argv = args["argv"]
                if not isinstance(argv, list) or not argv or not all(isinstance(v, str) for v in argv):
                    raise ValueError("argv must be a nonempty string array")
                if argv[0] not in CLI_COMMANDS.get(app, set()) | {"--help", "--version"}:
                    raise ValueError("CLI subcommand is not allowlisted")
                root = project_path(args["project_root"])
                timeout = args.get("timeout_seconds", 30)
                if type(timeout) is not int or not 1 <= timeout <= 120:
                    raise ValueError("timeout_seconds must be 1 to 120")
                env = os.environ.copy()
                tmp = root / ".artcraft-tmp"
                tmp.mkdir(exist_ok=True)
                env["TMPDIR"] = str(tmp)
                if app == "effectcraft":
                    config = root / ".artcraft-config" / "effectcraft"
                    config.mkdir(parents=True, exist_ok=True)
                    env["EFFECTCRAFT_CONFIG_DIR"] = str(config)
                with tempfile.TemporaryFile(dir=tmp) as stdout_file, tempfile.TemporaryFile(dir=tmp) as stderr_file:
                    try:
                        proc = subprocess.Popen([str(cli_path(app)), *argv], cwd=root, env=env,
                                                stdin=subprocess.DEVNULL, stdout=stdout_file, stderr=stderr_file)
                        try:
                            proc.wait(timeout=timeout)
                            done = proc
                        finally:
                            if proc.poll() is None:
                                proc.terminate()
                                try:
                                    proc.wait(timeout=3)
                                except subprocess.TimeoutExpired:
                                    proc.kill()
                                    proc.wait(timeout=3)
                    except subprocess.TimeoutExpired as exc:
                        raise TimeoutError(f"CLI timed out after {timeout}s; inspect outputs before retrying") from exc
                    if stdout_file.tell() > MAX_CLI_OUTPUT or stderr_file.tell() > MAX_CLI_OUTPUT:
                        raise ValueError("CLI output exceeded 2 MiB; narrow the command")
                    stdout_file.seek(0)
                    stderr_file.seek(0)
                    return self.result({"exit_code": done.returncode,
                                        "stdout": stdout_file.read().decode(errors="replace"),
                                        "stderr": stderr_file.read().decode(errors="replace")})
            raise ValueError(f"Unknown gateway tool: {name}")

    def handle(self, message: dict[str, Any]) -> None:
        ident = message.get("id")
        if ident is None:
            return
        try:
            method = message.get("method")
            if method == "initialize":
                version = message.get("params", {}).get("protocolVersion", "2024-11-05")
                if version not in ("2024-11-05", "2025-03-26", "2025-06-18"):
                    version = "2025-06-18"
                result = {"protocolVersion": version, "capabilities": {"tools": {"listChanged": False}},
                          "serverInfo": {"name": "artcraft-toolkit", "version": "0.2.1"}}
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": TOOLS}
            elif method == "tools/call":
                params = message.get("params", {})
                result = self.tool_call(params.get("name"), params.get("arguments", {}))
            else:
                self.emit({"jsonrpc": "2.0", "id": ident, "error": {"code": -32601, "message": "Method not found"}})
                return
            self.emit({"jsonrpc": "2.0", "id": ident, "result": result})
        except Exception as exc:
            self.emit({"jsonrpc": "2.0", "id": ident,
                       "result": {"isError": True, "content": [{"type": "text", "text": str(exc)}]}})

    def run(self) -> None:
        # One stateful session: serialize requests so pipelined writes retain order.
        def stop(signum, frame):
            raise SystemExit(128 + signum)
        signal.signal(signal.SIGTERM, stop)
        signal.signal(signal.SIGINT, stop)
        try:
            while True:
                raw = sys.stdin.buffer.readline(MAX_LINE + 1)
                if not raw:
                    break
                if len(raw) > MAX_LINE:
                    raise ValueError("Gateway request exceeds 8 MiB")
                try:
                    message = json.loads(raw)
                except ValueError:
                    continue
                if isinstance(message, dict):
                    self.handle(message)
        finally:
            if self.session:
                self.session.close()


if __name__ == "__main__":
    if len(sys.argv) != 1:
        raise SystemExit("usage: artcraft_gateway.py (MCP stdio)")
    Gateway().run()
