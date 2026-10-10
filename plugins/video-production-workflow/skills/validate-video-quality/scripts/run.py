#!/usr/bin/env python3
import sys as _sys
from pathlib import Path as _BootstrapPath
_PLUGIN_ROOT = next((p for p in _BootstrapPath(__file__).resolve().parents if (p / "video_workflow").is_dir()), None)
if _PLUGIN_ROOT is not None and str(_PLUGIN_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_PLUGIN_ROOT))
import argparse,json
from pathlib import Path
from video_workflow.qa import validate_video
p=argparse.ArgumentParser(); p.add_argument('input'); p.add_argument('--output',required=True); p.add_argument('--width',type=int); p.add_argument('--height',type=int); p.add_argument('--duration',type=float); p.add_argument('--deep',action='store_true'); a=p.parse_args(); report=validate_video(a.input,expected_width=a.width,expected_height=a.height,expected_duration=a.duration,deep=a.deep); Path(a.output).write_text(json.dumps(report,indent=2)+'\n'); raise SystemExit(0 if report['passed'] else 2)
