"""Scoped evidence validation. Fixtures are synthetic, not product QA receipts."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/codex_artifact_quality_gate.py'
spec = importlib.util.spec_from_file_location('quality_gate', SCRIPT)
gate = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gate
spec.loader.exec_module(gate)


class EvidenceGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'page.html'
        self.render = self.root / 'render.png'
        self.source.write_text('<p>Example text</p>')
        self.render.write_bytes(b'synthetic test fixture, not rendered proof')
        self.report_path = self.root / 'review.json'
        self.state_path = self.root / 'state.json'
        self.report = {
            'schema_version': 1, 'artifact_kind': 'interface',
            'files': [{'path': str(p), 'sha256': gate.file_digest(p), 'role': r}
                      for p, r in [(self.source, 'source'), (self.render, 'render')]],
            'scope': {'regions': ['example'], 'states': ['desktop-light'], 'exclusions': [],
                      'responsive': {'applicable': False, 'reason': 'Fixture has one fixed viewport'},
                      'themes': {'applicable': False, 'reason': 'Fixture only supports light theme'}},
            'coverage': [{'region': 'example', 'state': 'desktop-light', 'render': str(self.render),
                          'text_targets': ['card p', 'badge']}],
            'contrast': [{'region': 'example', 'state': 'desktop-light', 'target': t,
                          'foreground': '#222222', 'background': '#ffffff',
                          'font_size_px': 16, 'font_weight': 400} for t in ['card p', 'badge']],
            'checks': {c: {'status': 'pass', 'evidence': 'Synthetic fixture evidence'} for c in gate.REVIEW_CATEGORIES},
            'blockers': [],
        }

    def write(self):
        self.report_path.write_text(json.dumps(self.report))
        return str(self.report_path)

    def errors(self):
        return gate.validate_review(self.write())

    def mark(self, name='visual_qa'):
        return gate.update_obligation(name, status='done', reviewer='test reviewer',
                                      evidence=self.write(), state_path=self.state_path)

    def test_fixed_nested_text_and_badge_pass(self):
        self.assertEqual(self.errors(), [])
        self.mark()
        self.assertEqual(gate.status_payload(self.state_path)['status'], 'clear')

    def test_original_pale_inherited_paragraph_and_badge_fail(self):
        for item in self.report['contrast']:
            item['foreground'] = '#d5cec2'
        errors = self.errors()
        self.assertEqual(sum('Contrast failed' in e for e in errors), 2)
        with self.assertRaises(ValueError):
            self.mark()

    def test_outer_card_sample_does_not_cover_descendants(self):
        self.report['contrast'] = []
        self.assertTrue(any('Missing descendant' in e for e in self.errors()))

    def test_missing_and_nonpassing_categories_fail(self):
        for category in gate.REVIEW_CATEGORIES:
            original = copy.deepcopy(self.report['checks'])
            for status in ('pending', 'not_run', 'failed', 'unsupported', 'not_applicable'):
                self.report['checks'][category]['status'] = status
                self.assertTrue(self.errors(), (category, status))
            self.report['checks'] = copy.deepcopy(original)
            del self.report['checks'][category]
            self.assertTrue(self.errors(), category)
            self.report['checks'] = original

    def test_new_states_need_rendered_coverage(self):
        self.report['scope']['states'].append('narrow-dark')
        self.assertTrue(any('Missing rendered coverage' in e for e in self.errors()))

    def test_reasoned_specific_state_exclusion(self):
        self.report['scope']['states'].append('narrow-dark')
        self.report['scope']['exclusions'] = [{'scope': 'example@narrow-dark', 'reason': 'Component is not present in this state'}]
        self.assertEqual(self.errors(), [])

    def test_responsive_and_theme_applicability_required(self):
        for dimension in ('responsive', 'themes'):
            original = self.report['scope'].pop(dimension)
            self.assertTrue(self.errors())
            self.report['scope'][dimension] = original
            self.report['scope'][dimension]['applicable'] = True
            self.assertTrue(self.errors())
            self.report['scope'][dimension]['applicable'] = False

    def test_changed_source_or_render_invalidates_completed_mark(self):
        for path in (self.source, self.render):
            original = path.read_bytes()
            self.mark()
            path.write_bytes(b'changed')
            self.assertEqual(gate.status_payload(self.state_path)['status'], 'pending')
            path.write_bytes(original)

    def test_changed_report_invalidates_mark_even_if_still_valid(self):
        self.mark()
        self.report['checks']['aesthetics']['evidence'] += ' changed'
        self.write()
        self.assertEqual(gate.status_payload(self.state_path)['status'], 'pending')

    def test_free_text_marker_and_unknown_schema_rejected(self):
        with self.assertRaises(ValueError):
            gate.update_obligation('visual_qa', status='done', reviewer='test', evidence='looks fine', state_path=self.state_path)
        self.report['schema_version'] = 999
        self.assertTrue(self.errors())

    def test_nonvisual_reasoned_skip_and_detection(self):
        self.assertEqual(gate.detect_obligations('Fix backend configuration'), [])
        state = gate.update_obligation('visual_qa', status='skipped', note='Only backend configuration changed; no visible output', state_path=self.state_path)
        self.assertEqual(gate.pending_obligations(state), [])
        with self.assertRaises(ValueError):
            gate.update_obligation('visual_qa', status='skipped', state_path=self.state_path)

    def test_failed_unknown_and_legacy_done_are_unresolved(self):
        for status in ('failed', 'unsupported', 'not_run', 'done'):
            state = gate.build_state('Build a website', ['visual_qa'])
            state.obligations['visual_qa']['status'] = status
            self.assertEqual(gate.pending_obligations(state), ['visual_qa'])

    def test_followup_does_not_erase_unresolved_obligation(self):
        gate.detect_and_store('Fix website contrast', state_path=self.state_path)
        state = gate.detect_and_store('Thanks, keep working', state_path=self.state_path)
        self.assertEqual(gate.pending_obligations(state), ['visual_qa', 'design_taste'])

    def test_corrupt_state_is_pending(self):
        self.state_path.write_text('{bad')
        self.assertEqual(gate.status_payload(self.state_path)['status'], 'pending')

    def test_malformed_scope_is_pending(self):
        self.state_path.write_text(json.dumps({'scopes': {gate.current_scope_key(): {'obligations': []}}}))
        self.assertEqual(gate.status_payload(self.state_path)['status'], 'pending')

    def test_malformed_evidence_is_unresolved(self):
        self.assertTrue(gate.obligation_errors('visual_qa', {'status': 'done', 'reviewer': 'test', 'evidence': ['bad']}))

    def test_no_scope_review_cannot_verify_completion(self):
        self.assertEqual(gate.main(['verify', '--state-path', str(self.state_path)]), 1)

    def test_unsupported_composited_color_is_not_passed(self):
        self.report['contrast'][0]['background'] = 'rgba(255,255,255,.5)'
        self.assertTrue(any('Unsupported' in e for e in self.errors()))

    def test_threshold_uses_actual_font_metrics(self):
        sample = self.report['contrast'][0]
        sample['foreground'] = '#888888'  # approx 3.54:1, insufficient for body copy
        self.assertTrue(self.errors())
        sample['font_size_px'] = 24
        self.assertEqual(self.errors(), [])

    def test_document_can_reasonably_exclude_interaction(self):
        self.report['artifact_kind'] = 'document'
        self.report['checks']['usability'] = {'status': 'not_applicable', 'reason': 'Static decorative specimen, no interaction flow'}
        self.assertEqual(self.errors(), [])

    def test_communication_mark_requires_final_artifact_and_named_reviewer(self):
        artifact = self.root / 'final-email.txt'
        artifact.write_text('Final message')
        for reviewer, path in [('other reviewer', str(artifact)),
                               (gate.COMMUNICATION_REVIEWER, str(self.root / 'missing.txt'))]:
            with self.assertRaises(ValueError):
                gate.update_obligation('communication_review', status='done',
                    reviewer=reviewer, artifact=path, evidence='Reviewed final phrasing', state_path=self.state_path)
            self.assertFalse(self.state_path.exists())
        gate.update_obligation('communication_review', status='done',
            reviewer=gate.COMMUNICATION_REVIEWER, artifact=str(artifact),
            evidence='Reviewed final phrasing', state_path=self.state_path)
        self.assertEqual(gate.status_payload(self.state_path)['status'], 'clear')
        artifact.write_text('Changed message')
        payload = gate.status_payload(self.state_path)
        self.assertEqual(payload['status'], 'pending')
        self.assertIn('changed', payload['errors']['communication_review'][0])
        artifact.unlink()
        self.assertEqual(gate.status_payload(self.state_path)['status'], 'pending')

    def test_legacy_communication_mark_is_unverified(self):
        state = gate.build_state('Write email copy', ['communication_review'])
        state.obligations['communication_review'].update(
            status='done', reviewer='writing review', evidence='looks good', artifact='email.txt')
        gate.write_state(state, self.state_path)
        self.assertEqual(gate.status_payload(self.state_path)['status'], 'pending')

if __name__ == '__main__':
    unittest.main()
