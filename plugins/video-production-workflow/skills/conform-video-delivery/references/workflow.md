# Conform Video Delivery: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Start from a validated high-quality master and the approved delivery matrix.
2. Recheck current platform/client specifications and note the date/source.
3. Choose aspect-specific composition, crop, reflow, or alternate edit—not automatic scaling alone.
4. Set container, codec, profile/level, pixel format, frame rate, color metadata, audio codec/rate, bitrate/quality, and fast-start behavior.
5. Generate burn-in and sidecar caption variants as required.
6. Create poster/thumbnail and metadata packages where useful.
7. Probe and visually inspect every variant, including representative platform UI overlays.
8. Write checksums and a delivery manifest with source master hash and spec review date.

For a course Short, inventory approved 16:9 cover art and square course-card art before adapting a distinct 9:16 cover. Preserve the approved subject, typography, claims, and visual identity; do not replace them with generic generated imagery. Use imagegen for new artwork or a visual edit of the approved source, including a faithful portrait adaptation, and review it against that source. Reuse matching approved assets; optimize or compress an approved export separately. Inspect the actual portrait destination and any list/watch crop before handoff, since a local file preview cannot prove how the cover will appear there. Hand native upload, saved-image readback, and platform eligibility to `social-content-studio:social-publishing` using its YouTube catalog packaging reference.

For new artwork, use a specific teaching idea and real source evidence before
choosing a visual metaphor. Prefer a readable source screenshot or deliberately
designed explanatory diagram when it communicates the lesson better. For
generated imagery, inspect object relationships, perspective, contact/shadows
and any optical effect: a magnifier must enlarge the same underlying detail
coherently. Symbols and diagrams must carry an explainable meaning; decorative
complexity and a clean finish do not establish quality.

Use Writing Quality for thumbnail wording and truthful claims, Graphic Design
for composition/type and visual plausibility, and UX for meaning and attention.
Inspect the actual final export at full size and phone size, record source/region
anchors and observable findings, and bind that review to the delivered art hash.
Naming these skills or reviewing a prompt is not final-render evidence. Apply
this feedback to upcoming assets; leave approved published/scheduled artwork
intact unless the user explicitly requests a revision.

Bind the handoff to SHA-256 hashes for the source/master, each delivered video and cover variant, and the complete timed caption file. Record final output duration and caption end time after all cuts or retimes, source resolution, and which stages were prepared or reviewed locally. Reuse hash-matching artwork, transcripts, and analyses; on a resumed job, check existing receipts and do only missing or invalidated stages. A prepared asset or planned handoff is not a saved remote change.

## Checkpoints

- **Intent checkpoint:** the approved strategy and acceptance criteria are explicit.
- **Evidence checkpoint:** source and analysis data exist and match current hashes.
- **Draft checkpoint:** a low-cost, target-aspect artifact is inspectable.
- **Technical checkpoint:** schema, timing, stream, and file assertions pass.
- **Review checkpoint:** an independent reviewer inspects actual outputs.
- **Handoff checkpoint:** downstream skill, exceptions, and reversible choices are documented.

## Change discipline

A revision should change the highest-level artifact that expresses the feedback. Change the brief for strategy, storyboard for shot design, manifest for timing/layout, an isolated slot for animation, audio map for mix, and delivery matrix for export. Avoid patching a rendered MP4 when the editable source of truth exists.

## Recovery

On failure, preserve logs and intermediates. Identify whether the root cause is input, manifest, dependency, analysis, editorial choice, renderer, encoder, or QA threshold. Reproduce with the smallest fixture, add a regression test, and rerun only invalidated cache stages.
