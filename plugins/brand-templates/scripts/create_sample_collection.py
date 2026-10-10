#!/usr/bin/env python3
"""Create an explicit source-integrity fixture, never a replacement brand collection."""
import argparse, base64, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Authored neutral 1-pixel WebP fixture, no private identity or third-party artwork.
WEBP=base64.b64decode('UklGRh4AAABXRUJQVlA4TBEAAAAvAAAAAAdQ61rXuv+BiOh/AAA=')
def write(root,rel,value):
 p=root/rel;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_bytes(value if isinstance(value,bytes) else value.encode())
def build(root):
 root=Path(root).expanduser().resolve()
 if root.is_relative_to(ROOT) or (root.exists() and any(root.iterdir())):raise ValueError('Use an empty external directory')
 root.mkdir(parents=True,exist_ok=True)
 write(root,'templates/fixture-neutral/SKILL.md','---\nname: fixture-neutral\ndescription: Explicit synthetic brand source-integrity fixture.\n---\n\n# Fixture neutral\n\nRead DESIGN.md. Preserve the synthetic label and supplied facts. This fixture does not define a real reusable identity.\n')
 write(root,'templates/fixture-neutral/DESIGN.md','# Synthetic integrity fixture\n\nThis authored neutral fixture exercises catalog verification and a complete source closure. It supplies no private brand assets, fonts, logo or trademark clearance.\n')
 write(root,'library/media/fixture.webp',WEBP)
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 record={'id':'fixture-neutral','name':'Synthetic integrity fixture','summary':'Explicit synthetic neutral fixture for source verification only.','category':'Synthetic test','tags':['synthetic','fixture'],'version':'1.0.0','sourceTemplateIds':[],'sourceHash':sha(root/'templates/fixture-neutral/DESIGN.md'),'rightsSummary':'Authored MIT test fixture, no real identity or trademark claim.','previews':[{'src':'media/fixture.webp'}],'recognitionRules':['Keep the synthetic fixture label.'],'colors':[{'name':'Neutral','hex':'#d6d6d6'}],'typography':[{'role':'Test','family':'System sans-serif','usage':'No bundled fonts.'}]}
 write(root,'library/catalog.json',json.dumps({'brands':[record],'total':1},indent=2)+'\n')
 rows=[{'path':p.relative_to(root).as_posix(),'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file()]
 write(root,'provenance/source-files.json',json.dumps({'files':rows},indent=2)+'\n')
 return root
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 try:root=build(a.output)
 except ValueError as exc:p.error(str(exc))
 print(json.dumps({'synthetic':True,'BRAND_TEMPLATES_DATA_ROOT':str(root),'records':1},indent=2))
