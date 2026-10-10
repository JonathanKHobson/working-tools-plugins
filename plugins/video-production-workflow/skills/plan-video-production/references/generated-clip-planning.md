# Generated clip planning and Sora legacy handoff

Read this only when a video brief calls for generated footage, a Sora-era clip, or a remix-like variation. Keep the production brief, shot list, rights ledger, and rendered QA in Video Production Studio. Creative Writing Studio owns story premise, screenplay beats, dialogue, character continuity, and canon before these become shot instructions.

## Current provider boundary

As checked on 2026-09-29, OpenAI says the Sora web/app experience ended on 2026-04-26 and the Sora Videos API ended on 2026-09-24 ([Sora discontinuation](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation), [API deprecations](https://developers.openai.com/api/docs/deprecations)). The older local `sora` skill and `scripts/sora.py` target that retired API. Do not run the preserved legacy runner as a working generation path, claim that a ChatGPT subscription grants API access, or present its old model, size, duration, guardrail, or pricing tables as current. Existing exported clips can still be ingested as source media. If the user asks for new generation, prepare the shot brief; use a provider only after its current capability, terms, cost, and actual tool access are verified for this task. A prompt draft is not a generated clip.

## Shot brief

Start with the intended beat and the target delivery frame. For each proposed clip, specify only details that the user supplied or that the approved brief supports:

| Field | Decision |
|---|---|
| Purpose | Where the clip sits in the story and what it must communicate. |
| Scene | Subject, setting, visible materials, time of day, and atmosphere. |
| Action | One primary action, with sequential beats or counts when timing matters. |
| Camera | Framing, angle, lens/field of view if useful, and one main move or locked-off shot. |
| Look | Lighting direction/quality, palette anchors, texture, and continuity with neighboring shots. |
| Audio/text | Spoken line, ambient cue, or exact visible text only when required; plan captions and text overlays separately when legibility matters. |
| Invariants | What a variation must retain: subject, framing, camera, background, timing, or color. |
| Avoid | Specific known failure modes such as flicker, jitter, unstable reflections, illegible text, or abrupt motion. |

Keep generated-shot language compact: one main subject and action, one camera setup, and a small number of purposeful beats. Short prompts leave more variation; detailed prompts narrow interpretation without guaranteeing the result. For continuity, repeat stable descriptors across shots and change one variable per iteration. Split a complex sequence into independently reviewable shots when feasible. Provider-controlled duration, aspect ratio, resolution, and inputs belong in the actual tool parameters, not only in prose; verify those parameters against current provider documentation before use.

## Choose a shape

- **Cinematic or ambient:** Choose a static wide, dolly, short orbit, lateral move, or restrained handheld drift. Use lighting and palette to set mood; an ambient loop needs subtle movement and a clean join.
- **Social/product:** Give each beat a clear benefit or visual reveal. Keep onscreen copy short, verbatim, and inside the verified delivery safe area. A before/after needs an unmistakable state change, not only a transition effect.
- **UI/explainer:** Prefer a locked camera and a simple action sequence. Use real captured UI or deterministic motion graphics when exact interface text or state matters; a generated mock is not evidence of a working product.
- **Remix-like variation:** State the single requested change and explicit invariants. Compare the new clip to the source on subject, framing, timing, color, audio, and factual claims.

## Handoff and review

Record source/provider, model/version if known, prompt or brief, generation date, rights/consent status, input references, outputs, and hashes in the project asset ledger. Keep source exports unchanged; work from copies. For unavailable Sora jobs or assets, record the exact missing ID or file and do not imply retrieval succeeded. Route actual clips through `ingest-video-assets`, storyboard/timeline placement, audio and caption review, then `validate-video-quality`. Inspect rendered frames and listen to audio for continuity, flicker, malformed subjects, unwanted text/logos, dialogue errors, and mismatched aspect ratios. A storyboard, prompt, job request, downloaded file, and QA-approved final render are separate states.

This method adapts the useful shot grammar, cinematic/social templates, prompt iteration, and failure checks from the previously installed Apache-2.0 `sora` skill. The complete original source, every example/template, and its CLI/API files are preserved under `../../../libraries/sora/` and explicitly loaded by the production-planning head. The API execution route is historical; the full shot-craft procedures remain operative.

## Remote job receipts

For paid or asynchronous clip generation, follow [production routes and job control](production-routes-and-job-control.md): retain the original job ID, reconcile unknown submission outcomes, bound spend/attempts, and validate downloaded bytes before accepting the shot.
