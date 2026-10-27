#!/usr/bin/env python3
"""Read-only package integrity checks. Does not import or execute candidate code."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(root):
    root = Path(root).resolve()
    errors = []
    checked = {"skills": 0, "import_hashes": 0, "links": 0, "provider_methods": 0}

    def inside(relative):
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            raise ValueError("path escapes package: " + relative)
        return path

    def read_json(relative):
        try:
            return json.loads(inside(relative).read_text())
        except (OSError, ValueError) as exc:
            errors.append(f"{relative}: {exc}")
            return {}

    manifest = read_json(".codex-plugin/plugin.json")
    if manifest.get("name") != "development-studio" or manifest.get("skills") != "./skills/":
        errors.append("package identity or discovery root differs from contract")
    if (manifest.get("apps") or manifest.get("hooks") != "./hooks/hooks.json"
            or manifest.get("mcpServers") != "./.mcp.json"):
        errors.append("unexpected runtime/provider declaration outside the REA contract")
    expected_hooks = {"hooks": {
        event: [{"hooks": [{
            "type": "command",
            "command": (f'python3 -B "${{PLUGIN_ROOT}}/runtime/efficient-implementation/cli.py" hook {event}'
                        + (" --host codex" if event == "SubagentStart" else "")),
            "timeout": 2,
            "statusMessage": "Read scoped implementation preference",
        }]}] for event in ("SessionStart", "UserPromptSubmit", "SubagentStart")
    }}
    if read_json("hooks/hooks.json") != expected_hooks:
        errors.append("implementation lifecycle hooks differ from reviewed commands")
    expected_mcp = {"mcpServers": {"rea": {"command": "python3",
        "args": ["scripts/rea_runtime.py", "--mcp"], "cwd": ".",
        "env": {"PYTHONDONTWRITEBYTECODE": "1"}}}}
    if read_json(".mcp.json") != expected_mcp:
        errors.append("MCP launch differs from the reviewed REA contract")
    portable_mcp = {"$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
        "mcpServers": {"rea": {"type": "stdio", "command": "python3",
        "args": ["${PLUGIN_ROOT}/scripts/rea_runtime.py", "--mcp"],
        "cwd": "${PLUGIN_ROOT}", "env": {"PYTHONDONTWRITEBYTECODE": "1"}}}}
    if read_json("mcp.json") != portable_mcp:
        errors.append("portable MCP launch differs from the reviewed REA contract")
    # Current native AgentPlugin loading silently skips hooks. Keep the complete
    # portable metadata as a restoration template; the compatibility loader is
    # the verified executable layout until native hook readback supports both.
    if (root / "plugin.json").exists():
        errors.append("root portable manifest requires renewed native hook verification")
    portable_manifest = read_json("docs/portable-plugin-manifest.json")
    if (portable_manifest.get("description") != manifest.get("description") or
        portable_manifest.get("extensions", {}).get("com.openai", {}).get("interface") != manifest.get("interface") or
        portable_manifest.get("extensions", {}).get("com.openai", {}).get("hooks") != manifest.get("hooks")):
        errors.append("portable and compatibility plugin metadata differ")
    catalog = read_json("docs/rea-tool-catalog.json")
    names = catalog.get("tools", [])
    if (catalog.get("version") != "6.5.0" or len(names) != 207 or
        len(set(names)) != 207 or catalog.get("default_approval_mode") != "writes" or
        len(set(catalog.get("explicit_prompt_tools", []))) != 34 or
        not set(catalog.get("explicit_prompt_tools", [])).issubset(names)):
        errors.append("REA tool inventory or approval contract changed")
    if len(catalog.get("cli_commands", [])) != 149 or set(catalog.get("cli_commands", [])) & {"setup", "update", "uninstall", "mcp", "doctor", "completions"}:
        errors.append("REA analysis CLI contract changed")
    if not inside("scripts/rea_runtime.py").is_file():
        errors.append("missing REA runtime launcher")
    routes = read_json("docs/routes.json")
    entries = routes.get("skills", [])
    actual = {x.parent.name for x in (root / "skills").glob("*/SKILL.md")}
    if actual != {x["skill"] for x in entries}:
        errors.append("skill routes do not match discovery surface")
    methods = set()
    for entry in entries:
        path = inside("skills/" + entry["skill"] + "/SKILL.md")
        if not path.is_file():
            errors.append("missing skill: " + entry["skill"])
            continue
        text = path.read_text()
        if not text.startswith("---\n") or not re.search(r"(?m)^description: .+", text):
            errors.append("missing skill frontmatter: " + entry["skill"])
        if not re.search(r"(?m)^name: [\"\']?" + re.escape(entry["skill"]) + r"[\"\']?$", text):
            errors.append("skill name differs from directory: " + entry["skill"])
        checked["skills"] += 1
        for method in entry["full_methods"]:
            methods.add(method)
            if not inside(method).is_file() or method not in text:
                errors.append("full method not reachable from route: " + method)
        for method in entry.get("conditional_methods", []):
            if not inside(method).is_file() or method not in text:
                errors.append("conditional method not reachable from route: " + method)
    originals = {str(x.relative_to(root)) for x in
                 (root / "libraries/superpowers-6.4.2/skills").glob("*/SKILL.md")}
    if methods != originals:
        errors.append("Superpowers full method coverage differs from snapshot")

    inventory = read_json("docs/imports.json")
    local_mcp = read_json("docs/local-mcp-provenance.json")
    standalone = read_json("docs/standalone-imports.json")
    standalone_files = [{"target": row["path"], "target_sha256": row["output_sha256"], "source_sha256": row["source_sha256"], "disposition": "byte-identical" if row["source_sha256"] == row["output_sha256"] else "transformed"} for row in standalone.get("files", [])]
    imported_files = inventory.get("files", []) + local_mcp.get("files", []) + standalone_files + read_json("docs/rea-imports.json").get("files", [])
    for item in imported_files:
        if "target" not in item:
            if not item.get("reason"):
                errors.append("undocumented source omission: " + item.get("path", "?"))
            continue
        path = inside(item["target"])
        if not path.is_file() or digest(path) != item["target_sha256"]:
            errors.append("import hash mismatch: " + item["target"])
        elif item["disposition"] == "byte-identical" and item["source_sha256"] != item["target_sha256"]:
            errors.append("false byte-identity claim: " + item["target"])
        checked["import_hashes"] += 1
    for prefix in ("libraries/superpowers-6.4.2/", "libraries/alpic-1.0.1/",
                   "libraries/local-mcp-methods/", "libraries/code-intelligence-ebb3257/", "libraries/local-app-pipeline/", "libraries/rea-6.5.0/"):
        declared = {x["target"] for x in imported_files if x.get("target", "").startswith(prefix)}
        present = {str(x.relative_to(root)) for x in inside(prefix).rglob("*") if x.is_file()}
        if declared != present:
            errors.append("imported support closure differs from inventory: " + prefix)

    efficiency = read_json("docs/efficient-source-inventory.json")
    if efficiency.get("commit") != "b088b2df6e08d4306c6a3c3d575fe38c2d2d2989":
        errors.append("implementation source pin differs from reviewed v5")
    source_paths = [row.get("source") for row in efficiency.get("files", [])]
    if len(source_paths) != 199 or len(set(source_paths)) != 199:
        errors.append("implementation source inventory differs from reviewed full tree")
    for row in efficiency.get("files", []):
        if not row.get("disposition") or not row.get("sha256"):
            errors.append("incomplete implementation source disposition")
        if row.get("target"):
            target = inside(row["target"])
            if not target.is_file() or digest(target) != row.get("target_sha256"):
                errors.append("implementation source support hash mismatch: " + row["target"])
        for target in row.get("targets", []):
            if not inside(target).exists():
                errors.append("missing implementation capability destination: " + target)

    providers = read_json("docs/provider-inventory.json").get("providers", [])
    provider_ids = {x["id"] for x in providers}
    for values in routes.get("provider_routes", {}).values():
        if not set(values).issubset(provider_ids):
            errors.append("route names an uninventoried provider")
    provider_text = (root / "references/platform-providers.md").read_text()
    for provider in providers:
        for method in provider["skills"]:
            if "`" + method["directory"] + "`" not in provider_text:
                errors.append("missing documented provider method: " + method["path"])
            checked["provider_methods"] += 1

    # Immutable upstream snapshots retain historical external links; only maintained
    # operative content is held to local relative-link closure here.
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append("symlink in distribution: " + str(path.relative_to(root)))
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if path.name in {".DS_Store"} or path.suffix == ".pyc" or "__pycache__" in rel.parts:
            errors.append("generated host file in distribution: " + str(rel))
        if path.suffix not in {".md", ".json", ".toml", ".yaml", ".py", ".sh", ".txt"}:
            continue
        text = path.read_text(errors="replace")
        # Detect concrete home/volume paths; templated examples are allowed.
        if re.search(r"/(?:Users|home)/[A-Za-z][A-Za-z0-9_.-]*/|/" + r"Volumes/[A-Za-z][^\n`\"']+", text):
            if str(rel) != "scripts/validate_package.py":
                errors.append("concrete host path needs portability review: " + str(rel))
        if path.suffix != ".md" or (rel.parts[0] == "libraries" and rel.parts[1] in {"superpowers-6.4.2", "alpic-1.0.1"}):
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = target.split("#", 1)[0].strip("<>")
            if not target or re.match(r"[a-z][a-z0-9+.-]*:", target):
                continue
            dest = (path.parent / unquote(target)).resolve()
            if not dest.is_relative_to(root) or not dest.exists():
                errors.append(f"broken or escaping link: {rel}: {target}")
            checked["links"] += 1
    for required in ("LICENSE.md", "libraries/superpowers-6.4.2/LICENSE",
                     "libraries/alpic-1.0.1/LICENSE", "docs/local-mcp-provenance.json",
                     "docs/install-handoff.md", "docs/admission.md"):
        if not inside(required).is_file():
            errors.append("missing release requirement: " + required)
    return {"ok": not errors, "checks": checked, "errors": errors,
            "boundary": "Static integrity and declared route checks only; no model, provider, installation or live-host execution proof."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    result = check(args.root)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["ok"] else 1)
