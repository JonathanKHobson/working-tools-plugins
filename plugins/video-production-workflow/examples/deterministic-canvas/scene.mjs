// Deterministic 960x540 explainer: reference -> storyboard -> render.
// Every pixel is a pure function of (frame, fps). No clocks, no Math.random, no history.
export const W = 960, H = 540, DURATION = 12;
const ENTER = 0.6, EXIT = 0.5; // seconds; readable hold = remainder of each beat
export const BEATS = Object.freeze([
  { name: 'reference',  start: 0, end: 4,  label: '1  Reference',  caption: 'Start from approved source material.' },
  { name: 'storyboard', start: 4, end: 8,  label: '2  Storyboard', caption: 'Plan each beat before animating it.' },
  { name: 'render',     start: 8, end: 12, label: '3  Render',     caption: 'Render every frame from time alone.' },
]);
const FONT = 'MotionExample'; // preview loads local Arial explicitly before calling drawFrame
const C = { bg: '#101418', panel: '#1b222a', edge: '#3a4652', hi: '#e8c26a', ink: '#e9edf1', dim: '#7d8a96' };
const P = [60, 360, 660].map(x => ({ x, y: 150, w: 240, h: 190 }));

const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const ease = x => { x = clamp(x); return x * x * (3 - 2 * x); };
const lerp = (a, b, u) => a + (b - a) * u;
function hash(n) { // integer seed -> [0,1), stateless
  let x = (n | 0) ^ 0x9e3779b9;
  x = Math.imul(x ^ (x >>> 16), 0x85ebca6b);
  x = Math.imul(x ^ (x >>> 13), 0xc2b2ae35);
  return ((x ^ (x >>> 16)) >>> 0) / 4294967296;
}

export function sceneAt(frame, fps) {
  if (!Number.isInteger(frame) || frame < 0) throw new RangeError('frame must be a non-negative integer');
  if (!(Number.isFinite(fps) && fps > 0)) throw new RangeError('fps must be a positive number');
  const t = Math.min(frame / fps, DURATION);
  let index = BEATS.findIndex(b => t >= b.start && t < b.end);
  if (index < 0) index = BEATS.length - 1; // t === DURATION clamps to final hold
  const b = BEATS[index], local = t - b.start, len = b.end - b.start;
  const last = index === BEATS.length - 1; // final beat holds to the end, no exit
  const enter = ease(local / ENTER);
  const exit = last ? 0 : ease((local - (len - EXIT)) / EXIT);
  const phase = local < ENTER ? 'enter' : (!last && local >= len - EXIT) ? 'exit' : 'hold';
  return { frame, fps, t, beat: b.name, index, local, enter, exit, phase, pastEnd: frame / fps > DURATION };
}

