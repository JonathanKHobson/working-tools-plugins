"""Distribution regressions: traversal, private bindings and reproducibility."""
import importlib.util,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
SPEC=importlib.util.spec_from_file_location('packages',Path(__file__).resolve().parents[1]/'scripts/packages.py')
p=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(p)
class DistributionTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.patch=patch.object(p,'ROOT',self.root);self.patch.start();self.addCleanup(self.patch.stop)
  self.record={'id':'fixture','version':'1.0.0','skills':1,'distribution':'prepared','description':'Synthetic fixture'}
  self.package=self.root/'plugins/fixture'
  for rel in ['plugin.json','.codex-plugin/plugin.json','.claude-plugin/plugin.json']:
   p.write_json(self.package/rel,{'name':'fixture','version':'1.0.0','$schema':'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'})
  for rel in ['README.md','LICENSE','THIRD_PARTY_NOTICES.md','PROVENANCE.json']:(self.package/rel).write_text('{}' if rel.endswith('.json') else 'Fixture\n')
  skill=self.package/'skills/demo/SKILL.md';skill.parent.mkdir(parents=True);skill.write_text('---\nname: demo\ndescription: Synthetic demonstration.\n---\nRun a safe example.\n')
  self.record['license']='MIT'
  for rel in ['plugin.json','.codex-plugin/plugin.json','.claude-plugin/plugin.json']:
   manifest=p.read_json(self.package/rel);manifest['license']='MIT';p.write_json(self.package/rel,manifest)
  (self.package/'LICENSING.md').write_text('Synthetic fixture under MIT.\n')
  scope={'package':'fixture','version':'1.0.0','files':[{'path':path.relative_to(self.package).as_posix(),'category':'fixture','license':'MIT','sha256':p.hashlib.sha256(path.read_bytes()).hexdigest()} for path in p.files(self.package)]}
  p.write_json(self.package/'LICENSE-SCOPE.json',scope)
  for rel,value in zip(['.agents/plugins/marketplace.json','.claude-plugin/marketplace.json'],p.catalogs([self.record])):p.write_json(self.root/rel,value)
  hashes={path.relative_to(self.package).as_posix():p.hashlib.sha256(path.read_bytes()).hexdigest() for path in p.files(self.package)}
  digest=p.sibling_module('source_inventory').tree_digest
  inventory={'id':'fixture','version':'1.0.0','canonical_source':{'id':'fixture','revision':{'kind':'sha256-distributable-tree-v1','sha256':digest(hashes)}},'files':hashes,'components':[{'id':'fixture:skills/demo/SKILL.md','kind':'skill','path':'skills/demo/SKILL.md'}],'excluded_source':{'files':0,'tree_sha256':digest({}),'dispositions':[]}}
  p.write_json(self.root/'catalog/source-inventory.json',{'schema_version':1,'packages':[inventory]})
  p.write_json(self.root/'catalog/coverage-baseline.json',{'schema_version':1,'entries':[{'id':'audit:fixture','canonical_owner':'fixture','disposition':'included','capability_effect':'Full synthetic fixture included.','expected_components':['fixture:skills/demo/SKILL.md'],'evidence':['synthetic audit fixture']}]})
  p.write_json(self.root/'catalog/packages.json',{'schema_version':1,'packages':[self.record]})
 def test_build_is_deterministic(self):
  a=p.build([self.record],self.root/'one');b=p.build([self.record],self.root/'two');self.assertEqual(a,b)
 def test_escape_and_private_binding_are_rejected(self):
  (self.package/'README.md').write_text('[escape](../../../../outside)\nPrivate binding: /Users/fixture/private.json\n')
  errors=p.validate_package(self.record);self.assertTrue(any('broken reference' in e for e in errors));self.assertTrue(any('private binding' in e for e in errors))
 def test_private_account_and_host_patterns_are_rejected_but_placeholders_are_allowed(self):
  target=self.root/'plugins/local-model-toolkit'; self.package.rename(target); self.package=target; self.record['id']='local-model-toolkit'
  cases=['Contact: realperson@gmail.com','/home/jonathan/private.json',r'C:\Users\Jonathan\secret.json','AIzaSyAbcdefghijklmnopqrstuvwxyz123']
  for value in cases:
   (self.package/'README.md').write_text(value)
   self.assertTrue(any('private binding' in e for e in p.validate_package(self.record)), value)
  (self.package/'README.md').write_text('Use name@example.com, /home/<user>/project, and C:\\Users\\<user>\\project.')
  self.assertFalse(any('private binding' in e for e in p.validate_package(self.record)))

 def test_symlink_is_rejected(self):
  (self.package/'bad').symlink_to('/etc/hosts')
  with self.assertRaisesRegex(ValueError,'Symlink'):p.validate_package(self.record)
 def test_manifest_mismatch_fails(self):
  d=p.read_json(self.package/'plugin.json');d['version']='2.0.0';p.write_json(self.package/'plugin.json',d)
  with self.assertRaisesRegex(ValueError,'identity/version'):p.validate([self.record])
 def test_stale_provenance_fails(self):
  p.write_json(self.package/'PROVENANCE.json',{'files':[{'source_relative':'README.md','output_sha256':'0'*64}]})
  self.assertTrue(any('hash mismatch' in e for e in p.validate_package(self.record)))
 def test_host_only_fields_are_rejected_in_portable_manifest(self):
  d=p.read_json(self.package/'plugin.json');d['skills']='./skills/'
  p.write_json(self.package/'plugin.json',d)
  self.assertTrue(any('unsupported portable manifest fields: skills' in e for e in p.validate_package(self.record)))
  del d['skills'];p.write_json(self.package/'plugin.json',d)
  d['skills']='./skills/';p.write_json(self.package/'.codex-plugin/plugin.json',d)
  self.assertEqual(p.validate_package(self.record),[])
 def test_reference_cannot_escape_individual_package(self):
  (self.root/'README.md').write_text('Shared repository documentation')
  (self.package/'README.md').write_text('[shared](../../README.md)')
  self.assertTrue(any('broken reference' in e for e in p.validate_package(self.record)))
 def test_compatibility_mcp_cannot_replace_portable_declaration(self):
  manifest=p.read_json(self.package/'.codex-plugin/plugin.json');manifest['mcpServers']='./.mcp.json'
  p.write_json(self.package/'.codex-plugin/plugin.json',manifest)
  p.write_json(self.package/'.mcp.json',{'mcpServers':{'fixture-server':{'command':'python3','args':['server.py']}}})
  self.assertTrue(any('require portable root mcp.json' in e for e in p.validate_package(self.record)))
  p.write_json(self.package/'mcp.json',{'mcpServers':{}})
  self.assertTrue(any('omits compatibility servers: fixture-server' in e for e in p.validate_package(self.record)))
  p.write_json(self.package/'mcp.json',{'mcpServers':{'fixture-server':{'type':'stdio','command':'python3','args':['server.py']}}})
  self.assertEqual(p.validate_package(self.record),[])
 def test_inline_claude_servers_require_portable_coverage(self):
  manifest=p.read_json(self.package/'.claude-plugin/plugin.json');manifest['mcpServers']={'fixture-server':{'command':'python3'}}
  p.write_json(self.package/'.claude-plugin/plugin.json',manifest)
  self.assertTrue(any('require portable root mcp.json' in e for e in p.validate_package(self.record)))
 def test_mcp_declaration_cannot_escape_package(self):
  p.write_json(self.root/'outside.json',{'mcpServers':{}})
  manifest=p.read_json(self.package/'.codex-plugin/plugin.json');manifest['mcpServers']='../../outside.json'
  p.write_json(self.package/'.codex-plugin/plugin.json',manifest)
  self.assertTrue(any('MCP declaration path missing or escaping package' in e for e in p.validate_package(self.record)))
 def test_source_rights_hold_stops_release_before_archive_write(self):
  self.record['licensing']={'releaseReview':{'status':'held','reason':'Synthetic rights question','files':{'LICENSE':p.hashlib.sha256((self.package/'LICENSE').read_bytes()).hexdigest()},'resolution':None}}
  out=self.root/'rights-held-release'
  with self.assertRaisesRegex(ValueError,'Release source-rights gate failed'):
   p.release([self.record],out)
  self.assertFalse(out.exists())
 def test_malformed_licensing_stops_release_before_archive_write(self):
  self.record['licensing']='held'
  out=self.root/'malformed-rights-release'
  with self.assertRaisesRegex(ValueError,'Release source-rights gate failed'):
   p.release([self.record],out)
  self.assertFalse(out.exists())
 def test_resolved_source_rights_review_allows_exact_fixture_release(self):
  self.record['licensing']={'releaseReview':{'status':'resolved','files':{'LICENSE':p.hashlib.sha256((self.package/'LICENSE').read_bytes()).hexdigest()},'resolution':{'reviewer':'Fixture reviewer','date':'2026-10-24','basis':'Explicit synthetic grant','evidence':'Fixture only'}}}
  out=self.root/'rights-resolved-release';p.release([self.record],out)
  self.assertTrue((out/'fixture-1.0.0.zip').is_file())
 def test_release_emits_canonical_file_and_component_mapping(self):
  out=self.root/'release'
  p.release([self.record],out)
  manifest=p.read_json(out/'source-release-manifest.json')
  row=manifest['packages'][0]
  self.assertEqual(row['canonical_source']['id'],'fixture')
  self.assertIn('skills/demo/SKILL.md',row['included_files'])
  self.assertEqual(row['components'][0]['id'],'fixture:skills/demo/SKILL.md')
  self.assertIn('fixture/v1.0.0',row['destinations']['download'])
  self.assertFalse(manifest['canonical_live_source_checked'])
  self.assertTrue(p.verify_archives(out)['passed'])
 def test_release_cannot_hide_removed_support_by_rebuilding(self):
  (self.package/'README.md').unlink()
  with self.assertRaisesRegex(ValueError,'missing file README.md'):
   p.release([self.record],self.root/'release')
  self.assertFalse((self.root/'release').exists())
 def test_release_requires_inventory_even_when_development_build_works(self):
  (self.root/'catalog/source-inventory.json').unlink()
  p.build([self.record],self.root/'development')
  with self.assertRaisesRegex(ValueError,'Release completeness gate failed'):
   p.release([self.record],self.root/'release')
 def test_changed_download_fails_release_manifest_verification(self):
  out=self.root/'release';p.release([self.record],out)
  archive=out/'fixture-1.0.0.zip'
  with p.zipfile.ZipFile(archive,'w') as package:package.writestr('README.md','Altered download')
  result=p.verify_archives(out)
  self.assertFalse(result['passed'])
  self.assertTrue(any('archive sha256 mismatch' in err for err in result['packages'][0]['errors']))
if __name__=='__main__':unittest.main()
