#!/usr/bin/env node
import assert from 'node:assert/strict';
import { spawn, execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { createServer } from 'node:http';
import { readFile, writeFile, mkdir, mkdtemp, copyFile, rm, readdir, stat } from 'node:fs/promises';
import { homedir } from 'node:os';
import { basename, dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import { setTimeout as delay } from 'node:timers/promises';
import { pruneCache, validatePayload } from '../scripts/state.mjs';
import { inspectRichClipboard, writeRichClipboard } from '../scripts/clipboard.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const captureScript = join(root, 'scripts/capture.mjs');
const fixtureDir = join(root, 'fixtures');
if (!process.argv[2]) throw new Error('Usage: node tests/integration.mjs /absolute/path/to/test-output');
const verificationRoot = resolve(process.argv[2]);
const copyOnly = process.argv[3] === '--copy-only';
const copyOutput = copyOnly ? resolve(process.argv[4] || '') : null;
if (copyOnly && !process.argv[4]) throw new Error('Usage: node tests/integration.mjs OUTPUT --copy-only EXISTING_CAPTURE_OUTPUT');
const lockPath = join(homedir(), '.cache/html-to-figma-clipboard/capture.lock');
const checks = [];
const bugs = [];
let work, localServer, copyServer, copyBrowser;

function check(name, fn) {
  if (copyOnly && !['local Copy for Figma button preserves parsed payload',
    'capture copy server exits, closes port, and preserves parsed payload'].includes(name)) return Promise.resolve();
  return Promise.resolve().then(fn).then(
    detail => { checks.push({ name, status: 'passed', detail: detail ?? null }); },
    error => { checks.push({ name, status: 'failed', error: String(error.stack || error) }); bugs.push(name); },
  );
}

async function exists(path) { try { await stat(path); return true; } catch { return false; } }
async function json(path) { return JSON.parse(await readFile(path, 'utf8')); }
async function lockFree() {
  for (let i = 0; i < 120; i++) {
    if (!(await exists(lockPath))) return;
    await delay(500);
  }
  throw new Error('Capture lock did not clear within 60 seconds');
}
async function waitForLock(pid) {
  for (let i = 0; i < 120; i++) {
    if (await exists(lockPath)) {
      const lock = await json(lockPath).catch(() => null);
      if (lock?.pid === pid) return lock;
    }
    await delay(100);
  }
  throw new Error('Capture did not acquire its lock');
}
function ownedBrowserPids(parentPid) {
  const lines = execFileSync('/bin/ps', ['-axo', 'pid=,ppid=,command='], { encoding: 'utf8' }).split('\n');
  const processes = lines.map(line => /^\s*(\d+)\s+(\d+)\s+(.+)$/.exec(line)).filter(Boolean)
    .map(match => ({ pid: Number(match[1]), ppid: Number(match[2]), command: match[3] }));
  const descendants = new Set([parentPid]);
  let changed;
  do {
    changed = false;
    for (const process of processes) if (descendants.has(process.ppid) && !descendants.has(process.pid)) {
      descendants.add(process.pid); changed = true;
    }
  } while (changed);
  return processes.filter(process => descendants.has(process.pid) && process.pid !== parentPid &&
    /Chromium|Chrome for Testing|chrome-mac|chrome-headless-shell/i.test(process.command)).map(process => process.pid);
}
async function waitForOwnedBrowser(parentPid) {
  for (let i = 0; i < 60; i++) {
    const pids = ownedBrowserPids(parentPid);
    if (pids.length) return pids;
    await delay(100);
  }
  throw new Error(`No owned Chromium process appeared under capture PID ${parentPid}`);
}
async function assertOwnedBrowsersGone(pids) {
  for (let i = 0; i < 50; i++) {
    const alive = pids.filter(pid => { try { process.kill(pid, 0); return true; } catch { return false; } });
    if (!alive.length) return;
    await delay(100);
  }
  throw new Error(`Owned Chromium processes remain: ${pids.join(', ')}`);
}
function startCapture(input, out, extra = []) {
  const args = [captureScript, input, '--selector', '#diagnostic', '--out', out, '--no-copy', ...extra];
  const child = spawn(process.execPath, args, { stdio: ['ignore', 'pipe', 'pipe'] });
  let stdout = '', stderr = '';
  child.stdout.on('data', chunk => { stdout += chunk; });
  child.stderr.on('data', chunk => { stderr += chunk; });
  const done = new Promise((fulfill, reject) => {
    child.once('error', reject);
    child.once('close', (code, signal) => fulfill({ code, signal, stdout, stderr, pid: child.pid, args }));
  });
  return { child, done };
}
async function capture(input, name, extra = [], expectSuccess = true) {
  await lockFree();
  const out = join(work, name);
  const { done } = startCapture(input, out, extra);
  const result = await done;
  if (expectSuccess) assert.equal(result.code, 0, result.stderr || result.stdout);
  const report = await json(join(out, 'report.json'));
  return { ...result, out, report };
}
async function strictCapture(input, name, extra = []) {
  const run = await capture(input, name, [...extra, '--strict']);
  assert.equal(run.report.statuses.conversion, 'passed');
  assert.equal(run.report.statuses.clipboard, 'not-run');
  return run;
}
async function listen(server) {
  await new Promise((resolveReady, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolveReady);
  });
  return `http://127.0.0.1:${server.address().port}`;
}
async function closeServer(server) {
  if (!server) return;
  server.closeAllConnections();
  await new Promise(resolveClosed => server.close(resolveClosed));
}
function modified(html, addition) { return html.replace('</body>', `${addition}</body>`); }
async function setClipboardSentinel(label) {
  const html = `<meta charset="utf-8"><div><span data-metadata="<!--(figmeta)${label}(/figmeta)-->"></span><span data-buffer="<!--(figma)sentinel(/figma)-->"></span></div>`;
  await writeRichClipboard(html);
  assert.equal((await inspectRichClipboard()).html, html);
  return html;
}
async function assertBrowserClipboard(expected, sentinel) {
  const state = await inspectRichClipboard();
  assert.ok(state.types.includes('public.html'));
  assert.ok(state.html && state.html !== sentinel, 'Browser did not replace native clipboard sentinel');
  const runtime = (await json(join(homedir(), '.config/html-to-figma-clipboard/runtime.json'))).runtime;
  const { parseClipboardHtml } = await import(join(runtime, 'node_modules/@figit/fig-kiwi/dist/index.mjs'));
  const actual = parseClipboardHtml(state.html);
  const source = parseClipboardHtml(expected);
  const hash = bytes => createHash('sha256').update(bytes).digest('hex');
  assert.equal(hash(actual.fig), hash(source.fig), 'Browser clipboard fig-kiwi bytes differ from capture');
  assert.deepEqual(actual.meta, source.meta, 'Browser clipboard metadata differs from capture');
  return { types: state.types, figSha256: hash(actual.fig), meta: actual.meta, rawHtmlExact: state.html === expected };
}

await mkdir(verificationRoot, { recursive: true });
await lockFree();
work = await mkdtemp(join(verificationRoot, 'integration-'));
const fixtureSource = await readFile(join(fixtureDir, 'diagnostic.html'), 'utf8');
const sourceDir = join(work, 'source');
await mkdir(sourceDir);
const input = join(sourceDir, 'diagnostic.html');
const image = join(sourceDir, 'pattern.svg');
await writeFile(input, fixtureSource);
await copyFile(join(fixtureDir, 'pattern.svg'), image);

let first = copyOnly ? { out: copyOutput } : undefined;
let second, htmlChanged, assetChanged, viewportChanged, absolute;
await check('strict clean conversion and editable node types', async () => {
  first = await strictCapture(input, 'clean-first');
  assert.equal(first.report.cache.hit, false);
  assert.ok(first.report.nodeCounts.TEXT > 0);
  assert.ok(first.report.nodeCounts.VECTOR > 0);
  const document = await json(join(first.out, 'document.json'));
  assert.ok(document.nodeChanges.some(node => node.type === 'FRAME' && ['VERTICAL', 'HORIZONTAL'].includes(node.stackMode)));
  assert.equal(validatePayload(await readFile(join(first.out, 'clipboard.html'), 'utf8')).valid, true);
  return { counts: first.report.nodeCounts, cache: first.report.cache };
});
await check('same source uses cache', async () => {
  second = await strictCapture(input, 'clean-second');
  assert.equal(second.report.cache.hit, true);
  assert.equal(second.report.cache.key, first.report.cache.key);
});
await check('HTML change invalidates cache', async () => {
  await writeFile(input, fixtureSource.replace('Local fixture', 'Changed fixture'));
  htmlChanged = await strictCapture(input, 'html-changed');
  assert.equal(htmlChanged.report.cache.hit, false);
  assert.notEqual(htmlChanged.report.cache.key, second.report.cache.key);
});
await check('local image asset change invalidates cache', async () => {
  await writeFile(image, (await readFile(image, 'utf8')).replace(/#[a-fA-F0-9]{6}/, '#123456'));
  assetChanged = await strictCapture(input, 'asset-changed');
  assert.equal(assetChanged.report.cache.hit, false);
  assert.notEqual(assetChanged.report.cache.key, htmlChanged.report.cache.key);
});
await check('viewport change invalidates cache', async () => {
  viewportChanged = await strictCapture(input, 'viewport-changed', ['--width', '1024']);
  assert.equal(viewportChanged.report.cache.hit, false);
  assert.notEqual(viewportChanged.report.cache.key, assetChanged.report.cache.key);
});
await check('absolute layout invalidates cache and removes auto layout', async () => {
  absolute = await strictCapture(input, 'absolute', ['--layout', 'absolute']);
  assert.equal(absolute.report.cache.hit, false);
  assert.notEqual(absolute.report.cache.key, assetChanged.report.cache.key);
  const document = await json(join(absolute.out, 'document.json'));
  assert.ok(document.nodeChanges.every(node => Object.keys(node).every(key => !key.startsWith('stack'))));
  const auto = await json(join(assetChanged.out, 'document.json'));
  const geometry = node => node.nodeChanges.map(item => ({ type: item.type, name: item.name, size: item.size, transform: item.transform }));
  assert.deepEqual(geometry(document), geometry(auto));
});
await check('localhost URL input is supported', async () => {
  localServer = createServer(async (req, res) => {
    const file = req.url === '/pattern.svg' ? image : input;
    res.writeHead(200, { 'Content-Type': req.url === '/pattern.svg' ? 'image/svg+xml' : 'text/html' });
    res.end(await readFile(file));
  });
  const url = await listen(localServer);
  try {
    const run = await strictCapture(url + '/diagnostic.html', 'localhost');
    assert.equal(run.report.source, url + '/diagnostic.html');
    return { url, counts: run.report.nodeCounts };
  } finally {
    await closeServer(localServer); localServer = null;
  }
});
await check('external image, font, script, fetch and WebSocket are blocked', async () => {
  const external = join(sourceDir, 'external.html');
  const addition = `<style>@font-face{font-family:RemoteProbe;src:url(https://example.invalid/font.woff2)}#remote-font{font-family:RemoteProbe}</style><span id="remote-font">Remote font</span><img src="https://example.invalid/image.png"><script src="https://example.invalid/script.js"></script><script>fetch('https://example.invalid/data.json').catch(()=>{});try{new WebSocket('wss://example.invalid/socket')}catch{}</script>`;
  await writeFile(external, modified(fixtureSource, addition));
  const run = await capture(external, 'external');
  assert.equal(run.report.statuses.conversion, 'degraded');
  const blocked = run.report.blockedRequests.map(item => item.url);
  for (const resource of ['image.png', 'font.woff2', 'script.js', 'data.json', '/socket'])
    assert.ok(blocked.some(url => url.includes(resource)), `Missing blocked ${resource}: ${JSON.stringify(blocked)}`);
  return { blocked };
});
await check('missing local font is reported without remote substitution', async () => {
  const missing = join(sourceDir, 'missing-font.html');
  await writeFile(missing, fixtureSource.replace('font-family:Arial,sans-serif', 'font-family:DefinitelyMissingFont,sans-serif'));
  const run = await capture(missing, 'missing-font');
  assert.equal(run.report.statuses.conversion, 'degraded');
  assert.ok(run.report.diagnostics.fonts.some(font => font.error && /DefinitelyMissingFont/.test(JSON.stringify(font))));
  assert.equal(run.report.blockedRequests.filter(item => /font/.test(item.url)).length, 0);
  return { fonts: run.report.diagnostics.fonts, omitted: run.report.diagnostics.omitted.length };
});
await check('explicit font map resolves a local alias', async () => {
  const fontPath = '/System/Library/Fonts/Supplemental/Arial.ttf';
  assert.ok(await exists(fontPath), `Missing local test font: ${fontPath}`);
  const mapped = join(sourceDir, 'mapped-font.html');
  await writeFile(mapped, fixtureSource.replaceAll('Arial,sans-serif', 'LocalAlias,sans-serif'));
  const mapPath = join(sourceDir, 'fonts.json');
  await writeFile(mapPath, JSON.stringify([
    { family: 'LocalAlias', weight: 400, italic: false, path: fontPath },
    { family: 'LocalAlias', weight: 700, italic: false, path: '/System/Library/Fonts/Supplemental/Arial Bold.ttf' },
  ]));
  const run = await strictCapture(mapped, 'mapped-font', ['--font-map', mapPath]);
  assert.ok(run.report.diagnostics.fonts.some(font => /LocalAlias/.test(JSON.stringify(font)) && !font.error));
  return { fonts: run.report.diagnostics.fonts };
});
await check('bad selector fails and releases lock', async () => {
  await lockFree();
  const out = join(work, 'bad-selector');
  const { child, done } = startCapture(input, out, ['--selector', '#does-not-exist', '--settle-ms', '1500', '--timeout', '10000']);
  await waitForLock(child.pid);
  const browserPids = await waitForOwnedBrowser(child.pid);
  const run = await done;
  const report = await json(join(out, 'report.json'));
  assert.notEqual(run.code, 0);
  assert.equal(report.statuses.conversion, 'failed');
  assert.equal(await exists(lockPath), false);
  await assertOwnedBrowsersGone(browserPids);
});
await check('SIGTERM closes capture and releases lock', async () => {
  await lockFree();
  const { child, done } = startCapture(input, join(work, 'sigterm'), ['--settle-ms', '10000']);
  await waitForLock(child.pid);
  const browserPids = await waitForOwnedBrowser(child.pid);
  child.kill('SIGTERM');
  const run = await done;
  assert.equal(run.code, 143, JSON.stringify(run));
  await lockFree();
  assert.equal(await exists(lockPath), false);
  await assertOwnedBrowsersGone(browserPids);
});
await check('concurrent capture rejects second owner', async () => {
  await lockFree();
  const firstActive = startCapture(input, join(work, 'concurrent-first'), ['--settle-ms', '1500']);
  await waitForLock(firstActive.child.pid);
  const secondActive = startCapture(input, join(work, 'concurrent-second'));
  const rejected = await secondActive.done;
  assert.notEqual(rejected.code, 0);
  assert.match(rejected.stderr, /Another capture is running/);
  const completed = await firstActive.done;
  assert.equal(completed.code, 0, completed.stderr);
  await lockFree();
});
await check('cache pruning honors maxEntries', async () => {
  const cache = join(work, 'prune');
  await mkdir(cache);
  for (let i = 0; i < 3; i++) {
    const name = i.toString(16).padStart(64, '0') + '.json';
    await writeFile(join(cache, name), '{}');
    await delay(20);
  }
  await pruneCache(cache, { maxEntries: 2, maxAge: 7 * 86400000 });
  const remaining = (await readdir(cache)).filter(name => name.endsWith('.json'));
  assert.equal(remaining.length, 2);
});
await check('stale lock is recovered', async () => {
  await lockFree();
  await mkdir(dirname(lockPath), { recursive: true });
  await writeFile(lockPath, JSON.stringify({ pid: 99999999, token: 'integration-stale-lock' }), { flag: 'wx', mode: 0o600 });
  try {
    const out = join(work, 'stale-lock');
    const { done } = startCapture(input, out, ['--strict']);
    const result = await done;
    assert.equal(result.code, 0, result.stderr);
    const report = await json(join(out, 'report.json'));
    assert.equal(report.statuses.conversion, 'passed');
    assert.equal(await exists(lockPath), false);
  } finally {
    const value = await json(lockPath).catch(() => null);
    if (value?.token === 'integration-stale-lock') await rm(lockPath, { force: true });
  }
});
await check('local Copy for Figma button preserves parsed payload', async () => {
  const output = first?.out;
  assert.ok(output, 'Clean capture unavailable');
  const html = await readFile(join(output, 'clipboard.html'), 'utf8');
  const sentinel = await setClipboardSentinel('customserver');
  assert.notEqual(html, sentinel);
  copyServer = createServer(async (req, res) => {
    const file = req.url === '/copy.html' ? 'copy.html' : 'clipboard.html';
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(await readFile(join(output, file)));
  });
  const url = await listen(copyServer);
  const runtime = (await json(join(homedir(), '.config/html-to-figma-clipboard/runtime.json'))).runtime;
  process.env.PLAYWRIGHT_BROWSERS_PATH = join(runtime, 'browsers');
  const require = createRequire(join(runtime, 'package.json'));
  const { chromium } = require('playwright');
  let browserPids = [];
  try {
    copyBrowser = await chromium.launch({ headless: false, channel: 'chrome' });
    browserPids = ownedBrowserPids(process.pid);
    const context = await copyBrowser.newContext({ permissions: ['clipboard-read', 'clipboard-write'] });
    const page = await context.newPage();
    await page.goto(url + '/copy.html');
    await page.locator('#copy').click();
    await assert.doesNotReject(() => page.locator('#status').getByText('Rich clipboard write completed').waitFor());
    const readback = await assertBrowserClipboard(html, sentinel);
    return { htmlBytes: Buffer.byteLength(html), ...readback };
  } finally {
    if (copyBrowser) { await copyBrowser.close(); copyBrowser = null; }
    await assertOwnedBrowsersGone(browserPids);
    await closeServer(copyServer); copyServer = null;
  }
});
await check('capture copy server exits, closes port, and preserves parsed payload', async () => {
  const output = first?.out;
  assert.ok(output, 'Clean capture unavailable');
  const expectedHtml = await readFile(join(output, 'clipboard.html'), 'utf8');
  const sentinel = await setClipboardSentinel('realcopyserver');
  assert.notEqual(expectedHtml, sentinel);
  const child = spawn(process.execPath, [captureScript, 'copy', output], { stdio: ['ignore', 'pipe', 'pipe'] });
  let stdout = '', stderr = '', url;
  let exited = false;
  const done = new Promise((resolveDone, reject) => {
    child.once('error', reject);
    child.once('close', (code, signal) => { exited = true; resolveDone({ code, signal, stdout, stderr }); });
  });
  const announced = new Promise((resolveAnnounced, reject) => {
    const deadline = setTimeout(() => reject(new Error('Copy server did not announce a URL')), 10000);
    child.stdout.on('data', chunk => {
      stdout += chunk;
      if (url || !stdout.includes('\n')) return;
      try { url = JSON.parse(stdout.slice(0, stdout.indexOf('\n'))).url; clearTimeout(deadline); resolveAnnounced(url); }
      catch (error) { clearTimeout(deadline); reject(error); }
    });
    child.stderr.on('data', chunk => { stderr += chunk; });
  });
  let browser, browserPids = [];
  try {
    const copyUrl = await announced;
    assert.match(copyUrl, /^http:\/\/127\.0\.0\.1:\d+\/copy\.html$/);
    const runtime = (await json(join(homedir(), '.config/html-to-figma-clipboard/runtime.json'))).runtime;
    process.env.PLAYWRIGHT_BROWSERS_PATH = join(runtime, 'browsers');
    const require = createRequire(join(runtime, 'package.json'));
    browser = await require('playwright').chromium.launch({ headless: false, channel: 'chrome' });
    browserPids = ownedBrowserPids(process.pid);
    const context = await browser.newContext({ permissions: ['clipboard-read', 'clipboard-write'] });
    const page = await context.newPage();
    await page.goto(copyUrl);
    await page.locator('#copy').click();
    await page.locator('#status').getByText('Rich clipboard write completed').waitFor();
    const readback = await assertBrowserClipboard(expectedHtml, sentinel);
    const completion = await Promise.race([done, delay(10000).then(() => { throw new Error('Copy server stayed alive after button click'); })]);
    assert.equal(completion.code, 0, completion.stderr);
    await assert.rejects(fetch(copyUrl, { signal: AbortSignal.timeout(1000) }), /fetch failed|ECONNREFUSED|socket hang up/i);
    return { url: copyUrl, exitCode: completion.code, portClosed: true, htmlBytes: Buffer.byteLength(expectedHtml), ...readback };
  } finally {
    if (browser) await browser.close();
    await assertOwnedBrowsersGone(browserPids);
    if (!exited) { child.kill('SIGTERM'); await done; }
  }
});

const result = {
  generatedAt: new Date().toISOString(),
  suite: 'html-to-figma-clipboard integration',
  work,
  checks,
  passed: checks.filter(item => item.status === 'passed').length,
  failed: checks.filter(item => item.status === 'failed').length,
  bugs,
};
const resultPath = join(verificationRoot, copyOnly ? 'integration-copy-results.json' : 'integration-results.json');
await writeFile(resultPath, JSON.stringify(result, null, 2));
console.log(JSON.stringify({ resultPath, passed: result.passed, failed: result.failed, bugs }, null, 2));
if (result.failed) process.exitCode = 1;
