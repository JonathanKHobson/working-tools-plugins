"""Guard regressions with synthetic receipts; these are not model trial results."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
MODULE=ROOT/'scripts/release_manager/method_acceptance.py'
spec=importlib.util.spec_from_file_location('method_acceptance',MODULE)
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)

class MethodAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.primary='plugins/ux-design-toolkit/skills/task/SKILL.md'
        self.support='plugins/ux-design-toolkit/skills/task/support.md'
        self.write(self.primary,'Input: use supplied facts.\nSequence: inspect the task and repair the observed defect.\nEdge: unknown evidence stays unknown.\nOutput: concrete repair and limits.\nVerify: exercise authorized and benign paths.\n[Support](support.md)\n')
        self.write(self.support,'Full relevant support procedure.\n')
        self.write('scripts/packages.py',"def method_requirement_errors(row):\n return ['retired prerequisite'] if any('AIHumanizer' in v for v in row.get('requirements',[])) else []\n")
        self.json('catalog/packages.json',{'packages':[{'id':'ux-design-toolkit','requirements':['Actual runtime']} ]})
        self.json('tests/cases.json',{'protocol':'Return real requested output.','cases':[{'id':'CASE','request':'Repair supplied defect.'}]})
        self.json('tests/criteria.json',{'criteria':{'CASE':{'A':'Concrete repair with honest uncertainty.'}}})
        cap={'id':'ux','products':['ux-design-toolkit'],'cases':['CASE'],'sources':[self.primary,self.support],'procedure_sources':[self.primary],
             'watched_dirs':['plugins/ux-design-toolkit/skills/task'],'reviewed_requirements':{'ux-design-toolkit':['Actual runtime']}}
        cap['reviewed_layout']=gate._layout(self.root,cap)
        cap['reviewed_references']={p:gate._references(self.root,p) for p in cap['sources']}
        self.manifest={'schema_version':1,'cases':'tests/cases.json','criteria':'tests/criteria.json','required_hosts':['codex'],'capabilities':[cap]}
        self.json('catalog/method-acceptance.json',self.manifest)
        self.entry={'id':'ux-design-toolkit','changed_files':['skills/task/SKILL.md']}
        self.state=gate.snapshot(self.root,self.manifest,[cap])
        self.receipt=self.trial(self.state)
        self.hosts=[self.host(self.state)]

    def write(self,path,text):
        p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)

    def json(self,path,value):self.write(path,json.dumps(value))

    def trial(self,state):
        anchors=[{'id':str(i),'start':i,'end':i,'quote':line} for i,line in enumerate(state['procedure_lines'][self.primary],1)][:5]
        review={'sha256':state['procedure_sources'][self.primary],'kind':'complete-procedure','status':'pass'}
        for i,key in enumerate(('inputs','sequence','edge_cases','output','verification'),1):review[key]=[str(i)]
        output='The repaired path preserves source facts and reports the unavailable runtime check.'
        return {'schema_version':1,'kind':'executed-model-trial','run_id':'synthetic-unit-fixture','observed_at':'fixture only','provider':'fixture','exact_model':'fixture-model-v1','invocation_evidence_sha256':'a'*64,
                'source_hashes':state['source_hashes'],'case_hashes':state['case_hashes'],'contract_hashes':state['contract_hashes'],'method_only_providers_invoked':False,
                'reviewer':{'identity':'fixture reviewer','method':'source-and-output-review','limitations':'Synthetic unit test; no actual model invocation.'},
                'procedure_reviews':{self.primary:review},'procedure_source_evidence':{self.primary:anchors},'outputs':{'CASE':output},'output_hashes':{'CASE':gate.value_hash(output)},
                'evaluations':{'CASE':{'status':'pass','limitations':['fixture'],'criteria':{'A':{'status':'pass','reason':'Synthetic expected contract met.','output_evidence':['preserves source facts and reports']}}}}}

    def host(self,state):
        return {'kind':'verified-host-method-readback','host':'codex','status':'pass','source_hashes':state['source_hashes'],'contract_hashes':state['contract_hashes'],
                'observed_at':'fixture only','evidence_sha256':'b'*64,'checks':{'package_source_agreement':True,'loaded_method_agreement':True,'retired_prerequisites_absent':True},'limitations':['synthetic fixture']}

    def test_unchanged_current_receipt_reused_without_model_call(self):
        gate.validate_trial(self.state,self.receipt);gate.validate_trial(self.state,self.receipt)
        gate.validate_hosts(self.state,self.hosts,['codex'])

    def test_modified_full_support_invalidates_existing_trial(self):
        self.write(self.support,'Changed complete support procedure.\n')
        state=gate.snapshot(self.root,self.manifest,self.manifest['capabilities'])
        with self.assertRaisesRegex(ValueError,'Stale or missing trial source'):gate.validate_trial(state,self.receipt)

    def test_removed_primary_method_cannot_reuse_receipt(self):
        (self.root/self.primary).unlink()
        with self.assertRaisesRegex(ValueError,'Added/removed method support'):gate.snapshot(self.root,self.manifest,self.manifest['capabilities'])

    def test_added_support_or_reference_requires_reviewed_closure(self):
        self.write('plugins/ux-design-toolkit/skills/task/new.md','New requirement.')
        with self.assertRaisesRegex(ValueError,'reviewed closure'):gate.snapshot(self.root,self.manifest,self.manifest['capabilities'])
        (self.root/'plugins/ux-design-toolkit/skills/task/new.md').unlink()
        self.write(self.primary,(self.root/self.primary).read_text()+'[Other](../other.md)\n')
        with self.assertRaisesRegex(ValueError,'Unexpected method requirements/reference'):gate.snapshot(self.root,self.manifest,self.manifest['capabilities'])

    def test_routing_shell_review_and_fabricated_source_evidence_rejected(self):
        receipt=copy.deepcopy(self.receipt);receipt['procedure_reviews'][self.primary]['kind']='routing-shell'
        with self.assertRaisesRegex(ValueError,'routing shell'):gate.validate_trial(self.state,receipt)
        receipt=copy.deepcopy(self.receipt);receipt['procedure_source_evidence'][self.primary][0]['quote']='unseen source'
        with self.assertRaisesRegex(ValueError,'differs from current full source'):gate.validate_trial(self.state,receipt)

    def test_retired_and_unexpected_requirements_rejected(self):
        self.json('catalog/packages.json',{'packages':[{'id':'ux-design-toolkit','requirements':['Optional AIHumanizer']} ]})
        with self.assertRaisesRegex(ValueError,'retired prerequisite'):gate.snapshot(self.root,self.manifest,self.manifest['capabilities'])
        self.json('catalog/packages.json',{'packages':[{'id':'ux-design-toolkit','requirements':['Unexpected account']} ]})
        with self.assertRaisesRegex(ValueError,'Unexpected method/execution requirements'):gate.snapshot(self.root,self.manifest,self.manifest['capabilities'])

    def test_failed_missing_or_keyword_only_review_cannot_pass(self):
        for change in ('fail','missing','fake-evidence'):
            receipt=copy.deepcopy(self.receipt)
            if change=='fail':receipt['evaluations']['CASE']['criteria']['A']['status']='fail'
            elif change=='missing':receipt['evaluations']['CASE']['criteria'].clear()
            else:receipt['evaluations']['CASE']['criteria']['A']['output_evidence']=['all keywords passed']
            with self.subTest(change=change),self.assertRaises(ValueError):gate.validate_trial(self.state,receipt)

    def test_output_changed_after_semantic_review_rejected(self):
        receipt=copy.deepcopy(self.receipt);receipt['outputs']['CASE']='Changed output.'
        with self.assertRaisesRegex(ValueError,'output changed'):gate.validate_trial(self.state,receipt)

    def test_fixture_or_contract_weakening_invalidates_receipt(self):
        state=copy.deepcopy(self.state);state['case_hashes']['CASE']='c'*64
        with self.assertRaisesRegex(ValueError,'functional fixture'):gate.validate_trial(state,self.receipt)
        state=copy.deepcopy(self.state);state['contract_hashes']['ux']='c'*64
        with self.assertRaisesRegex(ValueError,'capability contract'):gate.validate_trial(state,self.receipt)

    def test_model_alias_not_resolved_execution_identity(self):
        receipt=copy.deepcopy(self.receipt);receipt['exact_model']='opus'
        with self.assertRaisesRegex(ValueError,'actual model identity'):gate.validate_trial(self.state,receipt)

    def test_host_content_or_claim_disagreement_blocks(self):
        hosts=copy.deepcopy(self.hosts);hosts[0]['source_hashes'][self.support]='c'*64
        with self.assertRaisesRegex(ValueError,'host method source'):gate.validate_hosts(self.state,hosts,['codex'])
        hosts=copy.deepcopy(self.hosts);hosts[0]['checks']['loaded_method_agreement']=False
        with self.assertRaisesRegex(ValueError,'disagreement'):gate.validate_hosts(self.state,hosts,['codex'])

    def test_unrelated_product_or_metadata_change_passes_through(self):
        self.assertEqual(gate.validate_release(self.root,{},[{'id':'other','changed_files':['README.md']}])['status'],'unaffected')
        self.assertEqual(gate.validate_release(self.root,{},[{'id':'ux-design-toolkit','changed_files':['plugin.json']}])['status'],'unaffected-method-content')

    def test_changed_method_requires_real_trial_and_host_receipts(self):
        with self.assertRaisesRegex(ValueError,'method_acceptance_receipt'):gate.validate_release(self.root,{},[self.entry])
        self.json('trial.json',self.receipt)
        config={'method_acceptance_receipt':str(self.root/'trial.json')}
        with self.assertRaisesRegex(ValueError,'host_receipts'):gate.validate_release(self.root,config,[self.entry])
        self.json('hosts.json',self.hosts);config['method_acceptance_host_receipts']=str(self.root/'hosts.json')
        self.assertEqual(gate.validate_release(self.root,config,[self.entry])['status'],'accepted')

if __name__=='__main__':unittest.main()
