#!/usr/bin/env python3
"""Create an external, authored source-integrity example, not a Studio template."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime/design-library"))
from catalog import source_fingerprint

def create(output):
    output = Path(output).expanduser().resolve()
    if output.is_relative_to(ROOT) or (output.exists() and any(output.iterdir())):
        raise ValueError("Use an empty directory outside the plugin")
    package = output / "templates/artifact-template-studio-synthetic-example"
    source = package / "assets/source"
    source.mkdir(parents=True)
    (source / "index.html").write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Synthetic source</title><h1>Source-integrity example</h1><p>This authored fixture tests source verification. It is not a replacement for a Studio template.</p></html>\n')
    (package / "artifact-template.json").write_text('{"kind":"site","reference":"assets/source"}\n')
    (package / "DESIGN.md").write_text('# Synthetic fixture\n\nKeep the heading and clear limitation. This is runtime evidence, not an approved visual template.\n')
    (package / "WORKFLOW.md").write_text('# Fixture adaptation\n\nRead the verified source and guidance, then copy to a new directory before changing it. Preserve the explicit synthetic limitation.\n')
    item = {"id":"synthetic-example","name":"Synthetic source-integrity example","summary":"Authored verification fixture; no original private template is included.",
        "category":"Verification","tags":["synthetic"],"bestFor":["Testing source-integrity handoffs"],"avoidWhen":["Production design selection"],
        "interactions":["Read"],"limitations":["Not an equivalent Studio template"],"skillName":package.name,
        "sourceHash":source_fingerprint(source),"sourceKind":"site","desktopPreview":"assets/synthetic-example-desktop.png","mobilePreview":"assets/synthetic-example-mobile.png"}
    gallery = output / "gallery"
    (gallery / "assets").mkdir(parents=True)
    # A valid neutral one-pixel PNG is intentionally a fixture, not reference art.
    pixel = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aZy0AAAAASUVORK5CYII=')
    for size in ("desktop", "mobile"):
        (gallery / "assets" / f"synthetic-example-{size}.png").write_bytes(pixel)
    catalog = gallery / "catalog.json"
    catalog.write_text(json.dumps({"schemaVersion":1,"owner":"Design Templates","items":[item]},indent=2)+'\n')
    (output / "provenance").mkdir()
    files = [{"path":f"templates/{package.name}/{f.relative_to(package).as_posix()}","sha256":hashlib.sha256(f.read_bytes()).hexdigest()} for f in package.rglob('*') if f.is_file()]
    (output / "provenance/template-assets.json").write_text(json.dumps({"schemaVersion":1,"files":files},indent=2)+'\n')
    (output / "templates/catalog.json").write_text(json.dumps({"owner":"Design Templates","items":[{"id":item['id'],"name":item['name'],"kind":"site","package":f"templates/{package.name}"}]},indent=2)+'\n')
    (output / "templates/adaptation-recipes.json").write_text('{"recipes":[]}\n')
    return {"synthetic":True,"DESIGN_LIBRARY_CATALOG":str(catalog),"DESIGN_TEMPLATES_DATA_ROOT":str(output),"item":item}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(create(args.output),indent=2))

if __name__ == "__main__":
    main()
