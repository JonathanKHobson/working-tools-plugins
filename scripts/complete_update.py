#!/usr/bin/env python3
"""Record local pending changes; publish only through an explicit release operation."""
from __future__ import annotations
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from release_manager import local_sync, pending
from release_manager.changes import propose_version
from release_manager.publisher import exact_commit_build, list_releases, publish, run

ROOT=Path(__file__).resolve().parents[1]
REPOSITORY='JonathanKHobson/working-tools-plugins'


def command(*args,cwd=ROOT):
    subprocess.run(list(args),cwd=cwd,check=True)


def load(path):return json.loads(Path(path).read_text())
def save(path,data):Path(path).parent.mkdir(parents=True,exist_ok=True);Path(path).write_text(json.dumps(data,indent=2)+'\n')


def pending_entries(product_ids=None):
    """Find prepared release records without repeating their version bump."""
    found=[]
    for path in sorted((ROOT/'catalog/releases').glob('*/*.json')):
        if product_ids is not None and path.parent.name not in product_ids:continue
        relative=path.relative_to(ROOT).as_posix()
        state=run('git','status','--porcelain','--untracked-files=all','--',relative,cwd=ROOT)
        if state:
            row=load(path)
            if path.parent.name!=row.get('product_id') or path.stem!=row.get('version'):
                raise ValueError('Prepared release identity differs from path: '+relative)
            found.append({'id':row['product_id'],'version':row['version'],
                          'changed_files':row['changed_files'],
                          'shared_sources':row.get('shared_sources',[])})
    return found


def unfinished_committed_entries(product_ids=None):
    """Recover current durable release records with absent or draft GitHub tags.

    Historical published versions are never rebuilt merely because they have
    a durable record. Only the registry's current version can be selected.
    """
    registry=load(ROOT/'catalog/packages.json')['packages']
    candidates=[]
    for record in registry:
        if product_ids is not None and record['id'] not in product_ids:continue
        path=ROOT/'catalog/releases'/record['id']/(record['version']+'.json')
        if not path.is_file():
            continue
        row=load(path)
        if row.get('product_id')!=record['id'] or row.get('version')!=record['version'] or row.get('git_tag')!=record['id']+'/v'+record['version']:
            raise ValueError('Current durable release record disagrees with registry: '+str(path))
        revision=run('git','log','-1','--format=%H','--',str(path.relative_to(ROOT)),cwd=ROOT).decode().strip()
        if len(revision)!=40:
            continue  # An uncommitted record is handled by pending_entries.
        candidates.append((record,row,revision))
    if not candidates:
        return []
    pages=list_releases(REPOSITORY)
    if not isinstance(pages,list) or any(not isinstance(page,list) for page in pages):
        raise ValueError('GitHub release listing was incomplete')
    by_tag={}
    for page in pages:
        for release in page:
            by_tag.setdefault(release['tag_name'],[]).append(release)
    unfinished=[]
    for record,row,revision in candidates:
        tag=row['git_tag'];matches=by_tag.get(tag,[])
        if len(matches)>1:
            raise ValueError('Duplicate GitHub release identity: '+tag)
        if matches and not matches[0]['draft']:
            continue
        if matches and matches[0].get('target_commitish')!=revision:
            raise ValueError('Draft source collision: '+tag)
        unfinished.append({'id':record['id'],'version':record['version'],
                           'changed_files':row['changed_files'],
                           'shared_sources':row.get('shared_sources',[])})
    return unfinished


