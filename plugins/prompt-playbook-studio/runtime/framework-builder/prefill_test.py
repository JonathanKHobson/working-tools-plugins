"""Focused tests against the shipped source catalog and editor field shapes."""

import json
from pathlib import Path
import unittest

from prefill import validate_prefill


CATALOG = {item['id']: item for item in json.loads(
    (Path(__file__).parent / 'data/catalog.json').read_text(encoding='utf-8'))['items']}


class PrefillTest(unittest.TestCase):
    def test_partial_real_catalog_values_and_context(self):
        values = {'goal': 'Make a decision', 'stage': 'plan', 'ctx': 'Small team'}
        result = validate_prefill(CATALOG['pattern-picker'], values)
        self.assertEqual(result, values)
        self.assertIsNot(result, values)

    def test_unknown_keys_and_oversized_values(self):
        item = CATALOG['pattern-picker']
        for values in ({'__proto__': 'x'}, {'constructor': 'x'}, {'goal': 'x' * 8001},
                       {'ctx': 'x' * 8001}, {'goal': ['wrong']}):
            with self.subTest(values=list(values)):
                with self.assertRaises(ValueError):
                    validate_prefill(item, values)
        with self.assertRaisesRegex(ValueError, 'total input'):
            validate_prefill({'fields': [{'key': f'k{i}', 'type': 'text'} for i in range(13)]},
                             {f'k{i}': 'x' * 8000 for i in range(13)})

    def test_select_multiselect_checkbox_and_typeahead(self):
        picker = CATALOG['pattern-picker']
        with self.assertRaisesRegex(ValueError, 'authored option'):
            validate_prefill(picker, {'stage': 'invented'})
        with self.assertRaisesRegex(ValueError, 'expected text'):
            validate_prefill(picker, {'stage': ['plan']})
        rubric = CATALOG['depth-method-prompt-builder']
        self.assertEqual(validate_prefill(rubric, {'rubric': ['Clarity', 'Accuracy', 'Clarity']}),
                         {'rubric': ['Clarity', 'Accuracy']})
        with self.assertRaisesRegex(ValueError, 'authored option'):
            validate_prefill(rubric, {'rubric': ['Made up']})
        tarot = CATALOG['tarot-spread-reflection']
        self.assertEqual(validate_prefill(tarot, {'reversals': True}), {'reversals': True})
        with self.assertRaisesRegex(ValueError, 'true or false'):
            validate_prefill(tarot, {'reversals': 1})
        self.assertEqual(validate_prefill(CATALOG['five-w-one-h-kipling'], {'who': 'A reader'}),
                         {'who': 'A reader'})

    def test_simple_repeater_normalizes_rows_and_enforces_max(self):
        item = CATALOG['active-imagination-dialogue']
        self.assertEqual(validate_prefill(item, {'figures': ['Critic', 'Future self']}),
                         {'figures': 'Critic\nFuture self'})
        with self.assertRaisesRegex(ValueError, 'too many rows'):
            validate_prefill(item, {'figures': ['x'] * 6})
        with self.assertRaisesRegex(ValueError, 'expected text'):
            validate_prefill(item, {'figures': ['x', 3]})
        with self.assertRaisesRegex(ValueError, '8000 characters'):
            validate_prefill(item, {'figures': ['x' * 5000, 'y' * 5000]})

    def test_group_repeater_partial_rows_and_nested_validation(self):
        item = CATALOG['okr-goal-setting']
        values = {'key_results': [{'metric': 'Time to first value', 'type': 'leading (predictive/behavioral)'},
                                  {'target': 'Four days'}]}
        self.assertEqual(validate_prefill(item, values), values)
        self.assertIsNot(validate_prefill(item, values)['key_results'], values['key_results'])
        for bad in ([{'__proto__': 'x'}], [{'type': 'invented'}], [{'metric': 9}]):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    validate_prefill(item, {'key_results': bad})


if __name__ == '__main__':
    unittest.main()
