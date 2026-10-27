import test from 'node:test';
import assert from 'node:assert/strict';
import { EventEmitter } from 'node:events';
import { browserProject, validateProjectShape, writeFrameToEncoder } from './render.mjs';

const project = () => ({
  schema: 'educational-canvas/1', fps: 24, durationSeconds: 12,
  formats: { landscape: [1280, 720], portrait: [720, 1280] },
  titleFirst: 'Check', titleSecond: 'one answer', takeaway: 'A check helps.',
  takeawayLines: ['A check', 'helps.'],
  steps: ['explorer', 'questioner', 'maker'].map(character => ({ action: 'Ask', why: 'Find a claim', example: 'Does it grow?', character })),
  palette: Object.fromEntries(['ink', 'teal', 'coral', 'yellow', 'aqua', 'white', 'muted'].map(key => [key, '#123ABC'])),
  diagramLabels: Object.fromEntries(['question', 'responsePrompt', 'response', 'source', 'sourceMeta', 'try', 'compare'].map(key => [key, 'Label'])),
  assets: Object.fromEntries(['fredoka', 'dmRegular', 'dmBold', 'shantell', 'logo', 'explorer', 'questioner', 'maker', 'underline', 'coralUnderline', 'flares'].map(key => [key, { path: `assets/${key}.png`, sha256: 'a'.repeat(64), source: '/private/source' }])),
  privateNote: '/private/note',
});

test('all browser consumed fields are checked before output creation', () => {
  const valid = project();
  assert.doesNotThrow(() => validateProjectShape(valid));
  for (const mutate of [
    p => { p.steps[1].why = null; },
    p => { p.steps[2].action = ''; },
    p => { p.steps[0].character = 'unknown'; },
    p => { p.takeawayLines[1] = 5; },
    p => { p.palette.ink = 'red'; },
    p => { p.diagramLabels.source = undefined; },
    p => { p.durationSeconds = Infinity; },
    p => { delete p.assets.logo; },
  ]) {
    const bad = project(); mutate(bad);
    assert.throws(() => validateProjectShape(bad));
  }
});

test('preview receives only declared rendering fields', () => {
  const input = project(), payload = browserProject(input);
  assert.equal(payload.steps[0].action, 'Ask');
  assert.equal(payload.assets.logo.path, 'assets/logo.png');
  assert.equal(JSON.stringify(payload).includes('/private/'), false);
  assert.equal(Object.hasOwn(payload, 'privateNote'), false);
  assert.equal(Object.hasOwn(payload.assets.logo, 'sha256'), false);
});

test('closed encoder rejects a backpressured write without waiting for drain', async () => {
  const encoder = new EventEmitter();
  encoder.exitCode = null;
  encoder.stdin = new EventEmitter();
  encoder.stdin.destroyed = false;
  encoder.stdin.write = () => false;
  const pending = writeFrameToEncoder(encoder, Buffer.from('frame'));
  encoder.exitCode = 1;
  encoder.stdin.destroyed = true;
  encoder.emit('close', 1, null);
  await assert.rejects(pending, /closed during frame write/);
});

test('drained encoder releases the blocked frame write', async () => {
  const encoder = new EventEmitter();
  encoder.exitCode = null;
  encoder.stdin = new EventEmitter();
  encoder.stdin.destroyed = false;
  encoder.stdin.write = () => false;
  const pending = writeFrameToEncoder(encoder, Buffer.from('frame'));
  encoder.stdin.emit('drain');
  await pending;
});
