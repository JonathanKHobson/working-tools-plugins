"""Behavioral checks for optional local text tools; no live account actions."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "skills/natural-prose-editor/scripts/linkedin_text"
spec = importlib.util.spec_from_file_location("text_review", TOOLS / "text_review.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class TextToolkitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.terms = review.load_lexicon()

    def cli(self, tool, *args, data=b""):
        return subprocess.run([sys.executable, "-B", str(TOOLS / tool), *map(str, args)],
                              input=data, capture_output=True, check=False)

    def test_all_source_terms_remain_report_only(self):
        self.assertEqual(len(self.terms), 113)
        text = "Leverage a robust ecosystem. The landscape matters."
        self.assertEqual(review.clean_text(text)["after"], text)
        self.assertTrue(review.stock_matches(text, self.terms))

    def test_default_preserves_meaningful_unicode(self):
        text = '\ufeff“Keep”—5–10… 6′ • →\u00a0👩🏽\u200d💻 👨\u200d👩\u200d👧\u200d👦\nمی\u200cروم \u200fעברית\u061c العربية\u2060\U000e0067\u00ad\u200b'
        result = review.clean_text(text)
        self.assertEqual(result["after"], text)
        self.assertEqual(result["changes"], [])

    def test_cli_preserves_exact_bytes_and_crlf(self):
        text = '\ufeff“Quote”\r\n👩\u200d💻 می\u200cروم\r\n'.encode()
        result = self.cli("humanize.py", data=text)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, text)

    def test_cleanup_reports_exact_original_offsets(self):
        text = '\ufeffco\u00adoperate and w\u200bord.'
        result = review.clean_text(text, cleanup=True)
        self.assertEqual(result["after"], 'cooperate and word.')
        self.assertEqual([c["offset"] for c in result["changes"]], [0, 3, 17])
        for change in result["changes"]:
            self.assertEqual(text[change["offset"]], change["before"])

    def test_cleanup_does_not_strip_script_emoji_or_direction_controls(self):
        text = 'می\u200cروم 👩\u200d💻 \u200fעברית \u061cالعربية foo\u2060bar ไทย\u200bภาษา'
        self.assertEqual(review.clean_text(text, cleanup=True)["after"], text)

    def test_protected_spans_survive_explicit_options(self):
        text = ('```python\n“foo\u00adbar”\n```\n`“co\u00adoperate”` '
                'https://example.org/“co\u200boperate” leverage@example.org '
                '[“WORK\u00adING”] {{“w\u200bord”}} ${“w\u200bord”} <“x\u200by”>\n'
                '    “co\u00adoperate”\n~~~\n“unclosed\u00adfence”')
        self.assertEqual(review.clean_text(text, cleanup=True, ascii_quotes=True)["after"], text)

    def test_inline_code_with_double_backtick_delimiter(self):
        text = '``some ` “co\u00adoperate” ` code`` and “plain”'
        after = review.clean_text(text, cleanup=True, ascii_quotes=True)["after"]
        self.assertEqual(after, '``some ` “co\u00adoperate” ` code`` and "plain"')

    def test_ascii_quotes_leave_other_typography(self):
        text = '“Don’t”—5–10… 6′ • →\u00a0'
        self.assertEqual(review.clean_text(text, ascii_quotes=True)["after"], '"Don\'t"—5–10… 6′ • →\u00a0')

    def test_lexical_matches_skip_code_urls_email_and_placeholders(self):
        text = 'leverage `leverage` https://example.com/leverage leverage@example.com [leverage] {{leverage}}'
        matches = review.stock_matches(text, self.terms)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["offset"], 0)

    def test_phrase_punctuation_and_word_boundaries(self):
        found = review.stock_matches('leveraged. What are your thoughts?', self.terms)
        self.assertEqual([m["candidate"] for m in found], ['what are your thoughts?'])

    def test_empty_and_short_panels_are_not_scores(self):
        for text in ['', 'I wrote this.']:
            result = review.descriptive_review(text, self.terms, 'en')
            self.assertEqual(len(result['panels']), 5)
            for name in ['sentence_variation', 'specificity_candidates', 'voice_cues']:
                self.assertEqual(result['panels'][name]['status'], 'unknown')
            self.assertNotIn('score', result)
            self.assertNotIn('verdict', result)

    def test_non_english_and_undeclared_context_are_unknown(self):
        for language, text in [('und', 'We wrote prose. ' * 30), ('ar', 'نكتب الكلمات. ' * 30), ('zh', '这是一个例子。' * 30)]:
            result = review.descriptive_review(text, self.terms, language)
            for name in ['sentence_variation', 'specificity_candidates', 'voice_cues']:
                self.assertEqual(result['panels'][name]['status'], 'unknown')

    def test_english_context_has_descriptive_counts(self):
        text = 'I wrote the first short explanation for a new reader. We tested one sentence in this hypothetical fixture. A third sentence adds enough words for the token threshold. You can inspect the fourth sentence independently.'
        result = review.descriptive_review(text, self.terms, 'en')
        self.assertEqual(result['panels']['sentence_variation']['status'], 'observed')
        self.assertEqual(result['panels']['sentence_variation']['approximate_sentence_count'], 4)
        self.assertNotIn('score', result)
        for panel in result['panels'].values():
            self.assertNotIn('score', panel)

    def test_json_cleanup_and_diff_report_changes_without_overwriting(self):
        with tempfile.TemporaryDirectory() as folder:
            path, out = Path(folder)/'draft.txt', Path(folder)/'clean.json'
            original = '\ufeffco\u00adoperate\r\n'.encode()
            path.write_bytes(original)
            result = self.cli('humanize.py', path, '--cleanup', '--json', '--diff', '-o', out)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(out.read_text())
            self.assertEqual(payload['after'], 'cooperate\r\n')
            self.assertEqual(len(payload['changes']), 2)
            self.assertIn(b'--- before', result.stderr)
            self.assertEqual(path.read_bytes(), original)

    def test_output_aliases_are_rejected_and_original_stays_unchanged(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'draft.txt'
            path.write_bytes(b'Original text')
            hard, sym = Path(folder)/'hard.txt', Path(folder)/'sym.txt'
            os.link(path, hard)
            sym.symlink_to(path)
            for tool in ['humanize.py', 'detect.py']:
                for target in [path, hard, sym]:
                    result = self.cli(tool, path, '-o', target)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(path.read_bytes(), b'Original text')

    def test_existing_unrelated_output_not_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            path, out = Path(folder)/'in.txt', Path(folder)/'out.txt'
            path.write_text('input')
            out.write_text('keep me')
            result = self.cli('humanize.py', path, '-o', out)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(out.read_text(), 'keep me')

    def test_invalid_utf8_nul_and_oversize_inputs_fail(self):
        for data in [b'\xff', b'text\x00more', b'a' * (review.MAX_INPUT_BYTES + 1)]:
            for tool in ['humanize.py', 'detect.py']:
                result = self.cli(tool, data=data)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, b'')

    def test_invalid_lexicons_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'lex.json'
            for data in [None, {}, {'version': True, 'terms': []}, {'version':1, 'terms':[{'find':'', 'suggestion':'', 'family':'x'}]},
                         {'version':1, 'terms':[{'find':'x', 'suggestion':17, 'family':'x'}]},
                         {'version':1, 'terms':[{'find':'x\x00', 'suggestion':'', 'family':'x'}]},
                         {'version':1, 'terms':[{'find':'x', 'suggestion':'', 'family':'x'}]*2}]:
                path.write_text(json.dumps(data))
                result = self.cli('detect.py', '--lexicon', path)
                self.assertEqual(result.returncode, 2)
            path.write_bytes(b'not json')
            self.assertEqual(self.cli('humanize.py', '--lexicon', path).returncode, 2)

    def test_custom_lexicon_is_literal_not_regex(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'lex.json'
            path.write_text(json.dumps({'version':1, 'terms':[{'find':'(a+)+', 'suggestion':'keep', 'family':'custom'}]}))
            terms = review.load_lexicon(path)
            self.assertEqual(len(review.stock_matches('(a+)+', terms)), 1)
            self.assertEqual(review.stock_matches('aaaaaa', terms), [])

    def test_before_after_comparison_has_only_descriptive_panels(self):
        with tempfile.TemporaryDirectory() as folder:
            before, after = Path(folder)/'before.txt', Path(folder)/'after.txt'
            before.write_text('Robust proposal.')
            after.write_text('Proposal.')
            result = self.cli('detect.py', before, after, '--json')
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(len(payload['before']['panels']), 5)
            self.assertEqual(len(payload['after']['panels']), 5)
            self.assertEqual(len(payload['before']['panels']['stock_terms']['matches']), 1)
            self.assertEqual(payload['after']['panels']['stock_terms']['matches'], [])
            self.assertNotIn('human_score', payload)
            self.assertNotIn('verdict', payload)

    def test_comparison_output_cannot_alias_second_input(self):
        with tempfile.TemporaryDirectory() as folder:
            a, b = Path(folder)/'a.txt', Path(folder)/'b.txt'
            a.write_text('first')
            b.write_text('second')
            self.assertEqual(self.cli('detect.py', a, b, '-o', b).returncode, 2)
            self.assertEqual(b.read_text(), 'second')

    def test_missing_input_and_double_stdin_fail(self):
        self.assertEqual(self.cli('detect.py', '-', '-').returncode, 2)
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(self.cli('humanize.py', Path(folder)/'absent.txt').returncode, 2)


if __name__ == '__main__':
    unittest.main()