def scoped_paths(entries):
    """Exact paths the completion command may stage for its own release."""
    paths={'catalog/packages.json','catalog/source-inventory.json',
           '.agents/plugins/marketplace.json','.claude-plugin/marketplace.json'}
    for entry in entries:
        ident,version=entry['id'],entry['version']
        if not ident or '/' in ident or not version or '/' in version:
            raise ValueError('Unsafe prepared release identity')
        base='plugins/'+ident+'/'
        for relative in entry['changed_files']:
            path=Path(relative)
            if path.is_absolute() or '..' in path.parts or not relative:
                raise ValueError('Unsafe changed file path: '+relative)
            paths.add(base+path.as_posix())
        for source in entry.get('shared_sources',[]):
            path=Path(source)
            if path.is_absolute() or '..' in path.parts or not source:
                raise ValueError('Unsafe shared source path: '+source)
            paths.add(path.as_posix())
        inventory=load(ROOT/'catalog/source-inventory.json') if (ROOT/'catalog/source-inventory.json').is_file() else {'packages':[]}
        reviewed=next((row['files'] for row in inventory['packages'] if row['id']==ident),{})
        paths.update(base+name for name in ('LICENSE-SCOPE.json','PUBLIC_FILE_MANIFEST.json') if name in reviewed)
        paths.update({base+'plugin.json',base+'.codex-plugin/plugin.json',
                      base+'.claude-plugin/plugin.json',base+'CHANGELOG.md',
                      base+'PROVENANCE.json',f'catalog/releases/{ident}/{version}.json'})
    return sorted(paths)


def commit_prepared(entries):
    if not entries:
        return None
    if run('git','diff','--cached','--name-only','-z',cwd=ROOT):
        raise ValueError('Unrelated staged changes exist; release completion will not include them')
    paths=scoped_paths(entries)
    command('git','add','-A','--',*paths)
    staged={p.decode() for p in run('git','diff','--cached','--name-only','-z',cwd=ROOT).split(b'\0') if p}
    if not staged:
        raise ValueError('Prepared release has no staged source or record changes')
    if not staged <= set(paths):
        raise ValueError('Staged paths escaped reviewed release scope')
    subject=('Release '+entries[0]['id']+' '+entries[0]['version'] if len(entries)==1
             else f'Release {len(entries)} Working Tools packages')
    command('git','commit','-m',subject)
    return run('git','rev-parse','HEAD',cwd=ROOT).decode().strip()


def validate_source_inventory(config, product_ids):
    """Always check the public snapshot; scope live source checks to releases."""
    args=[sys.executable,'-B','scripts/source_inventory.py']
    if product_ids:
        canonical=Path(config['canonical_root'])
        local_sync.approved_product_roots(ROOT,canonical,config.get('canonical_sources'),product_ids=product_ids)
        args.extend(('--canonical-root',str(canonical)))
        for ident in sorted(product_ids):
            args.extend(('--canonical-package',ident))
    command(*args)


def validate_committed(config, entries):
    """Finish local gates before any remote push."""
    if not entries:
        return
    command(sys.executable,'-B','scripts/packages.py','validate')
    validate_source_inventory(config,[entry['id'] for entry in entries])
    command(sys.executable,'-B','-m','unittest','discover','-s','tests','-v')
    manifests={}
    for entry in entries:
        path=f"catalog/releases/{entry['id']}/{entry['version']}.json"
        commit=run('git','log','-1','--format=%H','--',path,cwd=ROOT).decode().strip()
        if len(commit)!=40:
            raise ValueError('Release record must be committed before validation: '+path)
        if commit not in manifests:
            manifests[commit]=exact_commit_build(ROOT,commit,ROOT/'dist/release-manager'/commit)
        built={(row['id'],row['version']) for row in manifests[commit]['packages']}
        if (entry['id'],entry['version']) not in built:
            raise ValueError('Exact-commit build omitted a prepared package: '+path)


