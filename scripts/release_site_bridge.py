#!/usr/bin/env python3
"""Supported Sites host adapter for completion; no tokens or schedules stored.

A native Codex session supplies the authenticated Sites connector. The adapter
verifies the live generated catalog bytes after deployment before returning.
"""
from __future__ import annotations
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.request

from release_manager.catalog import SemVer
from release_manager.publisher import list_releases, resolved_tag

ROOT=Path(__file__).resolve().parents[1]
REPOSITORY='JonathanKHobson/working-tools-plugins'


def verify_promotion(expected, pages=None, tag_resolver=None):
    """Fail closed when a competing release has changed current selections."""
    pages=pages if pages is not None else list_releases(REPOSITORY)
    tag_resolver=tag_resolver or (lambda tag: resolved_tag(REPOSITORY,tag))
    rows=[r for page in pages for r in page]
    for wanted in expected:
        candidates=[]
        prefix=wanted['product_id']+'/v'
        for release in rows:
            if release.get('draft') or release.get('prerelease') or not release['tag_name'].startswith(prefix):continue
            version=release['tag_name'][len(prefix):]
            try:parsed=SemVer(version)
            except ValueError:continue
            if parsed.prerelease:continue
            assets=[a for a in release.get('assets',[]) if a['name']==wanted['product_id']+'-'+version+'.zip' and a.get('state')=='uploaded']
            if len(assets)==1:candidates.append((parsed,release,assets[0],version))
        if not candidates:raise ValueError('No complete published selection: '+wanted['product_id'])
        _,release,asset,version=max(candidates,key=lambda r:r[0])
        if version!=wanted['version'] or asset.get('digest')!='sha256:'+wanted['sha256']:
            raise ValueError('Catalog snapshot is stale: '+wanted['product_id'])
        if tag_resolver(release['tag_name'])!=wanted['source_commit']:
            raise ValueError('Release tag changed: '+wanted['product_id'])
    return True


def live_digest(url):
    request = urllib.request.Request(url.rstrip('/')+'/data/release-history.json',
        headers={'User-Agent': 'WorkingTools-ReleaseVerifier/1.0', 'Accept': 'application/json'})
    with urllib.request.urlopen(request,timeout=60) as response:
        return hashlib.sha256(response.read()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-promotion',type=Path)
    args=parser.parse_args()
    if args.check_promotion:
        request=json.loads(args.check_promotion.read_text())
        verify_promotion(request['published_set'])
        print(json.dumps({'status':'current','catalog_sha256':request['catalog_sha256']}));return
    config_path=Path(os.environ.get('WORKING_TOOLS_RELEASE_CONFIG',str(Path.home()/'.config/working-tools-release/config.json')))
    config=json.loads(config_path.read_text());site=Path(config['site_source'])
    expected_path=Path(os.environ['WORKING_TOOLS_EXPECTED_RELEASES'])
    expected=json.loads(expected_path.read_text())
    history=ROOT/'catalog/release-history.json'
    history_digest=hashlib.sha256(history.read_bytes()).hexdigest()
    receipt=Path(config['site_receipt'])
    work=ROOT/'dist/release-manager';work.mkdir(parents=True,exist_ok=True)
    request=work/'site-request.json'
    request.write_text(json.dumps({'site_source':str(site),'public_source':str(ROOT),
        'catalog_file':str(history),'catalog_sha256':history_digest,'sources_dir':config.get('site_sources_dir'),'expected_file':str(expected_path),
        'receipt_file':str(receipt),'published_set':expected,'promotion_check':[sys.executable,str(Path(__file__).resolve()),'--check-promotion',str(request)]},indent=2)+'\n')
    # Machine configuration deliberately stays outside public source.
    executable=config.get('codex_command') or shutil.which('codex')
    if not executable:raise SystemExit('Codex CLI unavailable: finish this exact site-request.json through the current Codex Sites connector, then retry.')
    prompt=f'''Complete ONLY the authorized Working Tools release catalog deployment described in {request}. The user has authorized publication of these exact public updates. Read the request, site AGENTS.md, docs/project-map.md and .openai/hosting.json. Do not start a new goal, delegate, schedule work, edit unrelated source or change site audience. Do not publish packages again.
Copy the supplied schema-validated release catalog to site data/release-history.json, run scripts/sync_plugin_registry.py against the public_source current commit, render static release pages, and run site validators. Preserve all existing components, useful URLs and historical downloads. Commit only these generated release/catalog changes (if any), fetch origin and ensure a fast-forward update without overwriting concurrent work. Push the verified maintained site source. Build using scripts/build_working_tools_site.py with an exact root revision and existing companion pins, using request.sources_dir for the companion checkouts when provided, or cloning the public repositories as needed. Keep generated Sites source separate.
Use the existing Sites connector: get_site, create_source_repository_write_credential, push exact prepared Sites source with credential kept private, save_site_version with a local tar archive, deploy_site_version, and get_deployment_status until succeeded. No unsupported HTTP endpoint or guessed credentials. Run the exact promotion_check argv from the request immediately before deploy_site_version to recheck canonical GitHub release state; if it has advanced beyond expected_file, stop with catalog_pending instead of rolling it back. Reconcile an already completed identical deployment before creating another version.
Verify the live /data/release-history.json SHA256 equals catalog_sha256 and all expected product/version/hash selections match it. Use User-Agent WorkingTools-ReleaseVerifier/1.0 and Accept application/json for public readback; the host rejects Python's default user agent. Write receipt_file JSON with status='deployed', deployment_id, source_commit (exact pushed Sites source), maintained_source_commit, catalog_sha256, published_set copied only after live match, live_url and saved version_id. If any capability/access is unavailable, write status='catalog_pending' with the precise dependency and do not claim success. Never log tokens. Return concise actual results.'''
    with (config_path.parent/'site-promotion.lock').open('w') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise SystemExit('Another Site promotion is active; retry synchronization after it settles.')
        verify_promotion(expected)
        if receipt.is_file():
            previous=json.loads(receipt.read_text())
            head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=site,text=True).strip()
            remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=site,text=True).split()[0]
            if (previous.get('status')=='deployed' and previous.get('catalog_sha256')==history_digest
                    and previous.get('published_set')==expected
                    and previous.get('maintained_source_commit')==head==remote
                    and not subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=site)
                    and live_digest(previous['live_url'])==history_digest):
                print(json.dumps({'status':'deployed','no_op':True,'deployment_id':previous['deployment_id']}));return
        result=subprocess.run([executable,'exec','--ephemeral','-m','gpt-6.1-sol','-c','model_reasoning_effort="high"','-s','danger-full-access','-c','approval_policy="never"','--color','never','-C',str(site),'-'],input=prompt,text=True)
        if result.returncode:raise SystemExit('Sites adapter failed; GitHub releases remain available. Retry --reconcile-only.')
        proof=json.loads(receipt.read_text())
        if proof.get('status')!='deployed' or proof.get('catalog_sha256')!=history_digest or proof.get('published_set')!=expected:
            raise SystemExit('Sites publication remains pending or its receipt mismatches intended catalog')
        if live_digest(proof['live_url'])!=history_digest:raise SystemExit('Live catalog differs from prepared input; retain partial completion')
        print(json.dumps({'status':'deployed','deployment_id':proof['deployment_id'],'catalog_sha256':history_digest}))
if __name__=='__main__':main()
