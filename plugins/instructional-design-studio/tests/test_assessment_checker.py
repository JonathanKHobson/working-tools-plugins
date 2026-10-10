"""Regression tests for assessment bank structure and CLI failure handling."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = (Path(__file__).resolve().parents[1] / 'skills' / 'assessment-rubric-design'
          / 'scripts' / 'check_assessment.py')
SPEC = importlib.util.spec_from_file_location('check_assessment', SCRIPT)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def bank():
    return {
        'schema_version': 'assessment-authoring-1',
        'id': 'bank-1', 'status': 'draft', 'purpose': 'formative',
        'intended_use': 'Guide revision', 'conditions': {'resources': 'source packet'},
        'outcomes': [{'id': 'LO-1', 'claim': 'Interpret conflicting notes',
                      'evidence': 'Names the unresolved conflict',
                      'decision_use': 'Target follow-up practice'}],
        'sources': [{'id': 'note-1', 'title': 'Source packet', 'version': '1',
                     'kind': 'fictional', 'content': 'Two target dates; neither approved.'}],
        'items': [{
            'id': 'Q-1', 'objective_ids': ['LO-1'], 'claim': 'Interpret notes',
            'evidence': 'Declines to invent approval',
            'source_refs': [{'source_id': 'note-1', 'locator': 'paragraph 1',
                             'supports': 'No approved date'}],
            'format': 'single-select', 'stem': 'What is supported?',
            'response_directions': 'Select one answer.',
            'options': [{'id': 'A', 'text': 'Date approved', 'rationale': 'Invented approval'},
                        {'id': 'B', 'text': 'Unresolved', 'rationale': 'Preserves conflict'}],
            'key': {'correct_option_ids': ['B']},
            'scoring': {'policy': 'exact-match', 'points_possible': 1},
            'feedback': {'explanation': 'Neither note approves a date.',
                         'next_step': 'Check decision authority.'},
            'cognitive_demand': {'label': 'analyze', 'rationale': 'Compare evidence'},
            'difficulty': {'intended': 'intermediate', 'observed': None},
            'review': {'source_verified': False, 'independent_key_check': False,
                       'pilot_status': 'not-piloted'},
        }],
    }


def messages(changed):
    errors, warnings = checker.validate(changed)
    return '\n'.join(errors), '\n'.join(warnings)


class AssessmentCheckerTests(unittest.TestCase):
    def test_valid_draft_has_review_warnings_only(self):
        errors, warnings = messages(bank())
        self.assertEqual(errors, '')
        self.assertIn('draft status', warnings)
        self.assertIn('not piloted', warnings)

    def test_duplicate_and_dangling_ids_fail(self):
        data = bank()
        data['outcomes'].append(copy.deepcopy(data['outcomes'][0]))
        data['items'][0]['options'][1]['id'] = 'A'
        data['items'][0]['key']['correct_option_ids'] = ['missing']
        data['items'][0]['objective_ids'] = ['LO-missing']
        data['items'][0]['source_refs'][0]['source_id'] = 'source-missing'
        errors, _ = messages(data)
        for expected in ('duplicate id LO-1', 'duplicate id A', 'unknown options',
                         'unknown outcomes', 'unknown or missing source', 'uncovered IDs'):
            self.assertIn(expected, errors)

    def test_multiselect_requires_consistent_count_and_safe_partial_rule(self):
        data = bank()
        item = data['items'][0]
        item['format'] = 'multiselect'
        item['options'].append({'id': 'C', 'text': 'Needs confirmation', 'rationale': 'Supported'})
        item['key']['correct_option_ids'] = ['B', 'C']
        item['select_count'] = 2
        item['scoring'] = {'policy': 'partial-credit', 'points_possible': 2,
                           'partial_credit_rule': {'correct_selection_points': 1,
                                                   'incorrect_selection_points': -1,
                                                   'omission_points': 0,
                                                   'minimum_score': 0}}
        self.assertEqual(messages(data)[0], '')
        item['select_count'] = 1
        item['scoring']['partial_credit_rule']['correct_selection_points'] = 1.1
        item['scoring']['partial_credit_rule']['incorrect_selection_points'] = -0.1
        errors, _ = messages(data)
        self.assertIn('must match keyed option count', errors)
        self.assertIn('correct-only raw score', errors)
        self.assertIn('selecting every option earns full credit', errors)

    def test_partial_credit_cannot_make_full_credit_impossible(self):
        data = bank()
        item = data['items'][0]
        item['format'] = 'multiselect'
        item['options'].append({'id': 'C', 'text': 'Needs confirmation', 'rationale': 'Supported'})
        item['key']['correct_option_ids'] = ['B', 'C']
        item['select_count'] = 2
        item['scoring'] = {'policy': 'partial-credit', 'points_possible': 2,
                           'partial_credit_rule': {'correct_selection_points': 0.5,
                                                   'incorrect_selection_points': -0.5,
                                                   'omission_points': 0,
                                                   'minimum_score': 0}}
        errors, _ = messages(data)
        self.assertIn('correct-only raw score 1.0 differs from points_possible 2', errors)
        self.assertNotIn('selecting every option earns full credit', errors)

    def test_numeric_checks_finite_value_tolerance_and_units(self):
        data = bank()
        item = data['items'][0]
        item['format'] = 'numeric'
        item.pop('options')
        item['key'] = {'value': 10, 'tolerance': 0.5, 'units': 'kg'}
        item['scoring']['policy'] = 'numeric-tolerance'
        self.assertEqual(messages(data)[0], '')
        item['key'] = {'value': float('nan'), 'tolerance': -1, 'units': ''}
        errors, _ = messages(data)
        self.assertIn('key.value: finite number required', errors)
        self.assertIn('key.tolerance: nonnegative finite number required', errors)
        self.assertIn('key.units: nonempty string required', errors)

    def test_constructed_response_criteria_and_scores(self):
        data = bank()
        item = data['items'][0]
        item['format'] = 'short-response'
        item.pop('options')
        item['key'] = {}
        item['scoring'] = {'policy': 'criterion-based', 'points_possible': 2,
                           'criteria': [{'id': 'evidence', 'description': 'Identifies conflict',
                                         'points': 1},
                                        {'id': 'action', 'description': 'Seeks confirmation',
                                         'points': 1}]}
        self.assertEqual(messages(data)[0], '')
        item['scoring']['criteria'][1]['points'] = -1
        errors, _ = messages(data)
        self.assertIn('positive finite number required', errors)
        item['scoring']['criteria'][1]['points'] = 0.5
        errors, _ = messages(data)
        self.assertIn('differs from points_possible', errors)

    def test_malformed_shapes_and_unsupported_format_do_not_raise(self):
        data = bank()
        data['outcomes'] = [42]
        data['sources'] = 'bad'
        data['items'][0]['format'] = ['matching']
        data['items'][0]['review'] = []
        errors, _ = messages(data)
        self.assertIn('outcomes[0]: object required', errors)
        self.assertIn('sources: nonempty list required', errors)
        self.assertIn('unsupported format', errors)

    def test_empty_observation_and_unsupported_positive_review_are_warned(self):
        data = bank()
        item = data['items'][0]
        item['difficulty']['observed'] = {}
        item['review']['source_verified'] = True
        errors, warnings = messages(data)
        self.assertEqual(errors, '')
        self.assertIn('observed difficulty has no evidence', warnings)
        self.assertIn('positive review flags need reviewer, reviewed_at, and evidence', warnings)

    def test_cli_reports_bad_json_without_modifying_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'bank.json'
            path.write_text('{bad', encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(json.loads(result.stdout)['ok'])
            self.assertEqual(path.read_text(encoding='utf-8'), '{bad')


if __name__ == '__main__':
    unittest.main()
