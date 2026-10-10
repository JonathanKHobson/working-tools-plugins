#!/usr/bin/env python3
"""Check package identity, complete source parity and local Markdown closure."""
from pathlib import Path
import hashlib,json,re,urllib.parse
ROOT=Path(__file__).resolve().parents[1]
def main():
    for rel in ["plugin.json",".codex-plugin/plugin.json",".claude-plugin/plugin.json"]:
        manifest=json.loads((ROOT/rel).read_text());assert manifest["name"]=="data-visualization-toolkit" and manifest["version"]=="0.2.0"
    heads=list((ROOT/"skills").glob("*/SKILL.md"));assert len(heads)==13
    original=ROOT/"libraries/build-web-data-visualization"
    records=(ROOT/"docs/source-manifest.sha256").read_text().splitlines();assert len(records)==164
    for line in records:
        digest,path=line.split("  ",1);assert hashlib.sha256((original/path).read_bytes()).hexdigest()==digest,path
    for p in ROOT.rglob("*"):
        assert not p.is_symlink(),p
        if not p.is_file() or p.suffix!=".md":continue
        for target in re.findall(r"\]\(([^)]+)\)",p.read_text()):
            target=target.strip().strip("<>").split(' "')[0].split("#")[0]
            if not target or re.match(r"[a-z][a-z0-9+.-]*:",target):continue
            q=(p.parent/urllib.parse.unquote(target)).resolve();assert q.is_relative_to(ROOT) and q.exists(),(p,target)
    print(json.dumps({"skills":13,"original_files":164,"relative_references":"closed","symlinks":0,"status":"passed"}))
if __name__=="__main__":main()
