# Author a bounded Lottie animation

Read for creating or materially editing a Lottie JSON asset from a brief, especially a logo, icon, loader or status sequence. Use [animated vector interop](../../graphic-asset-compositing/references/animated-vector-interop.md) for source geometry, keyframe correctness, text and the target feature matrix. Graphic Design owns the visual asset; UX owns its live product behavior; Video Production owns a rendered film and audio.

## Fix the output contract

Choose the real delivery player/platform and its pinned version before construction. A preview renderer is useful evidence only for itself. Inspect the current project and supplied asset, then record canvas size, frame rate, composition range, transparent/full-frame intent, one-shot/loop behavior, semantic beats, editable values and poster. Reuse approved palette, typography, geometry and motion vocabulary. For an overlay or icon preserve transparency unless a background is part of the brief; preview contrast belongs in the viewer rather than an unwanted baked rectangle.

Resolve the edit destination from the explicit file or project request. A currently visible scene is observational context, not permission to overwrite it. Re-read the latest source immediately before saving because a visual editor may write slot values back to the same JSON. If it changed, reconcile the actual changes rather than replacing them from a stale in-memory copy. Keep the input and a reversible version of the changed asset.

## Build and iterate

1. Define the message of entrance, action, settle and hold. Use a recognizable stable pose first. For a loader, keep pending state distinct from completion; for success/error, plan a stable final pose and restrained replay. A decorative progress sweep must not imply measured progress. Choose durations in seconds and translate them using the actual frame rate; fixed frame counts are not universal timing defaults.
2. Start with the few shapes or layers that carry that message. Preserve source pivots, stacking order, silhouette and negative space. Choose a single main mechanism such as a stroke reveal, staged assembly or orbit; add secondary motion only if it improves hierarchy. Design direction follows the actual brief, not an upstream universal ban on cards, borders, gradients or particular colors.
3. Author the composition metadata, assets and layers together. Validate `fr`, dimensions and `[ip, op)` against the output contract; valid composition frames end at `op-1`. Use the interop method's current/start-keyframe easing rule. Begin with a small rendered passage before adding the full sequence. If the selected player does not support a feature, simplify or bake it and record the compromise.
4. Make editability intentional. Expose only useful color, text or numeric values through slots or controls supported by the chosen player. Validate types, ranges and all references; an editable string needs long/short-copy checks and real font resolution. Preserve keyframed values when changing colors. A `controls.json` sidecar, `targetSids`, scene endpoint or font-loading convention from one authoring app is not part of every Lottie player.
5. Inspect the first valid frame (`ip`, not assumed zero), reveal, semantic beats, settle and last valid frame. Then play at delivery size and speed. For a loop, compare the wrap from `op-1` to `ip` with ordinary neighboring steps and intended velocity. Do not duplicate the first pose at the last sampled frame merely to make those images identical; this can create a hold in a continuous cycle.
6. Diagnose faults in order: parse/structure, missing assets or fonts, unsupported renderer feature, geometry/layer order, then design/timing. A valid JSON file can still be blank or illegible. Fix the smallest responsible layer and repeat the affected playback check.

If the project already uses Diffusion Studio's Skottie authoring app, use its actual bound local URL, scene route and supported frame controls, after checking the current application contract. Confirm the intended scene before any write. Its browser slot edits persist to source. Neither this method nor the MIT skill requires installing that app for a different delivery stack; setup and runnable server source require their own review before execution.

## Deliver and prove

Deliver the JSON, required assets/fonts with rights notes, editable source, poster, contract, any approximations, and exact tested player/version. Check transparency on light and dark preview surfaces; small icon readability; short/long editable text; initial/settled state; loop seam; and playback at intended size. Product use additionally needs UX's loading/error, pause, reduced-motion, interruption and teardown checks. If the target player is unavailable, label that acceptance gap instead of claiming cross-player readiness.

Map 3–8 actual visual anchors for the chosen asset and verify them after edits. A still/contact sheet can support frame findings but cannot prove motion continuity. No example render is implied by installing these instructions.

## Source

Adapted workflow concepts from [Diffusion Studio Text-to-Lottie](https://github.com/diffusionstudio/lottie/tree/3c72912fad543897f90045ed4d355813837927fc/skills/text-to-lottie), specifically the entrypoint, player contract and loader/icon recipe. The existing [source notice and MIT license](../../../docs/motion-svg-source-notices.md) apply. This original implementation procedure retains our corrected easing ownership and exclusive frame range, changes renderer lock-in to target-specific verification, and excludes upstream installation commands, runtime code and aesthetic mandates. The complete candidate remains in the private source-review record, not active discovery.
