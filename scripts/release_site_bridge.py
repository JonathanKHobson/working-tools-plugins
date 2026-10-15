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
import re
import shutil
import subprocess
import sys
import urllib.request

from release_manager.catalog import SemVer
from release_manager.publisher import list_releases, resolved_tag

ROOT=Path(__file__).resolve().parents[1]
REPOSITORY='JonathanKHobson/working-tools-plugins'
_SHA=re.compile(r'^[0-9a-f]{40}$')
_PUBLIC_HEADERS={'User-Agent': 'WorkingTools-ReleaseVerifier/1.0', 'Accept': 'application/json'}
STATIC_CONTRACT='static-dist-v1'
STATIC_PROJECTION='working-tools.static-release.v1'


def file_digest(path):
    result=hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda:source.read(1024*1024),b''):result.update(block)
    return result.hexdigest()


def catalog_owned_path(relative):
    return (relative in {'dist/data/release-history.json','dist/data/plugin-releases.json',
                         'dist/data/skill-downloads.json','dist/build-manifest.json',
                         'dist/sitemap.xml','dist/robots.txt'}
            or (relative.endswith('/index.html') and relative.startswith(('dist/plugins/','dist/releases/','dist/tools/'))))


def site_guard(site):
    from release_manager.local_sync import safe_file
    tracked=set(filter(None,subprocess.check_output(['git','ls-files','-z'],cwd=site,text=True).split('\0')))
    protected={relative:file_digest(safe_file(site,relative)) for relative in sorted(tracked) if not catalog_owned_path(relative)}
    headers={}
    for relative in sorted(tracked):
        if relative.startswith('dist/tools/') and relative.endswith('/index.html'):
            text=safe_file(site,relative).read_text()
            headers[relative]={}
            for kind in ('family','icons'):
                blocks=re.findall(rf'<!-- fc-{kind}:start -->.*?<!-- fc-{kind}:end -->',text,re.S)
                if len(blocks)!=1:raise ValueError('Guide has no unique accepted shared header/icon closure: '+relative)
                headers[relative][kind]=hashlib.sha256(blocks[0].encode()).hexdigest()
    return {'protected_files':protected,'guide_shared_blocks':headers}


def verify_site_guard(site,request):
    from release_manager.local_sync import safe_file
    guard=request.get('site_guard')
    if request.get('site_contract')!=STATIC_CONTRACT:return
    if not isinstance(guard,dict):raise ValueError('Static Site request lacks its preservation baseline')
    if Path(request['site_source']).resolve()!=Path(site).resolve():raise ValueError('Static Site guard targets another checkout')
    for relative,digest in guard['protected_files'].items():
        if file_digest(safe_file(site,relative))!=digest:raise ValueError('Protected Site file changed: '+relative)
    tracked=set(filter(None,subprocess.check_output(['git','ls-files','-z'],cwd=site,text=True).split('\0')))
    if any(not catalog_owned_path(path) and path not in guard['protected_files'] for path in tracked):
        raise ValueError('New Site source lies outside the catalog projection boundary')
    for relative,blocks in guard['guide_shared_blocks'].items():
        text=safe_file(site,relative).read_text()
        for kind,expected in blocks.items():
            actual=re.findall(rf'<!-- fc-{kind}:start -->.*?<!-- fc-{kind}:end -->',text,re.S)
            if len(actual)!=1 or hashlib.sha256(actual[0].encode()).hexdigest()!=expected:
                raise ValueError('Accepted guide header/icon changed: '+relative)


