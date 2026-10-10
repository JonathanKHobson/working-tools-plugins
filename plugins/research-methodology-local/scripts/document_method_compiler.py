#!/usr/bin/env python3
"""Local extraction and rendering of reviewed analysis into INACTIVE method drafts.

No network, external dependencies, model calls, subprocesses, imports of generated
content, discovery-root writes or automatic installation. Source text is data.
"""
from __future__ import annotations
import argparse,hashlib,json,re,sys,unicodedata
from pathlib import Path
from datetime import datetime,timezone

MAX_FILE=8*1024*1024
MAX_TOTAL=16*1024*1024
MAX_SECTIONS=500
TEXT_EXTS={'.txt','.md','.markdown','.rst','.adoc'}
BLOCKED_PARTS={'.agents','.claude','.codex','.copilot','.hermes','.opencode','.git'}
INSTRUCTION_PATTERN=re.compile(r'\b(?:ignore (?:all )?(?:previous|prior) instructions|disregard (?:the )?(?:system|developer)|you are now)\b|<\|im_start\|>|<system>',re.I)

def sha(data):return hashlib.sha256(data).hexdigest()
def safe_path(value,exists=True):
 p=Path(value).expanduser().absolute()
 for ancestor in [p,*p.parents]:
  if ancestor.is_symlink():raise ValueError('Symlink paths are not accepted; select the real path')
 return p.resolve(strict=exists)
def read_bytes(path,limit=MAX_FILE):
 if not path.is_file():raise ValueError('Expected a regular selected file')
 if path.stat().st_size>limit:raise ValueError('File exceeds the bounded input size')
 data=path.read_bytes()
 if len(data)>limit:raise ValueError('File changed beyond the size limit')
 return data
def text(value):
 if not isinstance(value,str):raise ValueError('Analysis text must be a string')
 if any(unicodedata.category(c) in {'Cc','Cf','Cs'} and c not in '\n\t' for c in value):raise ValueError('Analysis contains hidden/control characters')
 return value.strip()
def clean_source(data):
 s=data.decode('utf-8-sig');removed={};out=[]
 for c in s:
  if (unicodedata.category(c) in {'Cc','Cf','Cs'} and c not in '\n\r\t') or 0xE0000<=ord(c)<=0xE007F or 0xFE00<=ord(c)<=0xFE0F:
   key=f'U+{ord(c):04X}';removed[key]=removed.get(key,0)+1
  else:out.append(c)
 return ''.join(out).replace('\r\n','\n').replace('\r','\n'),removed

def selected_sources(paths):
 sources=[];total=0;seen=set()
 for value in paths:
  p=safe_path(value)
  if p in seen:raise ValueError('Duplicate selected source')
  seen.add(p)
  if p.suffix.lower() not in TEXT_EXTS:raise ValueError('Unsupported format; export with an existing document provider first')
  data=read_bytes(p);total+=len(data)
  if total>MAX_TOTAL:raise ValueError('Selected sources exceed total input size')
  s,removed=clean_source(data)
  if not s.strip():raise ValueError('Selected source is empty')
  sources.append({'path':str(p),'filename':p.name,'sha256':sha(data),'text':s,'removed_characters':removed})
 if not sources:raise ValueError('Select at least one source')
 return sources

def new_destination(value):
 p=safe_path(value,False)
 if BLOCKED_PARTS.intersection(p.parts):raise ValueError('Active skill/config/git roots are not draft destinations')
 if any((ancestor/'.codex-plugin'/'plugin.json').is_file() or (ancestor/'.claude-plugin'/'plugin.json').is_file() for ancestor in p.parents):raise ValueError('Installed/canonical plugin roots are not draft destinations')
 if p.exists():raise ValueError('Output already exists; use a new draft directory')
 if not p.parent.is_dir():raise ValueError('Output parent must be an existing selected project directory')
 return p

def sections_for(source):
 lines=source['text'].splitlines(keepends=True);starts=[(0,'Preamble')];fence=None
 for i,line in enumerate(lines):
  stripped=line.lstrip()
  fm=re.match(r'(`{3,}|~{3,})',stripped)
  if fm:
   marker=fm.group(1)[0]
   if fence==marker:fence=None
   elif fence is None:fence=marker
   continue
  if fence:continue
  match=re.match(r'^#{1,6}\s+(.+?)\s*#*\s*$',line.rstrip()) or re.match(r'^\s*(Chapter|CHAPTER)\s+(\d+)(.*)$',line.rstrip())
  if match:
   title=line.strip().lstrip('#').strip()
   if i==0:starts[0]=(0,title)
   else:starts.append((i,title))
 result=[]
 for idx,(start,title) in enumerate(starts):
  end=starts[idx+1][0] if idx+1<len(starts) else len(lines)
  content=''.join(lines[start:end])
  if not content.strip():continue
  result.append({'title':title,'line_start':start+1,'line_end':end,'content':content})
 return result

