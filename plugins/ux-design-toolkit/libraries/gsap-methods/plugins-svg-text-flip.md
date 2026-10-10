# Conditional GSAP plugins: SVG, text and Flip

Use only in a project that already selects GSAP or explicitly asks for it. Confirm the installed GSAP version, actual imports, bundler and relevant plugin APIs against [primary GSAP documentation](https://gsap.com/docs/v3/) before implementation. Register each needed plugin once before use. Keep animation selectors within an owned root and clean up owned contexts, splits, timelines and listeners at teardown. The [core](core.md), [timeline](timeline.md), [React](react.md) and [performance](performance.md) methods remain the main implementation support. No runtime or installer is packaged here.

After selecting a relevant plugin, read its **complete selected official procedure and examples** in [the deferred source excerpt](plugins-svg-text-flip-official.md). The adapter below adds project ownership and review constraints; it does not replace the full method.

## SVG shape choice

| Visual need | GSAP method if selected | Asset and behavior checks |
| --- | --- | --- |
| Reveal a drawn contour | DrawSVGPlugin on a visible stroked path | `drawSVG` is the visible path segment, e.g. `"0% 100%"`, not a duration. A fill alone cannot draw on. Check path direction, caps, dashes, transformed scale and completion. Split a multi-subpath contour if its sequence must be controlled. |
| Morph one shape into another | MorphSVGPlugin | Unlike direct CSS/SMIL path-data interpolation, MorphSVG can normalize different point counts. Inspect middle frames for crossing, twists, holes and identity. Try `map`, `shapeIndex`, rotational type or split paths only if the selected version supports them. Converting primitives to paths mutates DOM; scope and preserve semantics/IDs. |
| Move an object along a route | MotionPathPlugin | Check path/target alignment, origin, tangent rotation, responsive geometry, interruption and end position. A path-following object may need an independent focus/semantic location. |

All three are target-renderer methods, not Lottie export guarantees. Keep stable, namespaced SVG IDs; verify references in `url(#id)`, masks and clips after optimization. Consult Graphic Design Studio's animated vector interop method for source/export fidelity. Animate the owned SVG node rather than assuming the internals of an `<img src="...svg">` can be selected. Prefer simpler native transforms for a two-line icon toggle or a single fade. Test reduced-motion final states and keyboard interaction in the product.

## Text as readable content

SplitText is for per-word, character or line art direction when existing text remains accurate and accessible. Split only the units required. Wait for the actual font/layout or use the selected version's `autoSplit` with `onSplit` returning its owned animation so re-splits can clean up and track progress. A line split changes after width or font changes; test mobile, zoom and late font load. Revert the split on teardown to restore original markup. Verify the chosen `aria` mode with nested links and meaningful inline semantics; a screen-reader-only duplicate may be needed when wrappers would otherwise hide interactive content. Do not animate essential words to an inaccessible hidden state while users may focus them. SplitText does not operate on SVG `<text>`; use a separate asset method there. ScrambleText is optional expression, not a replacement for readable copy or a state label; show the final exact text without motion.

## Flip for layout changes

Use Flip when a grid/list/detail layout genuinely changes location. Capture the old layout with `Flip.getState()` **before** the DOM/class mutation, apply the new layout, then animate with `Flip.from()` using scoped targets. Preserve stable item identity and any focused control during reorder; do not let an animated clone become the only semantic element. Decide whether absolutely positioned transition elements can overlap other content. Nested transforms, image/font loading and responsive size changes require a rendered check; measure after the layout is ready. A reduced-motion path applies the final DOM state directly. Test rapid repeated toggles, reversals and component unmount, and clean up only the Flip animation this component owns. If CSS already handles a simple disclosure without losing state/focus, keep it.

## Review contract

Review at real playback speed and on the target device/viewport. Check entering and settled pixels plus mid-morph geometry, stroke coverage, path alignment, text wrap/reading order, focused state, interruption, reduced-motion changes and teardown. Profile a measured issue before claiming a plugin is faster. For source SVG-to-Lottie work, no GSAP tween by itself proves export compatibility; Graphic's target-player matrix and product-player validation still apply.

## Provenance

Adapted from GreenSock's official `greensock/gsap-skills` `aed9cfd3277740755f6bfc1155c7aa645403b760`, `skills/gsap-plugins/SKILL.md`, SVG, SplitText/ScrambleText and Flip sections. See [PROVENANCE](PROVENANCE.md) and the preserved [MIT notice](LICENSE). The documentation license does not imply a project has installed or licensed a runtime; check the current GSAP package/terms at use time.