def static_projection(site):
    """Bind the indexed deployment closure without a self-referential commit hash.

    New generated paths must be staged first. The manifest is excluded from its
    own payload digest; its historical source_revisions retain their meaning.
    """
    from release_manager.local_sync import safe_file
    site=Path(site)
    hosting=json.loads(safe_file(site,'.openai/hosting.json').read_text())
    if hosting.get('static',{}).get('directory')!='dist' or not hosting.get('project_id'):
        raise ValueError('Static Site contract requires an existing dist Site identity')
    indexed=set(filter(None,subprocess.check_output(
        ['git','ls-files','--cached','-z','--','.openai/hosting.json','dist'],cwd=site,text=True).split('\0')))
    actual={'.openai/hosting.json'}
    actual.update(p.relative_to(site).as_posix() for p in (site/'dist').rglob('*')
                  if (p.is_file() or p.is_symlink()) and p.name!='.DS_Store' and not p.name.startswith('._'))
    indexed={p for p in indexed if Path(p).name!='.DS_Store' and not Path(p).name.startswith('._')}
    if indexed!=actual:raise ValueError('Static payload has missing or unstaged paths; stage only reviewed Site changes first')
    files={}
    for relative in sorted(actual):
        path=safe_file(site,relative)
        if not path.is_file():raise ValueError('Static payload is not a regular file: '+relative)
        if relative!='dist/build-manifest.json':files[relative]=file_digest(path)
    encoded=json.dumps(files,sort_keys=True,separators=(',',':')).encode()
    result={'schema_version':STATIC_PROJECTION,'project_id':hosting['project_id'],
            'payload_sha256':hashlib.sha256(encoded).hexdigest(),
            'catalog_sha256':files['dist/data/release-history.json'],
            'plugin_catalog_sha256':files['dist/data/plugin-releases.json']}
    if 'dist/data/skill-downloads.json' in files:
        result['skill_catalog_sha256']=files['dist/data/skill-downloads.json']
    return result


def stamp_static_site(site,request=None):
    if request is not None:verify_site_guard(site,request)
    projection=static_projection(site)
    path=Path(site)/'dist/build-manifest.json'
    manifest=json.loads(path.read_text())
    if not isinstance(manifest,dict):raise ValueError('Existing Site build manifest must be an object')
    manifest['release_projection']=projection
    path.write_text(json.dumps(manifest,indent=2)+'\n')
    return projection


def verify_request_inputs(request):
    for path_key,hash_key in (('catalog_file','catalog_sha256'),('skill_catalog_file','skill_catalog_sha256')):
        if request.get(path_key) and file_digest(request[path_key])!=request.get(hash_key):
            raise ValueError('Catalog input changed after preparation: '+path_key)
    if request.get('expected_file'):
        if json.loads(Path(request['expected_file']).read_text())!=request['published_set']:
            raise ValueError('Published selection changed after preparation')


def static_site_context(config,site):
    workspace=Path(config.get('site_workspace','')).resolve()
    if (not (workspace/'docs/project-map.md').is_file()
            or not (workspace/'tools/build_tool_introductions.py').is_file()
            or Path(site).resolve()!=(workspace/'work/sites/working-tools').resolve()):
        raise ValueError('Static Site workspace does not own the configured Working Tools checkout')
    hosting=json.loads((Path(site)/'.openai/hosting.json').read_text())
    if hosting.get('static',{}).get('directory')!='dist' or not hosting.get('project_id'):
        raise ValueError('Static Site contract requires the existing dist hosting identity')
    return {'workspace':str(workspace),'project_id':hosting['project_id'],
            'guide_build':[sys.executable,str(workspace/'tools/build_tool_introductions.py'),'--strict'],
            'guide_build_policy':'only-explicitly-reconciled-editorial; routine-download-updates-skip',
            'skill_links_helper':str(workspace/'tools/skill_download_links.py'),
            'inspect_command':[sys.executable,str(Path(__file__).resolve()),'--inspect-static-site',str(site)],
            'stamp_command':[sys.executable,str(Path(__file__).resolve()),'--stamp-static-site',str(site)]}