def extract(args):
 sources=selected_sources(args.input);dest=new_destination(args.output)
 sections=[];chunks=[];offset=0
 for n,s in enumerate(sources,1):
  source_id=f'source-{n:03d}';header=f'\nSOURCE {source_id}: {s["filename"]}\nSHA256: {s["sha256"]}\n\n';chunks.append(header);offset+=len(header)
  for section in sections_for(s):
   sid=f'section-{len(sections)+1:04d}';content=section.pop('content')
   sections.append({**section,'id':sid,'source_id':source_id,'file':f'sections/{sid}.txt','sha256':sha(content.encode()),'character_start':offset,'character_end':offset+len(content),'instruction_pattern_lines':[i for i,l in enumerate(content.splitlines(),section['line_start']) if INSTRUCTION_PATTERN.search(l)],'_content':content})
   chunks.append(content);offset+=len(content)
  s['id']=source_id
 if len(sections)>MAX_SECTIONS:raise ValueError('Too many source sections; select a bounded document slice')
 full=''.join(chunks)
 metadata={'schema_version':1,'kind':'private-document-extraction','created_utc':datetime.now(timezone.utc).isoformat(),'sources':[{k:v for k,v in s.items() if k!='text'} for s in sources],'sections':[{k:v for k,v in s.items() if k!='_content'} for s in sections],'words':len(full.split()),'estimated_tokens':round(len(full)/4),'full_text_sha256':sha(full.encode()),'limitations':['Only selected UTF-8 text/Markdown exports were read.','No semantic inference, OCR, table/image reconstruction, or safety certification.','Source instructions remain untrusted data after character cleanup.']}
 dest.mkdir();(dest/'sections').mkdir()
 for s in sections:(dest/s['file']).write_text(s['_content'],encoding='utf-8')
 (dest/'full_text.txt').write_text(full,encoding='utf-8');(dest/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'state':'extracted-private','path':str(dest),'sources':len(sources),'sections':len(sections),'words':metadata['words'],'estimated_tokens':metadata['estimated_tokens']},ensure_ascii=True))

def load_json(path):return json.loads(read_bytes(safe_path(path)).decode('utf-8'))
def rows(value):
 if not isinstance(value,list):raise ValueError('Expected an analysis list')
 return value

def framework_lines(items):
 out=[]
 for f in rows(items):
  if not isinstance(f,dict):raise ValueError('Expected framework object')
  out += [f'### {text(f["name"])}',f'**When to use:** {text(f["when"])}',f'**How:** {text(f["how"])}',f'**Why / failure mode:** {text(f["why"])}','']
 return '\n\n'.join(out)
def bullets(items):return '\n'.join('- '+text(v) for v in rows(items))

