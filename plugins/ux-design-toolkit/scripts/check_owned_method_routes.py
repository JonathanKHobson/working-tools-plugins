from pathlib import Path
import re,json,hashlib
import argparse
parser=argparse.ArgumentParser(description='Check internal UX method route closure without loading provider packs or claiming runtime UX evidence.')
parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
args=parser.parse_args();R=args.root.resolve()
paths=[R/'README.md',R/'docs/full-design-host-adapter.md',R/'docs/owned-methods-migration.md',R/'LICENSING.md',R/'THIRD_PARTY_NOTICES.md']
paths+=list((R/'docs/procedures').glob('*.md'))
paths+=list((R/'skills').glob('*/SKILL.md'))
paths+=[R/'skills/design-studio/references'/name for name in ('spreadsheet-usability.md','product-task-context.md','product-prototyping.md','product-experience-methods.md','usability-testing.md','application-appearance.md','design-comparison-qa.md','mobile-prototype-runtime.md','product-pain-research.md')]
paths+=[R/'libraries'/name/'PROVIDER.md' for name in ('product-design','uiuxdesigner','spreadsheet-human-ux','codex-material-themes')]
failures=[];checked_links=0

def anchor_set(text):
 result=set()
 for h in re.findall(r'^#{1,6}\s+(.+)$',text,re.M):
  h=re.sub(r'<[^>]*>','',h).lower().replace(' ','-')
  result.add(re.sub(r'[^\w-]','',h))
 return result

for p in paths:
 text=p.read_text();relative=str(p.relative_to(R))
 if '\u2014' in text and '/PROVIDER.md' in str(p): failures.append('Authored compatibility has em dash: '+relative)
 for href in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
  if re.match(r'\w+://',href): continue
  href=href.split(' "')[0].strip('<>'); raw,_,anchor=href.partition('#')
  target=(p.parent/raw).resolve() if raw else p
  # Existing docs link dirs intentionally; check their existence as well.
  if not target.exists(): failures.append(relative+' -> missing '+href); continue
  checked_links+=1
  if anchor and target.is_file() and target.suffix=='.md' and anchor not in anchor_set(target.read_text()): failures.append(relative+' -> missing heading '+href)

for p in (R/'docs/procedures').glob('*.md'):
 if re.search(r'libraries/(product-design|uiuxdesigner|spreadsheet-human-ux)/PROVIDER',p.read_text()): failures.append('Ordinary map still delegates '+p.name)
for p in (R/'skills').glob('*/SKILL.md'):
 if re.search(r'(spreadsheet-human-ux|uiuxdesigner|product-design):|libraries/(product-design|uiuxdesigner|spreadsheet-human-ux)/PROVIDER',p.read_text()): failures.append('Ordinary skill still delegates '+p.parent.name)

legacy={'product-design':['audit','design-qa','get-context','ideate','image-to-code','index','research','share','url-to-code','user-context'],'uiuxdesigner':['accessibility-audit','aidesigner-guide','color-typography-theming','component-design','conversion-optimization','dashboard-saas-ui','design-handoff','design-inspiration-trends','design-system-builder','design-to-code','ecommerce-ux','figma-workflow','forms-onboarding-ux','high-fidelity-mockups','information-architecture','landing-page-design','layout-grid-hierarchy','microinteractions-motion','mobile-app-ui','personas-journey-maps','prototyping','recommended-tools','redesign-makeover','ui-ux-designer','ui-ux-help','usability-testing','user-flows','ux-audit-critique','ux-career-interview','ux-portfolio-case-study','ux-research-plan','ux-writing-microcopy','website-ui-design','wireframes'],'spreadsheet-human-ux':['spreadsheet-human-ux']}
for lib,slugs in legacy.items():
 actual=anchor_set((R/'libraries'/lib/'PROVIDER.md').read_text())
 for slug in slugs:
  if slug not in actual: failures.append('Missing compatibility anchor '+lib+'#'+slug)

# Direct method fixture checks validate instruction coverage, not runtime UX outcomes.
fixture_requirements={
'capacity-workbook':('spreadsheet-usability.md',['blank means unknown','pasted values','add or deleting','Traceability','Return visit','135','15 hours','screen-reader']),
'booking-prototype':('product-prototyping.md',['Map 3–8 anchors','fictional slot data','duplicate','forced failure','pending','supported browser','authoritative','native build']),
'commerce':('product-experience-methods.md',['denominator','instrumentation errors','payment authorization','hidden subscriptions','stopping rule','sold-out','confirmed order']),
'participant-study':('usability-testing.md',['neutral','consent','pseudonym','denominators','counterexamples','expert task walkthrough','participant testing']),
'appearance-export-no-native-claim':('application-appearance.md',['Robin Li','supported settings','contrast','rollback','Do not reverse-engineer','prepared'])}
fixtures=[]
for name,(filename,terms) in fixture_requirements.items():
 text=(R/'skills/design-studio/references'/filename).read_text()
 # One spelling-independent structural edit term.
 if name=='capacity-workbook': terms=[t.replace('add or deleting','adding or deleting') for t in terms]
 missing=[term for term in terms if term.casefold() not in text.casefold()]
 if missing: failures.append(name+' missing '+repr(missing))
 fixtures.append({'fixture':name,'result':'pass' if not missing else 'fail','kind':'method instruction coverage only'})
report={'result':'pass' if not failures else 'fail','files_checked':len(paths),'local_links_checked':checked_links,'legacy_anchors_checked':sum(map(len,legacy.values())),'external_method_packs_read':0,'fixtures':fixtures,'failures':failures,'runtime_ui_or_participant_test':False}
print(json.dumps(report,indent=2))
raise SystemExit(bool(failures))