def static_site_source_matches(site,proof):
    expected=proof.get('maintained_source_commit')
    if (proof.get('site_contract')!=STATIC_CONTRACT or not isinstance(expected,str) or not _SHA.fullmatch(expected)
            or any(proof.get(key)!=expected for key in ('source_commit','remote_source_commit','sites_version_source_commit'))
            or not all(isinstance(proof.get(key),str) and proof[key] for key in ('live_url','version_id','deployment_id'))):
        return False
    if type(proof.get('no_op')) is not bool:return False
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=site,text=True).strip()
    if head!=expected or subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=site):return False
    local=static_projection(site)
    manifest=json.loads((Path(site)/'dist/build-manifest.json').read_text())
    if (proof.get('project_id')!=local['project_id'] or proof.get('static_projection')!=local
            or proof.get('catalog_sha256')!=local['catalog_sha256']
            or proof.get('skill_catalog_sha256')!=local.get('skill_catalog_sha256')
            or proof['live_url'].rstrip('/')!=str(manifest.get('site_origin','')).rstrip('/')
            or not proof.get('audience_before') or proof.get('audience_before')!=proof.get('audience_after')
            or type(proof.get('access_revision_before')) is not int
            or proof.get('access_revision_before')!=proof.get('access_revision_after')):return False
    request=urllib.request.Request(proof['live_url'].rstrip('/')+'/build-manifest.json',headers=_PUBLIC_HEADERS)
    with urllib.request.urlopen(request,timeout=60) as response:live=json.load(response)
    return isinstance(live,dict) and live.get('release_projection')==local


def static_site_prompt(request_path):
    return f'''Complete ONLY the authorized current Working Tools catalog promotion in {request_path}. Read its metadata (use Python to omit the large site_guard from context; the helper verifies those hashes), its static_context.workspace/docs/project-map.md and current .openai/hosting.json. The configured site_source is the maintained Sites Git checkout; its tracked dist is already the redesigned Site. Do not build from a legacy source repository, run scripts/build_working_tools_site.py or tools/rebuild_working_tools.py, clone companion sites, change audience, publish packages, delegate, schedule work or create a new goal.
First use the native Sites connector and short-lived source credential to reconcile the current saved version and authenticated remote branch. Preserve newer compatible UI source by a clean fast-forward only. Stop with catalog_pending on local edits, conflicting source, missing capability or an unrelated writer; never overwrite them. Recheck current Site identity against static_context.project_id.
BEFORE ANY WRITE, evaluate a verification-only no-op. Read the prior receipt and run static_context.inspect_command against the clean local Site. If its static contract/project, current clean local commit, authenticated remote HEAD, current Sites saved-version source commit, live release_projection, both exact live catalog hashes and requested published_set ALL match, run promotion_check and reuse that exact current version/deployment. Refresh the receipt with verified current metadata and no_op=true, then return without projection, generation, staging, stamping, committing, pushing, saving or deploying. Missing old static evidence means this shortcut is unavailable, not permission to fabricate it. If publication is needed, continue below and set no_op=false in the final receipt.
Project the schema-validated catalog_file into dist/data/release-history.json and skill_catalog_file into dist/data/skill-downloads.json byte-for-byte. Derive plugin registry metadata from the exact public_source commit and its published release selections, preserving current storefront-copy fields, family ordering and private exclusions. Stage technical product/version metadata updates against the CURRENT Site shell: preserve existing authored copy, headers, favicon bindings, CSS/JS, assets, catalog index, Library donor and historical URLs/downloads. Consult the existing projection functions and current workspace generators rather than substituting a legacy whole-site output tree. Retain every historical release.
Routine download updates MUST SKIP guide_build. A version-only, reference or script update to an existing skill does not require editing its authored guide JSON or regenerating the guide. Keep the guide's explicitly labeled review version and source commit truthful even when older than the latest downloadable bundle. Never relabel old guide copy as newly reviewed or force metadata reconciliation merely to refresh a download. Independently update the generated latest-download block/version from skill_catalog_file on each existing skill page, and update technical/catalog release metadata separately.
Only run the optional strict guide_build when explicitly supplied editorial sources have actually been reconciled and reviewed for the new release. A package/guide version difference alone is not catalog_pending for an otherwise covered existing skill. New or removed skills, missing routes, or incompatible skill identities must report exact coverage gaps as catalog_pending; do not fabricate guide content or silently omit them. Run skill_links_helper using its documented CLI against existing pages after catalog projection (and after guide generation only when that optional reviewed step applies). It owns generated per-skill links; do not hand-maintain them or silently skip a missing helper. Check its supported arguments rather than guessing.
Before committing, verify the exact changed-path set, rendered changed anchors, current source links, internal links, copy controls and all protected UI/assets against the clean starting tree. Keep the staging and output scope bounded. Stage only reviewed generated/source changes, then run static_context.stamp_command; it adds release_projection to the existing build-manifest without relabeling historical source_revisions. Stage that manifest and commit the exact accepted Site tree. Push only fast-forward to the existing Sites repository, with credentials private. Package .openai/hosting.json plus its declared static dist from that exact pushed source. Do not push a legacy maintained repository or use a second generated Site checkout.
The request and its site_guard are immutable receiving evidence. Do not rewrite their baseline or broaden catalog_owned_path to make a failing projection pass. The stamp and promotion check enforce protected-file and guide-header preservation; stop with catalog_pending on a mismatch.
Use get_site, save_site_version with the local archive, deploy_site_version and get_deployment_status until succeeded; obtain credentials with create_source_repository_write_credential. Run the exact promotion_check argv immediately BEFORE deploy to catch newer GitHub selections or changed catalog inputs. Preserve the existing audience. A receipt alone is not a no-op: re-read the current Sites saved version/source and authenticated remote even if prior catalog hashes match. Reuse a deployment only if current Site source, remote source, complete static projection, catalog and skill catalog all match.
After success, refresh get_site/get_site_version and verify saved-version source.commit_sha and authenticated remote HEAD equal the exact clean local pushed commit. Read back /data/release-history.json and /data/skill-downloads.json as exact bytes and /build-manifest.json release_projection as the exact stamped object, using User-Agent WorkingTools-ReleaseVerifier/1.0 and Accept application/json. Check newly changed links and actual rendered states on production. The old source_revisions.compass-suite is historical upstream provenance, NOT the current Site source commit.
Only after all checks write receipt_file with status=deployed, site_contract=static-dist-v1, project_id, deployment_id, version_id, live_url, source_commit, maintained_source_commit, remote_source_commit and sites_version_source_commit (all four commit fields equal the authenticated pushed Site commit), catalog_sha256, skill_catalog_sha256, static_projection, audience_before, audience_after, access_revision_before, access_revision_after and published_set. Audience and access revision must be unchanged between the initial and final get_site reads. On any unmet condition write catalog_pending with its precise dependency. Never log tokens. Return concise actual results.'''


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


