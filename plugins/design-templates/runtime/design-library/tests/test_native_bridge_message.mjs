// Run with EXT_APPS_SDK_APP=/path/to/@modelcontextprotocol/ext-apps/dist/src/app.js node --test runtime/design-library/tests/test_native_bridge_message.mjs
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import { pathToFileURL } from 'node:url';
import { runInNewContext } from 'node:vm';

const sdkPath = process.env.EXT_APPS_SDK_APP;
if (!sdkPath) throw new Error('Set EXT_APPS_SDK_APP to the installed MCP Apps SDK app.js for protocol validation.');
const { McpUiMessageRequestSchema } = await import(pathToFileURL(sdkPath).href);
const bridgeSource = await readFile(new URL('../ui/bridge.js', import.meta.url), 'utf8');

function connectedBridge(messageResult = {}) {
  const sent = [];
  const listeners = new Map();
  const parent = {
    postMessage(message) {
      sent.push(message);
      const result = message.method === 'ui/initialize'
        ? { protocolVersion: '2026-01-26', hostCapabilities: { message: { text: {} }, openLinks: {} }, hostContext: {} }
        : message.method === 'ui/message' ? messageResult
          : message.method === 'ui/open-link' ? {} : undefined;
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
  await bridge.sendMessage('Verified template handoff');
  const message = sent.find(item => item.method === 'ui/message');
  assert.ok(message);
  assert.deepEqual(JSON.parse(JSON.stringify(message.params.content)), [
    { type: 'text', text: 'Verified template handoff' },
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

test('related Video Library link asks the native host to open the verified route', async () => {
  const { bridge, sent } = connectedBridge();
  const url = 'https://library.jkylehobson.chatgpt.site/video-library/';
  await bridge.openLink(url);
  const request = sent.find(item => item.method === 'ui/open-link');
  assert.deepEqual(JSON.parse(JSON.stringify(request.params)), { url });
});
