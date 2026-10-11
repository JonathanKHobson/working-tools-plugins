"""Reconcile reviewed public paths only; never widen a private export silently."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re

MANIFESTS=('plugin.json','.codex-plugin/plugin.json','.claude-plugin/plugin.json')

def digest(data):return hashlib.sha256(data).hexdigest()
def read(path):return json.loads(Path(path).read_text())
def write(path,data):Path(path).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def tree(files):return digest(''.join(f'{files[p]}  {p}\n' for p in sorted(files)).encode())

def safe_file(base, relative):
    """Reject traversal and symlink components on both sides of a transfer."""
    rel=Path(relative)
    if rel.is_absolute() or not relative or any(x in {'.','..'} for x in rel.parts):
        raise ValueError('Unsafe reviewed path: '+str(relative))
    path=Path(base)
    if path.is_symlink():raise ValueError('Symlinked product root: '+str(base))
    for part in rel.parts:
        path=path/part
        if path.is_symlink():raise ValueError('Symlink in reviewed path: '+str(path))
    return path


def approved_product_roots(root, canonical, canonical_sources=None):
    """Resolve only reviewed product-root links pinned by private configuration.

    A product-root redirect is deliberate; symlinks below that root remain unsafe.
    Rechecking this for each phase also catches a redirect changed during completion.
    """
    root=Path(root);canonical=Path(canonical)
    mapping={} if canonical_sources is None else canonical_sources
    if not isinstance(mapping,dict) or any(not isinstance(k,str) or not isinstance(v,str) for k,v in mapping.items()):
        raise ValueError('canonical_sources must map product IDs to absolute resolved directories')
    inventory=read(root/'catalog/source-inventory.json')
    rows={row['id']:row for row in inventory['packages']}
    if unknown:=set(mapping)-set(rows):
        raise ValueError('Unknown canonical_sources product: '+', '.join(sorted(unknown)))
    result={}
    for ident,row in rows.items():
        source=canonical/row['canonical_source']['id']
        if not source.is_dir():
            raise ValueError('Missing canonical product root: '+ident)
        physical=source.resolve(strict=True)
        if source.is_symlink() and ident not in mapping:
            raise ValueError('Unapproved canonical product root symlink: '+ident)
        if ident in mapping:
            expected=Path(mapping[ident])
            if not expected.is_absolute() or not expected.is_dir() or expected.resolve(strict=True)!=expected:
                raise ValueError('canonical_sources target must be an absolute resolved directory: '+ident)
            if physical!=expected:
                raise ValueError('Canonical product root target differs from approved mapping: '+ident)
        result[ident]=physical
    return result


def plan(root, canonical, canonical_sources=None):
    """Only already-reviewed paths transfer. New/removals demand explicit review."""
    root=Path(root);canonical=Path(canonical)
    changes={};conflicts=[]
    inventory=read(root/'catalog/source-inventory.json')
    roots=approved_product_roots(root,canonical,canonical_sources)
    for row in inventory['packages']:
        changed={}; public=root/'plugins'/row['id']; source=roots[row['id']]
        for rel,base in row['files'].items():
            try:local=safe_file(source,rel);target=safe_file(public,rel)
            except ValueError:
                conflicts.append(f"{row['id']}: unsafe source path {rel}");continue
            if not local.is_file() or not target.is_file():
                conflicts.append(f"{row['id']}: review removal of {rel}");continue
            a=digest(local.read_bytes());b=digest(target.read_bytes())
            if a!=base and b!=base and a!=b:
                conflicts.append(f"{row['id']}: divergent public and canonical edits: {rel}")
            elif a!=base or b!=base:
                changed[rel]={'source':'canonical' if a!=base else 'public','base':base,'sha256':a if a!=base else b}
        if changed:changes[row['id']]=changed
    return changes,conflicts


def apply_content(root, canonical, changes, canonical_sources=None):
    root=Path(root);canonical=Path(canonical)
    roots=approved_product_roots(root,canonical,canonical_sources)
    for ident,paths in changes.items():
        for rel,change in paths.items():
            local=safe_file(roots[ident],rel);public=safe_file(root/'plugins'/ident,rel)
            src=local if change['source']=='canonical' else public
            dst=public if change['source']=='canonical' else local
            data=src.read_bytes()
            if digest(data)!=change['sha256']:raise ValueError('Source changed during completion: '+ident+'/'+rel)
            if not dst.is_file() or digest(dst.read_bytes()) not in {change['base'],change['sha256']}:
                raise ValueError('Destination changed during completion: '+ident+'/'+rel)
            dst.write_bytes(data)


def refresh_reviewed(root, canonical, ident, version, notes, *, approved_additions=(), canonical_sources=None):
    """Refresh named reviewed paths after reconciled edits, preserving audit holds."""
    root=Path(root);canonical=Path(canonical)
    inventory=read(root/'catalog/source-inventory.json'); row=next(r for r in inventory['packages'] if r['id']==ident)
    public=root/'plugins'/ident;source=approved_product_roots(root,canonical,canonical_sources)[ident]
    registry=read(root/'catalog/packages.json');record=next(r for r in registry['packages'] if r['id']==ident)
    record['version']=version;record['distribution']='released'
    allowed=set(row['files'])
    if approved_additions:
        raise ValueError('Review new paths in source inventory and provenance before completion')
    for rel in allowed:
        if not safe_file(public,rel).is_file() or not safe_file(source,rel).is_file():
            raise ValueError('Missing reviewed file: '+rel)
    for rel in MANIFESTS:
        data=read(public/rel);data['version']=version;write(public/rel,data)
    changelog=public/'CHANGELOG.md'
    if not changelog.is_file():raise ValueError('Package needs reviewed changelog path')
    old=changelog.read_text()
    heading=f'## {version}\n'
    existing=rf'(?m)^##[ \t]+{re.escape(version)}(?:[ \t]+·[ \t]+\d{{4}}-\d{{2}}-\d{{2}})?[ \t]*\r?$'
    if not re.search(existing,old):
        changelog.write_text('# Changelog\n\n'+heading+'\n'+notes+'\n\n'+old.removeprefix('# Changelog').lstrip())
    provenance=read(public/'PROVENANCE.json');provenance['version']=version
    for entry in provenance.get('files',[]):
        rel=entry.get('path',entry.get('source_relative'))
        if rel in allowed and rel!='PROVENANCE.json':
            p=public/rel
            if not p.is_file():raise ValueError('Missing reviewed file: '+rel)
            h=digest(p.read_bytes());entry['source_sha256']=h;entry['output_sha256']=h;entry['bytes']=p.stat().st_size
    write(public/'PROVENANCE.json',provenance)
    for rel in allowed:
        p=public/rel
        if p.is_symlink() or not p.is_file():raise ValueError('Missing/unsafe reviewed file: '+rel)
        dst=safe_file(source,rel);dst.write_bytes(safe_file(public,rel).read_bytes())
    row['version']=version;row['files']={p:digest((public/p).read_bytes()) for p in sorted(allowed)}
    row['canonical_source']['revision']['sha256']=tree(row['files'])
    write(root/'catalog/packages.json',registry);write(root/'catalog/source-inventory.json',inventory)
    # Excluded scopes and coverage baseline intentionally remain untouched.
    return record
