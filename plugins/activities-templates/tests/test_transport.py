"""Synthetic transport isolation, lifecycle, threading and private socket checks."""
import asyncio
from concurrent.futures import ThreadPoolExecutor
import fcntl
import json
import os
from pathlib import Path
import socket
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import anyio

from fixtures import ROOT, make_fixture
from test_runtime import StdioClient
from stdio_proxy import backend_key, connect, connect_backend, locked_file, private_directory
from shared_backend import ThreadedFastMCP, sdk_transport


class TransportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='atl-test-', dir='/tmp')
        self.directory = Path(self.temporary.name)
        self.vault, self.db = make_fixture(self.directory)
        self.misses = self.directory / 'misses.sqlite'
        self.sockets = self.directory / 's'
        self.sockets.mkdir(mode=0o700)
        self.env = dict(os.environ, ACTIVITIES_BACKEND_SOCKET_DIR=str(self.sockets),
                        ACTIVITIES_BACKEND_IDLE_SECONDS='0.3', PYTHONDONTWRITEBYTECODE='1')
        self.previous = {name: os.environ.get(name) for name in ('ACTIVITIES_BACKEND_SOCKET_DIR', 'ACTIVITIES_BACKEND_IDLE_SECONDS')}
        for name in self.previous:
            os.environ[name] = self.env[name]
        self.clients = []

    def tearDown(self):
        for client in self.clients:
            client.close()
        deadline = time.monotonic() + 5
        while list(self.sockets.glob('*.pid')) and time.monotonic() < deadline:
            time.sleep(0.05)
        self.assertFalse(list(self.sockets.glob('*.pid')), 'Owned test backend did not retire')
        for name, previous in self.previous.items():
            if previous is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = previous
        self.temporary.cleanup()

    def client(self, domain='ux'):
        client = StdioClient([sys.executable, '-B', str(ROOT / 'runtime/studio_library/stdio_proxy.py'),
                              '--db', str(self.db), '--domain', domain, '--misses', str(self.misses),
                              '--interpreter', sys.executable], self.env)
        self.clients.append(client)
        client.initialize()
        return client

    def test_concurrent_start_session_domain_and_binding_isolation(self):
        # Simultaneous starts share one backend but preserve independent SDK sessions.
        with ThreadPoolExecutor(max_workers=4) as executor:
            clients = list(executor.map(lambda _: self.client(), range(4)))
        receipts = [json.loads(p.read_text()) for p in self.sockets.glob('*.pid')]
        self.assertEqual(len(receipts), 1)
        backend_pid = receipts[0]['pid']
        self.assertTrue(all(c.request('tools/list')['result']['tools'] for c in clients))
        other = self.client('security')
        self.assertEqual(len(list(self.sockets.glob('*.pid'))), 2)
        names = {t['name'] for t in other.request('tools/list')['result']['tools']}
        self.assertIn('search_security_atlas', names)
        self.assertNotIn('search_ux_atlas', names)
        closed = clients.pop()
        closed.close()
        self.clients.remove(closed)
        time.sleep(0.6)
        os.kill(backend_pid, 0)  # Active connections survive periods longer than idle timeout.
        self.assertTrue(clients[0].request('tools/list')['result']['tools'])
        self.assertNotEqual(backend_key(self.db, 'ux', self.misses, sys.executable),
                            backend_key(self.db, 'ux', self.directory / 'other.sqlite', sys.executable))

    def test_fragmented_json_malformed_input_and_pending_eof_drain(self):
        client = self.client()
        # One bad line follows SDK handling, and does not close a separate valid request.
        client.process.stdin.write('{invalid}\n')
        client.process.stdin.flush()
        self.assertTrue(client.request('tools/list')['result']['tools'])
        # Do not terminate a pending feedback write when stdin reaches EOF.
        message = {'jsonrpc': '2.0', 'id': 99, 'method': 'tools/call', 'params': {
            'name': 'record_library_search_miss', 'arguments': {
                'task_key': '74a925c4-e1d7-443c-915f-c4b1c4a564bd', 'need_key': 'fixture-need',
                'route': 'ux', 'intent': 'synthetic transport verification', 'search_terms': 'fixture',
                'evidence': 'No suitable authored fixture record found', 'result_count': 0}}}
        encoded = json.dumps(message)
        client.process.stdin.write(encoded[:23])
        client.process.stdin.flush()
        client.process.stdin.write(encoded[23:])  # Final line at EOF, without newline.
        client.process.stdin.close()
        response = None
        while client.selector.select(timeout=5):
            line = client.process.stdout.readline()
            if not line:
                break
            candidate = json.loads(line)
            if candidate.get('id') == 99:
                response = candidate
        self.assertIsNotNone(response)
        self.assertFalse(response['result'].get('isError', False))
        self.assertTrue(json.loads(response['result']['content'][0]['text'])['logged'])
        self.assertTrue(self.misses.exists())
        self.assertEqual(client.process.wait(timeout=5), 0)
        client.selector.close()
        client.process.stdout.close()
        client.process.stderr.close()
        self.clients.remove(client)

    def test_private_modes_and_symlinks_rejected(self):
        client = self.client()
        for path in self.sockets.iterdir():
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        link = self.sockets / 'unsafe.lock'
        link.symlink_to(self.directory / 'target')
        with self.assertRaises(OSError):
            locked_file(link)
        socket_link = self.sockets / 'unsafe.sock'
        socket_link.symlink_to(next(self.sockets.glob('*.sock')))
        with self.assertRaises(ValueError):
            connect(socket_link)
        self.sockets.chmod(0o755)
        try:
            with self.assertRaises(ValueError):
                private_directory()
        finally:
            self.sockets.chmod(0o700)
        self.assertTrue(client.request('tools/list')['result']['tools'])

    def test_sync_handler_runs_off_event_loop_and_preserves_schema(self):
        async def check():
            server = ThreadedFastMCP('synthetic threading check')
            @server.tool()
            def slow(value: int = 3) -> int:
                time.sleep(0.2)
                return value
            tool = server._tool_manager.get_tool('slow')
            self.assertEqual(tool.parameters['properties']['value']['type'], 'integer')
            ticks = []
            async def tick():
                await asyncio.sleep(0.03)
                ticks.append(time.monotonic())
            started = time.monotonic()
            result, _ = await asyncio.gather(tool.run({'value': 4}), tick())
            self.assertEqual(result, 4)
            self.assertLess(ticks[0] - started, 0.15)
            self.assertEqual(slow(2), 2)  # Original nested sync callers remain valid.
        asyncio.run(check())

    def test_cancellation_then_eof_drains_and_completes_shielded_handler(self):
        async def check():
            send_input, receive_input = anyio.create_memory_object_stream(0)
            send_output, receive_output = anyio.create_memory_object_stream(0)
            started, finished = threading.Event(), threading.Event()
            transport_done = anyio.Event()
            server = ThreadedFastMCP('synthetic cancellation check')

            @server.tool()
            def pending() -> str:
                started.set()
                time.sleep(0.15)
                finished.set()
                return 'finished'

            class Stream:
                async def receive(self, maximum):
                    return await receive_input.receive()
                async def send(self, value):
                    await send_output.send(value)

            async def run():
                await sdk_transport(Stream(), bytearray(), server)
                transport_done.set()

            async def send(message):
                await send_input.send(json.dumps(message).encode() + b'\n')

            with anyio.fail_after(5):
                async with anyio.create_task_group() as group:
                    group.start_soon(run)
                    await send({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {
                        'protocolVersion': '2024-11-05', 'capabilities': {},
                        'clientInfo': {'name': 'synthetic-cancellation', 'version': '1'}}})
                    self.assertEqual(json.loads(await receive_output.receive())['id'], 1)
                    await send({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
                    await send({'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call',
                                'params': {'name': 'pending', 'arguments': {}}})
                    await anyio.to_thread.run_sync(started.wait)
                    await send({'jsonrpc': '2.0', 'method': 'notifications/cancelled',
                                'params': {'requestId': 2, 'reason': 'synthetic test'}})
                    await send_input.aclose()
                    response = json.loads(await receive_output.receive())
                    self.assertEqual(response['id'], 2)
                    self.assertIn('error', response)
                    await transport_done.wait()
                    self.assertTrue(finished.is_set())
            await receive_input.aclose()
            await send_output.aclose()
            await receive_output.aclose()
        anyio.run(check)

    def test_failed_backend_start_surfaces_without_respawn_loop(self):
        env = dict(self.env, PYTHONPATH='', PYTHONHOME='')
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'runtime/studio_library/stdio_proxy.py'),
            '--db', str(self.directory / 'missing.sqlite'), '--domain', 'ux', '--misses', str(self.misses),
            '--interpreter', sys.executable], env=env, capture_output=True, text=True, timeout=10)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unavailable', result.stderr)
        self.assertEqual(result.stdout, '')

    def test_dropped_sdk_response_has_bounded_eof_drain(self):
        async def check():
            class DroppedSDK:
                received = 0
                def create_initialization_options(self):
                    return None
                async def run(self, read_stream, write_stream, options):
                    async for message in read_stream:
                        self.received += 1  # Simulate an SDK that drops a response.

            class Stream:
                data = b'{"jsonrpc":"2.0","id":1,"method":"ping"}\n'
                async def receive(self, maximum):
                    if self.data:
                        data, self.data = self.data, b''
                        return data
                    raise anyio.EndOfStream
                async def send(self, value):
                    raise AssertionError('A dropped response must not be invented or replayed')

            sdk = DroppedSDK()
            started = time.monotonic()
            with anyio.fail_after(1):
                await sdk_transport(Stream(), bytearray(), SimpleNamespace(_mcp_server=sdk),
                                    eof_drain_seconds=0.04)
            self.assertEqual(sdk.received, 1)
            self.assertGreaterEqual(time.monotonic() - started, 0.03)
        anyio.run(check)

    def test_retiring_lease_wait_does_not_spend_start_attempts(self):
        key = backend_key(self.db, 'ux', self.misses, sys.executable)
        lease = locked_file(self.sockets / (key + '.lease'))
        fcntl.flock(lease, fcntl.LOCK_EX)
        real_popen = subprocess.Popen
        owned_processes = []
        def spawn(*args, **kwargs):
            process = real_popen(*args, **kwargs)
            owned_processes.append(process)
            return process
        try:
            with patch('stdio_proxy.subprocess.Popen', side_effect=spawn) as start:
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(connect_backend, self.db, 'ux', self.misses, sys.executable)
                    try:
                        time.sleep(0.2)
                        self.assertFalse(future.done())
                        self.assertEqual(start.call_count, 0)
                    finally:
                        fcntl.flock(lease, fcntl.LOCK_UN)
                    connection = future.result(timeout=5)
                    connection.close()
                    self.assertEqual(start.call_count, 1)
                    self.assertEqual(owned_processes[0].wait(timeout=5), 0)
        finally:
            os.close(lease)

    def test_owned_backend_crash_isolated_and_new_client_recovers(self):
        old = self.client('ux')
        security = self.client('security')
        key = backend_key(self.db, 'ux', self.misses, sys.executable)
        receipt = json.loads((self.sockets / (key + '.pid')).read_text())
        # This unique temporary directory was created by this test. Its active UX
        # connection and matching binding identify exactly the backend we started.
        self.assertEqual(receipt['domain'], 'ux')
        self.assertEqual(receipt['key'], key)
        self.assertEqual(Path(receipt['socket']).parent, self.sockets)
        os.kill(receipt['pid'], signal.SIGKILL)
        try:
            with self.assertRaises((RuntimeError, BrokenPipeError)):
                old.request('tools/call', {'name': 'record_library_search_miss', 'arguments': {
                    'task_key': '74a925c4-e1d7-443c-915f-c4b1c4a564bd', 'need_key': 'crash-fixture',
                    'route': 'ux', 'intent': 'synthetic crash verification', 'search_terms': 'fixture',
                    'evidence': 'Synthetic request after owned backend crash', 'result_count': 0}})
            self.assertEqual(old.process.wait(timeout=5), 1)
            self.assertFalse(self.misses.exists())
            self.assertTrue(security.request('tools/list')['result']['tools'])
            replacement = self.client('ux')
            self.assertTrue(replacement.request('tools/list')['result']['tools'])
            self.assertNotEqual(json.loads((self.sockets / (key + '.pid')).read_text())['pid'], receipt['pid'])
            self.assertFalse(self.misses.exists(), 'Failed writes must not be replayed by a new client')
        finally:
            old.selector.close()
            try:
                old.process.stdin.close()
            except BrokenPipeError:
                pass
            old.process.stdout.close()
            old.process.stderr.close()
            self.clients.remove(old)


if __name__ == '__main__':
    unittest.main()
