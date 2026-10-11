"""Publish exact-commit packages through resumable drafts, never replace assets."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from urllib.parse import quote


def run(*args, cwd=None, input=None):
    return subprocess.check_output(list(args), cwd=cwd, input=input, stderr=subprocess.PIPE)


def api(repo, path='', method='GET', body=None):
    args=['gh','api',f'repos/{repo}/{path}','--method',method]
    if body is not None:
        args += ['--input','-']
    raw=run(*args,input=json.dumps(body).encode() if body is not None else None)
    return json.loads(raw) if raw.strip() else None


def list_releases(repo):
    return json.loads(run('gh','api','--paginate','--slurp',f'repos/{repo}/releases?per_page=100'))


def resolved_tag(repo, tag):
    value=api(repo,'git/ref/tags/'+quote(tag,safe='/'))['object']
    for _ in range(8):
        if value['type']=='commit': return value['sha']
        if value['type']!='tag': break
        value=api(repo,'git/tags/'+value['sha'])['object']
    raise ValueError('Tag does not resolve to a commit: '+tag)


def _assert_assets(release, expected):
    actual={a['name']:a for a in release['assets']}
    if set(actual) != {row[0] for row in expected}:
        raise ValueError('Release asset inventory differs from intended asset set')
    for name,digest,size in expected:
        a=actual.get(name)
        if not a or a.get('state')!='uploaded' or a['size']!=size:
            raise ValueError('Incomplete release asset: '+name)
        # Downloaded bytes are acceptance evidence, including on a retry.
        raw=run('gh','api','-H','Accept: application/octet-stream',a['url'])
        if len(raw)!=size or hashlib.sha256(raw).hexdigest()!=digest:
            raise ValueError('Immutable asset collision: '+name)


def publish(repo, record, source_commit, paths, *, notes, title=None):
    """Recognize completed releases or resume an incomplete draft at exact SHA."""
    tag=record.get('git_tag',record.get('tag'))
    if not tag or len(source_commit)!=40: raise ValueError('Exact tag and 40-character commit required')
    all_releases=[r for page in list_releases(repo) for r in page]
    matches=[r for r in all_releases if r['tag_name']==tag]
    if len(matches)>1: raise ValueError('Duplicate release identity')
    expected=[(p.name,hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size) for p in paths]
    if len({r[0] for r in expected})!=len(expected):raise ValueError('Duplicate upload name')
    if matches:
        release=matches[0]
        if not release['draft']:
            if resolved_tag(repo,tag)!=source_commit:raise ValueError('Published tag collision: '+tag)
            _assert_assets(release,expected)
            return release
        if release.get('target_commitish')!=source_commit:
            raise ValueError('Draft targets another commit: '+tag)
    else:
        # Check an already-existing tag before creation; only 404 permits no tag.
        try:
            if resolved_tag(repo,tag)!=source_commit:raise ValueError('Tag collision: '+tag)
        except subprocess.CalledProcessError as e:
            if b'404' not in e.stderr: raise
        release=api(repo,'releases','POST',{'tag_name':tag,'target_commitish':source_commit,
            'name':title or f"{record['id']} {record['version']}",'body':notes,
            'draft':True,'prerelease':'-' in record['version'].split('+')[0],'make_latest':'false'})
    actual={a['name']:a for a in release['assets']}
    for p,(_,digest,size) in zip(paths,expected):
        if p.name in actual:
            _assert_assets({**release,'assets':[actual[p.name]]},[(p.name,digest,size)])
        else:
            run('gh','release','upload',tag,str(p),'--repo',repo)
    release=api(repo,'releases/'+str(release['id']))
    _assert_assets(release,expected)
    release=api(repo,'releases/'+str(release['id']),'PATCH',{'draft':False,'make_latest':'false','body':notes})
    if resolved_tag(repo,tag)!=source_commit:raise ValueError('Published tag/source mismatch')
    _assert_assets(release,expected)
    return release


def exact_commit_build(checkout, commit, output):
    """Execute this repository's reviewed packager in an isolated committed tree."""
    checkout=Path(checkout); output=Path(output).resolve(); output.mkdir(parents=True,exist_ok=True)
    resolved=run('git','rev-parse',commit+'^{commit}',cwd=checkout).decode().strip()
    if commit!=resolved:raise ValueError('Build requires a full exact commit SHA')
    # A local detached checkout leaves current authoring files untouched.
    with tempfile.TemporaryDirectory(prefix='release-commit-',dir=output.parent) as tmp:
        root=Path(tmp)/'source'
        run('git','clone','--quiet','--no-hardlinks','--no-checkout',str(checkout),str(root))
        run('git','checkout','--quiet','--detach',commit,cwd=root)
        run('python3','-B','scripts/packages.py','release','--output',str(output),cwd=root)
    manifest=json.loads((output/'source-release-manifest.json').read_text())
    if manifest['assembly_commit']!=commit or manifest['assembly_worktree_dirty']:
        raise ValueError('Build receipt not bound to clean release commit')
    return manifest
