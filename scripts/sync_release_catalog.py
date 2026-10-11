#!/usr/bin/env python3
"""Generate the release catalog only after complete verified history import."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.release_manager.catalog import validate_catalog,select_current,SemVer
from scripts.release_manager.history import import_history

ROOT=Path(__file__).resolve().parents[1]

def generate(history, registry, previous=None):
    if not history:raise ValueError('Refusing empty release history')
    products=[]
    for r in registry:
        releases=[row for row in history if row['product_id']==r['id']]
        if not releases:raise ValueError('No verified history returned for '+r['id'])
        # Preserve a withdrawn/deleted record, not a now-missing current download.
        old=next((p for p in (previous or {}).get('products',[]) if p['id']==r['id']),{})
        keys={x['release_key'] for x in releases}
        for row in old.get('releases',[]):
            if row['release_key'] not in keys:
                releases.append({**row,'distribution_status':'withdrawn','summary':'Withdrawn: '+row['summary']})
        for release in releases:
            entry=ROOT/'catalog/releases'/r['id']/(release['version']+'.json')
            if entry.is_file():
                authored=json.loads(entry.read_text())
                for field in ('summary','compatibility','upgrade_guidance'):
                    release[field]=authored[field]
            elif release.get('notes'):
                lines=[line.strip().lstrip('#').strip() for line in release['notes'].splitlines() if line.strip()]
                if lines:release['summary']=lines[0]
        releases.sort(key=lambda x:(SemVer(x['version']),x['published_at']),reverse=True)
        p={'id':r['id'],'name':r['name'],'kind':'plugin',
           'repository':'https://github.com/JonathanKHobson/working-tools-plugins',
           'compatibility':'; '.join(r['requirements']),
           'upgrade_guidance':'Choose this exact version from the marketplace or replace the prior plugin directory with its ZIP. Review the release notes and package README.',
           'releases':releases}
        current=select_current(p);p['current_release_key']=current['release_key'] if current else None
        products.append(p)
    return {'schema_version':'working-tools.releases.v1','products':products}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--from-history',type=Path);p.add_argument('--output',type=Path,default=ROOT/'catalog/release-history.json');a=p.parse_args()
    registry=json.loads((ROOT/'catalog/packages.json').read_text())['packages']
    old=json.loads(a.output.read_text()) if a.output.exists() else None
    prior=[r for p in (old or {}).get('products',[]) if p.get('kind')=='plugin' for r in p['releases']]
    history=json.loads(a.from_history.read_text()) if a.from_history else import_history('JonathanKHobson','working-tools-plugins',repo_path=ROOT,package_ids={r['id'] for r in registry},cache_dir=ROOT/'dist/release-manager-cache',previous_releases=prior)
    catalog=generate(history,registry,old)
    from scripts.release_manager.legacy import load_external_products,external_release_records
    external=ROOT/'catalog/external-products.json'
    if external.exists():catalog['products'].extend(external_release_records(load_external_products(external)))
    from scripts.release_manager.packs import history_products
    catalog['products'].extend(history_products(ROOT))
    from jsonschema import Draft202012Validator
    schema=json.loads((ROOT/'schemas/release-catalog.schema.json').read_text())
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(catalog)
    errors=validate_catalog(catalog)
    if errors:raise ValueError('\n'.join(errors))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile('w',dir=a.output.parent,delete=False) as out:
        json.dump(catalog,out,indent=2,ensure_ascii=False);out.write('\n');name=out.name
    Path(name).replace(a.output)
    print(json.dumps({'products':len(catalog['products']),'releases':len(history),'recommended':sum(bool(p['current_release_key']) for p in catalog['products'])}))
if __name__=='__main__':main()
