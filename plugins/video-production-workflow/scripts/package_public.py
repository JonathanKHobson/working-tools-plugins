#!/usr/bin/env python3
"""Package only the frozen reviewed public allowlist, never local test receipts."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import tempfile
import stat
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    output=args.output.resolve()
    if output.exists() or Path(str(output)+'.sha256').exists():
        parser.error('Output or checksum already exists; choose a new output path')
    manifest_path=ROOT/'PUBLIC_FILE_MANIFEST.json'
    manifest=json.loads(manifest_path.read_text())
    files=[];seen=set()
    for record in manifest['files']:
        rel=Path(record['path'])
        if rel.is_absolute() or '..' in rel.parts or rel.as_posix() in seen:
            parser.error(f'Invalid or duplicate allowlist path: {rel}')
        seen.add(rel.as_posix());path=ROOT/rel
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent!=ROOT.parent):
            parser.error(f'Symlink is forbidden: {rel}')
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=record['sha256']:
            parser.error(f'Reviewed file missing or changed: {rel}')
        files.append((rel,path))
    files.append((Path('PUBLIC_FILE_MANIFEST.json'),manifest_path))
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent,prefix='.video-package-',delete=False) as handle:
        temporary=Path(handle.name)
    try:
        with ZipFile(temporary,'w',compression=ZIP_DEFLATED,compresslevel=9) as archive:
            for rel,path in sorted(files):
                info=ZipInfo('video-production-workflow/'+rel.as_posix(),date_time=(2026,10,10,0,0,0))
                info.external_attr=(stat.S_IMODE(path.stat().st_mode)&0xFFFF)<<16
                info.compress_type=ZIP_DEFLATED
                archive.writestr(info,path.read_bytes())
        # link is atomic and refuses to overwrite a raced destination.
        os.link(temporary,output)
    finally:
        temporary.unlink(missing_ok=True)
    digest=hashlib.sha256(output.read_bytes()).hexdigest()
    with Path(str(output)+'.sha256').open('x') as handle:
        handle.write(f'{digest}  {output.name}\n')
    print(json.dumps({'output':str(output),'sha256':digest,'files':len(files)},indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