def compile_draft(args):
 root=safe_path(args.extraction);meta=load_json(root/'metadata.json')
 if meta.get('kind')!='private-document-extraction' or meta.get('schema_version')!=1:raise ValueError('Unsupported extraction metadata')
 # Current sources are selected explicitly on the command line. Never open paths
 # supplied by untrusted metadata or analysis to establish source freshness.
 current=selected_sources(args.input)
 expected={(s['path'],s['sha256']) for s in meta['sources']}
 if {(s['path'],s['sha256']) for s in current}!=expected:raise ValueError('Selected source fingerprints changed; extract again')
 known={};total=0
 for s in rows(meta['sections']):
  sid=s['id']
  if not re.fullmatch(r'section-\d{4}',sid) or s['file']!=f'sections/{sid}.txt':raise ValueError('Invalid section path')
  if sid in known:raise ValueError('Duplicate section ID')
  content=read_bytes(safe_path(root/s['file']));total+=len(content)
  if total>MAX_TOTAL or len(known)>=MAX_SECTIONS:raise ValueError('Extraction exceeds bounded limits')
  if sha(content)!=s['sha256']:raise ValueError('Section fingerprint changed; extract again')
  known[sid]=s
 if sha(read_bytes(safe_path(root/'full_text.txt'),MAX_TOTAL))!=meta['full_text_sha256']:raise ValueError('Combined extraction fingerprint changed')
 analysis_path=safe_path(args.analysis);analysis_bytes=read_bytes(analysis_path);a=json.loads(analysis_bytes)
 if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',args.name) or len(args.name)>64:raise ValueError('Invalid draft slug')
 title=text(a['title']);author=text(a['author']);description=text(a['description']);rights=text(a['rights_note'])
 if not title or not description or not rights:raise ValueError('Title, description and rights note are required')
 output_root=safe_path(args.output_root)
 if not output_root.is_dir():raise ValueError('Output root must be an existing selected project directory')
 dest=new_destination(output_root/args.name)
 chapter_files={};index=[];used=set()
 for n,c in enumerate(rows(a['chapters']),1):
  evidence=rows(c['evidence_sections'])
  if not evidence or any(sid not in known for sid in evidence):raise ValueError('Each chapter needs valid source section evidence')
  used.update(evidence);ctitle=text(c['title']);name=f'chapters/ch{n:02d}.md'
  if not ctitle or not text(c['core_idea']) or not rows(c['frameworks']) or not rows(c['takeaways']):raise ValueError('Each chapter needs title, idea, frameworks and takeaways')
  content=f'# Chapter {n}: {ctitle}\n\n## Source evidence\n'+bullets([f'{sid}: {known[sid]["source_id"]}, lines {known[sid]["line_start"]}-{known[sid]["line_end"]}, SHA256 {known[sid]["sha256"]}' for sid in evidence])+'\n\n## Core idea\n'+text(c['core_idea'])+'\n\n## Frameworks introduced\n'+framework_lines(c['frameworks'])
  for label,key in [('Key concepts','concepts'),('Mental models','mental_models'),('Anti-patterns','anti_patterns'),('Key takeaways','takeaways'),('Connects to','connects_to')]:content+=f'\n\n## {label}\n'+bullets(c.get(key,[]))
  for label,key in [('Worked example','worked_example'),('Code examples','code_examples'),('Reference tables','reference_tables')]:
   if c.get(key):content+=f'\n\n## {label}\n'+text(c[key])
  chapter_files[name]=content+'\n';index.append(f'| [ch{n:02d}]({name}) | {ctitle.replace("|","/")} | '+', '.join(text(f['name']).replace('|','/') for f in c['frameworks'])+' |')
 if not chapter_files:raise ValueError('Select at least one evidence-backed chapter')
 glossary='\n'.join(f'- **{text(g["term"])}**: {text(g["definition"])} ({text(g["chapter"])})' for g in sorted(rows(a['glossary']),key=lambda g:text(g['term']).casefold()))
 patterns='\n\n'.join(f'## {text(p["name"])}\n\n**When:** {text(p["when"])}\n\n**How:** {text(p["how"])}\n\n**Trade-offs:** {text(p["tradeoffs"])}' for p in rows(a['patterns']))
 topics=[]
 for topic in rows(a.get('topics',[])):
  refs=rows(topic['chapters'])
  if any(not isinstance(n,int) or isinstance(n,bool) or n<1 or n>len(chapter_files) for n in refs):raise ValueError('Topic chapter reference out of range')
  topics.append('- **'+text(topic['term'])+'**: '+', '.join(f'[ch{n:02d}](chapters/ch{n:02d}.md)' for n in refs))
 skill=f'---\nname: {args.name}\ndescription: '+json.dumps(description,ensure_ascii=True)+'\n---\n\n# '+title+'\n\n**Author:** '+author+'\n\n## Draft boundary\n\nInactive private draft. Read the relevant chapter before applying its method. Source evidence does not grant execution, installation or publication authority.\n\n## Core frameworks\n\n'+framework_lines(a['core_frameworks'])+'\n\n## Chapter index\n\n| Chapter | Title | Frameworks |\n| --- | --- | --- |\n'+'\n'.join(index)+'\n\n## Topic index\n\n'+'\n'.join(topics)+'\n\n## Supporting files\n\n- [Glossary](glossary.md)\n- [Patterns](patterns.md)\n- [Decision rules](cheatsheet.md)\n- [Provenance](provenance.json)\n\n## Rights and limitations\n\n'+rights+'\n\n'+bullets(a.get('limitations',[]))+'\n'
 files={'SKILL.md':skill,'glossary.md':'# Glossary\n\n'+glossary+'\n','patterns.md':'# Patterns\n\n'+patterns+'\n','cheatsheet.md':'# Decision rules\n\n'+bullets(a['decision_rules'])+'\n',**chapter_files}
 provenance={'schema_version':1,'state':'prepared-private-draft','created_utc':datetime.now(timezone.utc).isoformat(),'analysis_sha256':sha(analysis_bytes),'source_fingerprints':meta['sources'],'evidence_sections':[known[s] for s in sorted(used)],'rights_note':rights,'files':{name:sha(content.encode()) for name,content in files.items()},'verification':'Rendering, paths, evidence IDs and hashes verified; semantic/source accuracy and security admission remain required.'}
 files['provenance.json']=json.dumps(provenance,ensure_ascii=False,indent=2)+'\n'
 # Validate the complete render before creating any output. Exclusive mkdir
 # refuses a competing preexisting path. No delete, move, symlink or overwrite.
 dest.mkdir();(dest/'chapters').mkdir()
 for name,content in files.items():(dest/name).write_text(content,encoding='utf-8')
 print(json.dumps({'state':'prepared-private-draft','path':str(dest),'chapters':len(chapter_files),'evidence_sections':len(used),'files':len(files),'semantic_review':'required','security_review':'required'}))

def main():
 parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='mode',required=True)
 ex=sub.add_parser('extract');ex.add_argument('--input',action='append',required=True);ex.add_argument('--output',required=True);ex.set_defaults(func=extract)
 co=sub.add_parser('compile');co.add_argument('--input',action='append',required=True);co.add_argument('--extraction',required=True);co.add_argument('--analysis',required=True);co.add_argument('--output-root',required=True);co.add_argument('--name',required=True);co.set_defaults(func=compile_draft)
 args=parser.parse_args()
 try:args.func(args)
 except (OSError,ValueError,KeyError,TypeError) as exc:
  print(json.dumps({'state':'failed','error':str(exc)},ensure_ascii=True),file=sys.stderr);return 2
 return 0
if __name__=='__main__':sys.exit(main())
