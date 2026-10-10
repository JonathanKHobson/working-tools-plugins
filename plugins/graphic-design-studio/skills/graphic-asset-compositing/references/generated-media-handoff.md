# Generated-media handoff and Open Generative AI web admission

Owners: Graphic Design Studio (image asset art direction) and Video Production Workflow (shot/media QA, ingest and final delivery). Original synthesis informed by Open Generative AI ebebc51eb3740641458a4a11ce03f390e7a58af1, MIT. This is an optional generation procedure and optional generation procedure and runtime boundary; it is not an installed image/video backend or new wrapper.

## Operation-first generation contract

Choose the task before the model. packages/studio/src/videoWorkflows.js:13-51 exposes animate_image, keyframes, references, edit_video, extend_uploaded_video and motion_transfer with required media. Use that separation in the existing studio owners:

| Task | Required input | Acceptance criterion |
| --- | --- | --- |
| Animate image | Approved start frame | Composition/identity remains recognizable; motion matches requested action |
| Start/end frames | Approved start and end frames | Both boundary frames respected; transition does not add factual labels |
| References | Specifically authorized image/video/audio references | Reference purpose/rights and likeness use clear; no unexplained identity drift |
| Edit video | Source video and bounded edit intent | Requested change visible; protected material preserved |
| Extend video | Source video, desired added duration | Seam continuity and duration checked; source stays retained |
| Motion transfer | Character image and driving video | Character identity preserved; motion meaning and permissions fit |

Models expose different capabilities; a selectable model name is not proof that it accepts all slots/durations/resolutions. Source code validation at videoWorkflows.js:891-939 rejects missing media and projects fields. Preserve an equivalent preflight using the actual provider's current schema: task, required slots, max references, aspect, duration, resolution, audio policy, negative prompt support and price boundary. On model change revalidate every supplied slot and surface discarded/unsupported fields before generation. Do not silently drop references.

## Asset record and transfer

Record one immutable generation receipt per accepted asset: project/shot ID; task; original file path/hash for each authorized reference; source/rights; purpose (illustration, dramatization, evidence); prompt/version; provider/model/revision if available; submitted task ID; options/duration/aspect/resolution; approved spend ceiling; output path/hash; actual decoded media properties; status; failed/incomplete/filtered outcome; provider URL/expiry; review anchors and reviewer decision. Prompt/model selection is prepared state. Task submitted is not a downloaded playable output. Provider URL alone is not a durable source file. Never report a model-catalog count as installed local models.

Download an actual completed output into project assets with deterministic safe naming, cap file size, reject HTML/error bodies, validate MIME/decoder, and keep source/receipt. A provider's hosted result must not be the only durable copy. Pass accepted local assets to Video Production Workflow's existing ingest/render and QA. It owns cuts, reading-time/safe-area checks, loudness/conform and final delivery. Graphic Design Studio owns deterministic exact copy, typography, QR destination and print export; generate illustration layers, then compose exact text in its established workflow.

For visual acceptance map 3-8 anchors before the generated job: subject identity, action, framing, continuity, protected text, relevant background. Compare actual output at those anchors, inspect representative frames and the whole transition/playback where needed. Flag unwanted artifacts, unsupported depiction, false evidence or broken anatomy. Regenerate only if material to the job; keep the failed receipt. Do not turn generated visuals into purported research observations.

## Runtime boundary

This contract works with the currently available authorized image/video tools. Open Generative AI itself was not installed: the 2026-10-01 audit found dependency advisories, persistent browser API-key storage, an upload proxy boundary needing hardening, and a desktop downloader that removes macOS quarantine. A later remediated web-only application needs a fresh source/dependency review, actual provider authorization and the complete generate/download/QA journey. The audit record retains exact pinned submodules and deployment requirements. Do not create a second generation app solely to use this handoff method.