def _reviewed_shared_changes(config, changes):
    """Map explicitly shared source bytes into already reviewed package paths."""
    mapping=config.get('shared_shipped_paths',{})
    if not isinstance(mapping,dict):
        raise ValueError('shared_shipped_paths must map source paths to package destinations')
    inventory=load(ROOT/'catalog/source-inventory.json')
    rows={row['id']:row for row in inventory['packages']}
    selected=config.get('_packages')
    roots=local_sync.approved_product_roots(ROOT,config['canonical_root'],config.get('canonical_sources'),product_ids=selected)
    updates={}; sources={}
    for source_name,destinations in mapping.items():
        if not isinstance(source_name,str) or not source_name or not isinstance(destinations,list) or not destinations:
            raise ValueError('Invalid shared shipped path mapping')
        if selected is not None:
            destinations=[d for d in destinations if isinstance(d,str) and len(Path(d).parts)>=3 and Path(d).parts[1] in selected]
            if not destinations:continue
        source_rel=Path(source_name)
        if source_rel.is_absolute() or '..' in source_rel.parts or source_rel.as_posix()!=source_name:
            raise ValueError('Unsafe shared source path: '+source_name)
        source=ROOT/source_rel
        if source.is_symlink() or any(parent.is_symlink() for parent in source.parents if parent!=ROOT and ROOT in parent.parents):
            raise ValueError('Unsafe shared source: '+source_name)
        if not source.is_file():
            raise ValueError('Shared source is missing: '+source_name)
        data=source.read_bytes(); actual=hashlib.sha256(data).hexdigest()
        for destination in destinations:
            if not isinstance(destination,str) or not destination.startswith('plugins/'):
                raise ValueError('Shared destination must be a reviewed plugin path')
            parts=Path(destination).parts
            if len(parts)<3 or '..' in parts or parts[0]!='plugins':
                raise ValueError('Unsafe shared destination: '+destination)
            ident,relative=parts[1],Path(*parts[2:]).as_posix()
            row=rows.get(ident)
            if row is None or relative not in row['files']:
                raise ValueError('Shared destination is not in reviewed source inventory: '+destination)
            baseline=row['files'][relative]
            if actual==baseline:
                continue
            try:
                public=local_sync.safe_file(ROOT/'plugins'/ident,relative)
                canonical=local_sync.safe_file(roots[ident],relative)
            except ValueError as exc:
                raise ValueError('Unsafe or missing shared destination: '+destination) from exc
            if not public.is_file() or not canonical.is_file():
                raise ValueError('Unsafe or missing shared destination: '+destination)
            observed={hashlib.sha256(public.read_bytes()).hexdigest(),hashlib.sha256(canonical.read_bytes()).hexdigest()}
            if not observed <= {baseline,actual}:
                raise ValueError('Shared source conflicts with reviewed package edits: '+destination)
            existing=changes.get(ident,{}).get(relative)
            if existing and existing['sha256']!=actual:
                raise ValueError('Shared source conflicts with planned package edit: '+destination)
            changes.setdefault(ident,{})[relative]={'source':'shared','base':baseline,'sha256':actual}
            updates[(ident,relative)]=(source,data,actual)
            sources.setdefault(ident,set()).add(source_name)
    return updates,{ident:sorted(paths) for ident,paths in sources.items()}


