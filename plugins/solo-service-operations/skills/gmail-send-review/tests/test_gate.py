import importlib.util
import base64
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/gate.py'
spec = importlib.util.spec_from_file_location('gate', SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
TOOL = 'mcp__codex_apps__gmail_send_email'
PAYLOAD = {'to': 'nobody@example.invalid', 'subject': 'Offline fixture',
           'payload': {'mime_type': 'text/plain', 'body': {'content': 'A private fixture sentence.'}}}
DRAFT = {'draft_id': 'draft-fixture', 'subject': 'Offline fixture',
         'payload': {'mime_type': 'text/plain', 'body': {'content': 'Saved private fixture.'}}}


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'state'
        self.addCleanup(self.tmp.cleanup)

    def review(self, payload=PAYLOAD, tool=TOOL, **overrides):
        opts = dict(voice='matched', audience='routine', authorization='send', skills_reviewed=True, now=100)
        opts.update(overrides)
        return gate.record_review(self.root, 'session-a', tool, payload, **opts)

    def event(self, payload=PAYLOAD, tool=TOOL, session='session-a', now=101):
        return gate.before_send({'tool_name': tool, 'tool_input': payload, 'session_id': session}, self.root, now)

    def denied(self, result):
        self.assertEqual(result['hookSpecificOutput']['permissionDecision'], 'deny')

    def test_unreviewed_send_requires_agent_review(self):
        result = self.event()
        self.denied(result)
        self.assertIn('not a request for human approval', result['hookSpecificOutput']['permissionDecisionReason'])

    def test_reviewed_send_preserves_normal_approval_policy(self):
        self.review()
        self.assertEqual({}, self.event())

    def test_unchanged_review_is_reused(self):
        self.review()
        self.assertEqual({}, self.event())
        self.assertEqual({}, self.event(now=110))

    def test_changed_fields_require_review(self):
        self.review()
        for field, value in [('to', 'different@example.invalid'), ('subject', 'Changed'),
                             ('cc', 'cc@example.invalid'), ('bcc', 'bcc@example.invalid'),
                             ('from_address', 'sender@example.invalid'), ('reply_message_id', 'other'),
                             ('payload', {'mime_type': 'text/plain', 'body': {'content': 'Edited'}})]:
            with self.subTest(field=field):
                self.denied(self.event({**PAYLOAD, field: value}))

    def test_response_projection_does_not_require_review(self):
        self.review()
        self.assertEqual({}, self.event({**PAYLOAD, 'response_fields': ['id']}))

    def test_direct_reply_cannot_receive_send_receipt(self):
        reply = {**PAYLOAD, 'reply_message_id': 'parent-message'}
        with self.assertRaisesRegex(ValueError, 'create_draft'):
            self.review(reply)
        result = self.event(reply)
        self.denied(result)
        self.assertIn('not a request for human approval', result['hookSpecificOutput']['permissionDecisionReason'])

    def test_direct_reply_stays_blocked_with_preexisting_receipt(self):
        reply = {**PAYLOAD, 'reply_message_id': 'parent-message'}
        key = gate.fingerprint(TOOL, reply)
        gate.write_state(gate.scoped_path(self.root, 'session-a'),
                         {key: {'expires': 1000, 'operation': 'send_email'}})
        self.denied(self.event(reply))

    def test_reply_guard_covers_registered_aliases(self):
        reply = {**PAYLOAD, 'reply_message_id': 'parent-message'}
        for tool in [TOOL, 'mcp__codex_apps__gmail.send_email', 'gmail.send_email']:
            with self.subTest(tool=tool):
                self.denied(self.event(reply, tool))

    def test_empty_reply_target_is_an_ordinary_send(self):
        for value in [None, '']:
            payload = {**PAYLOAD, 'reply_message_id': value}
            self.review(payload)
            self.assertEqual({}, self.event(payload))

    def test_receipt_cannot_cross_sessions_or_expiry(self):
        self.review()
        self.denied(self.event(session='session-b'))
        self.denied(self.event(now=1901))

    def test_read_search_and_draft_creation_do_not_trigger_or_write_state(self):
        for action in ['search_emails', 'read_email', 'get_profile', 'list_drafts', 'create_draft', 'update_draft']:
            self.assertEqual({}, self.event(tool='mcp__codex_apps__gmail_' + action))
        self.assertFalse(self.root.exists())

    def test_similar_unrelated_tools_do_not_trigger(self):
        for tool in ['mcp__codex_apps__slack_send_message', 'Bash', 'gmail_send_email', TOOL + '_preview']:
            self.assertEqual({}, self.event(tool=tool))

    def test_tool_spelling_aliases_use_same_receipt(self):
        self.review()
        for alias in ['mcp__codex_apps__gmail.send_email', 'gmail.send_email']:
            self.assertEqual({}, self.event(tool=alias))

    def test_forward_has_own_content_bound_receipt(self):
        tool = 'mcp__codex_apps__gmail_forward_emails'
        args = {'message_ids': ['fixture-id'], 'to': 'nobody@example.invalid'}
        self.denied(self.event(args, tool))
        self.review(args, tool)
        self.assertEqual({}, self.event(args, tool))
        self.denied(self.event({**args, 'message_ids': ['other']}, tool))

    def test_human_hold_and_uncompleted_reviews_cannot_record(self):
        for overrides in [{'authorization': 'hold'}, {'skills_reviewed': False}]:
            with self.assertRaises(ValueError):
                self.review(**overrides)

    def test_unavailable_style_source_can_proceed_honestly(self):
        self.review(voice='unavailable')
        self.assertEqual({}, self.event())

    def test_draft_requires_fresh_read_and_single_use(self):
        tool = 'mcp__codex_apps__gmail_send_draft'
        args = {'draft_id': 'draft-fixture'}
        with self.assertRaises(ValueError):
            self.review(args, tool)
        with self.assertRaisesRegex(ValueError, 'snapshot'):
            self.review(args, tool, draft_verified=True)
        self.review(args, tool, draft_verified=True, reviewed_draft=DRAFT)
        self.assertEqual({}, self.event(args, tool))
        self.denied(self.event(args, tool))
        self.review(args, tool, draft_verified=True, reviewed_draft=DRAFT)
        self.denied(self.event(args, tool, now=221))

    def test_em_dash_in_subject_and_authored_plain_body_denied_at_both_checks(self):
        for payload in [{**PAYLOAD, 'subject': 'A\u2014B'},
                        {**PAYLOAD, 'payload': {'mime_type': 'text/plain', 'body': {'content': 'A\u2014B'}}}]:
            with self.subTest(payload=payload):
                with self.assertRaisesRegex(ValueError, 'em dash'):
                    self.review(payload)
                key = gate.fingerprint(TOOL, payload)
                gate.write_state(gate.scoped_path(self.root, 'session-a'),
                                 {key: {'expires': 1000, 'operation': 'send_email'}})
                result = self.event(payload)
                self.denied(result)
                self.assertIn('em dash', result['hookSpecificOutput']['permissionDecisionReason'])

    def test_html_entities_and_base64url_text_are_inspected(self):
        for body in [{'content': '<p>Hello &mdash; there</p>'},
                     {'content': '<p>Hello &#x2014; there</p>'},
                     {'base64_url_content': base64.urlsafe_b64encode(b'Hello \xe2\x80\x94 there').decode().rstrip('=')}]:
            payload = {**PAYLOAD, 'payload': {'mime_type': 'text/html' if 'content' in body else 'text/plain', 'body': body}}
            with self.subTest(body=body):
                with self.assertRaisesRegex(ValueError, 'em dash'):
                    self.review(payload)
                result = self.event(payload)
                self.denied(result)
                self.assertIn('em dash', result['hookSpecificOutput']['permissionDecisionReason'])

    def test_html_accessible_attributes_are_inspected_outside_quotes(self):
        for markup in ['<img alt="Authored &mdash; description">',
                       '<span title="Authored &#8212; title">Visible</span>',
                       '<button aria-label="Authored \u2014 label">Go</button>',
                       '<img aria-label="Authored &mdash; image"/>']:
            payload = {**PAYLOAD, 'payload': {'mime_type': 'text/html', 'body': {'content': markup}}}
            with self.subTest(markup=markup):
                with self.assertRaisesRegex(ValueError, 'em dash'):
                    self.review(payload)
                key = gate.fingerprint(TOOL, payload)
                gate.write_state(gate.scoped_path(self.root, 'session-a'),
                                 {key: {'expires': 1000, 'operation': 'send_email'}})
                result = self.event(payload)
                self.denied(result)
                self.assertIn('em dash', result['hookSpecificOutput']['permissionDecisionReason'])

    def test_html_quote_attributes_are_preserved(self):
        payload = {**PAYLOAD, 'payload': {'mime_type': 'text/html', 'body': {'content':
            '<p>Authored</p><div class="gmail_quote" title="Old &mdash; title"><img alt="Old &mdash; alt"></div>'
            '<blockquote aria-label="Old &mdash; label">Old &mdash; quote</blockquote>'}}}
        self.review(payload)
        self.assertEqual({}, self.event(payload))

    def test_rfc2047_encoded_subject_is_inspected_at_receipt_and_hook(self):
        for subject in ['=?utf-8?B?4oCU?=', '=?utf-8?Q?=E2=80=94?=']:
            payload = {**PAYLOAD, 'subject': subject}
            with self.subTest(subject=subject):
                with self.assertRaisesRegex(ValueError, 'em dash'):
                    self.review(payload)
                key = gate.fingerprint(TOOL, payload)
                gate.write_state(gate.scoped_path(self.root, 'session-a'),
                                 {key: {'expires': 1000, 'operation': 'send_email'}})
                result = self.event(payload)
                self.denied(result)
                self.assertIn('em dash', result['hookSpecificOutput']['permissionDecisionReason'])

    def test_ambiguous_text_body_is_rejected_at_receipt_and_hook(self):
        payload = {**PAYLOAD, 'payload': {'mime_type': 'text/plain', 'body': {
            'content': 'Visible text', 'base64_url_content': base64.urlsafe_b64encode('Hidden \u2014 text'.encode()).decode()}}}
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            self.review(payload)
        key = gate.fingerprint(TOOL, payload)
        gate.write_state(gate.scoped_path(self.root, 'session-a'),
                         {key: {'expires': 1000, 'operation': 'send_email'}})
        result = self.event(payload)
        self.denied(result)
        self.assertIn('ambiguous', result['hookSpecificOutput']['permissionDecisionReason'])

    def test_only_authored_mime_text_is_scanned(self):
        payload = {**PAYLOAD, 'to': 'name\u2014suffix@example.invalid',
                   'payload': {'mime_type': 'multipart/mixed', 'parts': [
                       {'mime_type': 'text/html', 'body': {'content': '<p>Authored text</p><div class="gmail_quote"><p>Old\u2014text</p></div><blockquote>Quote\u2014text</blockquote>'}},
                       {'mime_type': 'text/plain', 'filename': 'original\u2014name.txt', 'body': {'content': 'Original\u2014text'}},
                       {'mime_type': 'message/rfc822', 'body': {'base64_url_content': 'bogus'}}]}}
        self.review(payload)
        self.assertEqual({}, self.event(payload))

    def test_plain_quote_and_forwarded_original_are_preserved(self):
        for original in ['> Old\u2014quote', '---------- Forwarded message ---------\nOld\u2014forward',
                         '-----Original Message-----\nOld\u2014forward', 'On Monday, Person wrote:\nOld\u2014quote']:
            payload = {**PAYLOAD, 'payload': {'mime_type': 'text/plain', 'body': {'content': 'New text\n' + original}}}
            with self.subTest(original=original):
                self.review(payload)
                self.assertEqual({}, self.event(payload))

    def test_forward_optional_authored_payload_is_checked(self):
        tool = 'mcp__codex_apps__gmail_forward_emails'
        args = {'message_ids': ['original-id'], 'to': 'nobody@example.invalid',
                'payload': {'mime_type': 'text/html', 'body': {'content': '<p>New &mdash; note</p>'}}}
        with self.assertRaisesRegex(ValueError, 'em dash'):
            self.review(args, tool)
        self.denied(self.event(args, tool))

    def test_multipart_authored_leaf_is_checked(self):
        payload = {**PAYLOAD, 'payload': {'mime_type': 'multipart/alternative', 'parts': [
            {'mime_type': 'text/plain', 'body': {'content': 'Fine'}},
            {'mime_type': 'text/html', 'body': {'content': '<p>Authored\u2014text</p>'}}]}}
        with self.assertRaisesRegex(ValueError, 'payload.parts\\[1\\]'):
            self.review(payload)

    def test_draft_snapshot_requires_matching_id_and_checks_saved_text(self):
        tool = 'mcp__codex_apps__gmail_send_draft'
        args = {'draft_id': 'draft-fixture'}
        with self.assertRaisesRegex(ValueError, 'match draft_id'):
            self.review(args, tool, draft_verified=True, reviewed_draft={**DRAFT, 'draft_id': 'other'})
        with self.assertRaisesRegex(ValueError, 'em dash'):
            self.review(args, tool, draft_verified=True, reviewed_draft={**DRAFT, 'subject': 'A\u2014B'})
        with self.assertRaisesRegex(ValueError, 'em dash'):
            self.review(args, tool, draft_verified=True, reviewed_draft={**DRAFT, 'payload': {'mime_type': 'text/plain', 'body': {'content': 'A\u2014B'}}})
        self.review(args, tool, draft_verified=True, reviewed_draft=DRAFT)
        stored = ''.join(path.read_text() for path in self.root.glob('*.json'))
        self.assertNotIn('Saved private fixture', stored)

    def test_draft_cli_requires_reviewed_snapshot_envelope(self):
        command = [sys.executable, str(SCRIPT), '--state-dir', str(self.root), 'review',
                   '--session', 'session-a', '--tool', 'mcp__codex_apps__gmail_send_draft',
                   '--voice', 'matched', '--audience', 'routine', '--authorization', 'send',
                   '--skills-reviewed', '--draft-verified']
        result = subprocess.run(command, input=json.dumps({'draft_id': 'draft-fixture'}), text=True, capture_output=True)
        self.assertNotEqual(0, result.returncode)
        result = subprocess.run(command, input=json.dumps({'tool_input': {'draft_id': 'draft-fixture'},
                                'reviewed_draft': DRAFT}), text=True, capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_missing_session_invalid_args_corrupt_state_hold_send(self):
        self.denied(self.event(session=''))
        self.denied(self.event(payload={}))
        self.review()
        gate.scoped_path(self.root, 'session-a').write_text('broken')
        self.denied(self.event())

    def test_no_email_content_or_addresses_in_state(self):
        self.review()
        text = ''.join(path.read_text() for path in self.root.glob('*'))
        for private in ['nobody', 'Offline fixture', 'private fixture', 'session-a']:
            self.assertNotIn(private, text)

    def test_hook_cli_round_trip(self):
        command = [sys.executable, str(SCRIPT), '--state-dir', str(self.root), 'hook']
        result = subprocess.run(command, input=json.dumps({'session_id': 's', 'tool_name': TOOL,
                                'tool_input': PAYLOAD}), text=True, capture_output=True, check=True)
        self.denied(json.loads(result.stdout))
        malformed = subprocess.run(command, input='bad json', text=True, capture_output=True, check=True)
        self.denied(json.loads(malformed.stdout))


if __name__ == '__main__':
    unittest.main()
