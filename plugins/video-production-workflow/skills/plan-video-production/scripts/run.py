#!/usr/bin/env python3
import sys as _sys
from pathlib import Path as _BootstrapPath
_PLUGIN_ROOT = next((p for p in _BootstrapPath(__file__).resolve().parents if (p / "video_workflow").is_dir()), None)
if _PLUGIN_ROOT is not None and str(_PLUGIN_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_PLUGIN_ROOT))
import argparse
from video_workflow.manifest import project_from_preset, save_project
p=argparse.ArgumentParser(); p.add_argument('output'); p.add_argument('--id',default='video-project'); p.add_argument('--preset',default='landscape-1080'); a=p.parse_args(); save_project(project_from_preset(a.id,a.preset),a.output)
