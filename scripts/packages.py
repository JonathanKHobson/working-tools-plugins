"""Validate reviewed packages and build deterministic distribution archives."""
from __future__ import annotations
import argparse,hashlib,json,re,stat,sys,zipfile
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
MARKETPLACE='working-tools'
# Agent Plugins 1.0.0 forbids undeclared top-level fields. Host-specific
# fields belong in extensions or the host's compatibility manifest.
PORTABLE_FIELDS={'$schema','name','version','description','author','homepage','repository','license','keywords','extensions'}
def read_json(path):return json.loads(path.read_text())
def write_json(path,value):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def files(root):
 for p in sorted(root.rglob('*')):
  if p.is_symlink():raise ValueError(f'Symlink is not distributable: {p.relative_to(ROOT)}')
  if p.is_file() and not any(x in p.parts for x in ['__pycache__','.pytest_cache','.git','.venv']) and p.name!='.DS_Store' and not p.name.endswith(('.pyc','.pyo')):yield p

def validate_package(record):
 root=ROOT/'plugins'/record['id'];errors=[]
 exceptions_path=ROOT/'catalog/validation-exceptions.json'
 exceptions=read_json(exceptions_path).get(record['id'],{}) if exceptions_path.exists() else {}
 def exempt(kind,p,target=None):
  digest=hashlib.sha256(p.read_bytes()).hexdigest();rel=p.relative_to(root).as_posix()
  return any(x['path']==rel and x.get('sha256',x.get('source_sha256'))==digest and (target is None or x.get('target')==target) for x in exceptions.get(kind,[]))
 def problem(s):errors.append(f"{record['id']}: {s}")
 for rel in ['plugin.json','.codex-plugin/plugin.json','.claude-plugin/plugin.json','README.md','LICENSE','THIRD_PARTY_NOTICES.md']:
  if not (root/rel).is_file():problem(f'missing {rel}')
 provenance=root/record.get('provenance','PROVENANCE.json')
 if not provenance.is_file():problem('missing provenance inventory')
 else:
  for item in read_json(provenance).get('files',[]):
   rel=item.get('path',item.get('source_relative'));digest=item.get('output_sha256',item.get('sha256'))
   if not rel or not digest:continue
   output=(root/rel).resolve()
   if not output.is_relative_to(root.resolve()) or not output.is_file():problem(f'provenance path missing or escaping package: {rel}')
   elif hashlib.sha256(output.read_bytes()).hexdigest()!=digest:problem(f'provenance output hash mismatch: {rel}')
 for rel in ['plugin.json','.codex-plugin/plugin.json','.claude-plugin/plugin.json']:
  if not (root/rel).exists():continue
  manifest=read_json(root/rel)
  if manifest.get('name')!=record['id'] or manifest.get('version')!=record['version']:problem(f'{rel} identity/version mismatch')
  if rel=='plugin.json' and manifest.get('$schema')!='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json':problem('missing portable schema')
  if rel=='plugin.json':
   unknown=set(manifest)-PORTABLE_FIELDS
   if unknown:problem(f'unsupported portable manifest fields: {", ".join(sorted(unknown))}')
 # A portable root manifest takes precedence over compatibility declarations.
 # Without root mcp.json, a successful install can silently omit the servers.
 declared_servers=set()
 def collect_servers(value,source,seen=None):
  seen=set() if seen is None else seen
  if isinstance(value,str):
   path=(root/value.replace('${CLAUDE_PLUGIN_ROOT}/','')).resolve()
   if not path.is_relative_to(root.resolve()) or not path.is_file():
    problem(f'MCP declaration path missing or escaping package: {source} -> {value}');return
   if path in seen:problem(f'cyclic MCP declaration: {source}');return
   collect_servers(read_json(path),str(path.relative_to(root.resolve())),seen|{path})
  elif isinstance(value,list):
   for entry in value:collect_servers(entry,source,seen)
  elif isinstance(value,dict):
   servers=value.get('mcpServers',value)
   if not isinstance(servers,dict):problem(f'invalid MCP server map in {source}')
   else:declared_servers.update(servers)
  elif value is not None:problem(f'invalid MCP declaration in {source}')
 for rel in ['.codex-plugin/plugin.json','.claude-plugin/plugin.json']:
  if (root/rel).is_file():collect_servers(read_json(root/rel).get('mcpServers'),rel)
 if declared_servers:
  portable_mcp=root/'mcp.json'
  if not portable_mcp.is_file():problem('compatibility MCP servers require portable root mcp.json')
  else:
   servers=read_json(portable_mcp).get('mcpServers',{})
   if not isinstance(servers,dict):problem('invalid portable MCP server map')
   else:
    missing=declared_servers-set(servers)
    if missing:problem(f'portable mcp.json omits compatibility servers: {", ".join(sorted(missing))}')
 heads=list((root/'skills').glob('*/SKILL.md'))
 if len(heads)!=record['skills']:problem(f'skill count {len(heads)} differs from registry')
 for p in files(root):
  if p.stat().st_size>10*1024*1024:problem(f'oversized source file {p.relative_to(root)}')
  try:text=p.read_text()
  except UnicodeDecodeError:continue
  if re.search(r'/(?:Users|Volumes)/[^\s\"\']+|plugin_asdk_app_[a-z0-9]+|(?<![A-Za-z0-9_-])sk-(?:proj-)?[a-zA-Z0-9_-]{25,}',text) and not exempt('privacy_exceptions',p):problem(f'private binding/credential candidate in {p.relative_to(root)}')
  if p.name=='SKILL.md':
   front=re.match(r'^---\n(.*?)\n---',text,re.S)
   if not front or not all(re.search(r'(?m)^'+key+r':\s*\S+',front[1]) for key in ['name','description']):problem(f'invalid frontmatter {p.relative_to(root)}')
  if p.suffix=='.md':
   for target in re.findall(r'\]\(([^)]+)\)',text):
    target=target.strip().strip('<>').split(' "')[0].split('#')[0]
    if not target or re.match(r'[a-z][a-z0-9+.-]*:',target):continue
    dest=(p.parent/unquote(target)).resolve()
    if (not dest.is_relative_to(root.resolve()) or not dest.exists()) and not exempt('reference_exceptions',p,target):problem(f'broken reference {p.relative_to(root)} -> {target}')
 return errors

