// Run with EXT_APPS_SDK_APP=/path/to/@modelcontextprotocol/ext-apps/dist/src/app.js node --test tests/test_native_bridge_message.mjs
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import { pathToFileURL } from 'node:url';
import { runInNewContext } from 'node:vm';

const sdkPath = process.env.EXT_APPS_SDK_APP;
if (!sdkPath) throw new Error('Set EXT_APPS_SDK_APP to the installed MCP Apps SDK app.js for protocol validation.');
const { McpUiMessageRequestSchema } = await import(pathToFileURL(sdkPath).href);
const bridgeSource = await readFile(new URL('../runtime/writing-voice-library/ui/bridge.js', import.meta.url), 'utf8');

function connectedBridge(messageResult = {}) {
  const sent = [];
  const listeners = new Map();
  const parent = {
    postMessage(message) {
      sent.push(message);
      const result = message.method === 'ui/initialize'
        ? { protocolVersion: '2026-01-26', hostCapabilities: { message: { text: {} } }, hostContext: {} }
        : message.method === 'ui/message' ? messageResult : undefined;
      if (result !== undefined) queueMicrotask(() => listeners.get('message')?.({
        source: parent,
        data: { jsonrpc: '2.0', id: message.id, result },
      }));
    },
  };
  const window = {
    parent,
    addEventListener(type, listener) { listeners.set(type, listener); },
  };
  const document = { documentElement: { clientWidth: 400, dataset: {} }, body: { getBoundingClientRect() { return { height: 500 }; } } };
  class ResizeObserver { observe() {} }
  runInNewContext(bridgeSource, { window, document, setTimeout, clearTimeout, ResizeObserver, requestAnimationFrame(callback) { callback(); } });
  return { bridge: window.LibraryBridge, sent };
}

test('native message uses the installed MCP Apps request schema', async () => {
  const { bridge, sent } = connectedBridge();
  await bridge.sendMessage('Verified V01 + P28 handoff');
  const message = sent.find(item => item.method === 'ui/message');
  assert.ok(message);
  assert.deepEqual(JSON.parse(JSON.stringify(message.params.content)), [
    { type: 'text', text: 'Verified V01 + P28 handoff' },
  ]);
  assert.equal(McpUiMessageRequestSchema.safeParse(message).success, true);
  assert.equal(McpUiMessageRequestSchema.safeParse({ ...message, params: {
    role: 'user', content: { type: 'text', text: 'old invalid shape' },
  } }).success, false);
});

test('a host rejection cannot be reported as sent', async () => {
  const { bridge } = connectedBridge({ isError: true });
  await assert.rejects(bridge.sendMessage('handoff'), /host rejected/);
});
