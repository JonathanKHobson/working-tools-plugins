#!/usr/bin/env python3
"""Search the full local template inventory or verify retained asset hashes."""
import argparse
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(os.environ.get("DESIGN_TEMPLATES_DATA_ROOT", Path(__file__).resolve().parents[1]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--query', default='')
    parser.add_argument('--kind', choices=['all','site','document','presentation','spreadsheet'], default='all')
    parser.add_argument('--verify', action='store_true')
    recipes = parser.add_mutually_exclusive_group()
    recipes.add_argument('--recipes', action='store_true', help='List small adaptations of existing templates')
    recipes.add_argument('--recipe', help='Return one adaptation recipe and its authoritative template paths')
    args = parser.parse_args()
    if (args.recipes or args.recipe) and (args.verify or args.query or args.kind != 'all'):
        parser.error('Use recipe lookup separately from inventory filtering or verification')
    if args.verify:
        manifest = json.loads((ROOT/'provenance/template-assets.json').read_text())
        invalid = []
        for item in manifest['files']:
            rel = Path(item['path'])
            if rel.is_absolute() or '..' in rel.parts:
                invalid.append(item['path']); continue
            file = ROOT / rel
            if file.is_symlink() or not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != item['sha256']:
                invalid.append(item['path'])
        print(json.dumps({'files':len(manifest['files']),'invalid':invalid}))
        return int(bool(invalid))
    data = json.loads((ROOT/'templates/catalog.json').read_text())
    if args.recipes or args.recipe:
        patterns = json.loads((ROOT/'templates/adaptation-recipes.json').read_text())['recipes']
        if args.recipes:
            print(json.dumps({'owner':'Design Templates','recipes':[{k:p[k] for k in ('id','name','templateId','purpose')} for p in patterns]},indent=2))
            return 0
        pattern = next((p for p in patterns if p['id'] == args.recipe), None)
        if pattern is None:
            parser.error('Unknown recipe; use --recipes to see available IDs')
        item = next((i for i in data['items'] if i['id'] == pattern['templateId']), None)
        if item is None:
            parser.error('Recipe template is not in the current catalog')
        package = ROOT/item['package']
        for mapping in pattern['sourceMap']:
            rel = Path(mapping['path'])
            target = package/rel
            if rel.is_absolute() or '..' in rel.parts or not target.is_file() or target.is_symlink():
                parser.error('Recipe source mapping is missing or unsafe')
        print(json.dumps({'owner':'Design Templates','recipe':pattern,'template':item,'status':'Adaptation instructions; not a created or tested variant'},indent=2))
        return 0
    items = [i for i in data['items'] if (args.kind=='all' or i['kind']==args.kind) and args.query.casefold() in (i['name']+' '+i['id']).casefold()]
    print(json.dumps({'owner':'Design Templates','items':items},indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
