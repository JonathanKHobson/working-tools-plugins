import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { drawAt, mountOrb, ORB_STATES } from '../orb-canvas.mjs';

test('staged source and generated output match the recorded hashes', async () => {
  const manifest = JSON.parse(await readFile(new URL('../input-output-sha256.json', import.meta.url)));
  assert.equal(Object.keys(manifest).length, 12);
  for (const [source, item] of Object.entries(manifest)) {
    const original = await readFile(new URL(`../vendor-src/${source}`, import.meta.url));
    const generated = await readFile(new URL(`../${item.output}`, import.meta.url));
    assert.equal(createHash('sha256').update(original).digest('hex'), item.sha256);
    assert.equal(createHash('sha256').update(generated).digest('hex'), item.outputSha256);
  }
});

function surface({ reduced = false, hidden = false, observe = true } = {}) {
  const calls = [];
  const attrs = {};
  const listeners = new Map();
  const queue = new Map();
  let id = 0;
  let observer;
  const mq = { matches: reduced, addEventListener: (_t, cb) => listeners.set('motion', cb), removeEventListener: () => listeners.delete('motion') };
  const win = {
    devicePixelRatio: 1.5,
    matchMedia: () => mq,
    requestAnimationFrame: cb => { const n = ++id; queue.set(n, cb); return n; },
    cancelAnimationFrame: n => queue.delete(n),
    IntersectionObserver: observe ? class { constructor(cb) { observer = { cb, disconnected: false }; } observe() {} disconnect() { observer.disconnected = true; } } : undefined
  };
  const doc = { defaultView: win, visibilityState: hidden ? 'hidden' : 'visible', addEventListener: (t, cb) => listeners.set(t, cb), removeEventListener: t => listeners.delete(t) };
  const ctx = { setTransform: (...x) => calls.push(['transform', ...x]), clearRect: (...x) => calls.push(['clear', ...x]), beginPath() {}, arc(...x) { assert.ok(x.every(Number.isFinite)); }, fill() {}, moveTo(...x) { assert.ok(x.every(Number.isFinite)); }, lineTo(...x) { assert.ok(x.every(Number.isFinite)); }, stroke() {} };
  const canvas = { ownerDocument: doc, style: {}, width: 0, height: 0, getContext: () => ctx, setAttribute: (k, v) => { attrs[k] = v; } };
  return { canvas, calls, attrs, queue, listeners, mq, doc, get observer() { return observer; }, step(now) { const pending = [...queue.values()]; queue.clear(); for (const cb of pending) cb(now); } };
}

test('all nine shipped states produce finite bounded geometry at both tuned sizes', () => {
  assert.equal(ORB_STATES.length, 9);
  for (const state of ORB_STATES) for (const size of [20, 64]) for (const timeSeconds of [0, 0.6, 8.3, 1234.5]) {
    const { canvas } = surface();
    const frame = drawAt(canvas, { state, size, timeSeconds, dark: false });
    assert.ok(frame.dots.length > 0, state);
    assert.ok(frame.dots.length < 5000, state);
    assert.ok(frame.lines.length < 5000, state);
    for (const dot of frame.dots) {
      for (const key of ['x', 'y', 'z', 'r', 'white']) assert.ok(Number.isFinite(dot[key]), `${state}.${key}`);
      assert.ok(dot.r > 0 && dot.r < size);
      assert.ok(dot.x > -size && dot.x < size * 2);
      assert.ok(dot.y > -size && dot.y < size * 2);
      // Upstream weaving can exceed 1 by ~0.002; CSS alpha clamps at paint time.
      if (dot.a !== undefined) assert.ok(Number.isFinite(dot.a) && dot.a >= 0 && dot.a < 1.1);
    }
    for (const line of frame.lines) for (const key of ['x1', 'y1', 'x2', 'y2', 'w', 'white']) assert.ok(Number.isFinite(line[key]), `${state}.${key}`);
    assert.equal(canvas.width, Math.round(size * 1.5));
  }
});

test('out of order calls return the identical requested frame', () => {
  const s = surface();
  const hash = frame => createHash('sha256').update(JSON.stringify(frame)).digest('hex');
  for (const state of ORB_STATES) {
    const a = hash(drawAt(s.canvas, { state, size: 64, timeSeconds: 2.75, dark: true }));
    drawAt(s.canvas, { state, size: 64, timeSeconds: 600, dark: false });
    assert.equal(hash(drawAt(s.canvas, { state, size: 64, timeSeconds: 2.75, dark: true })), a);
  }
});

test('invalid and unbounded public inputs fail clearly', () => {
  const { canvas } = surface();
  const good = { state: 'working', size: 64, timeSeconds: 0.6, dark: true };
  for (const bad of [{ state: '__proto__' }, { size: 999 }, { size: NaN }, { timeSeconds: Infinity }, { timeSeconds: -1 }, { timeSeconds: 1e8 }, { dark: 'yes' }]) assert.throws(() => drawAt(canvas, { ...good, ...bad }));
  for (const speed of [0, -1, Infinity, NaN, 5, '1']) assert.throws(() => mountOrb(canvas, { state: 'working', size: 64, dark: true, speed }));
  assert.throws(() => drawAt(null, good));
});

test('reduced motion, paused and hidden initial state are static', () => {
  for (const conditions of [{ reduced: true }, { hidden: true }, {}]) {
    const s = surface(conditions);
    const handle = mountOrb(s.canvas, { state: 'shaping', size: 20, dark: true, paused: !conditions.reduced && !conditions.hidden });
    assert.equal(s.queue.size, 0);
    assert.equal(s.attrs.role, 'img');
    assert.ok(s.calls.some(c => c[0] === 'clear'));
    handle.dispose();
  }
});

test('intersection, visibility and reduced preference govern RAF; teardown is idempotent', () => {
  const s = surface();
  const handle = mountOrb(s.canvas, { state: 'working', size: 64, dark: false, label: 'Thinking' });
  assert.equal(s.queue.size, 0); // await first intersection report
  s.observer.cb([{ isIntersecting: true }]);
  assert.equal(s.queue.size, 1);
  s.step(100);
  assert.equal(s.queue.size, 1);
  s.doc.visibilityState = 'hidden'; s.listeners.get('visibilitychange')();
  assert.equal(s.queue.size, 0);
  s.observer.cb([{ isIntersecting: false }]);
  s.doc.visibilityState = 'visible'; s.listeners.get('visibilitychange')();
  assert.equal(s.queue.size, 0);
  s.observer.cb([{ isIntersecting: true }]);
  assert.equal(s.queue.size, 1);
  s.mq.matches = true; s.listeners.get('motion')({ matches: true });
  assert.equal(s.queue.size, 0);
  s.mq.matches = false; s.listeners.get('motion')({ matches: false });
  assert.equal(s.queue.size, 1);
  handle.dispose(); handle.dispose();
  assert.equal(s.queue.size, 0);
  assert.equal(s.listeners.size, 0);
  assert.equal(s.observer.disconnected, true);
  assert.equal(s.attrs['aria-label'], 'Thinking');
});
