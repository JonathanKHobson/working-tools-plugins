"""Regression checks for local evidence, bounds and filesystem adaptations."""
import json
import math
import os
import tempfile
import unittest
from _load import load, example, ROOT

panel = load('founder-consumer', 'panel')
ue = load('founder-cfo', 'unit_economics')
vw = load('founder-pricing', 'van_westendorp')
plan = load('founder-plan', 'compile')


def numbers():
    with open(example('founder-cfo', 'example.json')) as f:
        return json.load(f)


class Adapter(unittest.TestCase):
    def test_all_eleven_methods_require_adapter(self):
        from pathlib import Path
        methods = list((Path(ROOT) / 'skills').glob('*/SKILL.md'))
        self.assertEqual(len(methods), 11)
        for p in methods:
            self.assertIn('../../ADAPTER.md', p.read_text())
        self.assertFalse((Path(ROOT) / '.claude-plugin').exists())

    def test_panel_default_and_bounds(self):
        with open(example('founder-consumer', 'customer.example.json')) as f:
            customer = json.load(f)
        self.assertEqual(len(panel.deal(customer)), 8)
        for n in (0, -1, 1001, True):
            with self.assertRaises(panel.PanelError): panel.deal(customer, n)
        for share in (-1, math.inf, math.nan):
            customer['segments'][0]['share'] = share
            with self.assertRaises(panel.PanelError): panel.deal(customer)

    def test_panel_init_preserves_existing_state_and_rejects_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            panel.init(d, example('founder-consumer', 'customer.example.json'), example('founder-consumer', 'pitch.example.md'), seed=7)
            with self.assertRaises(panel.PanelError):
                panel.init(d, example('founder-consumer', 'customer.example.json'), example('founder-consumer', 'pitch.example.md'))
            self.assertEqual(len(panel.write_briefs(d)), 8)
            for wave in (0, -1, 13):
                with self.assertRaises(panel.PanelError): panel.write_briefs(d, wave)
            with self.assertRaises(panel.PanelError): panel._path(d, '..', 'outside')
            with open(os.path.join(d, 'personas.json'), 'w') as f:
                json.dump([{'id': '../../outside'}], f)
            with self.assertRaises(panel.PanelError): panel.write_briefs(d)

    def test_invalid_save_does_not_destroy_existing_answer(self):
        with tempfile.TemporaryDirectory() as d:
            panel.init(d, example('founder-consumer', 'customer.example.json'), example('founder-consumer', 'pitch.example.md'))
            answer = {'id': 'P001', 'buys': False, 'reason_code': 'price', 'reason': 'Synthetic price objection'}
            path = panel.save(d, 'P001', json.dumps(answer))
            with self.assertRaises(panel.PanelError): panel.save(d, 'P001', '[] {"id":"P001"}')
            with open(path) as f: self.assertEqual(json.load(f), answer)
            self.assertIn('untrusted data', panel.BRIEF)

    def test_financial_inputs_reject_nonfinite_negative_and_zero_days(self):
        for key, value in [('price', math.nan), ('price', math.inf), ('price', True), ('days_per_month', 0), ('plan_per_day', -1), ('capacity_per_day', math.inf)]:
            spec = numbers(); spec[key] = value
            with self.assertRaises(ue.NumbersError): ue.analyse(spec)
        spec = numbers(); spec['variable'][0]['cost'] = -1
        with self.assertRaises(ue.NumbersError): ue.analyse(spec)
        with self.assertRaises(ue.NumbersError): ue.analyse(numbers(), volume=-1)

    def test_pricing_refuses_infinite_and_nonprogressing_grids(self):
        rows = [(2, 4, 6, 8)] * 5
        for step in (0, -1, math.inf, math.nan, 1e-20):
            with self.assertRaises(vw.PricingError): vw.analyse(rows, step=step)
        self.assertIsNone(vw._f('Infinity'))
        with self.assertRaises(vw.PricingError): vw.analyse([(2, 4, 6, math.inf)] * 5)

    def test_synthetic_rates_cannot_change_scenario_or_claim_viability(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, 'numbers.json'), 'w') as f: json.dump(numbers(), f)
            os.mkdir(os.path.join(d, 'panel'))
            for buys in (0, 100):
                with open(os.path.join(d, 'panel/results.json'), 'w') as f:
                    json.dump({'buys': buys, 'passes': 100-buys, 'answered': 100, 'buy_rate': buys/100}, f)
                verdict, text = plan.compile_plan(d)
                self.assertEqual(verdict, 'Scenario passes')
                self.assertNotIn('Profitable', text)
                self.assertIn('viability are unverified', text)
                self.assertIn('does not measure demand', text)
            for threshold in (-1, 2, math.nan):
                with self.assertRaises(ValueError): plan.compile_plan(d, threshold)
            spec = numbers(); spec['plan_per_day'] = 10000
            with open(os.path.join(d, 'numbers.json'), 'w') as f: json.dump(spec, f)
            self.assertEqual(plan.compile_plan(d)[0], 'Scenario fails')
