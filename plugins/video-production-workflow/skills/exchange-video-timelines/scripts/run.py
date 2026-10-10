#!/usr/bin/env python3
import sys as _sys
from pathlib import Path as _BootstrapPath
_PLUGIN_ROOT = next((p for p in _BootstrapPath(__file__).resolve().parents if (p / "video_workflow").is_dir()), None)
if _PLUGIN_ROOT is not None and str(_PLUGIN_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_PLUGIN_ROOT))
import argparse
from video_workflow.interchange import export_cmx3600,export_otio
p=argparse.ArgumentParser(); p.add_argument('manifest'); p.add_argument('--format',choices=['edl','otio'],required=True); p.add_argument('--output',required=True); a=p.parse_args(); (export_cmx3600 if a.format=='edl' else export_otio)(a.manifest,a.output)
