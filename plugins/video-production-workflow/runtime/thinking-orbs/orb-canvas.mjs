import { MODE_FRAMES, paintFrame } from './engine/index.mjs';
import { resolvePreset, STATE_TO_MODE } from './presets.mjs';

export const ORB_STATES = Object.freeze(Object.keys(STATE_TO_MODE));
const STATIC_TIME = 0.6;

function validate(canvas, { state, size, timeSeconds, dark, speed, paused, label }, mount = false) {
  if (!canvas || typeof canvas.getContext !== 'function') throw new TypeError('canvas must provide getContext');
  if (!Object.hasOwn(STATE_TO_MODE, state)) throw new RangeError('state must be one of the nine orb states');
  if (size !== 20 && size !== 64) throw new RangeError('size must be 20 or 64 CSS pixels');
  if (typeof dark !== 'boolean') throw new TypeError('dark must be boolean');
  if (mount) {
    if (typeof speed !== 'number' || !Number.isFinite(speed) || speed <= 0 || speed > 4) throw new RangeError('speed must be finite, greater than 0, and at most 4');
    if (typeof paused !== 'boolean') throw new TypeError('paused must be boolean');
    if (label !== undefined && (typeof label !== 'string' || !label.trim())) throw new TypeError('label must be a nonempty string');
  } else if (typeof timeSeconds !== 'number' || !Number.isFinite(timeSeconds) || timeSeconds < 0 || timeSeconds > 1e6) {
    throw new RangeError('timeSeconds must be finite and between 0 and 1,000,000');
  }
}

/** Deterministic frame at caller supplied elapsed seconds. Canvas remains transparent. */
export function drawAt(canvas, { state, size, timeSeconds, dark }) {
  validate(canvas, { state, size, timeSeconds, dark });
  const ctx = canvas.getContext('2d');
  if (!ctx) throw new Error('2D canvas context unavailable');
  const ratio = Math.min(2, Math.max(1, Number(canvas.ownerDocument?.defaultView?.devicePixelRatio) || 1));
  const pixels = Math.round(size * ratio);
  // This adapter owns the canvas. Reset even at an unchanged size: a caller's
  // clipping path, alpha or composite mode must not poison a later exact frame.
  canvas.width = pixels;
  if (canvas.height !== pixels) canvas.height = pixels;
  if (canvas.style) { canvas.style.width = `${size}px`; canvas.style.height = `${size}px`; }
  const { mode, opts } = resolvePreset(state, size);
  const frame = MODE_FRAMES[mode](size, timeSeconds, opts);
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  ctx.clearRect(0, 0, size, size);
  paintFrame(ctx, frame, dark);
  return frame;
}

/** Mount a single orb. Call dispose() before replacing it or removing its canvas. */
export function mountOrb(canvas, { state, size, speed = 1, dark, paused = false, label } = {}) {
  validate(canvas, { state, size, speed, dark, paused, label }, true);
  const doc = canvas.ownerDocument;
  const win = doc?.defaultView;
  if (!doc || !win || typeof win.requestAnimationFrame !== 'function' || typeof win.cancelAnimationFrame !== 'function') {
    throw new Error('mountOrb requires a browser canvas with requestAnimationFrame');
  }
  canvas.setAttribute('role', 'img');
  canvas.setAttribute('aria-label', label ?? `${state[0].toUpperCase()}${state.slice(1)}…`);
  const mq = typeof win.matchMedia === 'function' ? win.matchMedia('(prefers-reduced-motion: reduce)') : null;
  const baseSpeed = resolvePreset(state, size).speed;
  let reduced = Boolean(mq?.matches);
  let intersecting = false;
  let disposed = false;
  let raf = null;
  let elapsed = 0;
  let lastNow = null;
  const render = seconds => drawAt(canvas, { state, size, timeSeconds: seconds, dark });
  const stop = () => { if (raf !== null) win.cancelAnimationFrame(raf); raf = null; lastNow = null; };
  const eligible = () => !disposed && !paused && !reduced && doc.visibilityState !== 'hidden' && intersecting;
  const tick = now => {
    raf = null;
    if (!eligible()) return;
    if (lastNow !== null) elapsed = Math.min(1e6 / (speed * baseSpeed), elapsed + Math.max(0, Math.min(0.1, (now - lastNow) / 1000)));
    lastNow = now;
    render(elapsed * speed * baseSpeed);
    raf = win.requestAnimationFrame(tick);
  };
  const sync = () => {
    if (!eligible()) { stop(); if (reduced || paused) render(STATIC_TIME); return; }
    if (raf === null) raf = win.requestAnimationFrame(tick);
  };
  const onReduced = event => { reduced = Boolean(event.matches); sync(); };
  const onVisibility = () => sync();
  const Observer = win.IntersectionObserver;
  const io = typeof Observer === 'function' ? new Observer(([entry]) => { intersecting = Boolean(entry?.isIntersecting); sync(); }) : null;
  if (!io) intersecting = true;
  render(STATIC_TIME);
  mq?.addEventListener?.('change', onReduced);
  doc.addEventListener('visibilitychange', onVisibility);
  io?.observe(canvas);
  sync();
  return {
    dispose() {
      if (disposed) return;
      disposed = true;
      stop();
      io?.disconnect();
      mq?.removeEventListener?.('change', onReduced);
      doc.removeEventListener('visibilitychange', onVisibility);
    }
  };
}
