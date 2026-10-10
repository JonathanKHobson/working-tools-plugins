#!/usr/bin/env python3
"""Locate an explicitly configured, recipient-owned method without running it."""
import argparse
import json
from pathlib import Path
import sys

ENTRIES = {
    "visualize": "skills/visualize/SKILL.md",
    "scientific": "skills/scientific-visual-table-style/SKILL.md",
}


def resolve_source(provider, binding):
    if provider not in ENTRIES:
        raise ValueError("Unknown provider")
    binding = Path(binding).expanduser()
    if not binding.is_file():
        return {"available": False, "provider": provider, "reason": "binding_missing"}
    config = json.loads(binding.read_text())
    if not isinstance(config, dict):
        raise ValueError("Provider binding must be a JSON object")
    root_value = config.get(provider)
    if root_value is None:
        return {"available": False, "provider": provider, "reason": "provider_not_configured"}
    if not isinstance(root_value, str) or not root_value.strip():
        raise ValueError("Provider source must be an absolute directory path")
    root = Path(root_value).expanduser()
    if not root.is_absolute():
        raise ValueError("Provider source must be an absolute directory path")
    root = root.resolve()
    entry = (root / ENTRIES[provider]).resolve()
    if not entry.is_relative_to(root):
        raise ValueError("Provider entry cannot escape its configured source root")
    if not entry.is_file():
        return {"available": False, "provider": provider, "reason": "procedure_missing"}
    return {
        "available": True,
        "provider": provider,
        "source_root": str(root),
        "procedure": str(entry),
        "supporting_sources_verified": False,
        "runtime_verified": False,
        "redistribution_permission_verified": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("provider", choices=ENTRIES)
    parser.add_argument("--binding", type=Path,
                        default=Path.home() / ".config/studio-tools/data-visualization-providers.json")
    args = parser.parse_args()
    print(json.dumps(resolve_source(args.provider, args.binding), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print(f"Provider source unavailable: {exc}", file=sys.stderr)
        raise SystemExit(1)
