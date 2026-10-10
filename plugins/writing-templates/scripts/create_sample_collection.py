#!/usr/bin/env python3
"""Create an external synthetic contract fixture; no original voice/prose library."""
from pathlib import Path
import argparse, hashlib, json, shutil
ROOT=Path(__file__).resolve().parents[1]
ENGINE_FILES = (
 'metrics/cohort.cjs', 'metrics/constants.cjs', 'metrics/markdown.cjs',
 'metrics/measure.cjs', 'metrics/parser.cjs', 'metrics/text.cjs',
 'validation/validate.cjs', 'validation/validate.py',
 'validation/vendor/marked/LICENSE.md',
 'validation/vendor/marked/lib/marked.esm.js',
 'validation/vendor/marked/package.json',
)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(root,rel,value):
 p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(value)
def js(root,rel,obj):write(root,rel,json.dumps(obj,indent=2)+'\n')
def build(root):
 root=Path(root).expanduser().resolve()
 if root.is_relative_to(ROOT) or (root.exists() and any(root.iterdir())):raise ValueError('Use an empty external directory')
 root.mkdir(parents=True,exist_ok=True)
 routes={'V01':('V01',[]),'V02':('V02',[]),'P28':('V01',['P28']),'P29':('V02',['P29'])}
 records=[]
 for ident,(base,mods) in routes.items():
  guide=f'guides/{ident}.md'
  write(root,guide,f'# {ident}: synthetic integrity fixture\n\nApply only supplied facts. This fixture exercises routing, source pins and QA references; it is not an original Writing Library profile or claimed voice. Preserve uncertainty. For the module, use its actual base guide.\n')
  sample=f'examples/{ident}/specimen.md'
  write(root,sample,f'# Fictional example {ident}\n\n<!-- specimen:start -->\nThe fictional test desk opens at nine. It accepts only the supplied test record. Review the stated facts before taking a next step. This prose is an authored source-integrity fixture and makes no claim about a real service, organization or writer.\n<!-- specimen:end -->\n')
  record={'id':ident,'name':ident+' synthetic fixture','version':'1.0.0','resource_type':'module' if mods else 'legacy_profile','description':'Authored synthetic routing fixture, no original style corpus.','mechanism':'State supplied facts, then the bounded next action.','primary_layer':'structure','tags':['synthetic','fixture'],'truth_boundary':'No source facts beyond the explicit fictional fixture.','evidence_status':'synthetic_contract_check','guide_path':guide,'route':{'selected_resource_id':ident,'base_profile_id':base,'module_ids':mods},'examples':[{'id':ident+'-E1','brief_id':'E-B01','path':sample,'sha256':sha(root/sample)}]}
  records.append(record)
  for name in ('README.md','voice.md','tone.md','style.md','format.md','profile.json'):
   content=json.dumps({'id':ident,'synthetic':True})+'\n' if name.endswith('.json') else f'# {ident} {name}\n\nSynthetic axis reference only. Preserve supplied facts; levels are editorial descriptions, not tested thresholds.\n'
   write(root,f'styles/{ident}/axes/{name}',content)
 js(root,'records/catalog.json',{'schema_version':'wvl-catalog/2.0.0','private_included':False,'record_count':len(records),'records':records})
 write(root,'records/briefs.md','# Fictional shared test brief\n\nThe test desk opens at nine. This is synthetic fixture data only.\n')
 # Synthetic source-edition guide and reading exercise the complete historical-reading pin mechanism without historic/public-domain claims.
 edition_files={};edition_records={}
 for ident in routes:
  rel=f'guides/{ident}.md';write(root,'source-edition/'+rel,f'# {ident} source edition\n\nThis new synthetic reading proves the source-edition hash contract only. No historical author, private passage or personal voice is represented.\n')
  edition_files[rel]=sha(root/'source-edition'/rel);edition_records[ident]={'bundleFiles':[rel]}
 js(root,'source-edition/edition.json',{'records':edition_records,'files':edition_files})
 js(root,'axes/four-axes.json',{'schemaVersion':'wvl-axes/1','framework':'Synthetic four-axis contract fixture','levels':['descriptive'], 'profiles':[{'id':i,'synthetic':True} for i in routes]})
 # Full original licensed executable offline engine; corpus-specific companions/profiles are new synthetic fixtures.
 for relative in ENGINE_FILES:
  source=ROOT/'library/voice-library'/relative
  if source.is_symlink() or not source.is_file():raise ValueError('Required licensed QA engine file is unavailable: '+relative)
  dest=root/relative;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
 write(root,'validation/WORKFLOW.md','# Synthetic fixture QA\n\nRun `python3 validation/validate.py --input examples/V01/specimen.md --profile validation/profiles/V01.json --channel markdown` from the external root. The original complete engine describes prose and requires semantic review; no synthetic profile measurements establish acceptance bounds.\n')
 write(root,'validation/editorial-companion.md','# Synthetic editorial fixture\n\nPreserve supplied facts, uncertainty and authorization. Review for meaning before changing wording. This fixture is not the omitted original Humanizer companion.\n')
 units=['words/sentence','coefficient_of_variation','MATTR50_ratio','events/1000_words','events/1000_words','percent_sentences','words/paragraph','percent_words']
 for ident,(base,mods) in routes.items():
  js(root,f'validation/profiles/{ident}.json',{'schema':'wvl-qa-profile/1','resourceId':ident,'name':ident+' synthetic fixture','route':{'selected_resource_id':ident,'base_profile_id':base,'module_ids':mods},'extractorVersion':'wvl-metrics/1.0.0','observedFeatures':[{'featureId':'F'+str(i+1).zfill(2),'unit':unit,'n':0,'min':None,'median':None,'max':None} for i,unit in enumerate(units)],'toneTargets':[],'manualChecks':[{'id':'facts','label':'Preserve explicit fictional facts','source':'fixture brief'}],'hardConstraints':[]})
 runtime_files=[p.relative_to(root).as_posix() for p in sorted(root.rglob('*')) if p.is_file() and (p.parent==root/'metrics' or p.suffix in ('.cjs','.py') or 'vendor' in p.parts)]
 pins={p.relative_to(root).as_posix():sha(p) for p in sorted(root.rglob('*')) if p.is_file()}
 js(root,'validation/manifest.json',{'schema':'wvl-qa-manifest/1','runtimeFiles':runtime_files,'files':pins})
 pins['validation/manifest.json']=sha(root/'validation/manifest.json')
 js(root,'approved-sources.json',{'catalogSha256':pins['records/catalog.json'],'sourceEditionSha256':pins['source-edition/edition.json'],'validationManifestSha256':pins['validation/manifest.json'],'axesSha256':pins['axes/four-axes.json'],'files':pins})
 return root
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 try:root=build(a.output)
 except ValueError as exc:p.error(str(exc))
 print(json.dumps({'synthetic':True,'WRITING_TEMPLATES_DATA_ROOT':str(root),'records':4},indent=2))
