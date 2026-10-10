#!/usr/bin/env python3
"""Launch the bundled image workflow server with an explicitly prepared runtime."""
import os
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
def main():
    declared=os.environ.get('IMAGE_WORKFLOWS_PYTHON')
    interpreter=Path(declared).expanduser().absolute() if declared else ROOT/('.runtime/venv/Scripts/python.exe' if os.name=='nt' else '.runtime/venv/bin/python')
    if not interpreter.is_file() or not os.access(interpreter,os.X_OK):raise ValueError('Prepare the documented runtime or set IMAGE_WORKFLOWS_PYTHON to a suitable venv interpreter')
    server=ROOT/'runtime/image-workflows/server.py'
    os.execve(str(interpreter),[str(interpreter),str(server),*sys.argv[1:]],dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
if __name__=='__main__':
    try:main()
    except (OSError,ValueError) as exc:
        print(f'Image Workflows unavailable: {exc}',file=sys.stderr);raise SystemExit(1)