def prepare(config):
    canonical=Path(config['canonical_root'])
    canonical_sources=config.get('canonical_sources')
    selected=config.get('_packages')
    changes,conflicts=local_sync.plan(ROOT,canonical,canonical_sources,product_ids=selected)
    if conflicts:raise ValueError('\n'.join(conflicts))
    shared_updates,shared_sources=_reviewed_shared_changes(config,changes)
    registry=load(ROOT/'catalog/packages.json');by_id={r['id']:r for r in registry['packages']}
    notes_root=ROOT/'catalog/changes'
    entries=[]
    for note_file in sorted(notes_root.glob('*.json')):
        ident=note_file.stem
        if selected is not None and ident not in selected:continue
        note=load(note_file)
        additions=note.get('reviewed_additions',[])
        if 'reviewed_additions' in note and (not isinstance(additions,list) or any(not isinstance(p,str) for p in additions)):
            raise ValueError(ident+': reviewed_additions must be a list of relative paths')
        if additions:
            if ident not in by_id:raise ValueError('Unknown reviewed addition product: '+ident)
            admitted=local_sync.reviewed_additions(ROOT,canonical,ident,additions,canonical_sources)
            changes.setdefault(ident,{}).update(admitted)
    # Preflight the whole affected batch before content or version writes.
    inventory=load(ROOT/'catalog/source-inventory.json')
    reviewed={row['id']:row for row in inventory['packages']}
    roots=local_sync.approved_product_roots(ROOT,canonical,canonical_sources,product_ids=changes)
    for ident in changes:
        if 'CHANGELOG.md' not in reviewed[ident]['files']:
            raise ValueError(ident+': CHANGELOG.md must be admitted to the reviewed source inventory before preparation')
        for base in (ROOT/'plugins'/ident,roots[ident]):
            if not local_sync.safe_file(base,'CHANGELOG.md').is_file():
                raise ValueError(ident+': reviewed CHANGELOG.md must exist in both public and canonical source before preparation')
    # Check every semantic change record before modifying a source.
    for ident,paths in changes.items():
        note_file=notes_root/(ident+'.json')
        if not note_file.is_file():raise ValueError(f'{ident}: authoring agent must supply catalog/changes/{ident}.json from the actual diff; see docs/release-management.md')
        note=load(note_file)
        for field in ('summary','why','compatibility','upgrade_guidance','validation','notes'):
            if not isinstance(note.get(field),str) or not note[field].strip():raise ValueError(f'{ident}: missing evidence-based {field}')
        actual=[{'status':change.get('status','modified'),'path':f'plugins/{ident}/{p}'} for p,change in paths.items()]
        version=propose_version(by_id[ident]['version'],actual,change_level=note.get('level'))
        entries.append((ident,version,note,paths,shared_sources.get(ident,[])))
    ordinary={ident:{rel:row for rel,row in paths.items() if row['source']!='shared'}
              for ident,paths in changes.items()}
    local_sync.apply_content(ROOT,canonical,ordinary,canonical_sources)
    for (ident,relative),(source,data,digest) in shared_updates.items():
        if hashlib.sha256(source.read_bytes()).hexdigest()!=digest:
            raise ValueError('Shared source changed during completion: '+str(source))
        local_sync.safe_file(ROOT/'plugins'/ident,relative).write_bytes(data)
    for ident,version,note,paths,shared in entries:
        notes=f"{note['summary']}\n\n{note['why']}\n\n{note['notes']}\n\nCompatibility: {note['compatibility']}\n\nUpgrade: {note['upgrade_guidance']}\n\nValidation: {note['validation']}"
        previous=by_id[ident]['version']
        generated=('LICENSE-SCOPE.json','PUBLIC_FILE_MANIFEST.json')
        before={name:(ROOT/'plugins'/ident/name).read_bytes() for name in generated if (ROOT/'plugins'/ident/name).is_file()}
        local_sync.refresh_reviewed(ROOT,canonical,ident,version,notes,approved_additions=note.get('reviewed_additions',[]),canonical_sources=canonical_sources)
        for name,data in before.items():
            if (ROOT/'plugins'/ident/name).read_bytes()!=data:paths.setdefault(name,{})
        save(ROOT/'catalog/releases'/ident/(version+'.json'),{
            'product_id':ident,'version':version,'previous_version':previous,
            'git_tag':ident+'/v'+version,'notes':notes,'summary':note['summary'],
            'compatibility':note['compatibility'],'upgrade_guidance':note['upgrade_guidance'],
            'changed_files':sorted(paths),'shared_sources':shared,'validation':note['validation']})
        (notes_root/(ident+'.json')).unlink()
    command(sys.executable,'-B','scripts/packages.py','catalog')
    command(sys.executable,'-B','scripts/packages.py','validate')
    validate_source_inventory(config,[ident for ident,_,_,_,_ in entries])
    return [{'id':i,'version':v,'changed_files':sorted(p),'shared_sources':s} for i,v,n,p,s in entries]