function panelBox(ctx, p, active, alpha) {
  ctx.globalAlpha = alpha;
  ctx.fillStyle = C.panel; ctx.fillRect(p.x, p.y, p.w, p.h);
  ctx.strokeStyle = active ? C.hi : C.edge; ctx.lineWidth = active ? 3 : 1.5;
  ctx.strokeRect(p.x, p.y, p.w, p.h);
}
function drawReference(ctx, p, a) {
  ctx.globalAlpha = a; ctx.fillStyle = C.ink;
  ctx.beginPath(); ctx.arc(p.x + 60, p.y + 70, 28, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = C.dim; ctx.fillRect(p.x + 120, p.y + 44, 80, 52);
  ctx.fillStyle = C.hi; ctx.beginPath();
  ctx.moveTo(p.x + 120, p.y + 160); ctx.lineTo(p.x + 160, p.y + 112); ctx.lineTo(p.x + 200, p.y + 160);
  ctx.closePath(); ctx.fill();
}
function drawStoryboard(ctx, p, a, reveal) {
  const shown = Math.ceil(reveal * 6);
  for (let k = 0; k < 6; k++) {
    const cx = p.x + 18 + (k % 3) * 72, cy = p.y + 22 + Math.floor(k / 3) * 80;
    ctx.globalAlpha = a * (k < shown ? 1 : 0.15);
    ctx.strokeStyle = C.dim; ctx.lineWidth = 1.5; ctx.strokeRect(cx, cy, 60, 64);
    ctx.fillStyle = k % 2 ? C.ink : C.hi; // seeded, fixed per thumbnail
    ctx.beginPath(); ctx.arc(cx + 12 + hash(k) * 36, cy + 14 + hash(k + 99) * 36, 5, 0, Math.PI * 2); ctx.fill();
  }
}
function drawRender(ctx, p, a, local) {
  const u = clamp((local - ENTER) / 2.4); // dot travels, then holds settled
  ctx.globalAlpha = a; ctx.strokeStyle = C.dim; ctx.lineWidth = 1.5;
  ctx.strokeRect(p.x + 20, p.y + 20, p.w - 40, 110);
  ctx.fillStyle = C.hi; ctx.beginPath();
  ctx.arc(lerp(p.x + 40, p.x + p.w - 40, ease(u)), p.y + 75, 9, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = C.edge; ctx.fillRect(p.x + 20, p.y + 150, p.w - 40, 6);
  ctx.fillStyle = C.ink; ctx.fillRect(p.x + 20, p.y + 150, (p.w - 40) * u, 6); // playhead = f(t)
}

export function drawFrame(ctx, frame, fps) {
  const s = sceneAt(frame, fps);
  // This renderer owns its canvas; reset clears prior clips, paths, transforms and state.
  if (typeof ctx.reset !== 'function') throw new Error('CanvasRenderingContext2D.reset is required');
  ctx.reset();
  ctx.save();
  try {
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
    ctx.setLineDash([]); ctx.shadowBlur = 0; ctx.filter = 'none'; ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = C.bg; ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = C.ink; ctx.font = `600 30px ${FONT}`; ctx.fillText('From reference to render', 60, 96);
    for (let i = 0; i < 2; i++) { // connectors grow only as the next beat enters
      const g = s.index > i + 1 ? 1 : s.index === i + 1 ? s.enter : 0;
      if (!g) continue;
      const x0 = P[i].x + P[i].w + 8, x1 = P[i + 1].x - 8, y = P[i].y + P[i].h / 2;
      ctx.globalAlpha = 1; ctx.strokeStyle = C.dim; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(x0, y); ctx.lineTo(lerp(x0, x1, g), y); ctx.stroke();
    }
    P.forEach((p, i) => {
      const active = i === s.index;
      panelBox(ctx, p, active, i <= s.index ? 1 : 0.3);
      ctx.globalAlpha = 1; ctx.fillStyle = active ? C.ink : C.dim;
      ctx.font = `500 20px ${FONT}`; ctx.fillText(BEATS[i].label, p.x, p.y + p.h + 34);
      if (i > s.index) return;
      const a = active ? s.enter * (1 - 0.4 * s.exit) : 0.55; // past beats dim, never vanish
      if (i === 0) drawReference(ctx, p, a);
      if (i === 1) drawStoryboard(ctx, p, a, active ? clamp(s.local / 1.5) : 1);
      if (i === 2) drawRender(ctx, p, a, active ? s.local : DURATION);
    });
    const from = P[Math.max(0, s.index - 1)], to = P[s.index]; // persistent attention marker
    ctx.globalAlpha = 1; ctx.fillStyle = C.hi;
    ctx.fillRect(lerp(from.x, to.x, s.index ? s.enter : 1), to.y - 14, to.w, 4);
    ctx.globalAlpha = s.enter * (1 - s.exit); ctx.fillStyle = C.ink; ctx.font = `400 22px ${FONT}`;
    ctx.fillText(BEATS[s.index].caption, 60, 470);
  } finally { ctx.restore(); }
}
