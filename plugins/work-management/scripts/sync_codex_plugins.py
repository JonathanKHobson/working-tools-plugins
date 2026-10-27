#!/usr/bin/env python3
"""Refresh already-installed local Codex packages, with delta rollback."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid

spec = importlib.util.spec_from_file_location(
    "source_recorder", Path(__file__).with_name("plugin_change_record.py"))
recorder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recorder)


def hashes(tree):
    return {p: v["sha256"] for p, v in tree["files"].items()}


def native(cli, arguments):
    result = subprocess.run([cli, "plugin", *arguments], capture_output=True,
                            text=True, timeout=90)
    if result.returncode:
        raise RuntimeError("Native Codex plugin operation failed: " + result.stderr[-1000:])
    return json.loads(result.stdout)


def snapshot_delta(cache, changed, backup):
    saved = {}
    for relative in changed:
        source = cache / relative
        destination = backup / relative
        if source.is_symlink():
            saved[relative] = {"kind": "link", "target": os.readlink(source)}
        elif source.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            saved[relative] = {"kind": "file"}
        elif source.exists():
            raise ValueError("Refusing to replace a non-file cache entry.")
        else:
            saved[relative] = {"kind": "absent"}
    (backup / "restore.json").write_text(json.dumps(saved, indent=2) + "\n")
    return saved


def restore_delta(cache, backup, saved, before=None, source=None):
    # Native installation can create more than the predicted delta. Remove only
    # entries absent from the captured pre-install tree, never arbitrary paths.
    if before is not None:
        current = recorder._scan_product(cache, {})
        for relative in set(current["files"]) - set(before["files"]):
            target = cache / relative
            if target.is_file() or target.is_symlink():
                target.unlink()
    for relative, entry in saved.items():
        target = cache / relative
        if target.is_symlink() or target.is_file():
            target.unlink()
        elif target.exists():
            raise RuntimeError("Rollback requires review of non-file entry: " + str(target))
        if entry["kind"] == "file":
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup / relative, target)
        elif entry["kind"] == "link":
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(entry["target"])
    if before is not None:
        current = recorder._scan_product(cache, {})
        for relative, entry in before["files"].items():
            if current["files"].get(relative, {}).get("sha256") == entry["sha256"]:
                continue
            # An unexpectedly changed formerly identical file can be recovered
            # from canonical bytes only if they still match the old cache hash.
            original = source / relative
            available = recorder._file_entry(original, None) if original.exists() or original.is_symlink() else None
            if not available or available["sha256"] != entry["sha256"]:
                raise RuntimeError("Rollback cannot verify original bytes: " + relative)
            destination = cache / relative
            if destination.is_file() or destination.is_symlink():
                destination.unlink()
            destination.parent.mkdir(parents=True, exist_ok=True)
            if available.get("kind") == "symlink":
                destination.symlink_to(available["target"])
            else:
                shutil.copy2(original, destination)


def synchronize(config, mode, invoke=native):
    for mount in config.get("required_mounts", []):
        if not Path(mount).is_mount():
            raise ValueError("Required volume is unavailable: " + mount)
    state_root = Path(config["state_dir"])
    storage = Path(config["storage_root"]).resolve()
    if not state_root.resolve().is_relative_to(storage):
        raise ValueError("Codex state must remain in its selected storage root.")
    state_path = state_root / "state.json"
    previous = json.loads(state_path.read_text()) if state_path.exists() else {}
    if mode == "apply" and not state_path.exists():
        raise ValueError("Review native inventory and establish a baseline before automatic updates.")
    installed = {p["pluginId"]: p for p in invoke(config["cli"], ["list", "--json"])["installed"]}
    plans = {}
    conflicts = []
    for ident, target in config["packages"].items():
        entry = installed.get(ident)
        if not entry or not entry.get("enabled"):
            conflicts.append(ident + ": absent or disabled; preserve native user choice")
            continue
        source = Path(target["source"])
        cache = Path(target["cache"])
        if not source.is_dir() or not cache.is_dir():
            conflicts.append(ident + ": source or native cache unavailable")
            continue
        if entry.get("version") != target["version"]:
            conflicts.append(ident + ": native version changed; review the new installation")
            continue
        source_manifest = json.loads((source / ".codex-plugin/plugin.json").read_text())
        if source_manifest["version"] != target["version"]:
            conflicts.append(ident + ": new source version requires reviewed registration")
            continue
        old = previous.get(ident, {})
        if mode == "apply" and not old:
            conflicts.append(ident + ": native cache has no reviewed per-package baseline")
            continue
        expected = recorder._scan_product(source, old.get("source", {}))
        for relative in target.get("native_omissions", []):
            expected["files"].pop(relative, None)
        current = recorder._scan_product(cache, old.get("cache", {}))
        a, b = hashes(expected), hashes(current)
        baseline = hashes(old.get("cache", {"files": {}}))
        if old:
            for relative in b.keys() | baseline.keys():
                if b.get(relative) != baseline.get(relative) and b.get(relative) != a.get(relative):
                    conflicts.append(ident + ": edited native file " + relative)
        changed = sorted(p for p in a.keys() | b.keys() if a.get(p) != b.get(p))
        plans[ident] = {"source": expected, "cache": current, "changed": changed}
    result = {"mode": mode, "changed": {k: v["changed"] for k, v in plans.items() if v["changed"]},
              "conflicts": conflicts, "updated": [], "model_invocations": 0}
    if mode == "check" or conflicts:
        return result
    state_root.mkdir(parents=True, exist_ok=True, mode=0o700)
    if mode == "baseline":
        recorder._atomic_json(state_path, {k: {"source": v["source"], "cache": v["cache"]}
                                           for k, v in plans.items()})
        return result
    for ident, plan in plans.items():
        if not plan["changed"]:
            continue
        target = config["packages"][ident]
        source, cache = Path(target["source"]), Path(target["cache"])
        backup = state_root / "backups" / (ident.split("@")[0] + "-" + uuid.uuid4().hex[:12])
        backup.mkdir(parents=True, mode=0o700)
        saved = snapshot_delta(cache, plan["changed"], backup)
        try:
            receipt = invoke(config["cli"], ["add", ident, "--json"])
            if Path(receipt["installedPath"]).resolve() != cache.resolve():
                raise RuntimeError("Native installer selected an unexpected cache destination.")
            actual = recorder._scan_product(cache, {})
            if hashes(actual) != hashes(plan["source"]):
                raise RuntimeError("Native cache did not match the reviewed source snapshot.")
            # Also catch a source edit made while the native installer copied.
            fresh = recorder._scan_product(source, {})
            for relative in target.get("native_omissions", []):
                fresh["files"].pop(relative, None)
            if hashes(fresh) != hashes(plan["source"]):
                raise RuntimeError("Source changed during installation.")
            native_after = {p["pluginId"]: p for p in invoke(
                config["cli"], ["list", "--json"])["installed"]}.get(ident)
            if (not native_after or not native_after.get("enabled")
                    or native_after.get("version") != target["version"]):
                raise RuntimeError("Native version/enabled state did not read back.")
        except Exception as error:
            restore_delta(cache, backup, saved, plan["cache"], source)
            restored = recorder._scan_product(cache, {})
            rollback_ok = hashes(restored) == hashes(plan["cache"])
            result.update(error=str(error), rollback_verified=rollback_ok, backup=str(backup))
            recorder._atomic_json(state_root / "last-result.json", result)
            if not rollback_ok:
                raise RuntimeError("Codex delta rollback needs manual review.") from error
            return result
        previous[ident] = {"source": plan["source"], "cache": actual}
        recorder._atomic_json(state_path, previous)
        result["updated"].append({"id": ident, "backup": str(backup)})
    if result["updated"]:
        recorder._atomic_json(state_root / "last-result.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--baseline", action="store_true")
    args = parser.parse_args()
    result = synchronize(json.loads(args.config.read_text()),
                         "check" if args.check else "apply" if args.apply else "baseline")
    print(json.dumps(result, indent=2))
    return 2 if result.get("conflicts") or result.get("error") else 0


if __name__ == "__main__":
    sys.exit(main())