def publish_pending(config,receipt):
    registry=load(ROOT/'catalog/packages.json')['packages']
    by_id={row['id']:row for row in registry}
    published={(row['id'],row['version']):row for row in receipt.get('published',[])}
    manifests={}  # Invocation-local reuse; every product still passes its own release checks.
    for planned in receipt.get('changed',[]):
        record=by_id.get(planned['id'])
        if record is None or record['version']!=planned['version']:
            raise ValueError('Prepared release no longer matches registry: '+planned['id'])
        tag=record['id']+'/v'+record['version']
        entry_path=ROOT/'catalog/releases'/record['id']/(record['version']+'.json')
        if not entry_path.is_file():raise ValueError('Missing durable release record: '+tag)
        entry=load(entry_path)
        source=run('git','log','-1','--format=%H','--',str(entry_path.relative_to(ROOT)),cwd=ROOT).decode().strip()
        if len(source)!=40:raise ValueError('Release record must be committed before publishing')
        out=ROOT/'dist/release-manager'/source
        if source not in manifests:
            manifests[source]=exact_commit_build(ROOT,source,out)
        manifest=manifests[source]
        built=next(x for x in manifest['packages'] if x['id']==record['id'])
        if built['version']!=record['version']:raise ValueError('Release entry version not in selected source')
        archive=out/built['file'];files=out/(archive.stem+'.files.json')
        checksum=out/(archive.name+'.sha256');checksum.write_text(built['sha256']+'  '+archive.name+'\n')
        release=publish(REPOSITORY,{**record,'tag':tag},source,[archive,files,checksum],notes=entry['notes'])
        published[(record['id'],record['version'])]={'id':record['id'],'version':record['version'],
            'source_commit':source,'release_url':release['html_url'],'sha256':built['sha256'],
            'files':built['files'],'status':'published'}
        receipt['published']=sorted(published.values(),key=lambda row:(row['id'],row['version']))
        receipt['status']='releases_published'
        save(ROOT/'dist/release-manager/receipt.json',receipt)
    return receipt.get('published',[])


def external_plan(config):
    """Preflight every active guide owner before any plugin publication."""
    from release_manager.legacy import load_external_products, plan_active_external_updates
    ledger=ROOT/'catalog/external-products.json'
    document=load_external_products(ledger)
    checkouts=config.get('external_checkouts')
    if not isinstance(checkouts,dict):
        raise ValueError('Private release config must name external_checkouts for active guide owners')
    active={p['source']['id'] for p in document['products']
            if p['lifecycle'] in {'active-guide-download','active-guide-page'}}
    missing=active-set(checkouts)
    if missing:
        raise ValueError('Missing active guide source checkout: '+', '.join(sorted(missing)))
    plan=plan_active_external_updates(document,checkouts,ROOT/'catalog/external-changes')
    if plan['needs_notes']:
        names=', '.join(row['product_id'] for row in plan['needs_notes'])
        raise ValueError('Active guide changes need exact authored notes in catalog/external-changes: '+names)
    return plan,checkouts


def commit_external_ledger(receipt):
    """Persist a guide publisher's verified ledger before projecting the Site."""
    if run('git','diff','--cached','--name-only','-z',cwd=ROOT):
        raise ValueError('Unrelated staged changes exist before external ledger commit')
    command('git','add','--','catalog/external-products.json')
    staged={p.decode() for p in run('git','diff','--cached','--name-only','-z',cwd=ROOT).split(b'\0') if p}
    if staged not in (set(),{'catalog/external-products.json'}):
        raise ValueError('External ledger staging escaped its one-file scope')
    if staged:
        command('git','commit','-m','Record verified external guide release')
    # A previous run may have committed and failed before its push.
    command('git','push','origin','HEAD:main')
    receipt['external_pending_ledger']=False
    receipt['external_in_progress']=None
    receipt['status']='catalog_pending'
    save(ROOT/'dist/release-manager/receipt.json',receipt)


