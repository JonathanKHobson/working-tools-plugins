#!/usr/bin/env python3
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--music'); p.add_argument('--voiceover'); p.add_argument('--output',required=True); p.add_argument('--target-lufs',type=float,default=-16); a=p.parse_args(); cfg={'music':{'asset':a.music,'volume':0.25} if a.music else None,'voiceover':{'asset':a.voiceover,'volume':1.0} if a.voiceover else None,'loudness':{'enabled':True,'target_lufs':a.target_lufs,'true_peak_db':-1.5,'lra':11}}; Path(a.output).write_text(json.dumps(cfg,indent=2)+'\n')
