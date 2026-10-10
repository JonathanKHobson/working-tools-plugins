#!/usr/bin/env python3
import sys as _sys
from pathlib import Path as _BootstrapPath
_PLUGIN_ROOT = next((p for p in _BootstrapPath(__file__).resolve().parents if (p / "video_workflow").is_dir()), None)
if _PLUGIN_ROOT is not None and str(_PLUGIN_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_PLUGIN_ROOT))
import argparse
from video_workflow.audio import analyze_music,save_music_analysis
p=argparse.ArgumentParser(); p.add_argument('input'); p.add_argument('--output',required=True); p.add_argument('--fallback',action='store_true'); a=p.parse_args(); save_music_analysis(analyze_music(a.input,use_librosa=not a.fallback),a.output)
