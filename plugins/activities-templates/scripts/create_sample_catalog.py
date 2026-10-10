#!/usr/bin/env python3
"""Explicitly create an authored synthetic catalog outside the plugin."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
from fixtures import make_fixture

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output.is_relative_to(ROOT) or (output.exists() and any(output.iterdir())):
        parser.error("Use an empty directory outside the plugin")
    output.mkdir(parents=True, exist_ok=True)
    vault, database = make_fixture(output)
    binding = output / "atlas-library.json"
    binding.write_text(json.dumps({"interpreter": sys.executable, "database": str(database)}, indent=2) + "\n")
    print(json.dumps({"synthetic": True, "vault": str(vault), "database": str(database),
        "binding": str(binding), "next": "Set ACTIVITIES_ATLAS_CONFIG to the binding before enabling this plugin"}, indent=2))

if __name__ == "__main__":
    main()
