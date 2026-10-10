# Reference-led video adaptation

Use this when the user supplies an existing video as creative direction for a *new* piece. The output is an original brief and editable event plan that retains useful communication mechanisms while changing the content, not a frame-for-frame imitation. For a simple trim or platform crop, use the existing edit or conform owner instead. This procedure needs no Hypit installation or provider account.

## 1. Set the boundary

Record the target audience, viewer action, factual promise, source/reference identity, intended format, deadline, and authorized media. Infer from the supplied brief what the user wants to preserve; ask only when a consequential choice is missing: argument, comic premise, pacing, a visual device, or some combination. Name the required changes: speaker, product, claim, words, setting, appearance, duration, channel, or language. Mark exact source facts, third-party logos, faces, voices, music, footage, and distinctive creative elements as rights questions. A public reference is evidence for analysis, not permission to copy or impersonate it. Use material the user owns or has licensed; honor existing specific authorization for likeness/voice use, paid generation, and provider uploads. Resolve missing rights or authorization before the dependent action; do not ask again for a decision already supplied.

Keep the creative answer proportionate. One short test passage is often enough to prove the adaptation before a series of variants. Set a maximum test duration and generation/render cost before paid calls. The approved brief, asset rights ledger, and project manifest remain the source of truth.

## 2. Read the reference at two scales

Watch the full source with sound to understand its opening, promise, changes in attention, evidence, emotional turn, and payoff. Then inspect the smallest intervals needed to explain its distinctive behavior. Use `analyze-video-content` for transcript, word times, scene boundaries, representative frames, and contact sheets; seek denser frame views around short reveals, camera/graphic handoffs, and uncertain cuts. Reopen the source when a transcript or sparse sample cannot establish a visual or audio fact. Distinguish an observation from an interpretation: “the product image enters on the objection” is observed; “that makes the answer feel immediate” is an interpretation to test with the new piece.

Create a compact event map, not a transcript dump. For each distinct system, record:

| Field | Record |
| --- | --- |
| Source locator | Time range and evidence frame/clip path. |
| Viewer job | What the moment helps the viewer notice, understand, believe, feel, or do. |
| Trigger | A word, claim, question, reaction, action, musical event, or fixed clock interval. |
| Picture and sound | Subject, composition, caption, graphic, footage, motion, audio, and their relative placement. |
| Behavior | Entry, active state, change, hold, exit, and what persists across cuts. |
| Confidence | Observed, inferred, or unresolved; the next view needed if consequential. |

Document a recurring board, caption treatment, or sound motif once, then locate its changing states. Name the relationship that makes each device work. A reveal may answer a question; a picture may illustrate a phrase; an object may keep accumulating evidence. If the reference has no speech, use action and picture/sound changes as the anchors. Keep a few representative frames alongside the map so the user can evaluate the reading.

## 3. Transform purpose across the new piece

Write the new treatment around the user’s actual product, person, teaching task, or story. For each source device, decide **carry, redesign, or omit**, with a reason tied to the viewer’s job. Change every manifestation of a replaced subject: spoken claim, image, demonstration, graphic label, proof, offer and call to action. Preserve a useful role when its old physical form does not fit the new subject. If two references are used, assign each a distinct function and resolve conflicting rhythm or style explicitly.

Map the reference event to the target event by meaning. A graphic that appears when the source says a product name should follow the target’s corresponding word or claim; source seconds are locators for evidence, not target timing. Mark a fixed time only where a particular interval is itself the design. Write the target script and the event map together: event ID, target phrase/action anchor, graphic or media response, intended hold, and exit condition. Keep factual on-screen text exact and separately reviewable. Use the current output transcript’s word times when a recorded performance exists; do not reuse timestamps from a different voice or recording.

Choose one test segment with the strongest interaction among performance, media, caption, and motion. For every asset, record origin, rights/consent, provider/model if generated, input hashes, output hash, and actual decoded properties. A prompt, submitted job, playable clip, editable composition, and approved render are different states.

## 4. Build an editable expression

Place accepted media and target events in the renderer-neutral project manifest. Use `design-video-storyboards` for key states and `create-motion-graphics` for visual behavior beyond simple transforms. Group elements into one motion component when they share geometry, state, or coordinated movement; keep independent footage, caption and graphics separable when they have different lifetimes. Expose only the inputs a real revision would change: copy, image, semantic event, placement or style. Keep the project’s component/source files and dependencies with the project; normalize rendered slots before they enter the master timeline. Do not adopt a new renderer merely because the reference uses a similar visual effect.

For the test segment, retain the event map, script, storyboard, source/manifest and low-cost preview. Change the owning source when reviewing feedback; avoid patching only the exported video. If the target delivery changes duration, language or aspect ratio, recompute script/word anchors, caption layout, safe areas and the affected motion states. Run the relevant existing render and caption checks after each timing change.

## 5. Review what was actually made

Compare the target against the approved treatment and intended viewer job, not superficial resemblance. Inspect the full segment at normal speed with sound, then check first frame, each event entrance, the moment of meaning, settled hold, exit, captions, cut edges and final frame. Verify the visual elements land on the *target* words or actions and remain legible at delivery size. Record 3–8 anchors with source/output time, region, observed result, proposed change and recheck. Ask whether a changed person/product is represented consistently, the proof supports the claim, the piece avoids misleading continuity or false endorsement, and the transformation is original enough for its purpose and rights position.

Run `validate-video-quality` on the exact rendered file and keep its hash. If the one segment fails, fix that relationship before multiplying variants. If it succeeds and a series is authorized, parameterize only demonstrated variation and batch from the accepted editable source. Keep publish, upload and distribution status separate from local QA.

## Source and implementation boundary

This is independently written for Video Production Workflow after reviewing Hypit’s reference analysis, transformation, component and semantic timing ideas at commit `e8f94006e1eed9b299448fe5bce6afa5646e2ba5` (2026-10-02). It does not copy Hypit source text/code, SVML syntax, CLI, model providers, or project layout. Hypit uses its own modified Apache-style license with conditions on multi-tenant hosting, commercial redistribution and attribution; any future runtime use or copied implementation needs a separate license and security review. Source: https://github.com/hypit-ai/hypit/tree/e8f94006e1eed9b299448fe5bce6afa5646e2ba5 .
