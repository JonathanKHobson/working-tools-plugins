# SPDX-License-Identifier: AGPL-3.0-only
import io
import fcntl
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from codex_host_hooks import read_payload, prompt, stop_result
from quality_rules import detect_obligations
from scope_state import MAX_BYTES, ScopeStore, StateError, pending, scope_key


class HooksTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.parent = Path(self.temp.name).resolve()
        self.state = self.parent / 'state'
        self.key = scope_key({'session_id': 'session-one'})
        self.store = ScopeStore(self.state, self.key)

    def tearDown(self):
        self.temp.cleanup()

    def run_hook(self, command, payload):
        return subprocess.run([sys.executable, '-B', str(ROOT / 'codex_host_hooks.py'),
                               '--state-dir', str(self.state), command],
                              input=payload if isinstance(payload, bytes) else json.dumps(payload).encode(),
                              capture_output=True, timeout=5)

    def test_classifier_cases(self):
        cases = [
            ('Build an HTML landing page', ['visual_qa', 'design_taste']),
            ('Create a stakeholder email', ['communication_review']),
            ('Make a portfolio case-study page', list(('visual_qa', 'design_taste', 'communication_review'))),
            ('Fix this backend bug and run tests', []),
            ('Generate a PDF report', ['visual_qa', 'design_taste']),
            ('Generate a PDF report for stakeholders', list(('visual_qa', 'design_taste', 'communication_review'))),
            ('Set up a Gmail send hook that checks writing skills', []),
            ('Update hook config to mention email, message, image, and app behavior', []),
            ('Create a backend hook to route email messages', []),
            ('Create a config for email message handling', []),
            ('Create an email configuration guide for stakeholders', ['communication_review']),
            ('Build the app UI for email configuration', ['visual_qa', 'design_taste']),
            ('Write the email copy for the hook configuration notice', ['communication_review']),
            ('Generate a PDF configuration guide for stakeholders', list(('visual_qa', 'design_taste', 'communication_review'))),
            ('What does this image tool config do?', []),
            ('The app is slow', []),
            ('Hello', []),
            # Existing heuristic limitations remain deliberate, reviewable rules.
            ('What does this email mean?', ['communication_review']),
        ]
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(detect_obligations(value), expected)

    def test_payload_latest_user(self):
        self.assertEqual(prompt({'messages': [{'role': 'user', 'content': 'old'},
                                             {'role': 'human', 'content': [{'text': 'new'}]}]}), 'new')

    def test_prompt_stop_completion(self):
        data = {'hook_event_name': 'UserPromptSubmit', 'session_id': 'session-one',
                'prompt': 'Build an HTML landing page'}
        result = self.run_hook('prompt', data)
        self.assertEqual((result.returncode, result.stdout), (0, b''))
        stopped = self.run_hook('stop', {'hook_event_name': 'Stop', 'session_id': 'session-one'})
        self.assertEqual(json.loads(stopped.stdout)['decision'], 'block')
        marked = subprocess.run([sys.executable, '-B', str(ROOT / 'codex_host_hooks.py'),
                                 '--state-dir', str(self.state), 'quality', '--session-id', 'session-one',
                                 'mark', 'visual_qa', '--reviewer', 'manual reviewer',
                                 '--evidence', 'render inspected'], capture_output=True, timeout=5)
        self.assertEqual(marked.returncode, 0, marked.stderr)
        self.assertFalse(json.loads(marked.stdout)['independent_verification'])
        skipped = subprocess.run([sys.executable, '-B', str(ROOT / 'codex_host_hooks.py'),
                                  '--state-dir', str(self.state), 'quality', '--session-id', 'session-one',
                                  'skip', 'design_taste', '--reason', 'Review not applicable'],
                                 capture_output=True, timeout=5)
        self.assertEqual(skipped.returncode, 0, skipped.stderr)
        self.assertFalse(pending(self.store.read()))
        self.assertTrue(stop_result({'session_id': 'session-one'}, self.state)['continue'])

    def test_two_sessions_and_turn_fallback(self):
        self.store.detect(['visual_qa'])
        other = ScopeStore(self.state, scope_key({'session_id': 'session-two'}))
        other.detect(['communication_review'])
        self.store.update('visual_qa', 'done')
        self.assertEqual(pending(other.read()), ['communication_review'])
        self.assertTrue(stop_result({'session_id': 'session-one'}, self.state)['continue'])
        self.assertEqual(stop_result({'session_id': 'session-two'}, self.state)['decision'], 'block')
        self.assertNotEqual(scope_key({'turn_id': 'session-one'}), self.key)
        self.assertEqual(scope_key({'session_id': 'session-one', 'turn_id': 'any'}), self.key)

    def test_missing_scope_never_blocks_or_stores(self):
        self.store.detect(['visual_qa'])
        result = stop_result({}, self.state)
        self.assertNotIn('decision', result)
        empty = self.parent / 'unused'
        self.assertTrue(stop_result({}, empty)['continue'])
        self.assertFalse(empty.exists())
        self.assertIsNone(scope_key({'session_id': ' '}))
        self.assertIsNone(scope_key({'session_id': 'x' * 513}))

    def test_reentrant_stop_does_not_access_state(self):
        self.assertIsNone(stop_result({'session_id': 'session-one', 'stop_hook_active': True}, '/nonexistent/parent/state'))
        result = self.run_hook('stop', {'hook_event_name': 'Stop', 'stop_hook_active': True})
        self.assertEqual((result.returncode, result.stdout), (0, b''))

    def test_no_prompt_personal_text_or_paths_persisted(self):
        secret = 'UniquePrivateMarker API_KEY=secret user@example.test /private/workspace'
        self.run_hook('prompt', {'hook_event_name': 'UserPromptSubmit', 'session_id': 'session-one',
                                 'cwd': '/private/workspace', 'prompt': 'Build an HTML landing page ' + secret})
        self.store.update('visual_qa', 'done')
        files = list(self.state.iterdir())
        stored = ''.join(path.name + path.read_text() for path in files)
        for value in ('UniquePrivateMarker', 'API_KEY', 'secret', 'session-one', '@', '/private', 'prompt'):
            self.assertNotIn(value, stored)
        self.assertEqual(stat.S_IMODE(self.state.stat().st_mode), 0o700)
        self.assertTrue(all(stat.S_IMODE(path.stat().st_mode) == 0o600 for path in files))

    def test_nonvisual_prompt_replaces_previous_obligations(self):
        self.store.detect(['visual_qa'])
        self.run_hook('prompt', {'hook_event_name': 'UserPromptSubmit', 'session_id': 'session-one',
                                 'prompt': 'Fix this backend bug'})
        self.assertFalse(pending(self.store.read()))

    def test_malformed_oversized_and_wrong_event_fail_open(self):
        for raw in (b'{bad', b'[]', b'', b'{"prompt":"' + b'x' * MAX_BYTES + b'"}',
                    b'{"hook_event_name":"SessionStart"}', b'\xff',
                    b'[' * 2000 + b']' * 2000):
            for command in ('prompt', 'stop'):
                with self.subTest(raw=raw[:30], command=command):
                    result = self.run_hook(command, raw)
                    self.assertEqual((result.returncode, result.stdout), (0, b''))
        self.assertFalse(self.state.exists())

    def test_input_byte_bound(self):
        with self.assertRaises(ValueError):
            read_payload(io.BytesIO(b' ' * (MAX_BYTES + 1)))

    def test_corrupt_state_fail_open_without_clobber(self):
        self.store.detect(['visual_qa'])
        target = self.state / (self.key + '.json')
        target.write_bytes(b'{bad')
        result = self.run_hook('stop', {'hook_event_name': 'Stop', 'session_id': 'session-one'})
        self.assertEqual((result.returncode, result.stdout), (0, b''))
        with self.assertRaises(StateError):
            self.store.update('visual_qa', 'done')
        self.assertEqual(target.read_bytes(), b'{bad')

    def test_busy_scope_lock_fails_open(self):
        self.store.detect(['visual_qa'])
        with (self.state / (self.key + '.lock')).open('rb') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = self.run_hook('stop', {'hook_event_name': 'Stop', 'session_id': 'session-one'})
            self.assertEqual((result.returncode, result.stdout), (0, b''))
        self.assertEqual(pending(self.store.read()), ['visual_qa'])

    def test_oversized_unknown_schema_and_open_state_fail_open(self):
        self.store.detect(['visual_qa'])
        target = self.state / (self.key + '.json')
        for raw in (b' ' * (MAX_BYTES + 1), b'{"schema_version":999,"updated_at":0,"obligations":{}}',
                    b'{"schema_version":1,"updated_at":0,"obligations":{"other":{"status":"pending"}}}'):
            target.write_bytes(raw)
            result = self.run_hook('stop', {'hook_event_name': 'Stop', 'session_id': 'session-one'})
            self.assertEqual((result.returncode, result.stdout), (0, b''))
        target.chmod(0o644)
        with self.assertRaises(StateError):
            self.store.read()

    def test_completion_requires_detected_check_and_scope(self):
        with self.assertRaises(StateError):
            self.store.update('visual_qa', 'done')
        self.store.detect(['visual_qa'])
        with self.assertRaises(StateError):
            self.store.update('communication_review', 'done')
        with self.assertRaises(StateError):
            ScopeStore(self.state, None)

    def test_blank_mark_and_skip_rejected(self):
        self.store.detect(['visual_qa'])
        for action in (['mark', 'visual_qa', '--reviewer', ' ', '--evidence', 'test'],
                       ['skip', 'visual_qa', '--reason', ' ']):
            result = subprocess.run([sys.executable, '-B', str(ROOT / 'codex_host_hooks.py'),
                                     '--state-dir', str(self.state), 'quality', '--scope-key', self.key] + action,
                                    capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 2)
        self.assertEqual(pending(self.store.read()), ['visual_qa'])

    def test_symlink_directory_and_ancestor_rejected(self):
        target = self.parent / 'target'
        target.mkdir(mode=0o700)
        self.state.symlink_to(target, target_is_directory=True)
        with self.assertRaises(OSError):
            self.store.detect(['visual_qa'])
        with self.assertRaises(OSError):
            ScopeStore(self.state / 'child', self.key).detect(['visual_qa'])
        self.assertEqual(list(target.iterdir()), [])

    def test_symlink_file_and_lock_rejected(self):
        self.state.mkdir(mode=0o700)
        target = self.parent / 'untouched'
        target.write_text('untouched')
        target.chmod(0o600)
        for suffix in ('.json', '.lock'):
            with self.subTest(suffix=suffix):
                link = self.state / (self.key + suffix)
                if link.exists():
                    link.unlink()
                link.symlink_to(target)
                with self.assertRaises(OSError):
                    self.store.detect(['visual_qa'])
                self.assertEqual(target.read_text(), 'untouched')
                link.unlink()

    def test_world_readable_directory_rejected(self):
        self.state.mkdir(mode=0o755)
        self.state.chmod(0o755)
        with self.assertRaises(StateError):
            self.store.detect(['visual_qa'])

    def test_hardlinked_or_open_file_rejected(self):
        self.store.detect(['visual_qa'])
        path = self.state / (self.key + '.json')
        os.link(path, self.parent / 'other-link')
        with self.assertRaises(StateError):
            self.store.detect([])

    def test_clear_only_current_scope(self):
        self.store.detect(['visual_qa'])
        other = ScopeStore(self.state, scope_key({'session_id': 'two'}))
        other.detect(['design_taste'])
        self.store.clear()
        self.assertIsNone(self.store.read())
        self.assertEqual(pending(other.read()), ['design_taste'])


if __name__ == '__main__':
    unittest.main()
