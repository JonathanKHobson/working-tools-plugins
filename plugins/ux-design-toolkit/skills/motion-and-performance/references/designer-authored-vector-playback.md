# Designer-authored vector playback in products

Use when an existing product is given an animated SVG, Lottie/dotLottie file, or Rive asset. First decide what the asset communicates: decoration, status, progress, onboarding, or an interactive state. Native CSS/SVG and the current product stack are enough for a simple state transition; a packaged animation is justified when authored visuals, states, or reuse need it. Graphic Design owns visual source fidelity and sequence art direction; this method owns product playback, meaning, accessibility and lifecycle. It installs no player.

## Declare the playback contract

Record the exact asset revision, target device/browser, player package and version, render mode, intrinsic size/aspect, poster or static end state, loop/one-shot intent, and the UI state that starts, pauses, resumes, seeks and ends it. Inspect the supplied composition range: `ip` is inclusive, `op` exclusive, so valid composition frames are `ip..op-1` (for `ip:12, op:20`, frames 12–19). A player may expose frame values or seconds; name units on every seek and translate with the verified API. Do not assume frame zero is in a nonzero-`ip` composition. For a loop, compare the wrap from `op-1` to `ip` with ordinary adjacent frame steps and intended velocity; pixel identity is not a smoothness test.

Choose an integration path based on the required behavior, not the file extension alone:

| Need | Candidate | Verify |
| --- | --- | --- |
| Small UI feedback using existing DOM/SVG | CSS, Web Animations, native platform animation | Focus, interruption and reduced-motion state with no new player. |
| Authored timeline with bounded segments or a static poster | Existing Lottie/dotLottie player | Target feature support, exact range, load/readiness, loop and resize behavior. |
| Named artboard plus interactive state machine | Existing Rive player | Inputs, state transitions, poster/state fallback, event ownership and actual runtime support. |
| Narrated/rendered piece | Video Production | Treat it as media; UI player behavior stays with the product. |

Inspect `graphic-design-studio:graphic-asset-compositing`'s animated vector interop method when exchanging SVG/Lottie files, but confirm the declared player's support yourself. A JSON parse or authoring preview does not certify a product renderer. Rive's asset structure and player API differ from Lottie; do not reuse Lottie frame controls as if they were Rive state-machine inputs.

## Implement a stateful, owned instance

Create the player only after its host exists. Pin imports to the project's installed package/version and consult that version's primary API for load, ready, error, play/pause/seek, resize and destroy. Define app states such as `unloaded`, `loading`, `ready`, `playing`, `paused`, `complete` and `error`; connect them to meaningful UI state. Treat load failure, a missing font, unsupported feature and an empty canvas as different diagnoses. Apply frame/range controls, metadata reads and listeners only after the player confirms the asset is loaded. Preserve a visible poster or meaningful static/control state while loading and after failure; essential copy must never depend solely on canvas frames.

If playing only in view, scope the observer to the owned element and define what happens when it leaves view, the page becomes hidden, or a dialog obscures it. Scroll-driven progress and timeline seeking need a documented mapping and clamping to the valid range, plus layout refresh after size/font changes. Avoid launching a new instance or stacking listeners on every state update. When unmounting or replacing the asset, remove every owned load, error, playback, visibility, resize, scroll, IntersectionObserver, media-query and state-machine listener; cancel owned animation/timers, then destroy the owned player. Verify repeated mount/unmount and rapid state changes do not produce duplicate playback or callbacks into a dead component.

For web content that starts moving, blinking or scrolling automatically, lasts more than five seconds, and appears alongside other content, provide a user mechanism to pause, stop or hide it unless the motion is essential, as [WCAG 2.2 SC 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html) specifies. A reduced-motion preference alone does not replace that control for users without the preference. For reduced motion, choose a meaningful still or low-motion state that carries the same status/action. Check the preference at start **and** react to preference changes while mounted. Make control focus and labels independent of moving artwork. Decorative canvas/SVG can be hidden from assistive technology; meaningful graphics need an accessible name or adjacent text. If a control triggers animation, its accessible state and keyboard operation must remain usable while the animation is paused or unavailable. A Rive interaction cannot be the only way to perform a required action unless equivalent keyboard and assistive paths exist.

## Verify the delivered experience

Test actual player pixels at initial/loading/ready/complete/error states, semantic beats, narrow and large layouts, normal and reduced motion, keyboard and screen reader semantics, interruption and re-entry, live preference change, and teardown. For loops inspect the wrap at speed. Keep the authoring source, poster, feature matrix, exact player/version, fallback and observed failures with the handoff. If the target player or asset is absent, state that setup gap; these instructions do not make a playback stack available.

## Source and rights

Adapted from `benmacdeezy/orns-forge` `aed3325472e435001f25ee316e733296cca6a526` (`skills/lottie-rive-vector-animation/SKILL.md`) and the original iart.ai `web-animation-skills` `b6dba3eb...` Lottie method, with Diffusion Studio's player-compatibility cautions. Exact captured paths/hashes and full MIT notices are in [source notices](../../../docs/motion-svg-source-notices.md). No upstream player script, package, CDN, app or runtime is included. Version-sensitive APIs must be verified against the installed player.