def catalogs(records):
 available=[r for r in records if r['distribution'] in ('prepared','released')]
 codex={'name':MARKETPLACE,'interface':{'displayName':'Working Tools by Kyle Hobson'},'plugins':[]}
 claude={'name':MARKETPLACE,'owner':{'name':'Kyle Hobson'},'plugins':[]}
 for r in available:
  codex['plugins'].append({'name':r['id'],'source':{'source':'local','path':'./plugins/'+r['id']},'policy':{'installation':'AVAILABLE','authentication':'ON_INSTALL'},'category':r.get('category','Productivity')})
  claude['plugins'].append({'name':r['id'],'source':'./plugins/'+r['id'],'version':r['version'],'description':r['description']})
 return codex,claude

def validate(records):
 errors=[];ids=[r['id'] for r in records]
 if len(ids)!=len(set(ids)):errors.append('duplicate package id')
 for r in records:errors.extend(validate_package(r))
 expected=catalogs(records)
 for rel,want in zip(['.agents/plugins/marketplace.json','.claude-plugin/marketplace.json'],expected):
  if not (ROOT/rel).exists() or read_json(ROOT/rel)!=want:errors.append(f'{rel} out of date: run python3 scripts/packages.py catalog')
 if errors:raise ValueError('\n'.join(errors))
 return {'packages':len(records),'skills':sum(r['skills'] for r in records),'status':'passed'}

def build(records,out):
 validate(records);out.mkdir(parents=True,exist_ok=True);receipts=[]
 for r in records:
  root=ROOT/'plugins'/r['id'];artifact=out/f"{r['id']}-{r['version']}.zip";manifest={}
  with zipfile.ZipFile(artifact,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   for p in files(root):
    rel=p.relative_to(root).as_posix();data=p.read_bytes();manifest[rel]=hashlib.sha256(data).hexdigest()
    info=zipfile.ZipInfo(rel,(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
    info.external_attr=(stat.S_IFREG|(0o755 if p.stat().st_mode & 0o111 else 0o644))<<16;z.writestr(info,data)
  digest=hashlib.sha256(artifact.read_bytes()).hexdigest()
  write_json(out/f"{r['id']}-{r['version']}.files.json",manifest)
  receipts.append({'id':r['id'],'version':r['version'],'file':artifact.name,'sha256':digest,'files':len(manifest),'size':artifact.stat().st_size,'tag':f"{r['id']}/v{r['version']}"})
 write_json(out/'release-manifest.json',receipts)
 (out/'SHA256SUMS').write_text(''.join(f"{r['sha256']}  {r['file']}\n" for r in receipts))
 return receipts

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['catalog','validate','build']);p.add_argument('--output',type=Path,default=ROOT/'dist');a=p.parse_args()
 records=read_json(ROOT/'catalog/packages.json')['packages']
 if a.command=='catalog':
  for rel,value in zip(['.agents/plugins/marketplace.json','.claude-plugin/marketplace.json'],catalogs(records)):write_json(ROOT/rel,value)
  result={'generated':2,'packages':len(records)}
 elif a.command=='validate':result=validate(records)
 else:result=build(records,a.output)
 print(json.dumps(result,indent=2))
if __name__=='__main__':
 try:main()
 except (ValueError,KeyError) as e:sys.exit(str(e))