def live_digest(url,name='release-history.json'):
    if name not in {'release-history.json','skill-downloads.json'}:raise ValueError('Unsupported catalog readback')
    request = urllib.request.Request(url.rstrip('/')+'/data/'+name,
        headers=_PUBLIC_HEADERS)
    with urllib.request.urlopen(request,timeout=60) as response:
        return hashlib.sha256(response.read()).hexdigest()


def live_source_revision(url):
    """Read the root source revision actually rendered by the public Site."""
    request=urllib.request.Request(url.rstrip('/')+'/build-manifest.json',headers=_PUBLIC_HEADERS)
    with urllib.request.urlopen(request,timeout=60) as response:
        manifest=json.load(response)
    revisions=manifest.get('source_revisions') if isinstance(manifest,dict) else None
    revision=revisions.get('compass-suite') if isinstance(revisions,dict) else None
    if not isinstance(revision,str) or not _SHA.fullmatch(revision):
        raise ValueError('Live build manifest lacks an exact compass-suite source revision')
    return revision


def site_source_matches(site,proof,contract=None):
    """Only reuse or accept a deployment bound to this clean maintained tree."""
    if contract==STATIC_CONTRACT or proof.get('site_contract')==STATIC_CONTRACT:
        return static_site_source_matches(site,proof)
    expected=proof.get('maintained_source_commit')
    url=proof.get('live_url')
    if not isinstance(expected,str) or not _SHA.fullmatch(expected) or not isinstance(url,str) or not url:
        return False
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=site,text=True).strip()
    remote_output=subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=site,text=True).split()
    if len(remote_output)!=2 or remote_output[1]!='refs/heads/main':
        raise ValueError('Cannot resolve maintained Site origin/main')
    remote=remote_output[0]
    dirty=subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=site)
    if head!=expected or remote!=expected or dirty:
        return False
    return live_source_revision(url)==expected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-promotion',type=Path)
    parser.add_argument('--stamp-static-site',type=Path)
    parser.add_argument('--inspect-static-site',type=Path)
    parser.add_argument('--site-request',type=Path)
    args=parser.parse_args()
    if args.inspect_static_site:
        print(json.dumps(static_projection(args.inspect_static_site)));return
    if args.stamp_static_site:
        if not args.site_request:parser.error('--stamp-static-site requires the immutable --site-request')
        request=json.loads(args.site_request.read_text());verify_request_inputs(request)
        print(json.dumps(stamp_static_site(args.stamp_static_site,request)));return
    if args.check_promotion:
        request=json.loads(args.check_promotion.read_text())
        verify_request_inputs(request)
        verify_site_guard(Path(request['site_source']),request) if request.get('site_contract')==STATIC_CONTRACT else None
        verify_promotion(request['published_set'])
        print(json.dumps({'status':'current','catalog_sha256':request['catalog_sha256']}));return
    config_path=Path(os.environ.get('WORKING_TOOLS_RELEASE_CONFIG',str(Path.home()/'.config/working-tools-release/config.json')))
    config=json.loads(config_path.read_text());site=Path(config['site_source'])
    contract=config.get('site_contract','legacy-pins-v1')
    if contract not in ('legacy-pins-v1',STATIC_CONTRACT):raise ValueError('Unknown Site contract')
    static_context=static_site_context(config,site) if contract==STATIC_CONTRACT else None
    expected_path=Path(os.environ['WORKING_TOOLS_EXPECTED_RELEASES'])
    expected=json.loads(expected_path.read_text())
    history=ROOT/'catalog/release-history.json'
    history_digest=hashlib.sha256(history.read_bytes()).hexdigest()
    skills=ROOT/'catalog/skill-downloads.json'
    if contract==STATIC_CONTRACT and not skills.is_file():raise SystemExit('catalog_pending: generated skill catalog is missing')
    skill_digest=file_digest(skills) if skills.is_file() else None
    receipt=Path(config['site_receipt'])
    work=ROOT/'dist/release-manager';work.mkdir(parents=True,exist_ok=True)
    request=work/'site-request.json'
    if static_context:static_context['stamp_command'].extend(['--site-request',str(request)])
    request.write_text(json.dumps({'site_source':str(site),'public_source':str(ROOT),
        'catalog_file':str(history),'catalog_sha256':history_digest,'sources_dir':config.get('site_sources_dir') if not static_context else None,'expected_file':str(expected_path),
        'site_contract':contract,'static_context':static_context,
        'site_guard':site_guard(site) if static_context else None,
        'skill_catalog_file':str(skills) if skill_digest else None,'skill_catalog_sha256':skill_digest,
        'receipt_file':str(receipt),'published_set':expected,'promotion_check':[sys.executable,str(Path(__file__).resolve()),'--check-promotion',str(request)]},indent=2)+'\n')
    # Machine configuration deliberately stays outside public source.
    executable=config.get('codex_command') or shutil.which('codex')
    if not executable:raise SystemExit('Codex CLI unavailable: finish this exact site-request.json through the current Codex Sites connector, then retry.')
    prompt=f'''Complete ONLY the authorized Working Tools release catalog deployment described in {request}. The user has authorized publication of these exact public updates. Read the request, site AGENTS.md, docs/project-map.md and .openai/hosting.json. Do not start a new goal, delegate, schedule work, edit unrelated source or change site audience. Do not publish packages again.
Copy the supplied schema-validated release catalog to site data/release-history.json, run scripts/sync_plugin_registry.py against the public_source current commit, render static release pages, and run site validators. Preserve all existing components, useful URLs and historical downloads. Commit only these generated release/catalog changes (if any), fetch origin and ensure a fast-forward update without overwriting concurrent work. Push the verified maintained site source. Build using scripts/build_working_tools_site.py with an exact root revision and existing companion pins, using request.sources_dir for the companion checkouts when provided, or cloning the public repositories as needed. Keep generated Sites source separate.
Use the existing Sites connector: get_site, create_source_repository_write_credential, push exact prepared Sites source with credential kept private, save_site_version with a local tar archive, deploy_site_version, and get_deployment_status until succeeded. No unsupported HTTP endpoint or guessed credentials. Run the exact promotion_check argv from the request immediately before deploy_site_version to recheck canonical GitHub release state; if it has advanced beyond expected_file, stop with catalog_pending instead of rolling it back. Reconcile an already completed identical deployment only when both the catalog and maintained source commit match; a newer UI source needs a new deployment even with the same catalog.
Verify the live /data/release-history.json SHA256 equals catalog_sha256, all expected product/version/hash selections match it, and live /build-manifest.json source_revisions['compass-suite'] equals the exact clean maintained Site commit pushed to origin/main. Use User-Agent WorkingTools-ReleaseVerifier/1.0 and Accept application/json for public readback; the host rejects Python's default user agent. Write receipt_file JSON with status='deployed', deployment_id, source_commit (exact pushed Sites source), maintained_source_commit, catalog_sha256, published_set copied only after live matches, live_url and saved version_id. If any capability/access is unavailable, write status='catalog_pending' with the precise dependency and do not claim success. Never log tokens. Return concise actual results.'''
    if static_context:prompt=static_site_prompt(request)
    def catalogs_match(proof):
        return (live_digest(proof['live_url'])==history_digest
                and (not skill_digest or (proof.get('skill_catalog_sha256')==skill_digest
                     and live_digest(proof['live_url'],'skill-downloads.json')==skill_digest)))
    with (config_path.parent/'site-promotion.lock').open('w') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise SystemExit('Another Site promotion is active; retry synchronization after it settles.')
        verify_promotion(expected)
        verify_request_inputs(json.loads(request.read_text()))
        if receipt.is_file() and not static_context:
            previous=json.loads(receipt.read_text())
            if (previous.get('status')=='deployed' and previous.get('catalog_sha256')==history_digest
                    and previous.get('published_set')==expected
                    and site_source_matches(site,previous)
                    and catalogs_match(previous)):
                print(json.dumps({'status':'deployed','no_op':True,'deployment_id':previous['deployment_id']}));return
        result=subprocess.run([executable,'exec','--ephemeral','-m','gpt-6.1-sol','-c','model_reasoning_effort="high"','-s','danger-full-access','-c','approval_policy="never"','--color','never','-C',str(site),'-'],input=prompt,text=True)
        if result.returncode:raise SystemExit('Sites adapter failed; GitHub releases remain available. Retry --reconcile-only.')
        proof=json.loads(receipt.read_text())
        if proof.get('status')!='deployed' or proof.get('catalog_sha256')!=history_digest or proof.get('published_set')!=expected:
            raise SystemExit('Sites publication remains pending or its receipt mismatches intended catalog')
        if static_context:verify_site_guard(site,json.loads(request.read_text()))
        if not catalogs_match(proof):raise SystemExit('Live catalog differs from prepared input; retain partial completion')
        if not site_source_matches(site,proof,contract):raise SystemExit('Live Site build or maintained source differs from deployed receipt; retain partial completion')
        print(json.dumps({'status':'deployed','deployment_id':proof['deployment_id'],'catalog_sha256':history_digest,
                          **({'no_op':proof.get('no_op') is True} if static_context else {})}))
if __name__=='__main__':main()
