# Production routes and remote job control

Use when a new video combines several acquisition methods, needs missing footage, or depends on asynchronous generation. Keep the existing brief, shot list, asset-rights record and project manifest as the production contract. This is an agent procedure, not a new renderer or executable pipeline engine. Routine trims and exports go directly to their existing owner.

## Choose how each scene will be made

Choose from the actual inputs and the viewer's task. A project can mix routes; it does not need a new plugin or a mandatory cast of specialist agents.

| Route | Use when | First evidence and owner |
| --- | --- | --- |
| Recorded lesson or live software demo | The real interaction or instructor performance is the evidence | Ingest the recording and align transcript to actual UI events; `edit-dialogue-footage` preserves the demonstrated steps. |
| Original motion explainer | Diagrams, typography or controlled state changes explain an idea | `design-video-storyboards` defines key states; `create-motion-graphics` renders editable components using an available engine. |
| Footage-led montage | Actual motion, setting or historical material carries the story | Use [shot acquisition](../../ingest-video-assets/references/shot-acquisition.md) before choosing a generator or building a large media index. |
| Generated shot or product sequence | A necessary shot cannot reasonably be captured, licensed or built | Use [generated clip planning](generated-clip-planning.md), verify the provider, and test one representative shot. |
| Repurposed excerpt | A supplied long video contains a self-contained teaching payoff | Route to `edit-dialogue-footage`; use its course Shorts procedure when making a course Short. Preserve context and truthful title/thumbnail promises. |
| Translated version | An existing lesson needs a new language track or captions | Use [narration and dubbing](../../mix-video-audio/references/narration-and-dubbing.md); approve meaning and terminology before synthesis. |

For a software demonstration, distinguish a recording of real behavior from an authored simulation. A synthetic terminal or UI may explain a concept, but cannot serve as evidence that commands ran, an integration worked or a product supports a behavior. Label illustrative simulations and preserve actual execution evidence separately. Do not substitute one for a requested real recording.

For mixed routes, add only these planning columns to the existing shot list: scene ID, viewer purpose, acquisition route, required input, next owner, output location, and acceptance evidence. Choose meaningful movement: a demonstration, tracked relationship, animated diagram or actual moving footage. A pan across a still does not fulfill a promise of filmed action. A still may be the best teaching choice; record the choice instead of adding motion to meet an arbitrary quota.

## Bound generation before submitting it

For each external operation, record the available tool, provider/model, input media that would leave the machine, rights/voice consent where relevant, expected output, maximum attempts, elapsed-time limit, and authorized spend. Unknown pricing is not zero. With no paid authorization, keep the permitted incremental spend at zero and choose existing/local/free capabilities whose limits are verified. Do not inherit an upstream example's dollar allowance or assume a subscription includes API credits.

Set a small test sufficient to prove the hardest relationship before a batch: narration-to-diagram timing, product continuity, target-language instruction or motion through an occluder. Reuse an already approved strategy and authorization; pause only the action requiring a missing consequential choice. Reversible local assembly can continue while a provider job is pending.

## Keep a receipt beside the project

Use the project's existing asset/job record. If it has none, a short table or JSON sidecar is sufficient; do not create a daemon or second task database. Record:

- Scene/segment ID and input hashes, prompt/script revision, provider/model/settings revision.
- Submission time, operation, provider job ID, current state and last status-check time.
- Approved limit, estimated/reserved amount, actual charge when known; mark unknown charges explicitly.
- Local output path and hash, decoded duration/dimensions/audio properties, and review status.

Never include credentials, authorization headers or signed download URLs in receipts. States must distinguish planned, submitted, pending, failed, cancelled, downloaded, decoded and accepted. Provider success is not delivery acceptance.

If submission times out, query the original job or provider history before retrying. Use a documented idempotency mechanism if offered. An unknown outcome remains unknown; do not issue a second potentially chargeable submission to make a timeout disappear. Poll within the tool's documented limits and the task's wait budget; a job ID enables later resumption without keeping a worker alive. On a confirmed failed job, retry only within the agreed attempts and budget. Cancellation requests and confirmed cancellation are different states.

Validate downloaded bytes and media properties before linking them into the master timeline. A changed script, voice, source, model or visual direction invalidates dependent outputs; retain accepted unaffected assets by matching input/output hashes. Regenerate only affected dependencies, then recheck captions, mixes and exports that depend on them. Never silently substitute a paid provider, different voice or different renderer when a selected route fails.

## Example application

For a lesson promo, use an authentic screen excerpt for the demonstrated result, a brief authored diagram for the concept, and owned or item-licensed B-roll only where it adds meaning. For a requested Spanish version, reuse the source picture and approved segment map, test one representative translated passage, then update language-specific timing and captions. Keep publication in the existing social publishing workflow. These are planning examples, not claims that a clip has been rendered or a dubbing provider is connected.

## Source boundary

Review prompt: [OpenMontage](https://github.com/calesthio/OpenMontage/tree/9327439db69021ab4b0e2776729bf3b58fdb5a87), reviewed 2026-10-04; particularly its pipeline definitions and provider job/cost interfaces. This procedure is independently written for the existing studio and includes no upstream source, schema, agent roster or executable adapter. The upstream repository declares AGPL-3.0; copying or modifying its implementation for a future fork requires retaining its notices and reviewing the actual use/distribution and separate dependency/model terms. This reference does not authorize or install OpenMontage, Remotion, HyperFrames, a background board, cloud account or model.
