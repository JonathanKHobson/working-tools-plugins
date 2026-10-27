"""Validate reviewed packages and build deterministic distribution archives."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,re,stat,subprocess,sys,zipfile
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
MARKETPLACE='working-tools'
REPOSITORY='https://github.com/JonathanKHobson/working-tools-plugins'

def sibling_module(name):
 spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(name+'.py'))
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 return module

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

# These retired instruction-only packs are incorporated methods, not execution
# dependencies. Official host providers and real apps/APIs/runtimes remain valid.
INCORPORATED_METHOD_PACKS = (
 'aihumanizer', 'uiuxdesigner', 'coverletterwriter', 'injectionchecker',
 'promptengineer', 'spreadsheethumanux', 'researchwritingguardrails',
 'codexmaterialthemes',
)

def method_requirement_errors(record):
 errors=[]
 for requirement in record.get('requirements',[]):
  normalized=re.sub(r'[^a-z0-9]','',requirement.lower())
  if any(name in normalized for name in INCORPORATED_METHOD_PACKS):
   errors.append(f"{record['id']}: incorporated method pack cannot be an installation requirement: {requirement}")
 return errors

def hook_registration_errors(root, ident):
 """Validate shipped operative hooks without activating archived library copies."""
 errors=[]
 def problem(message):errors.append(f'{ident}: {message}')
 def hook_map(value, source, seen=None):
  seen=set() if seen is None else seen
  if isinstance(value,str):
   relative=value.replace('${CLAUDE_PLUGIN_ROOT}/','').replace('${PLUGIN_ROOT}/','')
   path=(root/relative).resolve()
   if not path.is_relative_to(root.resolve()) or not path.is_file() or path.is_symlink():
    problem(f'hook declaration path missing or escaping package: {source} -> {value}');return None
   if path in seen:problem(f'cyclic hook declaration: {source}');return None
   return hook_map(read_json(path),source,seen|{path})
  if isinstance(value,dict):
   result=value.get('hooks',value)
   if isinstance(result,dict):return result
  problem(f'missing or invalid hook registration: {source}');return None
 # Only the host-native compatibility manifests (.codex-plugin for Codex,
 # .claude-plugin for Claude) are actually dispatched for hooks at runtime.
 # The portable root manifest (plugin.json/plugin.portable.json) uses the
 # Agent Plugins "extensions.com.openai" format, which the installed Codex
 # CLI's loader explicitly skips for hook discovery (core-plugins loader.rs),
 # so it must never be treated as authoritative or required to match here.
 for directory in ('hooks','optional-hooks'):
  for name,manifest in (('hooks.json','.codex-plugin/plugin.json'),('claude-hooks.json','.claude-plugin/plugin.json')):
   definition=root/directory/name
   if not definition.is_file():continue
   expected=hook_map(read_json(definition),f'{directory}/{name}')
   if not expected:continue
   if name=='hooks.json' and (root/'plugin.json').is_file():
    problem('root plugin.json suppresses Codex hook discovery on the supported runtime; retain portable metadata as plugin.portable.json')
   seen_handlers=set()
   for event,groups in expected.items():
    for group in groups:
     for handler in group.get('hooks',[]):
      command=handler.get('command','')
      key=(event,group.get('matcher',''),command)
      if key in seen_handlers:problem(f'duplicate or conflicting hook handler in {directory}/{name}: {event}')
      seen_handlers.add(key)
      for script in re.findall(r'(?:scripts|hooks)/[^\s"\x27}]+\.(?:py|js|mjs|sh)\b',command):
       target=(root/script).resolve()
       if not target.is_relative_to(root.resolve()) or not target.is_file():
        problem(f'missing hook handler script: {script}')
   declaration=root/manifest
   if not declaration.is_file():
    problem(f'missing or invalid hook registration: {manifest}');continue
   registration=read_json(declaration).get('hooks')
   if name=='claude-hooks.json' and registration is None and (root/'hooks/hooks.json').is_file():
    # Claude loads hooks/hooks.json automatically. A separately retained
    # claude-hooks.json template does not require duplicate registration.
    # The default file and its handlers are validated in the Codex pass above.
    continue
   actual=hook_map(registration,manifest)
   if actual is not None and actual!=expected:
    problem(f'{manifest} hook registration differs from shipped {directory}/{name}')
 return errors

def validate_package(record):
 root=ROOT/'plugins'/record['id'];errors=method_requirement_errors(record)
 errors.extend(hook_registration_errors(root,record['id']))
 exceptions_path=ROOT/'catalog/validation-exceptions.json'
 exceptions=read_json(exceptions_path).get(record['id'],{}) if exceptions_path.exists() else {}
 def exempt(kind,p,target=None):
  digest=hashlib.sha256(p.read_bytes()).hexdigest();rel=p.relative_to(root).as_posix()
  return any(x['path']==rel and x.get('sha256',x.get('source_sha256'))==digest and (target is None or x.get('target')==target) for x in exceptions.get(kind,[]))
 def problem(s):errors.append(f"{record['id']}: {s}")
 # plugin.portable.json is the renamed portable root manifest for packages whose
 # native .codex-plugin hooks would otherwise be skipped if a root plugin.json
 # (Agent Plugins schema) were present; either name satisfies the portable manifest.
 portable_rel=next((n for n in ('plugin.json','plugin.portable.json') if (root/n).is_file()),'plugin.json')
 for rel in [portable_rel,'.codex-plugin/plugin.json','.claude-plugin/plugin.json','README.md','LICENSE','THIRD_PARTY_NOTICES.md']:
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
 for rel in [portable_rel,'.codex-plugin/plugin.json','.claude-plugin/plugin.json']:
  if not (root/rel).exists():continue
  manifest=read_json(root/rel)
  if manifest.get('name')!=record['id'] or manifest.get('version')!=record['version']:problem(f'{rel} identity/version mismatch')
  if rel==portable_rel and manifest.get('$schema')!='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json':problem('missing portable schema')
  if rel==portable_rel:
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
  private_patterns=[
   r'/(?:Users|Volumes)/[^\s\"\']+',
   r'plugin_asdk_app_[a-z0-9]+',
   r'(?<![A-Za-z0-9_-])sk-(?:proj-)?[a-zA-Z0-9_-]{25,}',
  ]
  # New public toolkits use a stricter recipient audit. Existing packages may
  # contain retained third-party examples, so their historical scan remains
  # limited to the established binding and token patterns.
  if record.get('id') in {'claude-toolkit','gemini-toolkit','apple-foundation-model-toolkit','local-model-toolkit','work-management'}:
   private_patterns.extend([
    r'(?<![A-Za-z0-9_-])/(?:home|root)/(?!(?:user|username|recipient|example)(?:[/\\]|$))[A-Za-z][A-Za-z0-9._-]{2,}(?:[/\\]|$)',
    r'(?<![A-Za-z0-9_-])[A-Za-z]:\\Users\\(?!(?:user|username|recipient|example)(?:\\|$))[A-Za-z][A-Za-z0-9._-]{2,}(?:\\|$)',
    r'(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@(?!example\.)(?:gmail|icloud|outlook|hotmail|yahoo|proton)\.(?:com|me)(?![A-Za-z0-9.-])',
    r'(?<![A-Za-z0-9_-])AIza[0-9A-Za-z_-]{20,}',
   ])
  if any(re.search(pattern,text) for pattern in private_patterns) and not exempt('privacy_exceptions',p):problem(f'private binding/credential candidate in {p.relative_to(root)}')
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

def release(records,out,canonical_root=None):
 errors=sibling_module('source_inventory').validate_inventory(ROOT,records,canonical_root)
 if errors:raise ValueError('Release completeness gate failed:\n'+'\n'.join(errors))
 legal=sibling_module('license_checks')
 errors=[error for record in records for error in legal.legal_errors(ROOT/'plugins'/record['id'],record)]
 if errors:raise ValueError('Release legal packaging gate failed:\n'+'\n'.join(errors))
 errors=[error for record in records for error in legal.source_rights_release_errors(ROOT/'plugins'/record['id'],record)]
 if errors:raise ValueError('Release source-rights gate failed:\n'+'\n'.join(errors))
 receipts=build(records,out)
 manifest=source_release_manifest(records,receipts,out)
 manifest['canonical_live_source_checked']=canonical_root is not None
 write_json(out/'source-release-manifest.json',manifest)
 verification=verify_archives(out)
 if not verification['passed']:raise ValueError(json.dumps(verification,indent=2))
 return receipts

def source_release_manifest(records,receipts,out):
 inventory=read_json(ROOT/'catalog/source-inventory.json')
 by_id={row['id']:row for row in inventory['packages']}
 try:
  commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip()
  dirty=bool(subprocess.check_output(['git','status','--porcelain','--untracked-files=normal'],cwd=ROOT,text=True))
 except (OSError,subprocess.CalledProcessError):
  commit=None;dirty=True
 packages=[]
 for receipt in receipts:
  locked=by_id[receipt['id']]
  actual=read_json(out/f"{receipt['id']}-{receipt['version']}.files.json")
  if actual!=locked['files']:raise ValueError(f"{receipt['id']}: built archive differs from reviewed source inventory")
  packages.append({
   **receipt,
   'canonical_source':locked['canonical_source'],
   'components':locked['components'],
   'included_files':actual,
   'excluded_source':locked['excluded_source'],
   'destinations':{
    'source':REPOSITORY+'/tree/'+(commit if commit and not dirty else 'main')+'/plugins/'+receipt['id'],
    'release':REPOSITORY+'/releases/tag/'+receipt['tag'],
    'download':REPOSITORY+'/releases/download/'+receipt['tag']+'/'+receipt['file'],
    'website':'https://working-tools.jkylehobson.chatgpt.site/'
   }
  })
 return {
  'schema_version':1,
  'source_revision_semantics':'A canonical directory has no assumed Git revision. Its reviewed distributable tree is pinned by sorted path/content SHA256 records. Held scopes are accounted for separately.',
  'assembly_commit':commit,'assembly_worktree_dirty':dirty,
  'canonical_live_source_checked':False,
  'registry_sha256':hashlib.sha256((ROOT/'catalog/packages.json').read_bytes()).hexdigest(),
  'source_inventory_sha256':hashlib.sha256((ROOT/'catalog/source-inventory.json').read_bytes()).hexdigest(),
  'coverage_baseline_sha256':hashlib.sha256((ROOT/'catalog/coverage-baseline.json').read_bytes()).hexdigest(),
  'packages':packages
 }

def verify_archives(out):
 manifest=read_json(out/'source-release-manifest.json')
 verify=sibling_module('release_archive').verify_archive
 results=[]
 for record in manifest['packages']:
  filename=record['file']
  if Path(filename).name!=filename or not filename.endswith('.zip'):
   raise ValueError('Invalid archive basename in release manifest')
  result=verify(out/filename,record['included_files'],record['sha256'])
  results.append({'id':record['id'],'version':record['version'],**result})
 return {'passed':all(row['passed'] for row in results),'packages':results}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['catalog','validate','build','release','verify-archives']);p.add_argument('--output',type=Path,default=ROOT/'dist');p.add_argument('--canonical-root',type=Path);a=p.parse_args()
 records=read_json(ROOT/'catalog/packages.json')['packages']
 if a.command=='catalog':
  for rel,value in zip(['.agents/plugins/marketplace.json','.claude-plugin/marketplace.json'],catalogs(records)):write_json(ROOT/rel,value)
  result={'generated':2,'packages':len(records)}
 elif a.command=='validate':result=validate(records)
 elif a.command=='verify-archives':
  result=verify_archives(a.output)
  if not result['passed']:raise ValueError(json.dumps(result,indent=2))
 elif a.command=='release':result=release(records,a.output,a.canonical_root)
 else:result=build(records,a.output)
 print(json.dumps(result,indent=2))
if __name__=='__main__':
 try:main()
 except (ValueError,KeyError) as e:sys.exit(str(e))
