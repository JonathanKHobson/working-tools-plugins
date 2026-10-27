"""Owned bounded stdio test client; adapted from Activities Templates transport tests."""
import subprocess,selectors,json,queue,threading,tempfile
from pathlib import Path

class StdioClient:
    def __init__(self, command, env):
        self.errors = tempfile.TemporaryFile(mode='w+t')
        self.process = subprocess.Popen(command, cwd=Path(__file__).resolve().parents[1], env=env, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=self.errors, text=True)
        self.responses = queue.Queue()
        def read():
            for line in self.process.stdout:
                self.responses.put(line)
            self.responses.put(None)
        self.reader = threading.Thread(target=read, daemon=True)
        self.reader.start()
        self.serial = 0

    def request(self, method, params=None):
        self.serial += 1
        message = {'jsonrpc': '2.0', 'id': self.serial, 'method': method}
        if params is not None:
            message['params'] = params
        self.process.stdin.write(json.dumps(message) + '\n')
        self.process.stdin.flush()
        while True:
            try:
                line = self.responses.get(timeout=20)
            except queue.Empty:
                raise RuntimeError('MCP response timed out: '+method)
            if not line:
                self.errors.seek(0)
                raise RuntimeError('MCP server exited: ' + self.errors.read()[-1500:])
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
        if not self.process.stdin.closed:
            self.process.stdin.close()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            self.process.wait(timeout=5)
        self.process.stdout.close()
        self.reader.join(timeout=2)
        self.errors.close()
