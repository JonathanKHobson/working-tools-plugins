#!/usr/bin/env python3
import sys as _sys
from pathlib import Path as _BootstrapPath
_PLUGIN_ROOT = next((p for p in _BootstrapPath(__file__).resolve().parents if (p / "video_workflow").is_dir()), None)
if _PLUGIN_ROOT is not None and str(_PLUGIN_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_PLUGIN_ROOT))
import argparse,json
from pathlib import Path
from video_workflow.captions import parse_srt,validate_cues,write_ass
p=argparse.ArgumentParser(); p.add_argument('srt'); p.add_argument('--ass',required=True); p.add_argument('--report',required=True); p.add_argument('--width',type=int,default=1920); p.add_argument('--height',type=int,default=1080); a=p.parse_args(); cues=parse_srt(a.srt); write_ass(cues,a.ass,width=a.width,height=a.height); Path(a.report).write_text(json.dumps({'cues':len(cues),'issues':validate_cues(cues)},indent=2)+'\n')
