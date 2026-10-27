# Thinking Orbs Canvas adaptation

This folder supplies the complete nine-state geometry engine from `Jakubantalik/thinking-orbs` revision `de85557ca220332586d070d8788c0e1d6e877a0d` (repository archive SHA-256 `2fd523b0d78a7b4cd0d0bafccc86f7009e3d0d06bf3453abf5b29a567cb3a7d1`). The upstream MIT license is preserved in full in [LICENSE](LICENSE). `vendor-src/src` contains the unchanged production source. `engine/*.mjs` and `presets.mjs` are a dependency-free conversion of the pure TypeScript geometry and presets; [input-output-sha256.json](input-output-sha256.json) records both sides of every conversion. `orb-canvas.mjs` is the local browser adapter. Use it through the existing motion workflow and review each consuming interface or film.

## Integration

Keep `orb-canvas.mjs`, `presets.mjs`, `engine/`, and `LICENSE` together. Import `drawAt` for deterministic frames or `mountOrb` for animation:

```js
import { mountOrb } from './orb-canvas.mjs';
const orb = mountOrb(canvas, {
  state: 'working', size: 64, speed: 1, dark: true,
  paused: false, label: 'Working'
});
// When replacing or removing the canvas:
orb.dispose();
```

`drawAt(canvas, { state, size, timeSeconds, dark })` uses engine time directly. The nine states are `working`, `searching`, `solving`, `listening`, `connecting`, `weaving`, `composing`, `breathing`, and `shaping`. Only the tuned sizes 20 and 64 CSS pixels are accepted. `timeSeconds` must be finite in `[0, 1,000,000]`, `speed` finite in `(0, 4]`, and `dark`/`paused` boolean. `drawAt` returns a geometry frame, so callers can inspect or export the actual marks.

`mountOrb` draws a static frame at engine time 0.6 on mount, for paused and reduced-motion states, and when motion preference changes to reduced. It waits for the first intersection report before starting RAF, never schedules RAF while the document is hidden, and cancels RAF on offscreen, hidden, reduced, and disposal transitions. If IntersectionObserver is unavailable it uses document visibility alone. It sets `role="img"` and an accessible label on the canvas. The owning UI must provide visible state text or status as appropriate; this package supplies visuals only. Recreate the mount for changed state/size/theme/speed props. Call `dispose()` at teardown; repeat calls are safe.

## Audit and verification

- The reviewed read-only `skillguard_scan.py` scanned 53 source files: 0 active findings, digest `07dc6eb0ea35a9fd8a9aaebe03e687546c1cb65ebb6b64645108f1047598d0ed`.
- Manual review covered all 11 `src/engine/*.ts` files plus `src/presets.ts`, `src/theme.ts`, `src/ThinkingOrb.tsx`, and `src/types.ts`. The shipped React component has a React peer dependency; the adapted runtime imports none of it. The source geometry and presets use `Math`, arrays, and local modules. No network, storage, credentials, dynamic code execution, subprocess, or external runtime imports appeared in those production files. Upstream demo, port, and package scripts were excluded from execution and runtime delivery.
- A geometry test found upstream `weaving` alpha of about 1.0023 for size 64 at time zero. CSS Canvas alpha clamps this at paint time. It is retained to preserve source geometry and recorded here as a minor source behavior, not a security finding.
- Run `node --test tests/orb.test.mjs` in this folder with an existing Node 24 runtime. To regenerate after reviewing a source change, run `node build.mjs`, then the tests. Node's built-in `module.stripTypeScriptTypes` strips types; this script rewrites only local extensionless imports to `.mjs`. It reads the bundled `vendor-src`, with no external source checkout. No npm install or upstream script is needed.
- Tests cover input/output file hashes, all nine states at both tuned sizes and four times, finite geometry, out-of-order deterministic frames, invalid input rejection, reduced/paused/initially hidden static behavior, visibility/intersection gates, live motion preference, and repeated teardown.

The automated lifecycle tests use a fake Canvas. Actual browser rendering and visual comparison remain required for a new consumer; unit tests do not establish cross-browser equality. The source archive was bound to a stable branch head during retrieval; archive SHA-256 and per-file hashes are provenance evidence, not signed runtime attestation. This adapter resets its owned canvas on every exact draw to remove inherited clipping, alpha and compositing state.

Open `gallery.html` through an existing local HTTP server to inspect all nine states at both sizes. It starts paused and provides play/pause and light/dark controls. Reduced motion remains static. No remote asset or package load is required.
