#!/usr/bin/env python3
import sys as _sys
from pathlib import Path as _BootstrapPath
_PLUGIN_ROOT = next((p for p in _BootstrapPath(__file__).resolve().parents if (p / "video_workflow").is_dir()), None)
if _PLUGIN_ROOT is not None and str(_PLUGIN_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_PLUGIN_ROOT))
import argparse,json
from pathlib import Path
from video_workflow.probe import probe_media
p=argparse.ArgumentParser(); p.add_argument('input'); p.add_argument('--output',required=True); a=p.parse_args(); Path(a.output).write_text(json.dumps(probe_media(a.input),indent=2)+'\n')
