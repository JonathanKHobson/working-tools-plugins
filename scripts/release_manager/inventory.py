"""Read the distributable package file inventory from an exact Git commit."""

from __future__ import annotations

import hashlib
import subprocess
import tempfile
from pathlib import Path


def _git(repo, args, runner=None) -> bytes:
    if runner is not None:
        result = runner(args)
        return result.encode() if isinstance(result, str) else result
    return subprocess.check_output(['git', *args], cwd=repo)


def resolve_commit(repo, revision: str, *, runner=None) -> str:
    value = _git(repo, ['rev-parse', '--verify', f'{revision}^{{commit}}'], runner).decode().strip()
    if len(value) != 40 or any(c not in '0123456789abcdef' for c in value):
        raise ValueError(f'{revision}: did not resolve to a full commit')
    return value


def expected_package_files(repo, revision: str, product_id: str, *, runner=None) -> dict[str, str]:
    """SHA256 manifest for the same included paths as packages.py at a commit.

    This does not trust today's worktree or today's reviewed inventory for old tags.
    """
    commit = resolve_commit(repo, revision, runner=runner)
    prefix = f'plugins/{product_id}/'
    raw = _git(repo, ['ls-tree', '-r', '-z', commit, '--', prefix], runner)
    files = {}
    entries = []
    for entry in raw.split(b'\0'):
        if not entry:
            continue
        metadata, path = entry.split(b'\t', 1)
        mode, kind, oid = metadata.decode().split()
        name = path.decode('utf-8')
        if not name.startswith(prefix) or kind != 'blob' or mode not in {'100644', '100755'}:
            raise ValueError(f'unsupported release tree entry: {name}')
        relative = name[len(prefix):]
        parts = relative.split('/')
        if (not relative or any(part in {'.git', '.venv', '__pycache__', '.pytest_cache'} for part in parts)
                or parts[-1] == '.DS_Store' or parts[-1].endswith(('.pyc', '.pyo'))):
            continue
        entries.append((relative, oid))
    if runner is not None:
        for relative, oid in entries:
            files[relative] = hashlib.sha256(_git(repo, ['cat-file', 'blob', oid], runner)).hexdigest()
    elif entries:
        # One Git process for the complete tree, including binary contents.
        # On macOS/Python 3.9, simultaneous buffered pipe writes can deadlock
        # when Git fills stdout before consuming all input. A seekable input
        # file retains the single-process batch without two competing pipes.
        scratch = Path(repo) / 'dist'
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryFile(dir=scratch) as request:
            request.write(''.join(oid+'\n' for _,oid in entries).encode())
            request.seek(0)
            raw = subprocess.check_output(['git', 'cat-file', '--batch'], cwd=repo,
                                          stdin=request, timeout=120)
        offset=0
        for relative, oid in entries:
            end=raw.index(b'\n',offset)
            actual,kind,size=raw[offset:end].decode().split()
            if actual!=oid or kind!='blob':raise ValueError('Unexpected Git batch object')
            size=int(size);start=end+1;data=raw[start:start+size]
            if len(data)!=size or raw[start+size:start+size+1]!=b'\n':raise ValueError('Truncated Git batch object')
            files[relative]=hashlib.sha256(data).hexdigest();offset=start+size+1
        if offset!=len(raw):raise ValueError('Extra Git batch output')
    if not files:
        raise ValueError(f'{product_id}: no distributable files at {commit}')
    return dict(sorted(files.items()))
