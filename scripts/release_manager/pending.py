"""Private offline change journal. Observations never authorize release or import."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

from . import local_sync

SCHEMA='working-tools.pending.v1'
FIELDS=('summary','why','compatibility','upgrade_guidance','validation','notes')
SKIP={'.git','.venv','__pycache__','.pytest_cache','node_modules','dist'}


def fingerprint(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def read_previous(path):
    if not path.exists():return {'schema_version':SCHEMA,'entries':[],'boundaries':[]}
    try:
        value=json.loads(path.read_text())
        if (not isinstance(value,dict) or value.get('schema_version')!=SCHEMA
                or not isinstance(value.get('entries'),list) or not isinstance(value.get('boundaries'),list)):
            raise ValueError()
        keys=set()
        for entry in value['entries']:
            if (not isinstance(entry,dict) or not all(isinstance(entry.get(k),str) and entry[k]
                    for k in ('id','kind','first_seen','fingerprint'))):raise ValueError()
            key=(entry['kind'],entry['id'])
            if key in keys:raise ValueError()
            keys.add(key)
            observed={k:v for k,v in entry.items() if k not in {'fingerprint','first_seen'}}
            if entry['fingerprint']!=fingerprint(observed):raise ValueError()
        if value.get('fingerprint')!=fingerprint({k:v for k,v in value.items() if k!='fingerprint'}):raise ValueError()
        return value
    except (OSError,ValueError,TypeError):
        raise ValueError('Pending journal is unreadable or corrupt; original bytes preserved') from None


def atomic_save(path,document):
    path.parent.mkdir(parents=True,exist_ok=True)
    descriptor,name=tempfile.mkstemp(prefix='.pending-',dir=path.parent)
    try:
        with os.fdopen(descriptor,'w') as stream:
            os.fchmod(stream.fileno(),0o600)
            stream.write(json.dumps(document,indent=2,sort_keys=True)+'\n')
            stream.flush();os.fsync(stream.fileno())
        os.replace(name,path)
    finally:
        if os.path.exists(name):os.unlink(name)


def file_hash(base,relative):
    try:
        path=local_sync.safe_file(base,relative)
        return local_sync.digest(path.read_bytes()) if path.is_file() else None
    except (ValueError,OSError):return None


def unreviewed_paths(base,allowed,excluded=()):
    found=[]
    for directory,dirs,files in os.walk(base,followlinks=False):
        kept=[]
        for name in sorted(dirs):
            rel=(Path(directory)/name).relative_to(base).as_posix()
            if name in SKIP:continue
            excluded_here=any(rel==scope or rel.startswith(scope.rstrip('/')+'/') for scope in excluded)
            if excluded_here and not any(p.startswith(rel+'/') for p in allowed):continue
            if (Path(directory)/name).is_symlink():
                if not excluded_here:found.append(rel+'/ [symlink]')
            else:kept.append(name)
        dirs[:]=kept
        for name in sorted(files):
            rel=(Path(directory)/name).relative_to(base).as_posix()
            if name=='.DS_Store' or name.endswith(('.pyc','.pyo')) or name.startswith('._'):continue
            if rel not in allowed and not any(rel==scope or rel.startswith(scope.rstrip('/')+'/') for scope in excluded):
                found.append(rel)
    return found


def notes_state(root,ident):
    path=root/'catalog/changes'/(ident+'.json')
    if not path.exists():return {},False,[]
    try:
        note=local_sync.read(path)
        if not isinstance(note,dict):raise ValueError()
        return note,all(isinstance(note.get(k),str) and note[k].strip() for k in FIELDS),[]
    except (ValueError,OSError):return {},False,['semantic change note is unreadable']


def plugin_observation(root,config,row,version):
    ident=row['id'];public=root/'plugins'/ident;files=row['files']
    note,ready,signals=notes_state(root,ident)
    canonical=Path(config['canonical_root'])
    try:
        changes,conflicts=local_sync.plan(root,canonical,config.get('canonical_sources'),product_ids=[ident])
        source=local_sync.approved_product_roots(root,canonical,config.get('canonical_sources'),product_ids=[ident])[ident]
    except (ValueError,OSError):
        return {'id':ident,'kind':'plugin','recorded_version':version,'state':'pending-review',
                'changes':[],'conflicts':['canonical source unavailable or unsafe'],
                'review_signals':signals,'notes_ready':ready,'reviewed_additions':[]}
    observed=[]
    for rel,baseline in sorted(files.items()):
        a=file_hash(source,rel);b=file_hash(public,rel)
        source_baseline=row.get('canonical_files',{}).get(rel,baseline)
        if a!=source_baseline or b!=baseline:
            observed.append({'path':rel,'baseline_sha256':baseline,'canonical_sha256':a,
                             'public_sha256':b,'source':changes.get(ident,{}).get(rel,{}).get('source','conflict')})
    for source_name,destinations in config.get('shared_shipped_paths',{}).items():
        if not isinstance(source_name,str) or not isinstance(destinations,list):
            signals.append('shared source mapping needs review');continue
        for destination in destinations:
            if not isinstance(destination,str) or not destination.startswith('plugins/'+ident+'/'):continue
            relative=destination[len('plugins/'+ident+'/'):]
            if relative not in files:
                signals.append('shared destination is not reviewed: '+relative);continue
            actual=file_hash(root,source_name)
            if actual!=files[relative]:
                observed.append({'path':relative,'baseline_sha256':files[relative],
                    'canonical_sha256':file_hash(source,relative),'public_sha256':file_hash(public,relative),
                    'source':'shared','shared_source':source_name,'shared_sha256':actual})
                if actual is None:signals.append('shared source unavailable or unsafe')
    additions=note.get('reviewed_additions',[])
    if not isinstance(additions,list) or any(not isinstance(p,str) for p in additions):
        signals.append('reviewed_additions must be an exact relative-path list');additions=[]
    elif additions:
        try:local_sync.reviewed_additions(root,canonical,ident,additions,config.get('canonical_sources'))
        except (ValueError,OSError):signals.append('listed additions need inventory, byte, provenance or license review')
        for rel in sorted(set(additions)):
            if rel not in files:continue
            if not any(item['path']==rel for item in observed):
                observed.append({'path':rel,'baseline_sha256':files[rel],
                    'canonical_sha256':file_hash(source,rel),'public_sha256':file_hash(public,rel),'source':'reviewed-addition'})
    excluded=[d['scope'] for d in row.get('excluded_source',{}).get('dispositions',[]) if isinstance(d,dict) and isinstance(d.get('scope'),str)]
    for side,base in [('canonical',source),('public',public)]:
        signals.extend(side+': unreviewed path '+rel for rel in unreviewed_paths(base,files,excluded if side=='canonical' else ()))
    if not observed and not conflicts and not signals:return None
    return {'id':ident,'kind':'plugin','recorded_version':version,
            'state':'pending-review' if conflicts or signals or not ready else 'pending',
            'changes':sorted(observed,key=lambda item:item['path']),'conflicts':conflicts,
            'review_signals':sorted(signals),'notes_ready':ready,'reviewed_additions':sorted(set(additions))}


def git_paths(checkout,base=None,paths=()):
    """Local Git only: committed differences plus working-tree and new paths."""
    if not Path(checkout).is_dir():return None
    try:
        found=set()
        commands=[['diff','--name-only','-z','--no-renames',base or 'HEAD','--',*paths],
                  ['ls-files','--others','--exclude-standard','-z','--',*paths]]
        for args in commands:
            raw=subprocess.check_output(['git',*args],cwd=checkout,stderr=subprocess.DEVNULL,
                env={**os.environ,'GIT_NO_LAZY_FETCH':'1','GIT_TERMINAL_PROMPT':'0'})
            found.update(p.decode('utf-8') for p in raw.split(b'\0') if p)
        return sorted(found)
    except (OSError,subprocess.CalledProcessError,UnicodeError):return None


def other_observations(root,config):
    entries=[];boundaries=[]
    integration=root/'catalog/integrations.json'
    if integration.is_file():
        for row in local_sync.read(integration)['products']:
            changed=[{'path':p,'baseline_sha256':h,'public_sha256':file_hash(root,p)}
                     for p,h in sorted(row['source_files'].items()) if file_hash(root,p)!=h]
            extra=unreviewed_paths(root/row['source_root'],
                {Path(p).relative_to(row['source_root']).as_posix() for p in row['source_files']})
            boundaries.append({'kind':'integration','id':row['id'],'state':'pending' if changed or extra else 'clean',
                               'coverage':'registered source hashes and unreviewed-path signals; separate release owner'})
            if changed or extra:entries.append({'kind':'integration','id':row['id'],'recorded_version':row['version'],
                'state':'pending-review','changes':changed,'review_signals':['unreviewed path '+p for p in extra]})
    external=root/'catalog/external-products.json'
    if external.is_file():
        document=local_sync.read(external)
        for row in document['products']:
            if row['lifecycle'] not in {'active-guide-page','active-guide-download'}:continue
            source=row['source'];checkout=config.get('external_checkouts',{}).get(source['id'])
            base=source.get('commit') or document['sources'][source['id']]['commit']
            paths=git_paths(checkout,base,source['files']) if checkout else None
            boundaries.append({'kind':'external','id':row['id'],
                'state':'unconfigured' if not checkout else 'unavailable' if paths is None else 'pending' if paths else 'clean',
                'coverage':'registered owner paths against recorded local Git revision; no network or asset verification'})
            if paths:entries.append({'kind':'external','id':row['id'],'recorded_version':row['version'].get('value'),
                'state':'pending-review','changes':[{'path':p,'source_sha256':file_hash(Path(checkout),p)} for p in paths]})
    site=config.get('site_source');baseline=None
    if config.get('site_receipt'):
        try:
            candidate=local_sync.read(config['site_receipt']).get('maintained_source_commit')
            if isinstance(candidate,str) and len(candidate)==40 and all(c in '0123456789abcdef' for c in candidate):baseline=candidate
        except (ValueError,OSError,AttributeError):pass
    paths=git_paths(site,baseline) if site else None
    boundaries.append({'kind':'site','id':'working-tools-site',
        'state':'unconfigured' if not site else 'unavailable' if paths is None else 'pending' if paths else 'clean' if baseline else 'unknown-deployment-baseline',
        'deployment_baseline':baseline or 'unknown',
        'coverage':'local Git against saved maintained deployment commit plus working-tree/untracked changes; no live deployment check'
                   if baseline else 'working-tree/untracked changes only; deployment baseline unknown and committed unpublished changes not checked'})
    if paths:entries.append({'kind':'site','id':'working-tools-site','state':'pending-review',
        'changes':[{'path':p,'source_sha256':file_hash(Path(site),p)} for p in paths]})
    return entries,boundaries



def recovery_boundary(root,registered):
    path=root/'dist/release-manager/receipt.json'
    boundary={'kind':'publication-recovery','id':'completion','state':'absent',
              'coverage':'saved local completion receipt only; no live publication verification'}
    if not path.exists():return boundary
    try:
        receipt=local_sync.read(path)
        status=receipt.get('status')
        if status not in {'complete','preparing','releases_published','catalog_pending','external_publishing'}:
            raise ValueError()
        boundary.update({'state':'complete' if status=='complete' else 'incomplete','receipt_status':status})
        scope=receipt.get('selected_packages')
        if scope is None:boundary['selected_packages']='all'
        elif isinstance(scope,list) and all(isinstance(p,str) and p in registered for p in scope):
            boundary['selected_packages']=sorted(set(scope))
        else:boundary['selected_packages']='unknown'
    except (ValueError,OSError,AttributeError):boundary['state']='unreadable'
    return boundary

def refresh(root,config,product_ids=None):
    root=Path(root);path=root/'dist/release-manager/pending.json'
    previous=read_previous(path)  # Validate before any write or observation side effect.
    inventory=local_sync.read(root/'catalog/source-inventory.json')
    versions={row['id']:row['version'] for row in local_sync.read(root/'catalog/packages.json')['packages']}
    selected=set(versions) if product_ids is None else set(product_ids)
    if unknown:=selected-set(versions):raise ValueError('Unknown selected package: '+', '.join(sorted(unknown)))
    if not config.get('canonical_root'):raise ValueError('Local queue requires configured canonical_root')
    entries=[entry for entry in previous['entries'] if product_ids is not None
             and (entry['kind']!='plugin' or entry['id'] not in selected)]
    for row in inventory['packages']:
        if row['id'] in selected:
            entry=plugin_observation(root,config,row,versions[row['id']])
            if entry:entries.append(entry)
    if product_ids is None:
        others,boundaries=other_observations(root,config);entries.extend(others)
    else:boundaries=previous['boundaries']
    boundaries=[b for b in boundaries if b.get('kind')!='publication-recovery']
    boundaries.append(recovery_boundary(root,versions))
    prior={(e['kind'],e['id']):e for e in previous['entries']}
    now=datetime.now(timezone.utc).isoformat(timespec='seconds')
    for entry in entries:
        if 'fingerprint' in entry:continue  # Unselected entries are preserved exactly.
        entry['fingerprint']=fingerprint(entry)
        entry['first_seen']=prior.get((entry['kind'],entry['id']),{}).get('first_seen',now)
    document={'schema_version':SCHEMA,'entries':sorted(entries,key=lambda e:(e['kind'],e['id'])),
              'boundaries':boundaries,'promotion':'explicit --publish only; no time or count trigger'}
    document['fingerprint']=fingerprint(document)
    atomic_save(path,document)
    return document


def summary(document):
    lines=[f"Local pending queue: {len(document['entries'])} product(s). No release or deployment started."]
    for entry in document['entries']:
        lines.append(f"{entry['kind']} {entry['id']}: {entry['state']}, {len(entry.get('changes',[]))} path(s)"
                     +(f", recorded {entry['recorded_version']}" if entry.get('recorded_version') else ''))
    for boundary in document['boundaries']:
        lines.append(f"{boundary['kind']} {boundary['id']}: {boundary['state']} ({boundary['coverage']})")
    return '\n'.join(lines)
