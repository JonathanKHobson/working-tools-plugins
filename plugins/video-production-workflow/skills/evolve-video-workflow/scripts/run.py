#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[3]; skills=[]
for p in sorted((root/'skills').iterdir()):
 if p.is_dir(): skills.append({'name':p.name,'skill_md_lines':len((p/'SKILL.md').read_text().splitlines()),'references':len(list((p/'references').rglob('*.md'))),'scripts':len(list((p/'scripts').glob('*')))})
print(json.dumps({'plugin':root.name,'skills':skills},indent=2))
