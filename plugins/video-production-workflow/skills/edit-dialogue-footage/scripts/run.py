#!/usr/bin/env python3
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser(description='Create a conservative dialogue EDL template from approved ranges.'); p.add_argument('--source',required=True); p.add_argument('--ranges',required=True,help='JSON list with start,end,quote,reason'); p.add_argument('--output',required=True); a=p.parse_args(); ranges=json.loads(Path(a.ranges).read_text()); edl={'version':1,'sources':{'source':str(Path(a.source).resolve())},'ranges':[{'source':'source',**r} for r in ranges]}; Path(a.output).write_text(json.dumps(edl,indent=2)+'\n')
