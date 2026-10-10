import importlib.util
from pathlib import Path
import unittest

P = Path(__file__).resolve().parents[1] / 'skills/content-calendar/scripts/linkedin_metrics.py'
spec = importlib.util.spec_from_file_location('metrics', P)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class MetricsTests(unittest.TestCase):
    def row(self, **kwargs):
        return dict(id='a', impressions=1000, reactions=30, comments=8, reposts=2,
                    followers_at_posting=500, **kwargs)

    def test_arithmetic_not_reach(self):
        got = m.analyze([self.row()])['records'][0]['metrics']
        self.assertEqual(got['interaction_rate_pct'], 4)
        self.assertEqual(got['impression_follower_multiple'], 2)
        self.assertIsNone(got['members_reached'])

    def test_missing_is_not_zero(self):
        row = self.row(); del row['comments']
        got = m.analyze([row])['records'][0]
        self.assertIsNone(got['metrics']['interaction_rate_pct'])
        self.assertIn('comments', got['missing'])

    def test_zero_denominators(self):
        row = self.row(); row.update(impressions=0, reactions=0, followers_at_posting=0)
        got = m.analyze([row])['records'][0]['metrics']
        for key in ('interaction_rate_pct', 'comment_reaction_ratio', 'impression_follower_multiple'):
            self.assertIsNone(got[key])

    def test_bad_numbers(self):
        for bad in (-1, float('nan'), float('inf'), True, '20', 10**500):
            row = self.row(); row['impressions'] = bad
            with self.assertRaises(ValueError): m.analyze([row])

    def test_duplicate_and_bad_input(self):
        for rows in ([self.row(), self.row()], {}, [None], [{'id': ''}]):
            with self.assertRaises(ValueError): m.analyze(rows)

    def test_time_validation(self):
        for timestamp in ('invalid', '2026-01-01T12:00:00'):
            with self.assertRaises(ValueError): m.analyze([self.row(published_at=timestamp)])
        with self.assertRaises(ValueError):
            m.analyze([self.row(published_at='2026-01-02T12:00:00Z', observed_at='2026-01-01T12:00:00Z')])

    def test_ranking_excludes_unknown(self):
        a=self.row(); b={'id':'b'}; c=self.row(); c.update(id='c', comments=48)
        result=m.analyze([a,b,c], 'interaction_rate_pct')
        self.assertEqual([x['id'] for x in result['ranking']], ['c','a'])
        self.assertEqual(result['medians']['interaction_rate_pct']['n'], 2)

    def test_comparability_warnings(self):
        a=self.row(published_at='2026-01-01T12:00:00Z', observed_at='2026-01-08T12:00:00Z', scope='organic')
        b=dict(a, id='b', observed_at='2026-01-02T12:00:00Z', scope='paid')
        got=m.analyze([a,b])
        self.assertTrue(any('Different post ages' in w for w in got['warnings']))
        self.assertTrue(any('Mixed organic/paid' in w for w in got['warnings']))


if __name__ == '__main__': unittest.main()
