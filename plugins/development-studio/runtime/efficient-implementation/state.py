"""Private session preferences and explicitly accepted implementation scope."""

import hashlib
import json
import os
from pathlib import Path
import re
import secrets

from filesystem import directory, read_at

MODES = ("lite", "full", "ultra", "off")
MAX_JSON = 131072
MAX_CONTRACT = 65536


def mode(value):
    if not isinstance(value, str) or value.strip().lower() not in MODES:
        raise ValueError("mode must be lite, full, ultra, or off")
    return value.strip().lower()


def config_dir(explicit=None):
    if explicit:
        selected = Path(explicit).absolute()
    elif os.environ.get("EFFICIENT_IMPLEMENTATION_STATE_DIR"):
        selected = Path(os.environ["EFFICIENT_IMPLEMENTATION_STATE_DIR"]).absolute()
    else:
        base = os.environ.get("XDG_CONFIG_HOME")
        if not base and os.name == "nt":
            base = os.environ.get("APPDATA")
        selected = Path(base or Path.home() / ".config") / "development-studio" / "efficient-implementation"
    # Canonicalize recipient-owned ancestors (for example macOS /var -> /private/var),
    # preserving the selected leaf so a symlink replacing the state directory is refused.
    return selected.parent.resolve() / selected.name


def read_json(path):
    try:
        with directory(path.parent) as parent:
            raw, _ = read_at(parent, path.name, MAX_JSON)
        if len(raw) > MAX_JSON:
            return {}
        value = json.loads(raw.decode("utf-8-sig"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError, UnicodeError):
        return {}


def write_json(path, value):
    with directory(path.parent, create=True) as parent:
        name = ".state-" + secrets.token_hex(16)
        descriptor = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                             mode=0o600, dir_fd=parent)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                os.fchmod(handle.fileno(), 0o600)
                json.dump(value, handle, ensure_ascii=True, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.rename(name, path.name, src_dir_fd=parent, dst_dir_fd=parent)
        finally:
            try:
                os.unlink(name, dir_fd=parent)
            except FileNotFoundError:
                pass


def default_mode(directory):
    candidates = (os.environ.get("EFFICIENT_IMPLEMENTATION_DEFAULT_MODE"),
                  read_json(directory / "config.json").get("default_mode"), "full")
    for candidate in candidates:
        try:
            return mode(candidate)
        except ValueError:
            pass


def set_default(directory, value):
    value = mode(value)
    config = read_json(directory / "config.json")
    config["default_mode"] = value
    write_json(directory / "config.json", config)
    return value


def project_root(value):
    root = Path(value).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("project root must be a directory")
    return root


def digest(value):
    return hashlib.sha256(value).hexdigest()


def contract_file(root, relative):
    if not isinstance(relative, str):
        raise ValueError("contract path must be text")
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("contract must be project-relative without parent traversal")
    with directory(root) as parent:
        content, details = read_at(parent, path, MAX_CONTRACT)
    if not content.strip() or len(content) > MAX_CONTRACT:
        raise ValueError("contract must be nonempty and at most 65536 bytes")
    return {"kind": "file", "path": path.as_posix(), "sha256": digest(content),
            "size": len(content), "mtime_ns": details.st_mtime_ns}


class Session:
    def __init__(self, directory, root, session_id):
        self.directory = Path(directory)
        self.root = project_root(root)
        if not isinstance(session_id, str) or not session_id.strip() or len(session_id) > 256:
            raise ValueError("an explicit session ID of 1 to 256 characters is required")
        self.session_id = session_id
        key = digest((str(self.root) + "\0" + session_id).encode("utf-8"))
        self.path = self.directory / "sessions" / (key + ".json")

    def raw(self):
        value = read_json(self.path)
        if (value.get("version") != 1 or value.get("root") != str(self.root)
                or value.get("session_id") != self.session_id):
            return {}
        return value

    def status(self, scope=None):
        value = self.raw()
        current = value.get("mode", "off")
        ready = value.get("ready") is True and current in MODES and current != "off"
        reason = "accepted" if ready else "not-ready"
        if ready and scope is not None and value.get("scope") != scope:
            ready, reason = False, "scope-changed"
        contract = value.get("contract", {})
        if not isinstance(contract, dict):
            contract = {}
        if ready and (not isinstance(value.get("scope"), str) or not value["scope"].strip() or len(value["scope"]) > 512
                      or not isinstance(contract.get("sha256"), str)
                      or re.fullmatch(r"[a-f0-9]{64}", contract["sha256"]) is None):
            ready, reason = False, "invalid-contract-state"
        if ready and contract.get("kind") == "file":
            try:
                fresh = contract_file(self.root, contract["path"])
                if fresh != contract:
                    ready, reason = False, "contract-changed"
            except (OSError, ValueError, KeyError):
                ready, reason = False, "contract-unavailable"
        elif ready:
            acceptance = contract.get("acceptance")
            if (contract.get("kind") != "inline" or not isinstance(acceptance, str)
                    or not acceptance.strip() or len(acceptance.encode("utf-8")) > 4096
                    or digest(acceptance.encode("utf-8")) != contract["sha256"]):
                ready, reason = False, "contract-unavailable"
        return {"mode": current if current in MODES else "off", "active": ready,
                "ready": ready, "reason": reason, "scope": value.get("scope"),
                "contract_sha256": contract.get("sha256"),
                "badge": "[efficient-implementation:" + (current if ready else "off") + "]"}

    def set(self, value=None, *, ready=False, scope=None, contract=None, acceptance=None):
        chosen = mode(value if value is not None else default_mode(self.directory))
        if chosen == "off":
            return self.off()
        if not ready or not isinstance(scope, str) or not scope.strip() or len(scope) > 512:
            raise ValueError("activation requires --ready and a nonempty --scope (up to 512 characters)")
        if bool(contract) == bool(acceptance):
            raise ValueError("provide exactly one --contract or --acceptance")
        if contract:
            accepted = contract_file(self.root, contract)
        else:
            if not isinstance(acceptance, str) or not acceptance.strip() or len(acceptance.encode("utf-8")) > 4096:
                raise ValueError("inline acceptance must be nonempty and at most 4096 bytes")
            accepted = {"kind": "inline", "sha256": digest(acceptance.encode("utf-8")),
                        "acceptance": acceptance}
        write_json(self.path, {"version": 1, "root": str(self.root), "session_id": self.session_id,
                              "mode": chosen, "ready": True, "scope": scope, "contract": accepted})
        return self.status()

    def switch(self, value):
        chosen = mode(value)
        if chosen == "off":
            return self.off()
        if not self.status()["active"]:
            raise ValueError("accept or revalidate the implementation contract before switching modes")
        current = self.raw()
        current["mode"] = chosen
        write_json(self.path, current)
        return self.status()

    def off(self, reason="off"):
        current = self.raw()
        current.update(version=1, root=str(self.root), session_id=self.session_id,
                       mode="off", ready=False, invalidated=reason)
        write_json(self.path, current)
        return self.status()