def publish_external(config,receipt,plan,checkouts):
    """Run existing guide publisher once per ready source, with a retry journal."""
    from release_manager.legacy import load_external_products
    if receipt.get('external_pending_ledger'):
        commit_external_ledger(receipt)
    for row in plan['ready']:
        ident=row['product_id'];source_id=next(p['source']['id'] for p in
            load_external_products(ROOT/'catalog/external-products.json')['products'] if p['id']==ident)
        receipt['external_in_progress']={'product_id':ident,'source_commit':row['source_commit']}
        receipt['status']='external_publishing'
        save(ROOT/'dist/release-manager/receipt.json',receipt)
        command(sys.executable,'-B','scripts/complete_external_update.py','--product',ident,
                '--checkout',str(checkouts[source_id]),'--notes-dir',str(ROOT/'catalog/external-changes'),
                '--publish')
        document=load_external_products(ROOT/'catalog/external-products.json')
        product=next(p for p in document['products'] if p['id']==ident)
        if product['source']['commit']!=row['source_commit']:
            raise ValueError('Guide publisher did not record verified source commit: '+ident)
        receipt.setdefault('external_published',[]).append({'product_id':ident,
            'source_commit':row['source_commit'],'distribution':product['disposition']})
        receipt['external_pending_ledger']=True
        save(ROOT/'dist/release-manager/receipt.json',receipt)
        commit_external_ledger(receipt)


def recover_external_ledger(receipt):
    """Finish a verified guide ledger write before checking later guide notes."""
    if receipt.get('external_pending_ledger'):
        commit_external_ledger(receipt)
        return
    progress=receipt.get('external_in_progress')
    if not progress:
        return
    from release_manager.legacy import load_external_products
    document=load_external_products(ROOT/'catalog/external-products.json')
    product=next((p for p in document['products'] if p['id']==progress['product_id']),None)
    if product and product['source']['commit']==progress['source_commit']:
        receipt['external_pending_ledger']=True
        save(ROOT/'dist/release-manager/receipt.json',receipt)
        commit_external_ledger(receipt)


def publish_integrations(receipt):
    """Complete registered integration packs through their exact-source owner."""
    if not (ROOT/'catalog/integrations.json').is_file():
        return
    from release_manager.packs import complete
    receipt['integration_in_progress']=True
    save(ROOT/'dist/release-manager/receipt.json',receipt)
    publications=complete(ROOT,ROOT/'catalog/integration-changes')
    if publications:
        saved={(row['id'],row['version'],row['source_commit']):row
               for row in receipt.get('integrations_published',[])}
        for row in publications:
            saved[(row['id'],row['version'],row['source_commit'])]=row
        receipt['integrations_published']=sorted(saved.values(),key=lambda row:(row['id'],row['version']))
        receipt['status']='catalog_pending'
    receipt['integration_in_progress']=False
    save(ROOT/'dist/release-manager/receipt.json',receipt)


def current_published_set(catalog):
    expected=[]
    for product in catalog['products']:
        if product.get('kind')=='external':
            continue
        key=product.get('current_release_key')
        if not key:
            raise ValueError('No verified current release for '+product['id'])
        matching=[row for row in product['releases'] if row['release_key']==key]
        if len(matching)!=1:
            raise ValueError('Current release key is ambiguous: '+key)
        release=matching[0]
        assets=[row for row in release['assets'] if row['role']=='installation']
        if len(assets)!=1:
            raise ValueError('Current release lacks one installation asset: '+key)
        expected.append({'release_key':key,'product_id':product['id'],
            'version':release['version'],'source_commit':release['source_commit'],
            'sha256':assets[0]['sha256']})
    required={row['id'] for row in load(ROOT/'catalog/packages.json')['packages']}
    integrations=ROOT/'catalog/integrations.json'
    if integrations.is_file():
        required.update(row['id'] for row in load(integrations)['products'])
    selected={row['product_id'] for row in expected}
    if selected!=required or len(expected)!=len(required):
        raise ValueError('Current release set differs from registered products: '
                         f'missing={sorted(required-selected)} unexpected={sorted(selected-required)}')
    return sorted(expected,key=lambda row:row['product_id'])


