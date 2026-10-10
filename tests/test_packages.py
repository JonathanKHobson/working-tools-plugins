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
  for rel,value in zip(['.agents/plugins/marketplace.json','.claude-plugin/marketplace.json'],p.catalogs([self.record])):p.write_json(self.root/rel,value)
 def test_build_is_deterministic(self):
  a=p.build([self.record],self.root/'one');b=p.build([self.record],self.root/'two');self.assertEqual(a,b)
 def test_escape_and_private_binding_are_rejected(self):
  (self.package/'README.md').write_text('[escape](../../../../outside)\nPrivate binding: /Users/fixture/private.json\n')
  errors=p.validate_package(self.record);self.assertTrue(any('broken reference' in e for e in errors));self.assertTrue(any('private binding' in e for e in errors))
 def test_symlink_is_rejected(self):
  (self.package/'bad').symlink_to('/etc/hosts')
  with self.assertRaisesRegex(ValueError,'Symlink'):p.validate_package(self.record)
 def test_manifest_mismatch_fails(self):
  d=p.read_json(self.package/'plugin.json');d['version']='2.0.0';p.write_json(self.package/'plugin.json',d)
  with self.assertRaisesRegex(ValueError,'identity/version'):p.validate([self.record])
 def test_stale_provenance_fails(self):
  p.write_json(self.package/'PROVENANCE.json',{'files':[{'source_relative':'README.md','output_sha256':'0'*64}]})
  self.assertTrue(any('hash mismatch' in e for e in p.validate_package(self.record)))
 def test_reference_cannot_escape_individual_package(self):
  (self.root/'README.md').write_text('Shared repository documentation')
  (self.package/'README.md').write_text('[shared](../../README.md)')
  self.assertTrue(any('broken reference' in e for e in p.validate_package(self.record)))
if __name__=='__main__':unittest.main()
