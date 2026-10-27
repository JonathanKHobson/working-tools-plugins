#!/usr/bin/env python3
"""Launch the reviewed external REA runtime without installers or inherited secrets.

This is an integrity/environment boundary, not an OS sandbox or a target policy.
MCP call approval belongs to the client. The private binding is trusted host config.
"""
import hashlib
import json
import os
from pathlib import Path
import sys
import stat

VERSION = "6.5.0"
PROVIDER_ENV = {
    "GHIDRA_INSTALL_DIR", "JAVA_HOME", "GHIDRA_HEADLESS_MAXMEM",
    "DOTNET_ROOT", "DOTNET_ROOT_X64", "DOTNET_ROOT_ARM64",
    "REA_ANALYSIS_PROVIDER", "REA_GHIDRA_STARTUP_TIMEOUT_MS",
    "REA_ILSPY_CMD_PATH", "REA_JADX_MCP_JAR", "REA_JADX_HEAP_MIB",
    "REA_JADX_ACTIVE_PROCESSOR_COUNT", "REA_WABT_BIN_DIRECTORY",
    "REA_BROWSER_EXECUTABLE", "REA_OBJDUMP_COMMAND", "REA_RIZIN_COMMAND",
    "REA_TSHARK_COMMAND", "REA_SIGROK_COMMAND", "REA_BINWALK_COMMAND",
    "REA_UNBLOB_COMMAND", "REA_WAKARU_COMMAND", "REA_PWNTOOLS_PYTHON",
    "REA_MITMDUMP_COMMAND", "REA_ADB_PATH", "REA_APKTOOL_COMMAND",
    "REA_MCP_MAX_RESPONSE_BYTES", "REA_SWIFTC_COMPILE_TIMEOUT_MS",
}


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def verify(binding):
    if binding.get("version") != VERSION:
        raise ValueError("REA version differs from the reviewed integration")
    root = Path(binding["runtime_root"]).resolve(strict=True)
    node = Path(binding["node"]).resolve(strict=True)
    cli = root / "node_modules/rea-agents/scripts/rea.mjs"
    if Path(binding["cli"]).resolve(strict=True) != cli.resolve(strict=True):
        raise ValueError("CLI is not the reviewed package entrypoint")
    package = json.loads((cli.parent.parent / "package.json").read_text())
    if package.get("name") != "rea-agents" or package.get("version") != VERSION:
        raise ValueError("Installed REA identity differs from the review")
    if sha256(node) != binding["node_sha256"]:
        raise ValueError("Node changed; review the runtime binding before use")
    inventory = Path(binding["integrity_file"])
    if sha256(inventory) != binding["integrity_sha256"]:
        raise ValueError("Runtime integrity inventory changed")
    entries = json.loads(inventory.read_text())["files"]
    declared = set()
    for item in entries:
        rel = item["path"]
        path = root / rel
        if Path(rel).is_absolute() or ".." in Path(rel).parts:
            raise ValueError("Invalid integrity inventory path")
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError("Runtime entry escapes its installation")
        declared.add(rel)
        if item["kind"] == "symlink":
            if not path.is_symlink() or os.readlink(path) != item["value"]:
                raise ValueError("Runtime link changed: " + rel)
        elif item["kind"] != "file" or not stat.S_ISREG(path.lstat().st_mode):
            raise ValueError("Runtime entry is not a regular file: " + rel)
        elif sha256(path) != item["value"]:
            raise ValueError("Runtime file changed: " + rel)
    actual = {str(p.relative_to(root)) for p in (root / "node_modules").rglob("*")
              if not p.is_dir() or p.is_symlink()}
    actual.update({"package.json", "package-lock.json"})
    if actual != declared:
        raise ValueError("Runtime file inventory changed; review before use")
    return root, node, cli


def clean_environment(binding, root):
    # Deliberately exclude HOME overrides, NODE_OPTIONS, loader flags, proxy
    # variables, cloud tokens, browser profiles, and initial-target settings.
    env = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "en_US.UTF-8",
           "REA_LOG_LEVEL": "error", "TMPDIR": str(root / "tmp")}
    configured = binding.get("environment", {})
    if set(configured) - PROVIDER_ENV:
        raise ValueError("Unreviewed provider environment key")
    if any(not isinstance(v, str) or "\x00" in v for v in configured.values()):
        raise ValueError("Invalid provider environment value")
    env.update(configured)
    paths = binding.get("tool_path", [])
    if not isinstance(paths, list) or any(
        not isinstance(p, str) or os.pathsep in p or "\x00" in p or
        not Path(p).is_absolute() or not Path(p).is_dir() for p in paths
    ):
        raise ValueError("Invalid reviewed tool PATH directory")
    env["PATH"] = os.pathsep.join(paths + [env["PATH"]])
    return env


def prepare_tmp(root):
    tmp = root / "tmp"
    if tmp.is_symlink():
        raise ValueError("Runtime temporary directory must not be a symlink")
    tmp.mkdir(mode=0o700, exist_ok=True)
    if not tmp.is_dir() or tmp.resolve() != root / "tmp":
        raise ValueError("Runtime temporary directory escapes its installation")
    if tmp.stat().st_uid != os.getuid():
        raise ValueError("Runtime temporary directory must belong to the current user")
    if tmp.stat().st_mode & 0o077:
        raise ValueError("Runtime temporary directory must have private mode 0700")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    path = Path.home() / ".config/studio-tools/rea.json"
    binding = json.loads(path.read_text())
    root, node, cli = verify(binding)
    env = clean_environment(binding, root)
    if argv == ["status"]:
        print(json.dumps({"version": VERSION, "integrity": "verified",
                          "mode": "external CLI and full stdio MCP",
                          "os_sandbox": False,
                          "environment_keys": sorted(env)}))
        return 0
    if argv == ["--mcp"]:
        args = ["--mcp"]
    elif argv and argv[0] == "cli" and len(argv) > 1:
        # Administrative setup, registration and update commands are excluded.
        catalog_path = Path(__file__).resolve().parents[1] / "docs/rea-tool-catalog.json"
        if sha256(catalog_path) != binding["catalog_sha256"]:
            raise ValueError("Analysis command catalog changed; review before use")
        catalog = json.loads(catalog_path.read_text())
        commands = set(catalog["cli_commands"])
        if argv[1] not in commands | {"--help", "--version"}:
            raise ValueError("Use a reviewed analysis command; setup/update is separate")
        if any(arg.split("=", 1)[0] in {"--update", "--mcp"} for arg in argv[2:]):
            raise ValueError("Administrative flags are not allowed in analysis calls")
        args = argv[1:]
    else:
        raise ValueError("Usage: rea_runtime.py status | --mcp | cli ANALYSIS-COMMAND ...")
    prepare_tmp(root)
    os.chdir(root)
    os.execve(str(node), [str(node), str(cli), *args], env)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        # Do not print binding values, environment or target arguments.
        print("Development Studio REA launcher refused: " + str(exc), file=sys.stderr)
        sys.exit(1)
