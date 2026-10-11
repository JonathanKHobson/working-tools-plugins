"""Publication must not turn incorporated instruction methods into prerequisites."""
import importlib.util
from pathlib import Path
import unittest

path=Path(__file__).resolve().parents[1]/'scripts/packages.py'
spec=importlib.util.spec_from_file_location('owned_packages',path)
packages=importlib.util.module_from_spec(spec);spec.loader.exec_module(packages)

class MethodOwnership(unittest.TestCase):
 def test_rejects_separate_method_pack_even_when_optional(self):
  for name in ('AIHumanizer','UI UX Designer','Cover Letter Writer','Injection Checker',
               'Prompt Engineer','Spreadsheet Human UX','Research Writing Guardrails','Codex Material Themes'):
   with self.subTest(name=name):
    self.assertTrue(packages.method_requirement_errors({'id':'fixture','requirements':['Optional '+name+' plugin']}))

 def test_preserves_real_execution_requirements(self):
  self.assertEqual(packages.method_requirement_errors({'id':'fixture','requirements':[
   'FFmpeg on PATH','DaVinci Resolve','Authenticated external API access',
   'Official OpenAI Product Design','Native Spreadsheets runtime','Python 3 for included scripts']}),[])

 def test_current_public_catalog_has_no_reintroduced_method_prerequisites(self):
  for record in packages.read_json(packages.ROOT/'catalog/packages.json')['packages']:
   with self.subTest(product=record['id']):
    self.assertEqual(packages.method_requirement_errors(record),[])

if __name__=='__main__':unittest.main()
