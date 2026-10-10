"""Exercise the actual stdin helper on useful synthetic cards and contract failures."""
from pathlib import Path
import json,subprocess,sys,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
HELPER=ROOT/'skills/live-table-director/scripts/check_live_output.py'
EXAMPLE=(ROOT/'examples/live-run-card.txt').read_text()
def run(text,cwd=None):
    return subprocess.run([sys.executable,'-B',str(HELPER)],input=text,text=True,capture_output=True,cwd=cwd,timeout=5)
class LiveCardTests(unittest.TestCase):
    def test_real_sample_passes_without_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            result=run(EXAMPLE,directory);self.assertEqual(result.returncode,0,result.stderr);self.assertTrue(result.stdout.startswith('ok: '));self.assertEqual(list(Path(directory).iterdir()),[])
    def test_missing_required_fields_fail(self):
        for marker in ['CLOCK | SCENE | ENERGY | SPOTLIGHT','NOW:','SAY:','ASK:','WATCH:','CUT WHEN:','NEXT:']:
            with self.subTest(marker=marker):
                result=run(EXAMPLE.replace(marker,''));self.assertEqual(result.returncode,1);self.assertIn('missing marker: '+marker,result.stderr)
    def test_word_ceiling_140_passes_141_fails(self):
        # These literal ASCII fixtures have eleven marker words plus129/130cuewords.
        base='CLOCK | SCENE | ENERGY | SPOTLIGHT\nNOW: {words}\nSAY:\nASK:\nWATCH:\nCUT WHEN:\nNEXT:\n'
        accepted=run(base.format(words=' '.join(['cue']*129)));rejected=run(base.format(words=' '.join(['cue']*130)))
        self.assertEqual(accepted.returncode,0,accepted.stderr);self.assertIn('140 words',accepted.stdout);self.assertEqual(rejected.returncode,1);self.assertIn('141 exceeds 140',rejected.stderr)
    def test_diagnostic_or_shaming_labels_fail(self):
        for label in ['shy','anxious','ADHD','autistic','bored','problem player','power gamer','diagnosis']:
            with self.subTest(label=label):
                result=run(EXAMPLE+'\n'+label);self.assertEqual(result.returncode,1);self.assertIn('diagnostic or shaming',result.stderr)
    def test_preserved_five_scenarios_have_real_checked_cards(self):
        scenarios=json.loads((ROOT/'skills/live-table-director/tests/live-output-scenarios.json').read_text())['scenarios']
        moves={
            'eval-001-quiet-newcomer':('Invite a short preference with a pass option.','You may answer briefly, write it, or pass and return.','Whether each person gets a turn.'),
            'eval-002-dominant-veteran':('Redistribute spotlight before the next plan.','Let each person give one option before we answer.','Whether the next speaker finishes without interruption.'),
            'eval-003-npc-tunnel':('End the NPC speech at a player choice.','I can offer the map or the warning; which do you ask about?','Whether a player chooses the next action.'),
            'eval-010-derailment':('With40 minutes left, protect the finale by cutting optional beats.','We can follow this lead or move toward the final scene.','Whether the group selects a route.'),
            'eval-014-tech-failure':('Switch to an analog description and preserve the decision.','The bridge shakes; the path ahead splits in two.','Whether everyone understands the visible routes.')}
        self.assertEqual(len(scenarios),5)
        for case in scenarios:
            move,say,signal=moves[case['id']];text=f'CLOCK | SCENE | ENERGY | SPOTLIGHT\n40 minutes | Current choice | Visible discussion | Next player\nNOW: {move}\nSAY: "{say}"\nASK: "Which option do you choose? You may pass."\nWATCH: {signal}\nCUT WHEN: The table chooses or needs clarification.\nNEXT: Frame the selected route or finale.\n'
            with self.subTest(scenario=case['id']):
                result=run(text);self.assertEqual(result.returncode,0,result.stderr)
                for phrase in case['must_include']:self.assertIn(phrase.casefold(),text.casefold())
                for phrase in case['must_not_include']:self.assertNotIn(phrase.casefold(),text.casefold())
if __name__=='__main__':unittest.main()
