"""Contract checks exercise observable failures, scope limits and source safety."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'check_template_tokens.py'
spec = importlib.util.spec_from_file_location('template_tokens', SCRIPT)
checker = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = checker
spec.loader.exec_module(checker)


class TokenChecks(unittest.TestCase):
    def check(self, css, reference=None):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp).resolve() / 'adapted.css'
            path.write_text(css)
            original = None
            if reference is not None:
                original = Path(temp).resolve() / 'original.css'
                original.write_text(reference)
            return checker.check_source(path, original)

    def codes(self, result, field='errors'):
        return {x['code'] for x in result[field]}

    def test_multiple_declarations_and_alias_chain(self):
        result = self.check(':root { --base: #abc; --ink: var(--base); }\na { color:var(--ink); border: 1px solid var(--base); }')
        self.assertTrue(result['ok'])
        self.assertEqual(result['tokens']['declared'], ['--base', '--ink'])
        self.assertEqual(result['tokens']['used'], ['--base', '--ink'])

    def test_missing_token_reports_location(self):
        result = self.check('/* introduction */\na { color: var(--absent); }')
        self.assertFalse(result['ok'])
        self.assertEqual(result['errors'][0]['line'], 2)
        self.assertEqual(result['errors'][0]['file'], 'adapted.css')
        self.assertIn('undefined_token', self.codes(result))

    def test_valid_nested_multiple_and_empty_fallbacks(self):
        css = 'a { color:var(--x, var(--y, red)); box-shadow:var(--a,0 0 1px black),var(--b,0 0 2px white); padding:var(--empty,); }'
        self.assertTrue(self.check(css)['ok'])

    def test_invalid_nested_fallback(self):
        self.assertFalse(self.check('a{color:var(--x,var(--y));}')['ok'])

    def test_inactive_bad_fallback_not_an_error(self):
        self.assertTrue(self.check(':root{--ink:red}a{color:var(--ink,var(--absent));}')['ok'])

    def test_no_false_fail_strings_comments_and_data_url(self):
        css = '/* --bad:var(--missing); */ a{content:"var(--missing)"; background:url("data:image/svg+xml;<svg>{;:}</svg>"); color: red;}'
        result = self.check(css)
        self.assertTrue(result['ok'])
        self.assertEqual(result['tokens']['used'], [])

    def test_original_literals_are_valid(self):
        result = self.check('a {color:blue;margin:12px}', 'a {color:red;margin:10px}')
        self.assertTrue(result['ok'])
        self.assertEqual(result['tokens']['baseline_used'], [])

    def test_consumed_baseline_removed_even_with_literal_substitution(self):
        result = self.check(':root{--ink:red}a{color:red}', ':root{--ink:red}a{color:var(--ink)}')
        self.assertIn('baseline_token_removed', self.codes(result))
        self.assertEqual(result['errors'][0]['location'], 'reference')

    def test_scope_override_does_not_create_false_cycle(self):
        result = self.check(':root{--a:var(--b);--b:red}.card{--b:var(--a);color:var(--b)}')
        self.assertTrue(result['ok'])

    def test_exact_scope_and_duplicate_override(self):
        result = self.check('.card{--ink:var(--missing);--ink:red;color:var(--ink)}')
        # An overridden declaration can contain a missing var without affecting
        # computation, but its syntactic consumption remains part of the contract.
        self.assertIn('undefined_token', self.codes(result))
        result = self.check(':root{--ink:red;--ink:blue}a{color:var(--ink)}')
        self.assertEqual(result['status'], 'pass')

    def test_unrelated_scope_is_limit_not_claimed_global(self):
        result = self.check('.card{--ink:red} .other{color:var(--ink)}')
        self.assertEqual(result['status'], 'limited')
        self.assertIn('scope_unresolved', self.codes(result, 'limits'))

    def test_comma_selector_scope_is_checked_separately(self):
        result = self.check('.card{--ink:red}.card,.other{color:var(--ink)}')
        self.assertEqual(result['status'], 'limited')
        self.assertEqual(result['limits'][0]['selector'], '.other')

    def test_conditional_definition_not_assumed_available(self):
        result = self.check('@media (min-width:600px){:root{--ink:red}}a{color:var(--ink)}')
        self.assertEqual(result['status'], 'limited')
        self.assertIn('scope_unresolved', self.codes(result, 'limits'))

    def test_cycle_and_fallback_cycle(self):
        for css in [':root{--a:var(--b);--b:var(--a)}a{color:var(--a)}', ':root{--a:var(--b,var(--a));--b:red}']:
            self.assertIn('alias_cycle', self.codes(self.check(css)))

    def test_html_styles_and_script_strings(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp).resolve() / 'index.html'
            path.write_text('<script>const text="var(--fake)";</script>\n<style>:root{--ink:red}a{color:var(--ink)}</style>\n<a style="color:var(--missing)">Link</a>')
            result = checker.check_source(path)
            self.assertEqual(result['tokens']['used'], ['--ink', '--missing'])
            self.assertEqual(result['errors'][0]['line'], 3)

    def test_symlink_file_and_directory_member_rejected_trusted_root_allowed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            real = root / 'real'
            real.mkdir()
            css = real / 'style.css'
            css.write_text('a{color:red}')
            linked = root / 'linked'
            linked.symlink_to(real, target_is_directory=True)
            self.assertTrue(checker.check_source(linked)['ok'])
            (real / 'alias.css').symlink_to(css)
            with self.assertRaises(ValueError):
                checker.check_source(real)
            with self.assertRaises(ValueError):
                checker.check_source(real / 'alias.css')

    def test_runtime_provider_is_limit_with_location(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            (root / 'style.css').write_text('.image{width:var(--native-width)}')
            (root / 'main.js').write_text("// other.style.setProperty('--fake', 'x')\nviewport.style.setProperty('--native-width', width+'px');")
            result = checker.check_source(root, root)
            self.assertTrue(result['ok'])
            self.assertEqual(result['status'], 'limited')
            self.assertEqual(result['tokens']['runtime_set'], ['--native-width'])
            self.assertEqual(result['runtime_providers'][0]['line'], 2)
            (root / 'style.css').write_text('.image{width:10px}')
            # Baseline consumed tokens remain defined by CSS consumption, not
            # a setter that might no longer be used by any element.
            original = root / 'original.css'
            original.write_text('.image{width:var(--native-width)}')
            self.assertIn('baseline_token_removed', self.codes(checker.check_source(root / 'style.css', original)))

    def test_incomplete_css_is_limited(self):
        self.assertEqual(self.check('a { color: var(--missing')['status'], 'limited')

    def test_cli_determinism_and_exit_status(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp).resolve() / 'missing.css'
            path.write_text('a{color:var(--missing)}')
            command = [sys.executable, str(SCRIPT), str(path)]
            first = subprocess.run(command, capture_output=True, text=True)
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 1)
            self.assertEqual(first.stdout, second.stdout)
            self.assertFalse(json.loads(first.stdout)['ok'])


if __name__ == '__main__':
    unittest.main()
