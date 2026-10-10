"""Observable binding, scoping and actual stdio MCP contract checks."""
import hashlib
import json
import os
from pathlib import Path
import selectors
import subprocess
import sys
import tempfile
import unittest

from fixtures import ROOT, make_fixture
from binding import load_binding
from catalog import Catalog


class StdioClient:
    def __init__(self, command, env):
        self.process = subprocess.Popen(command, cwd=ROOT, env=env, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.process.stdout, selectors.EVENT_READ)
        self.serial = 0

    def request(self, method, params=None):
        self.serial += 1
        message = {'jsonrpc': '2.0', 'id': self.serial, 'method': method}
        if params is not None:
            message['params'] = params
        self.process.stdin.write(json.dumps(message) + '\n')
        self.process.stdin.flush()
        while True:
            if not self.selector.select(timeout=20):
                raise RuntimeError('MCP response timed out')
            line = self.process.stdout.readline()
            if not line:
                raise RuntimeError('MCP server exited: ' + self.process.stderr.read()[:300])
            response = json.loads(line)
            if response.get('id') == self.serial:
                return response

    def initialize(self):
        response = self.request('initialize', {'protocolVersion': '2024-11-05',
            'capabilities': {}, 'clientInfo': {'name': 'activities-synthetic-check', 'version': '1.0'}})
        if 'error' in response:
            raise RuntimeError(str(response['error']))
        self.process.stdin.write(json.dumps({'jsonrpc': '2.0', 'method': 'notifications/initialized'}) + '\n')
        self.process.stdin.flush()

    def close(self):
        self.selector.close()
        self.process.stdin.close()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            self.process.wait(timeout=5)
        self.process.stdout.close()
        self.process.stderr.close()


class RuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='activities-tests-')
        cls.directory = Path(cls.temporary.name).resolve()
        cls.vault, cls.db = make_fixture(cls.directory)
        cls.binding = cls.directory / 'atlas-library.json'
        cls.binding.write_text(json.dumps({'interpreter': sys.executable, 'database': str(cls.db)}))
        cls.registrations = json.loads((ROOT / '.mcp.json').read_text())['mcpServers']

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_external_binding_and_absent_state(self):
        self.assertEqual(load_binding(self.binding)['database'], self.db)
        self.assertEqual(load_binding(self.binding)['search_misses_database'], self.db.parent / 'observability/library-search-misses.sqlite')
        env = dict(os.environ, ACTIVITIES_ATLAS_CONFIG=str(self.directory / 'absent.json'), PYTHONDONTWRITEBYTECODE='1')
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/atlas_library_mcp.py'), 'facilitation'], env=env, capture_output=True, text=True, timeout=10)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unavailable', result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertFalse((self.directory / 'absent.json').exists())

    def test_malformed_binding_and_domain_override(self):
        malformed = self.directory / 'malformed.json'
        malformed.write_text('{')
        for arguments, binding in [(['facilitation'], malformed), (['facilitation', 'ux'], self.binding), (['unknown'], self.binding)]:
            env = dict(os.environ, ACTIVITIES_ATLAS_CONFIG=str(binding), PYTHONDONTWRITEBYTECODE='1')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/atlas_library_mcp.py'), *arguments], env=env, capture_output=True, text=True, timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn('Traceback', result.stderr)

    def test_scoped_fts_and_constraints(self):
        catalog = Catalog(self.db, 'ux')
        result = catalog.search(query='fixture " OR *')
        self.assertGreaterEqual(result['total'], 0)
        self.assertTrue(catalog.search(query='fixture')['items'])
        with self.assertRaises(KeyError):
            catalog.get('patterns:fixture-security')
        activities = Catalog(self.db, 'facilitation').search(participants=4, minutes=15, mode='online')
        self.assertEqual(activities['total'], 4)
        self.assertTrue(all(i['collection'] == 'file-o-fun' for i in activities['items']))
        self.assertEqual(Catalog(self.db, 'facilitation').search(participants=20)['total'], 0)

    def test_all_registered_stdio_contracts(self):
        before = hashlib.sha256(self.db.read_bytes()).hexdigest()
        for server_id, registration in self.registrations.items():
            domain = registration['args'][1]
            tool_domain = domain.replace('-', '_')
            catalog = Catalog(self.db, domain)
            expected_ids = {i['id'] for i in catalog.export()['items']}
            all_ids = {i['id'] for d in self.registrations.values() for i in Catalog(self.db, d['args'][1]).export()['items']}
            foreign_id = next(i for i in sorted(all_ids) if i not in expected_ids)
            with self.subTest(server_id=server_id):
                env = dict(os.environ, ACTIVITIES_ATLAS_CONFIG=str(self.binding), PYTHONDONTWRITEBYTECODE='1')
                client = StdioClient([os.environ.get('ACTIVITIES_BOOTSTRAP_PYTHON', sys.executable), str(ROOT / 'scripts/atlas_library_mcp.py'), domain], env)
                try:
                    client.initialize()
                    tools = client.request('tools/list')['result']['tools']
                    names = {t['name'] for t in tools}
                    self.assertEqual(names, {f'search_{tool_domain}_atlas', f'browse_{tool_domain}_atlas', f'read_{tool_domain}_atlas', 'record_library_search_miss', 'review_library_search_misses'})
                    browse = next(t for t in tools if t['name'] == f'browse_{tool_domain}_atlas')
                    uri = f'ui://atlas-{domain}/library-prompt-v2.html'
                    self.assertEqual(browse['_meta']['ui']['resourceUri'], uri)
                    search = client.request('tools/call', {'name': f'search_{tool_domain}_atlas', 'arguments': {'limit': 100}})['result']
                    data = search['structuredContent']
                    self.assertEqual({i['id'] for i in data['items']}, expected_ids)
                    self.assertTrue(all('body' not in i for i in data['items']))
                    own_id = data['items'][0]['id']
                    read = client.request('tools/call', {'name': f'read_{tool_domain}_atlas', 'arguments': {'entry_ids': [own_id]}})['result']
                    self.assertIn('body', read['structuredContent']['items'][0])
                    rejected = client.request('tools/call', {'name': f'read_{tool_domain}_atlas', 'arguments': {'entry_ids': [foreign_id]}})['result']
                    self.assertTrue(rejected['isError'])
                    resources = client.request('resources/list')['result']['resources']
                    self.assertEqual([r['uri'] for r in resources], [uri])
                    html = client.request('resources/read', {'uri': uri})['result']['contents'][0]['text']
                    self.assertIn(own_id, html)
                    self.assertNotIn(foreign_id, html)
                    self.assertNotIn('__LIBRARY_DATA__', html)
                finally:
                    client.close()
        self.assertEqual(hashlib.sha256(self.db.read_bytes()).hexdigest(), before)
        self.assertFalse((self.db.parent / 'observability/library-search-misses.sqlite').exists())


if __name__ == '__main__':
    unittest.main()
