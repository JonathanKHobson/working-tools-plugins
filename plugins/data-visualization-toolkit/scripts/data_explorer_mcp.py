#!/usr/bin/env python3
"""Launch the bundled Data Explorer using an explicitly prepared runtime."""
import os
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
def main():
    if len(sys.argv)!=1:raise ValueError("This launcher accepts no arguments")
    declared=os.environ.get("DATA_EXPLORER_PYTHON")
    # Resolving a venv executable symlink would discard its site-packages environment.
    interpreter=Path(declared).expanduser().absolute() if declared else ROOT/(".runtime/venv/Scripts/python.exe" if os.name=="nt" else ".runtime/venv/bin/python")
    if not interpreter.is_file() or not os.access(interpreter,os.X_OK):raise ValueError("Prepare the Python runtime as documented in docs/installation.md; set DATA_EXPLORER_PYTHON for an external venv")
    state=Path(os.environ.get("DATA_EXPLORER_DATA_DIR",str(Path(os.environ.get("XDG_DATA_HOME",str(Path.home()/".local/share")))/"working-tools/data-explorer"))).expanduser().resolve()
    server=ROOT/"runtime/data-explorer/server.py"
    os.execve(str(interpreter),[str(interpreter),str(server),"--data-dir",str(state),"--stdio"],dict(os.environ,PYTHONDONTWRITEBYTECODE="1"))
if __name__=="__main__":
    try:main()
    except (OSError,ValueError) as exc:
        print(f"Data Explorer unavailable: {exc}",file=sys.stderr);raise SystemExit(1)
