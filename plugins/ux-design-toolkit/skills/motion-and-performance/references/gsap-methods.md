# Conditional GSAP implementation

Code/JSON examples are illustrative and were inspected statically, not executed in a project runtime. Applying this method still requires task-specific execution and rendered verification.

Use for an explicitly selected or already installed GSAP implementation, especially sequencing, scroll-linked timelines, React lifecycle defects or measured GSAP frame-cost problems. The complete existing animate playbook still owns purpose, timing, accessibility and design judgment. Native platforms use their own providers; Figma-authored motion uses Figma's motion-context procedure. A small CSS transition needs no GSAP addition.

## Load the complete matching procedure

Read the needed full method and its dependencies, rather than using this entrypoint as a substitute:

- [Core](../../../libraries/gsap-methods/core.md): tweens, properties, target scope, interruptions, responsive/reduced-motion contexts.
- [Timeline](../../../libraries/gsap-methods/timeline.md), with core: labels, position parameters, nesting and playback.
- [React](../../../libraries/gsap-methods/react.md), with core and timeline/scroll when applicable: refs, useGSAP, context-safe callbacks, dependency updates and teardown.
- [ScrollTrigger](../../../libraries/gsap-methods/scrolltrigger.md), with core and timeline when applicable: range mapping, pinning, batch callbacks, custom scrollers, containerAnimation and refresh.
- [Performance](../../../libraries/gsap-methods/performance.md), with the method being profiled: frequent updates, batching, cleanup and target-device evidence.
- [SVG, text and Flip plugins](../../../libraries/gsap-methods/plugins-svg-text-flip.md), with core and the matching framework method: plugin selection, full official examples, SVG path/shape review, readable text and stateful layout changes.

## Project boundary and correctness checks

Availability checked 2026-10-05: [GSAP 3.13](https://gsap.com/blog/3-13/) added the former bonus plugins to the public package at no charge, including commercial use. MorphSVG, DrawSVG, SplitText, ScrollSmoother and Flip are available options; do not reject them solely as paid/Club-only. The [standard no-charge license](https://gsap.com/community/standard-license/) has restrictions on competing visual animation builders; ordinary AI-generated GSAP code is explicitly allowed in its FAQ. Check the project's actual use and version rather than describing GSAP as unrestricted or MIT-licensed. The MIT notice below covers the adapted method source, not the GSAP runtime. This update does not install any GSAP dependency.

1. Inspect the project's manifest/lockfile and existing imports. Reuse its package manager, GSAP version and architecture. This prose integration does not install a runtime, enable tools, approve new network code or migrate a chosen library. Re-check version-sensitive APIs against [primary GSAP docs](https://gsap.com/docs/v3/) at use time.
2. Keep selectors inside an owned root, or use direct refs. Store the owned context/media/timeline objects. Cleanup only those objects and owned listeners/timers; a component must not kill other components' ScrollTriggers. contextSafe records animation creation; it does not make callbacks inert after unmount.
3. For responsive and reduced-motion changes, revert the old setup before constructing the new one. Keep meaningful feedback and final content visible without spatial effects. Do not hide essential content while waiting for GSAP.
4. For fake horizontal scroll, calculate pixel distance with `x`, or calculate a true percentage with `xPercent`; do not mix units. Use `ease: "none"`, a scrubbed parent, functions for dimensions and refresh after layout changes. When pinning, move the child rather than its pinned wrapper. Higher `refreshPriority` values refresh first; default creation order is preferable.
5. Preserve focus, semantics and component lifetime. autoAlpha may hide content from interaction/accessibility; do not fade a focused control without an intentional focus destination. Respect existing transforms and do not use blanket clearProps where another system owns inline styles.
6. Validate interruptions and reversals; repeated mounting/unmounting; dependency updates; image/font-driven layout changes; mobile and keyboard; reduced-motion changes; and owned teardown. Inspect rendered anchors and profile expensive effects. CSS hints, numeric scrub and transform usage do not prove a frame-rate benefit.

## Acceptance examples

- Existing GSAP/React drawer: scoped creation, repeat open/close, interruption, listener removal and unmount all behave; the reduced-motion path reaches the same usable final state.
- Existing CSS hover: retain CSS; this method has no distinct work to do.
- Figma motion node: fetch the actual provider motion data and preserve its values; do not substitute these example timings.
- Missing GSAP dependency: name the execution/setup gap; use an authorized project setup path or existing stack. Never claim these Markdown methods made GSAP callable.

[Source and adaptations](../../../libraries/gsap-methods/PROVENANCE.md); [MIT notice](../../../libraries/gsap-methods/LICENSE). No source helper, hook, MCP, browser launcher or automatic updater is included.
