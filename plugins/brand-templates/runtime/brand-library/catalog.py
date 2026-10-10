"""Read-only selection and complete source closure checks for Brand Templates."""
from pathlib import Path
import hashlib
import json
import re
import os

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get('BRAND_TEMPLATES_DATA_ROOT') or PACKAGE_ROOT).expanduser().absolute()
if os.environ.get('BRAND_TEMPLATES_DATA_ROOT') and ROOT.resolve().is_relative_to(PACKAGE_ROOT):
    raise ValueError('Explicit brand collection must stay outside the installed package')
ID = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')


def catalog_path(root=ROOT):
    return Path(os.environ['BRAND_TEMPLATES_CATALOG']).expanduser() if root == ROOT and 'BRAND_TEMPLATES_CATALOG' in os.environ else root / 'library/catalog.json'


def source_manifest_path(root=ROOT):
    return Path(os.environ['BRAND_TEMPLATES_SOURCE_MANIFEST']).expanduser() if root == ROOT and 'BRAND_TEMPLATES_SOURCE_MANIFEST' in os.environ else root / 'provenance/source-files.json'


def catalog(root=ROOT):
    data = json.loads(catalog_path(root).read_text())['brands']
    ids = [item['id'] for item in data]
    if len(set(ids)) != len(ids) or not all(ID.fullmatch(i) for i in ids):
        raise ValueError('Invalid or duplicate brand IDs')
    return data


def select(brand_id, root=ROOT):
    if not isinstance(brand_id, str) or not ID.fullmatch(brand_id):
        raise ValueError('Invalid brand ID')
    return next((item for item in catalog(root) if item['id'] == brand_id), None) or _missing()


def _missing():
    raise ValueError('Unknown brand ID')


def search(query='', category='all', root=ROOT):
    if len(query) > 2000:
        raise ValueError('Query too long')
    words = query.casefold().split()
    items = []
    for item in catalog(root):
        hay = ' '.join([item['id'], item['name'], item['summary'], item['category'], *item['tags']]).casefold()
        if (category in ('', 'all') or item['category'] == category) and all(w in hay for w in words):
            items.append({k:item[k] for k in ('id','name','summary','category','tags','version','sourceTemplateIds','rightsSummary')})
    return {'owner':'Brand Templates','query':query,'category':category,'items':items,'total':len(items)}


def validate(brand_id, root=ROOT):
    item = select(brand_id, root)
    prefix = f'templates/{brand_id}/'
    manifest = json.loads(source_manifest_path(root).read_text())['files']
    rows = [row for row in manifest if row['path'].startswith(prefix)]
    catalog_row = next((row for row in manifest if row['path'] == 'library/catalog.json'), None)
    if not catalog_row or hashlib.sha256(catalog_path(root).read_bytes()).hexdigest() != catalog_row['sha256']:
        raise ValueError('Brand catalog differs from registered edition')
    if not rows:
        raise ValueError('Brand source closure is not registered')
    for row in rows:
        path = root / row['path']
        if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink() or not path.is_file():
            raise ValueError('Missing or unsafe brand source')
        if hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Brand source differs from registered edition')
    digest = hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(',',':')).encode()).hexdigest()
    return item, digest, len(rows)


def handoff(brand_id, brief='', root=ROOT):
    if not isinstance(brief,str) or len(brief)>8000:
        raise ValueError('Brief must be text up to 8000 characters')
    item, digest, count = validate(brand_id, root)
    template = root/'templates'/brand_id
    message = f"Use Brand Templates: {item['name']} (ID: {brand_id}, version {item['version']}).\nRead {template/'SKILL.md'} and {template/'DESIGN.md'}; preserve all recognition rules, source facts and font notices.\nSource closure verified: {digest} ({count} files).\nBrief: {brief or '(none supplied)'}\nUse Graphic Design for visual execution, UX Design for interfaces, and Writing Templates only for an explicitly selected writing structure. Source design IDs: {', '.join(item['sourceTemplateIds'])}. Adapt a new copy and review the rendered output. This selection does not install, publish or trademark-clear the brand."
    return {'brandId':brand_id,'version':item['version'],'sourceHash':item['sourceHash'],'closureHash':digest,'verifiedFiles':count,'handoffText':message,'sourcePath':str(template),'rightsSummary':item['rightsSummary']}
