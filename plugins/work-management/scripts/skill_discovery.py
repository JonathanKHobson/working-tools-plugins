#!/usr/bin/env python3
"""Read-only, on-demand skill lookup using native registration or explicit packages.

Native mode uses only initialize and skills/list. Portable mode reads bounded
package manifests and SKILL.md metadata from explicitly supplied roots. Neither
mode executes skills, calls a model/network, or changes host registration/policy.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import select
import shutil
import subprocess
import sys
import time


RPC_TIMEOUT = 20.0
MAX_RESPONSE_BYTES = 16 * 1024 * 1024
MAX_RESULTS = 10
MAX_METADATA_BYTES = 64 * 1024
MAX_FRONTMATTER_BYTES = 16 * 1024
MAX_PACKAGE_DEPTH = 5
MAX_PACKAGE_ENTRIES = 5000
STANDALONE = "standalone"
QUERY_STOPWORDS = frozenset({
    "a", "an", "and", "can", "could", "find", "for", "help", "how", "i", "in",
    "is", "it", "me", "my", "need", "of", "on", "or", "please", "should",
    "that", "the", "this", "to", "want", "what", "which", "with", "would",
})


class DiscoveryError(Exception):
    """A useful, expected lookup failure."""


def _send(process: subprocess.Popen, message: dict) -> None:
    assert process.stdin is not None
    process.stdin.write((json.dumps(message, ensure_ascii=False) + "\n").encode("utf-8"))
    process.stdin.flush()


def _rpc(process: subprocess.Popen, request_id: int, method: str, params: dict,
         pending: bytearray) -> dict:
    _send(process, {"id": request_id, "method": method, "params": params})
    deadline = time.monotonic() + RPC_TIMEOUT
    received_bytes = len(pending)
    assert process.stdout is not None
    while True:
        while b"\n" in pending:
            line, _, remainder = pending.partition(b"\n")
            pending[:] = remainder
            if not line.strip():
                continue
            try:
                message = json.loads(line)
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise DiscoveryError(f"Invalid app-server response to {method}: {exc}") from exc
            if not isinstance(message, dict) or message.get("id") != request_id:
                continue  # Server notifications are not lookup results.
            if "error" in message:
                raise DiscoveryError(f"Native {method} failed: {message['error']}")
            if not isinstance(message.get("result"), dict):
                raise DiscoveryError(f"Native {method} returned no result object")
            return message["result"]
        remaining = deadline - time.monotonic()
        if remaining <= 0 or not select.select([process.stdout], [], [], remaining)[0]:
            raise DiscoveryError(f"Native {method} timed out after {RPC_TIMEOUT:g}s")
        chunk = os.read(process.stdout.fileno(), 65536)
        if not chunk:
            raise DiscoveryError(f"Native app-server exited during {method}")
        received_bytes += len(chunk)
        if received_bytes > MAX_RESPONSE_BYTES:
            raise DiscoveryError("Native skill inventory exceeded the response limit")
        pending.extend(chunk)


def native_inventory(cwd: Path, codex: str) -> dict:
    """Make two read-only RPC requests, then reap the short-lived server."""
    executable = shutil.which(codex)
    if not executable:
        raise DiscoveryError(f"Codex binary not found: {codex}")
    if not cwd.is_dir():
        raise DiscoveryError(f"Working directory does not exist: {cwd}")
    try:
        process = subprocess.Popen(
            [executable, "app-server", "--stdio"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
    except OSError as exc:
        raise DiscoveryError(f"Could not start Codex app-server: {exc}") from exc
    try:
        pending = bytearray()
        _rpc(process, 1, "initialize", {
            "clientInfo": {"name": "work-management-skill-discovery", "version": "1"},
            "capabilities": {"experimentalApi": True},
        }, pending)
        _send(process, {"method": "initialized"})
        return _rpc(process, 2, "skills/list", {
            "cwds": [str(cwd)], "forceReload": True,
        }, pending)
    except (BrokenPipeError, OSError) as exc:
        raise DiscoveryError(f"Native skill lookup failed: {exc}") from exc
    finally:
        if process.poll() is None:
            try:
                process.terminate()
            except ProcessLookupError:
                pass
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            try:
                process.kill()
            except ProcessLookupError:
                pass
            process.wait(timeout=2)
        for stream in (process.stdin, process.stdout):
            if stream is not None:
                stream.close()


def load_inventory(path: Path) -> dict:
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DiscoveryError(f"Cannot read inventory snapshot {path}: {exc}") from exc
    if not isinstance(result, dict):
        raise DiscoveryError("Inventory snapshot must be a JSON object")
    return result



def _bounded_text(path: Path) -> str:
    try:
        if path.is_symlink():
            raise DiscoveryError(f"Symlink is not allowed inside a selected package: {path}")
        with path.open("rb") as stream:
            content = stream.read(MAX_METADATA_BYTES + 1)
        if len(content) > MAX_METADATA_BYTES:
            raise DiscoveryError(f"Metadata file exceeds {MAX_METADATA_BYTES} bytes: {path}")
        return content.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise DiscoveryError(f"Cannot read package metadata {path}: {exc}") from exc


def _json_metadata(path: Path) -> dict:
    try:
        value = json.loads(_bounded_text(path))
    except json.JSONDecodeError as exc:
        raise DiscoveryError(f"Invalid JSON metadata {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise DiscoveryError(f"Package metadata must be an object: {path}")
    return value


def _inside(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise DiscoveryError(f"Package path must be relative: {relative!r}")
    target = root / relative
    if ".." in Path(relative).parts or not target.resolve().is_relative_to(root):
        raise DiscoveryError(f"Package path escapes selected root: {relative!r}")
    current = root
    for part in Path(relative).parts:
        current /= part
        if current.is_symlink():
            raise DiscoveryError(f"Symlink is not allowed inside a selected package: {current}")
    return target


def _scalar(value: str, path: Path) -> str:
    value = value.strip()
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise DiscoveryError(f"Invalid quoted metadata in {path}: {exc}") from exc
        if not isinstance(parsed, str):
            raise DiscoveryError(f"Expected text metadata in {path}")
        return parsed
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise DiscoveryError(f"Unclosed quoted metadata in {path}")
        return value[1:-1].replace("''", "'")
    if not value or value.startswith(("[", "{", "&", "*", "!")) or value in ("null", "~", "true", "false"):
        raise DiscoveryError(f"Expected nonempty text metadata in {path}")
    return value.split(" #", 1)[0].rstrip()


def _skill_metadata(path: Path) -> dict:
    """Parse only the small YAML text/boolean fields used for discovery.

    No YAML objects, tags or body instructions are interpreted. Unsupported
    values in required fields fail explicitly instead of inventing a summary.
    """
    lines = _bounded_text(path).splitlines()
    if not lines or lines[0].strip() != "---":
        raise DiscoveryError(f"Missing SKILL.md frontmatter: {path}")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise DiscoveryError(f"Unclosed SKILL.md frontmatter: {path}") from exc
    if len("\n".join(lines[:end]).encode("utf-8")) > MAX_FRONTMATTER_BYTES:
        raise DiscoveryError(f"SKILL.md frontmatter exceeds limit: {path}")
    metadata = {}
    index = 1
    parent = ""
    while index < end:
        line = lines[index]
        index += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if not match:
            if not line[0].isspace():
                raise DiscoveryError(f"Malformed SKILL.md frontmatter: {path}")
            nested = re.match(r"^\s+(short-description|shortDescription):\s*(.*)$", line)
            if parent not in ("metadata", "interface") or not nested:
                continue  # Unselected nested metadata is not a discovery field.
            key, value = nested.groups()
        else:
            key, value = match.groups()
            parent = key
        if key not in ("name", "description", "short-description", "shortDescription", "enabled"):
            continue
        if key == "shortDescription":
            key = "short-description"
        if key in metadata:
            raise DiscoveryError(f"Duplicate {key} metadata: {path}")
        if key == "enabled":
            if value not in ("true", "false"):
                raise DiscoveryError(f"enabled must be true or false: {path}")
            metadata[key] = value == "true"
        elif value in (">", ">-", ">+", "|", "|-", "|+"):
            block = []
            while index < end and (not lines[index].strip() or lines[index][0].isspace()):
                block.append(lines[index].strip())
                index += 1
            metadata[key] = ("\n" if value.startswith("|") else " ").join(block).strip()
        else:
            metadata[key] = _scalar(value, path)
    for required in ("name", "description"):
        if not metadata.get(required) or not isinstance(metadata[required], str):
            raise DiscoveryError(f"Missing nonempty {required} metadata: {path}")
    return metadata


def portable_inventory(plugin_roots: list[Path], manifest_path: Path | None = None) -> tuple[list[dict], list[dict]]:
    """Read only explicitly selected package trees; never inspect a home registry."""
    selections = [{"root": str(path)} for path in plugin_roots]
    if manifest_path:
        manifest_path = manifest_path.expanduser().resolve()
        manifest = _json_metadata(manifest_path)
        if set(manifest) != {"plugins"} or not isinstance(manifest["plugins"], list):
            raise DiscoveryError("Portable manifest must contain only a plugins list")
        for entry in manifest["plugins"]:
            if not isinstance(entry, dict) or set(entry) - {"root", "enabled", "skills"}:
                raise DiscoveryError("Portable manifest entries accept root, enabled and skills only")
            if not isinstance(entry.get("root"), str) or not entry["root"]:
                raise DiscoveryError("Portable manifest entry needs a root")
            selected = dict(entry)
            root = Path(entry["root"]).expanduser()
            selected["root"] = str(root if root.is_absolute() else manifest_path.parent / root)
            selections.append(selected)
    # Explicit repeats are harmless, but conflicting policy must never re-enable.
    selected_roots = {}
    for selection in selections:
        root = Path(selection["root"]).expanduser().resolve()
        if not root.is_dir():
            raise DiscoveryError(f"Selected plugin root is not a directory: {root}")
        enabled = selection.get("enabled", True)
        overrides = selection.get("skills", {})
        if not isinstance(enabled, bool) or not isinstance(overrides, dict) or any(
                not isinstance(key, str) or not key or not isinstance(value, bool)
                for key, value in overrides.items()):
            raise DiscoveryError("Portable enabled state must be boolean; skills must map relative entrypoint paths to booleans")
        for relative in overrides:
            _inside(root, relative)
        if root in selected_roots:
            prior = selected_roots[root]
            prior["enabled"] = prior["enabled"] and enabled
            for key, value in overrides.items():
                prior["skills"][key] = prior["skills"].get(key, True) and value
        else:
            selected_roots[root] = {"enabled": enabled, "skills": dict(overrides)}
    skills, sources = [], []
    for root, policy in selected_roots.items():
        manifest_file = _inside(root, ".codex-plugin/plugin.json")
        if not manifest_file.is_file():
            manifest_file = _inside(root, "plugin.json")
        package = _json_metadata(manifest_file)
        owner = package.get("name")
        if not isinstance(owner, str) or not owner.strip() or "::" in owner:
            raise DiscoveryError(f"Package needs a nonempty name without '::': {manifest_file}")
        package_enabled = package.get("enabled", True)
        if not isinstance(package_enabled, bool):
            raise DiscoveryError(f"Package enabled state must be boolean: {manifest_file}")
        # Current Codex package schema declares one relative skills directory.
        declared = package.get("skills")
        skill_root = _inside(root, declared)
        if not skill_root.is_dir():
            raise DiscoveryError(f"Declared skills directory is missing: {skill_root}")
        source = {"root": str(root), "manifest": str(manifest_file), "owner": owner,
                  "kind": "explicit-package", "installationState": "unverified",
                  "activationState": "unverified"}
        sources.append(source)
        count, discovered = 0, set()
        def walk_error(exc: OSError) -> None:
            raise DiscoveryError(f"Cannot inspect selected skills directory: {exc}")

        for directory, directories, files in os.walk(skill_root, followlinks=False, onerror=walk_error):
            current = Path(directory)
            count += len(directories) + len(files)
            if count > MAX_PACKAGE_ENTRIES or len(current.relative_to(skill_root).parts) > MAX_PACKAGE_DEPTH:
                raise DiscoveryError(f"Selected skills tree exceeds traversal limits: {skill_root}")
            for name in directories + files:
                _inside(root, str((current / name).relative_to(root)))
            if "SKILL.md" not in files:
                continue
            path = current / "SKILL.md"
            metadata = _skill_metadata(path)
            relative = path.relative_to(root).as_posix()
            discovered.add(relative)
            enabled = policy["enabled"] and package_enabled and metadata.get("enabled", True) and policy["skills"].get(relative, True)
            skill_id = f"{owner}::{path}"
            skills.append({"id": skill_id, "name": metadata["name"],
                           "qualifiedName": f"{owner}::{metadata['name']}", "owner": owner,
                           "description": metadata["description"],
                           "shortDescription": metadata.get("short-description", metadata.get("shortDescription", "")),
                           "entrypoint": str(path), "entrypointExists": True, "enabled": enabled,
                           "source": "explicit-package", "installationState": "unverified",
                           "activationState": "unverified" if enabled else "disabled-by-explicit-metadata"})
        unknown = set(policy["skills"]) - discovered
        if unknown:
            raise DiscoveryError(f"Portable skill policy names undiscovered entrypoints: {', '.join(sorted(unknown))}")
    return sorted(skills, key=lambda s: (s["name"].casefold(), s["owner"], s["entrypoint"])), sources


def _owner(record: dict) -> str:
    value = record.get("pluginId")
    return value if isinstance(value, str) and value else STANDALONE


def skills_from_inventory(inventory: dict) -> list[dict]:
    data = inventory.get("data")
    if not isinstance(data, list):
        raise DiscoveryError("Native inventory is missing the data list")
    skills: dict[str, dict] = {}
    for group in data:
        if not isinstance(group, dict):
            raise DiscoveryError("Native inventory contains an invalid skill group")
        if group.get("errors"):
            detail = json.dumps(group["errors"], ensure_ascii=False, default=str)[:500]
            raise DiscoveryError(f"Native skill inventory errors for {group.get('cwd', 'unknown cwd')}: {detail}")
        if not isinstance(group.get("skills"), list):
            raise DiscoveryError("Native inventory contains an invalid skill group")
        for record in group["skills"]:
            if not isinstance(record, dict):
                continue
            name, path = record.get("name"), record.get("path")
            if not isinstance(name, str) or not name or not isinstance(path, str) or not Path(path).is_absolute():
                continue
            owner = _owner(record)
            skill_id = f"{owner}::{path}"
            interface = record.get("interface")
            short = interface.get("shortDescription", "") if isinstance(interface, dict) else ""
            if not short and isinstance(record.get("shortDescription"), str):
                short = record["shortDescription"]
            skills[skill_id] = {
                "id": skill_id, "name": name, "qualifiedName": f"{owner}::{name}",
                "owner": owner, "description": record.get("description", "") if isinstance(record.get("description"), str) else "",
                "shortDescription": short if isinstance(short, str) else "",
                "entrypoint": path, "entrypointExists": Path(path).is_file(),
                "enabled": record.get("enabled") is True,
            }
    return sorted(skills.values(), key=lambda s: (s["name"].casefold(), s["owner"], s["entrypoint"]))


def owners(skills: list[dict]) -> list[dict]:
    counts: dict[str, dict] = {}
    for skill in skills:
        entry = counts.setdefault(skill["owner"], {"owner": skill["owner"], "enabled": 0, "total": 0})
        entry["total"] += 1
        entry["enabled"] += bool(skill["enabled"])
    return sorted(counts.values(), key=lambda entry: (-entry["enabled"], entry["owner"]))


def _words(value: str) -> list[str]:
    return re.findall(r"\w+", value.casefold(), flags=re.UNICODE)


def _field_match(term: str, words: list[str]) -> bool:
    return term in words or (len(term) >= 4 and any(word.startswith(term) for word in words))


def _term_weight(term: str, fields: tuple[list[str], list[str], list[str]]) -> int:
    name, short, description = fields
    if term in name:
        return 70
    if _field_match(term, name):
        return 40
    if term in short:
        return 20
    if _field_match(term, short):
        return 15
    if _field_match(term, description):
        return 8
    return 0


def _score(fields: tuple[list[str], list[str], list[str]], terms: list[str],
           rarity: dict[str, float]) -> tuple[float, list[str]]:
    matched = [term for term in terms if _term_weight(term, fields)]
    # Long free-form requests need at least two shared concepts. A single
    # incidental word is too weak to recommend a skill from a large registry.
    if not matched or (len(terms) >= 5 and len(matched) < 2):
        return 0.0, []
    coverage = len(matched) / len(terms)
    score = sum(_term_weight(term, fields) * rarity[term] for term in matched) * coverage ** 2
    name, short, description = fields
    if name == terms:
        score += 1000
    elif " ".join(terms) in " ".join(name):
        score += 200
    if " ".join(terms) in " ".join(short):
        score += 80
    if " ".join(terms) in " ".join(description):
        score += 30
    return round(score, 2), matched


def search(skills: list[dict], query: str, owner: str | None, limit: int) -> list[dict]:
    terms = list(dict.fromkeys(word for word in _words(query) if word not in QUERY_STOPWORDS))
    if not terms:
        raise DiscoveryError("Search query must contain a searchable word")
    candidates = [skill for skill in skills if skill["enabled"] and
                  (not owner or owner in (skill["owner"], skill["owner"].split("@")[0]))]
    fields = [(skill, (_words(skill["name"]), _words(skill["shortDescription"]),
                       _words(skill["description"]))) for skill in candidates]
    rarity = {term: 1 + math.log((len(fields) + 1) /
                                 (1 + sum(bool(_term_weight(term, parts)) for _, parts in fields)))
              for term in terms}
    ranked = []
    for skill, parts in fields:
        score, matched = _score(parts, terms, rarity)
        if score:
            ranked.append((score, skill, matched))
    ranked.sort(key=lambda item: (-item[0], item[1]["name"].casefold(), item[1]["id"]))
    return [dict(skill, score=score, matchedTerms=matched,
                 partialMatch=len(matched) < len(terms))
            for score, skill, matched in ranked[:limit]]


def _lookup_aliases(skill: dict) -> set[str]:
    """Accept the plugin:skill spelling used by native catalogs and docs.

    A native name may already carry its owner while a portable frontmatter name
    is usually bare. Strip only a matching owner prefix, never an arbitrary one.
    Registry suffixes remain selectable; their short aliases may be ambiguous.
    """
    owner = skill["owner"]
    owners = {owner, owner.split("@", 1)[0]}
    name = skill["name"]
    for prefix in sorted(owners, key=len, reverse=True):
        for separator in ("::", ":"):
            if name.startswith(prefix + separator):
                name = name[len(prefix + separator):]
                return {f"{candidate}:{name}" for candidate in owners}
    return {f"{candidate}:{name}" for candidate in owners}


def show(skills: list[dict], identifier: str) -> dict:
    for skill in skills:
        if skill["id"] == identifier:
            return skill
    matches = [skill for skill in skills if skill["qualifiedName"] == identifier]
    if not matches:
        matches = [skill for skill in skills if skill["name"] == identifier or
                   identifier in _lookup_aliases(skill)]
    if len(matches) == 1:
        return matches[0]
    if matches:
        choices = ", ".join(skill["id"] for skill in matches[:MAX_RESULTS])
        raise DiscoveryError(f"Ambiguous skill ID {identifier!r}; use one of: {choices}")
    raise DiscoveryError(f"No registered skill matches {identifier!r}")


def _print_text(command: str, result: dict) -> None:
    label = {"snapshot": "Snapshot", "live": "Live native registry",
             "portable": "Explicit packages (installation/activation unverified)"}[result["mode"]]
    print(f"{label} | {result['cwd']}")
    if command == "owners":
        for entry in result["owners"]:
            if result["mode"] == "portable":
                print(f"{entry['owner']}: {entry['enabled']} enabled for lookup / {entry['total']} selected")
            else:
                print(f"{entry['owner']}: {entry['enabled']} enabled / {entry['total']} registered")
    elif command == "search":
        if not result["skills"]:
            print("No enabled skills matched.")
        for skill in result["skills"]:
            snippet = (skill["shortDescription"] or skill["description"]).replace("\n", " ")
            print(f"{skill['name']} [{skill['owner']}] | {snippet[:180]}")
            match_kind = "partial" if skill["partialMatch"] else "full"
            print(f"  match: {match_kind} ({', '.join(skill['matchedTerms'])})")
            print(f"  id: {skill['id']}")
    else:
        skill = result["skill"]
        state = "enabled" if skill["enabled"] else "DISABLED"
        if result["mode"] == "portable" and skill["enabled"]:
            state = "eligible for lookup; host activation unverified"
        print(f"{skill['name']} [{skill['owner']}] | {state}")
        print(f"id: {skill['id']}")
        print(f"entrypoint: {skill['entrypoint']} ({'exists' if skill['entrypointExists'] else 'missing'})")
        if skill["shortDescription"]:
            print(f"short description: {skill['shortDescription']}")
        print(f"description: {skill['description']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", type=Path, default=Path.cwd(), help="Directory for native skill registration")
    parser.add_argument("--codex", default="codex", help="Codex executable or command name")
    parser.add_argument("--inventory", type=Path, help="Offline JSON snapshot; skips native lookup")
    parser.add_argument("--portable", action="store_true", help="Read only explicit packages; no roots produces an empty result")
    parser.add_argument("--plugin-root", type=Path, action="append", default=[], help="Explicit package root (repeatable); selects portable mode")
    parser.add_argument("--manifest", type=Path, help="Explicit portable roots/state JSON; selects portable mode")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    commands = parser.add_subparsers(dest="command", required=True)
    owners_parser = commands.add_parser("owners", help="List registered owners and counts")
    search_parser = commands.add_parser("search", help="Rank enabled skills by registry metadata")
    search_parser.add_argument("query")
    search_parser.add_argument("--owner", help="Exact plugin ID or owner name")
    search_parser.add_argument("--limit", type=int, default=5, help="Results (1-10; default 5)")
    show_parser = commands.add_parser("show", help="Show a registered skill by exact ID or unique name")
    show_parser.add_argument("skill_id")
    # Common options are accepted on either side of the subcommand.
    for subparser in (owners_parser, search_parser, show_parser):
        subparser.add_argument("--cwd", type=Path, default=argparse.SUPPRESS)
        subparser.add_argument("--codex", default=argparse.SUPPRESS)
        subparser.add_argument("--inventory", type=Path, default=argparse.SUPPRESS)
        subparser.add_argument("--portable", action="store_true", default=argparse.SUPPRESS)
        subparser.add_argument("--plugin-root", type=Path, action="append", dest="plugin_root_after", default=[])
        subparser.add_argument("--manifest", type=Path, default=argparse.SUPPRESS)
        subparser.add_argument("--json", action="store_true", default=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        cwd = args.cwd.expanduser().resolve()
        if args.command == "search" and not 1 <= args.limit <= MAX_RESULTS:
            raise DiscoveryError(f"--limit must be between 1 and {MAX_RESULTS}")
        plugin_roots = args.plugin_root + args.plugin_root_after
        portable = args.portable or bool(plugin_roots) or args.manifest is not None
        if portable and args.inventory:
            raise DiscoveryError("Portable package inputs cannot be combined with --inventory")
        if portable:
            skills, sources = portable_inventory(plugin_roots, args.manifest)
            result = {"mode": "portable", "cwd": str(cwd), "sources": sources,
                      "capabilities": {"metadataLookup": True, "nativeRegistrationVerified": False,
                                       "toolAccessVerified": False}}
        else:
            inventory = load_inventory(args.inventory) if args.inventory else native_inventory(cwd, args.codex)
            skills = skills_from_inventory(inventory)
            result = {"mode": "snapshot" if args.inventory else "live", "cwd": str(cwd)}
        if args.inventory:
            result["inventory"] = str(args.inventory.resolve())
        if args.command == "owners":
            result["owners"] = owners(skills)
        elif args.command == "search":
            result["query"] = args.query
            result["skills"] = search(skills, args.query, args.owner, args.limit)
        else:
            result["skill"] = show(skills, args.skill_id)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            _print_text(args.command, result)
        return 0
    except DiscoveryError as exc:
        print(f"skill discovery: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
