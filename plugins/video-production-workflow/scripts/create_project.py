#!/usr/bin/env python3
from __future__ import annotations
import sys as _sys
from pathlib import Path as _BootstrapPath
_PLUGIN_ROOT = next((p for p in _BootstrapPath(__file__).resolve().parents if (p / "video_workflow").is_dir()), None)
if _PLUGIN_ROOT is not None and str(_PLUGIN_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_PLUGIN_ROOT))
import argparse, shutil
from pathlib import Path
from video_workflow.manifest import project_from_preset, save_project
p=argparse.ArgumentParser(); p.add_argument('directory'); p.add_argument('--id'); p.add_argument('--preset',default='landscape-1080'); a=p.parse_args(); root=Path(a.directory).resolve(); root.mkdir(parents=True,exist_ok=True)
for name in ('source','work','cache','output'): (root/name).mkdir(exist_ok=True)
project=project_from_preset(a.id or root.name,a.preset); save_project(project,root/'project.json')
(root/'project.md').write_text('# Project Decisions\n\n- Status: intake\n- Unresolved: purpose, audience, rights, runtime, design, accessibility, delivery.\n')
print(root)
