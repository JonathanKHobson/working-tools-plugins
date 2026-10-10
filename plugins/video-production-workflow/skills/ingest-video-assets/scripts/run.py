#!/usr/bin/env python3
import sys as _sys
from pathlib import Path as _BootstrapPath
_PLUGIN_ROOT = next((p for p in _BootstrapPath(__file__).resolve().parents if (p / "video_workflow").is_dir()), None)
if _PLUGIN_ROOT is not None and str(_PLUGIN_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_PLUGIN_ROOT))
import argparse,json,hashlib
from pathlib import Path
from video_workflow.probe import probe_media
p=argparse.ArgumentParser(); p.add_argument('inputs',nargs='+'); p.add_argument('--output',required=True); a=p.parse_args(); out=[]
for raw in a.inputs:
 q=Path(raw).resolve(); h=hashlib.sha256(q.read_bytes()).hexdigest(); item={'path':str(q),'sha256':h,'bytes':q.stat().st_size}
 try: item['probe']=probe_media(q)
 except Exception as e: item['probe_error']=str(e)
 out.append(item)
Path(a.output).write_text(json.dumps({'assets':out},indent=2)+'\n')
