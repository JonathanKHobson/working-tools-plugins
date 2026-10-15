#!/usr/bin/env python3
"""Inspect or explicitly backfill skill assets for already-published plugins.

Normal plugin releases call the same synchronizer automatically. This command
is for the initial backfill/recovery, never a separate per-skill authoring step.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from release_manager.skill_downloads import current_plugins, synchronize

ROOT = Path(__file__).resolve().parents[1]
if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish',action='store_true',help='Generate and publish companion assets for verified current releases')
    args=parser.parse_args()
    history=json.loads((ROOT/'catalog/release-history.json').read_text())
    if args.publish:
        try:
            result=synchronize(ROOT,history)
        except subprocess.CalledProcessError as exc:
            if exc.stderr:
                print(exc.stderr.decode(errors="replace")[:2000],file=sys.stderr)
            raise
        print(json.dumps({'plugins':len(result['products']), 'skills':sum(len(p['skills']) for p in result['products'])}))
    else:
        print(json.dumps({'mode':'read-only','current_plugins':[{'id':i,'version':r['version']} for i,r,_ in current_plugins(history)]}))
