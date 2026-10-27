"""One native advisory registration with either host's package-root variable."""
import json
import os
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]

class HookRegistrationTests(unittest.TestCase):
    def test_claude_default_is_not_registered_twice(self):
        manifest = json.loads((ROOT / '.claude-plugin/plugin.json').read_text())
        self.assertNotIn('hooks', manifest)
        codex = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
        self.assertEqual(codex['hooks'], './hooks/hooks.json')
        config = json.loads((ROOT / 'hooks/hooks.json').read_text())
        commands = [hook['command'] for group in config['hooks']['UserPromptSubmit'] for hook in group['hooks']]
        self.assertEqual(len(commands), 1)

    def test_actual_hook_command_resolves_each_supported_host_root(self):
        config = json.loads((ROOT / 'hooks/hooks.json').read_text())
        command = config['hooks']['UserPromptSubmit'][0]['hooks'][0]['command']
        for host in ['PLUGIN_ROOT', 'CLAUDE_PLUGIN_ROOT']:
            with self.subTest(host=host):
                env = dict(os.environ)
                env.pop('PLUGIN_ROOT', None)
                env.pop('CLAUDE_PLUGIN_ROOT', None)
                env[host] = str(ROOT)
                result = subprocess.run(command, shell=True, env=env, text=True,
                    input=json.dumps({'hook_event_name':'UserPromptSubmit','prompt':'Please rewrite this prompt to improve clarity.'}),
                    capture_output=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, '')
                messages = result.stdout.strip().splitlines()
                self.assertEqual(len(messages), 1)
                context = json.loads(messages[0])['hookSpecificOutput']['additionalContext']
                self.assertIn('Prompt Playbook advisory:', context)
                self.assertEqual(context.count('Prompt Playbook advisory:'), 1)

if __name__ == '__main__':
    unittest.main()
