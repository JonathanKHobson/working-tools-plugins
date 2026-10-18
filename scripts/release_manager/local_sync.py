"""Reconcile reviewed public paths only; never widen a private export silently."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re

MANIFESTS=('plugin.json','.codex-plugin/plugin.json','.claude-plugin/plugin.json')

# Only these host-native compatibility manifests are actually dispatched for
# hooks/MCP servers at runtime (Codex reads .codex-plugin, Claude reads
# .claude-plugin). The portable root manifest (plugin.json, or
# plugin.portable.json for packages where a root Agent Plugins manifest would
# otherwise make the installed Codex CLI skip native hook discovery) is
# metadata only, so it is intentionally excluded from registration parity.
REGISTRATION_MANIFESTS=('.codex-plugin/plugin.json','.claude-plugin/plugin.json')

def root_manifest_name(base):
    return next((n for n in ('plugin.json','plugin.portable.json') if (Path(base)/n).is_file()),None)

def version_manifest_names(base):
    root=root_manifest_name(base)
    return list(REGISTRATION_MANIFESTS)+([root] if root else [])

def registrations(document, prefix=''):
    """Keep host registrations, including portable extensions, out of metadata sync."""
    result={}
    if isinstance(document,dict):
        for key,value in document.items():
            path=prefix+'/'+key if prefix else key
            if key in {'hooks','mcpServers'}:result[path]=value
            else:result.update(registrations(value,path))
    return result

def require_matching_registrations(ident, rel, source, public):
    if rel not in REGISTRATION_MANIFESTS:return
    local=registrations(read(source));remote=registrations(read(public))
    # Exact, previously reviewed projections may use different portable paths.
    # The pins must match both current manifests; edits invalidate the exception.
    package=Path(public)
    for _ in Path(rel).parts:package=package.parent
    inventory=package.parent.parent/'catalog/source-inventory.json'
    if inventory.is_file():
        row=next((r for r in read(inventory).get('packages',[]) if r.get('id')==ident),{})
        if (row.get('canonical_files',{}).get(rel)==digest(Path(source).read_bytes())
                and row.get('files',{}).get(rel)==digest(Path(public).read_bytes())):
            return
    for field in sorted(set(local)|set(remote)):
        if field not in local or field not in remote or local[field]!=remote[field]:
            raise ValueError('Registration mismatch requires explicit reconciliation: '+ident+'/'+rel+' -> '+field)

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


def approved_product_roots(root, canonical, canonical_sources=None, *, product_ids=None):
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
    if product_ids is not None and set(product_ids)-set(rows):
        raise ValueError('Unknown selected product: '+', '.join(sorted(set(product_ids)-set(rows))))
    for ident,row in rows.items():
        if product_ids is not None and ident not in product_ids:continue
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


def plan(root, canonical, canonical_sources=None, *, product_ids=None):
    """Only already-reviewed paths transfer, and only canonical -> public.

    Canonical is never written by publication. A path's public bytes may
    legitimately diverge from canonical (e.g. after a version bump, or a
    deliberately reviewed public-only projection) without that being a
    conflict; only a genuine disagreement between a fresh canonical edit and
    an already-diverged public edit needs explicit reconciliation.
    """
    root=Path(root);canonical=Path(canonical)
    changes={};conflicts=[]
    inventory=read(root/'catalog/source-inventory.json')
    roots=approved_product_roots(root,canonical,canonical_sources,product_ids=product_ids)
    for row in inventory['packages']:
        if row['id'] not in roots:continue
        changed={}; public=root/'plugins'/row['id']; source=roots[row['id']]
        canonical_base=row.get('canonical_files') or row['files']
        public_only=set(row.get('public_only_files',[])) | set(row.get('public_projection_overrides',[]))
        for rel,public_base in row['files'].items():
            # Public projections such as portable manifests and audit inventories
            # are reviewed in the public checkout. Some are absent canonically;
            # LICENSE-SCOPE is present canonically but intentionally regenerated
            # for the public file set. All remain inventory- and metadata-locked.
            if rel in public_only:
                continue
            source_base=canonical_base.get(rel,public_base)
            try:local=safe_file(source,rel);target=safe_file(public,rel)
            except ValueError:
                conflicts.append(f"{row['id']}: unsafe source path {rel}");continue
            if not local.is_file() or not target.is_file():
                conflicts.append(f"{row['id']}: review removal of {rel}");continue
            a=digest(local.read_bytes());b=digest(target.read_bytes())
            if a==source_base:continue  # Canonical unchanged: nothing to publish for this path.
            if b!=public_base and b!=a:
                conflicts.append(f"{row['id']}: divergent public and canonical edits: {rel}")
            else:
                changed[rel]={'source':'canonical','base':source_base,'sha256':a,'public_sha256':b}
        if changed:changes[row['id']]=changed
    return changes,conflicts


def apply_content(root, canonical, changes, canonical_sources=None):
    """Copy canonical bytes into public only; canonical is never written."""
    root=Path(root);canonical=Path(canonical)
    roots=approved_product_roots(root,canonical,canonical_sources,product_ids=changes)
    for ident,paths in changes.items():
        for rel,change in paths.items():
            if change.get('source')!='canonical':
                raise ValueError('Publication may only copy canonical -> public: '+ident+'/'+rel)
    # Preflight the entire batch before copying any files.
    for ident,paths in changes.items():
        for rel in paths:
            require_matching_registrations(ident,rel,safe_file(roots[ident],rel),safe_file(root/'plugins'/ident,rel))
    for ident,paths in changes.items():
        for rel,change in paths.items():
            local=safe_file(roots[ident],rel);public=safe_file(root/'plugins'/ident,rel)
            data=local.read_bytes()
            if digest(data)!=change['sha256']:raise ValueError('Canonical source changed during completion: '+ident+'/'+rel)
            expected_public=change.get('public_sha256',change['base'])
            if not public.is_file() or digest(public.read_bytes())!=expected_public:
                raise ValueError('Destination changed during completion: '+ident+'/'+rel)
            public.write_bytes(data)


def entry_path(entry):
    return entry.get('path') or entry.get('source_relative')


def current_hash_fields(entry):
    # Source, upstream and dated snapshot hashes document historical inputs.
    return [key for key in ('sha256','output_sha256','public_sha256') if key in entry]


def metadata_excludes(document, name):
    excluded={name}
    for key in ('inventory_excludes','manifest_self_exclusion'):
        value=document.get(key,[])
        if not isinstance(value,list) or any(not isinstance(p,str) for p in value):
            raise ValueError('Invalid metadata exclusions: '+name)
        excluded.update(value)
    value=document.get('self_hash_omitted',document.get('self_excluded'))
    if isinstance(value,str):excluded.add(value)
    return excluded


def reviewed_additions(root, canonical, ident, additions, canonical_sources=None):
    """Admit an exact author-reviewed list; never discover or expand public scope."""
    if not isinstance(additions,list) or any(not isinstance(p,str) for p in additions):
        raise ValueError(ident+': reviewed_additions must be a list of relative paths')
    if len(set(additions))!=len(additions):
        raise ValueError(ident+': duplicate reviewed addition')
    root=Path(root)
    row=next(r for r in read(root/'catalog/source-inventory.json')['packages'] if r['id']==ident)
    public=root/'plugins'/ident
    source=approved_product_roots(root,canonical,canonical_sources,product_ids=[ident])[ident]
    documents={name:read(safe_file(public,name)) for name in ('PROVENANCE.json','LICENSE-SCOPE.json')}
    changes={}
    for rel in additions:
        if rel not in row['files']:
            raise ValueError(ident+': addition is not in reviewed source inventory: '+rel)
        a=safe_file(public,rel);b=safe_file(source,rel)
        expected=row['files'][rel]
        if not a.is_file() or not b.is_file() or digest(a.read_bytes())!=expected or digest(b.read_bytes())!=expected:
            raise ValueError(ident+': reviewed addition bytes disagree: '+rel)
        for name,document in documents.items():
            entries=[e for e in document.get('files',[]) if entry_path(e)==rel]
            if rel in metadata_excludes(document,name) or len(entries)!=1:
                raise ValueError(ident+': addition lacks reviewed '+name+' coverage: '+rel)
            fields=current_hash_fields(entries[0])
            if not fields or any(entries[0][field]!=expected for field in fields):
                raise ValueError(ident+': addition '+name+' hash disagrees: '+rel)
            if name=='LICENSE-SCOPE.json' and not entries[0].get('license'):
                raise ValueError(ident+': addition lacks reviewed license grant: '+rel)
        changes[rel]={'source':'canonical','base':expected,'sha256':expected,'status':'added'}
    return changes



def metadata_entries(document, name):
    files=document.get('files',[])
    if isinstance(files,dict):
        if any(not isinstance(path,str) or not isinstance(value,str) for path,value in files.items()):
            raise ValueError('Invalid path-to-hash metadata: '+name)
        entries=[{'path':path,'sha256':value} for path,value in files.items()]
    elif isinstance(files,list) and all(isinstance(entry,dict) for entry in files):
        entries=list(files)
    else:
        raise ValueError('Invalid metadata files shape: '+name)
    if name=='PROVENANCE.json':
        # These are public projection inventories, rather than archived input receipts.
        entries.extend(document.get('added_files',[]))
        entries.extend(document.get('standalone_imports',[]))
        entries.extend(document.get('standalone_additions',{}).get('full_original_closures',[]))
    return entries

def refresh_metadata(public, allowed, version):
    """Refresh current output fields in dependency order without changing grants."""
    documents={name:read(public/name) for name in
               ('PROVENANCE.json','LICENSE-SCOPE.json','PUBLIC_FILE_MANIFEST.json')
               if name in allowed and (public/name).is_file()}
    dependencies={}
    for name,document in documents.items():
        excluded=metadata_excludes(document,name)
        document['version']=version
        # Existing schema scope is authoritative; do not auto-add inventory rows.
        entries=metadata_entries(document,name)
        dependencies[name]={entry_path(e) for e in entries
                            if entry_path(e) in documents and entry_path(e) not in excluded}
    pending=set(documents)
    while pending:
        ready=sorted(name for name in pending if not dependencies[name]&pending)
        if not ready:raise ValueError('Cyclic metadata hashes: '+', '.join(sorted(pending)))
        for name in ready:
            document=documents[name];excluded=metadata_excludes(document,name)
            for entry in metadata_entries(document,name):
                rel=entry_path(entry)
                if rel in excluded or rel not in allowed:continue
                path=safe_file(public,rel)
                if not path.is_file():raise ValueError('Missing reviewed file: '+str(rel))
                fields=current_hash_fields(entry)
                if not fields:fields=['output_sha256']
                value=digest(path.read_bytes())
                for field in fields:entry[field]=value
                if isinstance(document.get('files'),dict) and rel in document['files']:
                    document['files'][rel]=value
                if 'bytes' in entry:entry['bytes']=path.stat().st_size
            write(public/name,document)
            pending.remove(name)


def refresh_reviewed(root, canonical, ident, version, notes, *, approved_additions=(), canonical_sources=None, expected_source_hashes=None):
    """Refresh named reviewed paths after reconciled edits, preserving audit holds."""
    root=Path(root);canonical=Path(canonical)
    inventory=read(root/'catalog/source-inventory.json'); row=next(r for r in inventory['packages'] if r['id']==ident)
    public=root/'plugins'/ident;source=approved_product_roots(root,canonical,canonical_sources,product_ids=[ident])[ident]
    registry=read(root/'catalog/packages.json');record=next(r for r in registry['packages'] if r['id']==ident)
    record['version']=version;record['distribution']='prepared'
    allowed=set(row['files'])
    if approved_additions:
        reviewed_additions(root,canonical,ident,list(approved_additions),canonical_sources)
    canonical_allowed=set(row.get('canonical_files', row['files']))
    for rel in allowed:
        if not safe_file(public,rel).is_file() or (rel in canonical_allowed and not safe_file(source,rel).is_file()):
            raise ValueError('Missing reviewed file: '+rel)
    expected_source_hashes=(dict(expected_source_hashes) if expected_source_hashes is not None else
                            {rel:digest(safe_file(source,rel).read_bytes()) for rel in canonical_allowed})
    def unchanged_source(rel):
        path=safe_file(source,rel)
        if not path.is_file() or digest(path.read_bytes())!=expected_source_hashes.get(rel):
            raise ValueError('Canonical source changed during metadata refresh: '+ident+'/'+rel)
        return path
    for rel in canonical_allowed:unchanged_source(rel)
    for rel in REGISTRATION_MANIFESTS:
        if rel not in canonical_allowed:continue
        require_matching_registrations(ident,rel,safe_file(source,rel),safe_file(public,rel))
    for rel in version_manifest_names(public):
        data=read(public/rel);data['version']=version;write(public/rel,data)
    changelog=public/'CHANGELOG.md'
    if not changelog.is_file():raise ValueError('Package needs reviewed changelog path')
    old=changelog.read_text()
    heading=f'## {version}\n'
    existing=rf'(?m)^##[ \t]+{re.escape(version)}(?:[ \t]+·[ \t]+\d{{4}}-\d{{2}}-\d{{2}})?[ \t]*\r?$'
    if not re.search(existing,old):
        changelog.write_text('# Changelog\n\n'+heading+'\n'+notes+'\n\n'+old.removeprefix('# Changelog').lstrip())
    refresh_metadata(public,allowed,version)
    # Publication only ever reads canonical; it is never written here. The
    # public tree is free to move ahead of canonical (e.g. this version bump),
    # so the public and canonical hashes are tracked separately below.
    for rel in allowed:
        p=public/rel
        if p.is_symlink() or not p.is_file():raise ValueError('Missing/unsafe reviewed file: '+rel)
        if rel in canonical_allowed:unchanged_source(rel)
    row['version']=version;row['files']={p:digest((public/p).read_bytes()) for p in sorted(allowed)}
    row['canonical_files']={p:expected_source_hashes[p] for p in sorted(canonical_allowed)}
    row['canonical_source']['revision']['sha256']=tree(row['files'])
    write(root/'catalog/packages.json',registry);write(root/'catalog/source-inventory.json',inventory)
    # Excluded scopes and coverage baseline intentionally remain untouched.
    return record
