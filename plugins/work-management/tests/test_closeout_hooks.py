"""Check lifecycle safety without reading or terminating live processes."""
import contextlib
import importlib.util
import io
import os
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

binding = os.environ.get('WORK_MANAGEMENT_CLOSEOUT_HELPER')
if not binding:
    raise unittest.SkipTest('Optional external closeout helper requires explicit WORK_MANAGEMENT_CLOSEOUT_HELPER; it is not bundled or registered')
SCRIPT = Path(binding).expanduser()
spec = importlib.util.spec_from_file_location('closeout_under_test', SCRIPT)
closeout = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = closeout
spec.loader.exec_module(closeout)


class CloseoutTests(unittest.TestCase):
    def hook(self, payload, quality=None):
        output = io.StringIO()
        with mock.patch.object(sys, 'argv', [str(SCRIPT)]), \
             mock.patch.object(closeout, 'read_hook_input', return_value=payload), \
             mock.patch.object(closeout, 'artifact_quality_payload', return_value=quality or {}), \
             mock.patch.object(closeout, 'list_processes', side_effect=AssertionError('live scan')), \
             mock.patch.object(closeout.os, 'kill', side_effect=AssertionError('process termination')), \
             contextlib.redirect_stdout(output):
            self.assertEqual(closeout.main(), 0)
        return output.getvalue()

    def test_routine_stop_reminds_without_block_or_process_scan(self):
        data = json.loads(self.hook({'hook_event_name': 'Stop', 'session_id': 'test'}))
        self.assertTrue(data['continue'])
        self.assertNotIn('decision', data)

    def test_reentry_is_quiet(self):
        self.assertEqual(self.hook({'hook_event_name': 'Stop', 'stop_hook_active': True}), '')

    def test_only_scoped_pending_obligation_blocks_once(self):
        quality = {'status': 'pending', 'advisory': 'Complete verified obligation.'}
        data = json.loads(self.hook({'hook_event_name': 'Stop', 'session_id': 'test'}, quality))
        self.assertEqual(data, {'decision': 'block', 'reason': quality['advisory']})
        # Without native session/turn identity, never borrow global obligations.
        data = json.loads(self.hook({'hook_event_name': 'Stop'}, quality))
        self.assertNotIn('decision', data)

    def test_diagnostic_dry_run_never_kills_or_writes_state(self):
        row = closeout.ProcessRow(999999, 1, 10, 'Google Chrome --headless --user-data-dir=/tmp/test')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = io.StringIO()
            with mock.patch.object(closeout, 'STATE_DIR', root), \
                 mock.patch.object(closeout, 'STATE_PATH', root / 'state.json'), \
                 mock.patch.object(closeout, 'load_session_epoch', return_value=0), \
                 mock.patch.object(closeout, 'list_processes', return_value=[row]), \
                 mock.patch.object(closeout, 'enabled_mcps', return_value=[]), \
                 mock.patch.object(closeout, 'git_has_changes', return_value=False), \
                 mock.patch.object(closeout, 'artifact_quality_payload', return_value={}), \
                 mock.patch.object(closeout, 'pressure_guard_payload', return_value={}) as pressure, \
                 mock.patch.object(closeout.os, 'kill', side_effect=AssertionError('process termination')), \
                 contextlib.redirect_stdout(output):
                closeout.run_closeout(dry_run=True, json_mode=True, workspace=root)
            pressure.assert_called_once_with(dry_run=True)
            data = json.loads(output.getvalue())
            self.assertFalse(data['automatic_termination'])
            self.assertEqual(data['closed'], [])
            self.assertEqual(len(data['unverified_candidates']), 1)
            self.assertEqual(list(root.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