def sync_site(config,receipt):
    # A host adapter is an explicit argv array, never shell interpolation.
    adapter=config.get('site_adapter')
    if not isinstance(adapter,list) or not all(isinstance(x,str) for x in adapter) or not adapter:
        raise ValueError('Site adapter argv is required; releases remain published. Configure the existing host deployment route.')
    if run('git','status','--porcelain','--','catalog/external-products.json',cwd=ROOT):
        raise ValueError('External release ledger must be committed before Site projection')
    if (ROOT/'catalog/integrations.json').is_file() and run(
            'git','status','--porcelain','--','catalog/integrations.json',cwd=ROOT):
        raise ValueError('Integration release ledger must be committed before Site projection')
    command(sys.executable,'-B','scripts/sync_release_catalog.py')
    catalog_path=ROOT/'catalog/release-history.json'
    if not catalog_path.is_file():
        raise ValueError('Release history sync returned no durable catalog')
    if run('git','diff','--cached','--name-only','-z',cwd=ROOT):
        raise ValueError('Unrelated staged changes exist before catalog commit')
    command('git','add','--','catalog/release-history.json')
    staged={p.decode() for p in run('git','diff','--cached','--name-only','-z',cwd=ROOT).split(b'\0') if p}
    if staged not in (set(),{'catalog/release-history.json'}):
        raise ValueError('Catalog staging escaped its one-file scope')
    if staged:
        command('git','commit','-m','Refresh Working Tools release catalog')
        command('git','push','origin','HEAD:main')
    expected=current_published_set(load(catalog_path))
    expectation=ROOT/'dist/release-manager/site-expected.json'
    save(expectation,expected)
    receipt['expected_published_set']=expected
    catalog_digest=hashlib.sha256(catalog_path.read_bytes()).hexdigest()
    site_receipt=Path(config['site_receipt'])
    receipt['status']='catalog_pending';save(ROOT/'dist/release-manager/receipt.json',receipt)
    env={**os.environ,'WORKING_TOOLS_EXPECTED_RELEASES':str(expectation)}
    if config.get('_config_path'):
        env['WORKING_TOOLS_RELEASE_CONFIG']=config['_config_path']
    subprocess.run(adapter,cwd=ROOT,env=env,check=True)
    proof=load(site_receipt)
    if (proof.get('status')!='deployed' or not proof.get('deployment_id')
            or not proof.get('source_commit') or not proof.get('maintained_source_commit')
            or not proof.get('live_url') or not proof.get('version_id')):
        raise ValueError('Site adapter did not return verified deployment evidence')
    if proof.get('published_set')!=expected:
        raise ValueError('Site adapter receipt does not match the full current release set')
    if proof.get('catalog_sha256')!=catalog_digest:
        raise ValueError('Site adapter receipt does not match the prepared catalog bytes')
    receipt['catalog']=proof;receipt['status']='complete'
    return True


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config',type=Path,default=Path.home()/'.config/working-tools-release/config.json')
    mode=p.add_mutually_exclusive_group()
    mode.add_argument('--publish',action='store_true',help='Explicitly run release, publication and Site deployment')
    p.add_argument('--reconcile-only',action='store_true',help='Resume publication recovery; requires --publish')
    mode.add_argument('--prepare-only',action='store_true')
    mode.add_argument('--status',action='store_true',help='Refresh and display the local pending queue')
    p.add_argument('--json',action='store_true',help='Print the local pending journal as JSON')
    p.add_argument('--package',action='append',dest='packages',help='Release only this registered plugin; repeat for multiple plugins')
    a=p.parse_args()
    if a.reconcile_only and not a.publish:p.error('--reconcile-only requires explicit --publish')
    config=load(a.config);config['_config_path']=str(a.config.resolve())
    selected=sorted(set(a.packages)) if a.packages else None
    if selected is not None:
        registered={row['id'] for row in load(ROOT/'catalog/packages.json')['packages']}
        if unknown:=set(selected)-registered:raise ValueError('Unknown selected package: '+', '.join(sorted(unknown)))
        config['_packages']=selected
    state=ROOT/'dist/release-manager';state.mkdir(parents=True,exist_ok=True)
    with (state/'completion.lock').open('w') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise SystemExit('Another completion run owns publication; retry after its receipt settles.')
        if not (a.publish or a.prepare_only or a.reconcile_only):
            journal=pending.refresh(ROOT,config,selected)
            print(json.dumps(journal,indent=2) if a.json else pending.summary(journal))
            return
        if a.publish or a.reconcile_only:
            pending.read_previous(state/'pending.json')  # Corrupt local evidence must survive a failed release.
        receipt_path=state/'receipt.json'
        prior=load(receipt_path) if receipt_path.is_file() else None
        if prior and prior.get('status')=='complete' and prior.get('selected_packages')!=selected:
            prior=None  # Completed evidence remains on disk until a new receipt is saved.
        if prior and prior.get('status')!='complete':
            previous_scope=prior.get('selected_packages')
            if previous_scope!=selected or (selected is not None and (
                    any(row['id'] not in selected for row in prior.get('changed',[]))
                    or prior.get('external_in_progress') or prior.get('external_pending_ledger')
                    or prior.get('integration_in_progress'))):
                raise ValueError('In-progress completion receipt has incompatible package scope; resume its original scope first')
        if prior and not a.prepare_only and selected is None:
            recover_external_ledger(prior)
        resume_external=bool(prior and (prior.get('external_in_progress') or prior.get('external_pending_ledger')))
        external,external_checkouts=(external_plan(config) if selected is None and (not a.reconcile_only or resume_external)
                                    else (None,None))
        prepared=pending_entries(selected) if selected is not None else pending_entries()
        if prepared:
            receipt=prior if prior and prior.get('changed')==prepared else {'status':'preparing','changed':prepared,'published':[]}
        elif prior and prior.get('status') in {'preparing','releases_published','catalog_pending',
                                               'external_publishing'}:
            receipt=prior
        else:
            unfinished=unfinished_committed_entries(selected) if selected is not None else unfinished_committed_entries()
            if unfinished:
                receipt={'status':'preparing','changed':unfinished,'published':[]}
            elif a.reconcile_only:
                receipt=prior if prior else {'status':'catalog_pending','changed':[],'published':[]}
            else:
                changes=prepare(config)
                if changes:
                    prepared=pending_entries(selected) if selected is not None else pending_entries()
                    if sorted(prepared,key=lambda row:row['id'])!=sorted(changes,key=lambda row:row['id']):
                        raise ValueError('Freshly prepared release records differ from the reviewed change plan')
                receipt=({'status':'preparing','changed':changes,'published':[]}
                         if changes else prior if prior and prior.get('status')=='complete'
                         else {'status':'catalog_pending','changed':[],'published':[]})
        receipt['selected_packages']=selected
        if a.prepare_only:save(state/'receipt.json',receipt);print(json.dumps(receipt));return
        if prepared:
            receipt['source_commit']=commit_prepared(prepared)
            save(receipt_path,receipt)
        published_ids={(row['id'],row['version']) for row in receipt.get('published',[])}
        active_release=bool(receipt['changed']) and (
            receipt.get('status')=='preparing' or any(
                (row['id'],row['version']) not in published_ids for row in receipt['changed']))
        if active_release:
            if receipt.get('status')=='preparing':
                validate_committed(config,receipt['changed'])
            command('git','push','origin','HEAD:main')
            receipt['published']=publish_pending(config,receipt)
        if external is not None:
            publish_external(config,receipt,external,external_checkouts)
        if selected is None and (not a.reconcile_only or receipt.get('integration_in_progress')):
            publish_integrations(receipt)
        sync_site(config,receipt)
        save(state/'receipt.json',receipt)
        if receipt.get('status')=='complete':pending.refresh(ROOT,config,selected)
        print(json.dumps(receipt,indent=2))

if __name__=='__main__':
    try:main()
    except (ValueError,subprocess.CalledProcessError) as e:sys.exit(str(e))
