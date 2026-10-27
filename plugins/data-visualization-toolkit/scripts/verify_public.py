#!/usr/bin/env python3
"""Check the declared distributable inventory and preserved source methods.

Optional recipient-owned provider collections are outside this inventory.
Repository release validation separately rejects unexpected public files.
"""
from pathlib import Path
import hashlib,json,re,urllib.parse
ROOT=Path(__file__).resolve().parents[1]
def main():
    provenance=json.loads((ROOT/"PROVENANCE.json").read_text())
    version=provenance["version"]
    for rel in ["plugin.json",".codex-plugin/plugin.json",".claude-plugin/plugin.json"]:
        manifest=json.loads((ROOT/rel).read_text());assert manifest["name"]=="data-visualization-toolkit" and manifest["version"]==version,rel
    heads=list((ROOT/"skills").glob("*/SKILL.md"));assert len(heads)==14
    original=ROOT/"libraries/build-web-data-visualization"
    records=(ROOT/"docs/source-manifest.sha256").read_text().splitlines();assert len(records)==164
    for line in records:
        digest,path=line.split("  ",1);assert hashlib.sha256((original/path).read_bytes()).hexdigest()==digest,path
    paths=[]
    for item in provenance["files"]:
        p=ROOT/item["path"]
        assert p.resolve().is_relative_to(ROOT),item["path"]
        assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==item["output_sha256"],item["path"]
        paths.append(p)
    assert len(paths)==len(set(paths)),"duplicate inventory path"
    for p in paths:
        assert not p.is_symlink(),p
        if not p.is_file() or p.suffix!=".md":continue
        for target in re.findall(r"\]\(([^)]+)\)",p.read_text()):
            target=target.strip().strip("<>").split(' "')[0].split("#")[0]
            if not target or re.match(r"[a-z][a-z0-9+.-]*:",target):continue
            q=(p.parent/urllib.parse.unquote(target)).resolve();assert q.is_relative_to(ROOT) and q.exists(),(p,target)
    print(json.dumps({"version":version,"skills":14,"original_files":164,"distributable_files":len(paths)+1,"relative_references":"closed","symlinks":0,"status":"passed","scope":"declared distribution; optional private provider sources excluded"}))
if __name__=="__main__":main()
