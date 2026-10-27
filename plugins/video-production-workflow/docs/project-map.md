# Video Production Studio project map

- `.codex-plugin/plugin.json` and `skills/*/SKILL.md`: discovery and narrow entrypoints.
- `skills/*/references/`: conditional workflow details; `references/sources/` holds provenance.
- `video_workflow/`, `adapters/`, and `scripts/`: existing media operations and validation.
- `evaluations/` and `tests/`: routing/pressure scenarios and executable checks.
- `docs/OPERATING_GUIDE.md` and `docs/MANIFEST_REFERENCE.md`: existing operating and manifest contracts.
- `PLUGIN_MAP.md`, `docs/PROJECT_MEMORY.md`, `research/`: full first-party routing, project-learning and dated source-research references. `docs/OPTIONAL_INTEGRATIONS.md` gives current dependency boundaries.

The course path is a conditional reference owned by `skills/edit-dialogue-footage/references/google-vids-course-editing.md`, discoverable from planning, ingest, dialogue, audio, and validation. Instructional Design Studio owns lesson integration, and Writing Quality Studio owns spoken-script revision. No new tools or skills are required.

Repeated installation of exported course recordings: `skills/ingest-video-assets/references/course-video-installation.md`. Deterministic sidecars live in `video_workflow/course_media.py`, exposed by `scripts/package_course_media.py`; `tests/test_course_media.py` covers timing, integrity and safe reruns. The default command is read-only and has no network capability. Service-specific adapters and release state stay in the course project.

Course Shorts craft belongs to `skills/edit-dialogue-footage/references/course-shorts-repurposing.md`; the installation reference connects authorized website handoffs to Social Content Studio's existing publishing owner. Calendar arithmetic and platform receipts belong there, not in media editing.
Each new Short includes a TikTok candidate assessment and reusable clean-master/media
handoff; Social Publishing's `references/tiktok-manual-publishing.md` owns the full
attended native future scheduling guide, queue/horizon checks, schedule receipt and
separate eventual public receipt. Immediate/Now TikTok posting is prohibited; the
shared source must be public before Social schedules at most one video per account
calendar day. Direct/custom variants and authorized owned-account reuse keep distinct
variant IDs/hashes/receipts under the source, preserving published renditions. No TikTok runtime, posting API,
external scheduler service, bot or unattended UI loop belongs to this media plugin.

`skills/ingest-video-assets/references/cross-channel-course-handoff.md` owns the
conditional course/workshop derivative handoff: YouTube full/parts and Shorts,
LinkedIn promotion, substantive Substack
article candidates and later LinkedIn native video/article adaptations. It passes
source spans, exact media/text hashes, review and release constraints without
expanding local media preflight into a publishing adapter. Channel policy and
approved spacing remain Social Publishing/project data; course mutation is conditional.

Maintain the canonical owner and mirror reviewed distributable files byte-for-byte to the public package. Recipient-owned media, host bindings and generated reports stay outside that payload. Validate changed skills and links, run `scripts/validate_plugin.py`, the test suite, and `scripts/verify_release.py` with its declared runtime dependencies; historical UI examples require current interface inspection at use time.

Final lesson/Short/workshop delivery preflight: `video_workflow/delivery.py`, exposed by the shared CLI `preflight-delivery`. The conditional contract is `skills/conform-video-delivery/references/delivery-preflight.md`; `tests/test_delivery.py` covers batch checks, stale review bindings, format-specific art and read-only operation. It owns local artifacts only, leaving native publishing to Social Content Studio.

Batch part/combined/Short SRT export from existing reviewed cue timelines:
`video_workflow/caption_exports.py`, shared CLI `export-captions`, with the
conditional contract in `skills/conform-video-delivery/references/caption-variant-export.md`.
`tests/test_caption_exports.py` covers hash binding, output offsets, retimes,
joins, partial-cue rejection and safe reruns. It never edits recordings or approves speech alignment.

Existing Drive recording trims and same-file replacement: `skills/edit-dialogue-footage/references/drive-trim-and-replace.md`; validation owns silent-QA limitations, caption/container timing and integrity readback. Project source media and service receipts stay in the owning project.

Requested retention diagnosis: `skills/analyze-video-content/references/audience-retention-editorial-review.md` maps observed intervals to the reviewed output and a bounded experiment. YouTube description chapters: `skills/ingest-video-assets/references/youtube-description-chapters.md`, with read-only `scripts/export_youtube_chapters.py` and `video_workflow/youtube_chapters.py`; tests bind existing course-package chapter/receipt inputs to final render bytes. Complete selected third-party methods/support are inactive in `libraries/youtube-agent-methods/` with license/provenance. No new discoverable skill or provider is added.

Subject-neutral editorial techniques: `edit-dialogue-footage/references/editorial-treatment.md` owns pacing/reframing/color/B-roll decisions; `create-video-typography/references/expressive-captions.md` owns semantic emphasis and restyling; `create-motion-graphics/references/tracked-layer-compositing.md` owns tracked anchors, mattes, layer order and selective blur. Paths are under `skills/`. The core renderer does not execute arbitrary effect metadata: use verified authored composites as supported picture segments and preserve audio separately.

- Mixed production and remote generation: `plan-video-production/references/production-routes-and-job-control.md` routes existing stage owners and records bounded jobs; `ingest-video-assets/references/shot-acquisition.md` fills specific footage gaps. These are agent methods with no added runtime/provider.

Motion design: `skills/create-motion-graphics/` owns full code-authored motion storytelling as well as isolated slots. Its `references/code-authored-motion-storytelling.md` contains the semantic event-map, continuity, sound and authentic-narration production branches, acceptance and future research intake. Graphic owns visual direction through motion; UX owns interactive behavior; Social owns release. Worked media and approval evidence remain in their project.

Educational animation extension: `skills/create-motion-graphics/references/anidoodle-production.md` routes the retained, inert Anidoodle source for local, reviewed 2D scenes. `runtime/thinking-orbs/` is a first-party, dependency-free adapter for optional loading or thinking states; it is not a provider, install hook or learner-outcome signal. The generic educational-motion example is a portable handoff pattern and keeps Fresh Curiosity assets in the owning private project.

Conditional Remotion 2D implementation: `skills/create-motion-graphics/references/remotion-implementation-and-review.md` owns frame-derived scene timing, local asset and version checks, and review of the rendered output when Remotion is already selected. The existing motion story and art-direction contracts remain primary; this adds no runtime dependency.

Motion/SVG source integration: `skills/create-motion-graphics/references/animated-diagram-production.md` owns semantic animated diagrams; `libraries/motion-diagram-methods/PROVENANCE.md` records source revisions and notices. No runtime dependency is added.

Procedural-video intake: `create-motion-graphics/references/procedural-video-methods.md` routes complete pinned Animate, Charlie and HyperFrames production libraries. `design-video-storyboards/references/video-style-discovery.md` connects optional Video Templates catalog selection and a separately verified storyboard backend to production and Draw and Think. Video Templates owns its chooser, catalog and storage. The author's source-only `runtime/video-style-library/` symlink is excluded from distribution; `scripts/video_style_library_mcp.py` is an unregistered conditional bridge requiring a recipient-owned templates-root binding. No provider/runtime is auto-installed or claimed tested by file parity.

Article/source companions: `skills/design-video-storyboards/references/source-article-to-video.md` binds source revision and claims to timed story, motion/assembly, captions, authorized personal voice and editable handoff. Graphic owns format choice; Social owns article placement and release. No new runtime or skill is added.

Resolve operation: `skills/edit-davinci-resolve/` owns edition-aware import/UI,
native finishing and saved-project readback. Existing editorial/audio/motion/QA
owners retain their stages. `exchange-video-timelines/references/resolve-roundtrip.md`
owns editable timeline/archive acceptance and exporter loss limits. Source
review and custom-license decision: `research/AI_VIDEO_EDITING_PACK_REVIEW.md`.
Private host profiles and current runtime paths remain outside plugin source.

Default original-motion craft: `skills/create-motion-graphics/references/art-directed-motion.md` is the shared type/photography/composition/depth/movement contract, reached from planning, storyboards, motion, typography and QA. Routine approved trims/exports bypass redesign.

Art-direction reuse: the same shared method owns controlled comparisons and project style-record intake. `research/ART_DIRECTION_HANDOFF_REVIEW.md` holds the rights-safe source summary and conditional primary-source checks; it does not register new runtimes. Private original handoff evidence remains in the author archive.

Reusable production evidence and template portability: `skills/evolve-video-workflow/references/production-learning-transfer.md` owns stage/variant identity, source-versus-adaptation proof, cold-start closure, media-freeze sequencing and evidence roles. `create-motion-graphics/references/generated-assets-for-motion.md` owns saved artwork, hash-bound measurements, joints and cadence-aware caching. `video_workflow/provenance.py` and `scripts/verify_template_bundle.py` verify a declared relative inventory, with behavioral tests in `tests/test_relative_bundle.py`; they do not infer dependencies, lock media, execute templates or approve craft. Integration provenance and test limits belong to the handoff-improvements project receipt, not these generic methods.

## Reconciled standalone methods

- `skills/loom-review-packet/` and `skills/loom-walkthrough-scripting/`: complete source-first transcript/frame packet helper and script method. Worked product details are fictional and current project evidence remains required. File-level disposition is in `docs/standalone-additions-provenance.json`.

- `mix-video-audio/references/audio-perception-and-synthesis.md` routes complete Earshot/recorded-sound methods and the offline adapter. `create-motion-graphics/references/product-film-production.md` and `motion-recipe-production.md` route complete product-film and recipe methods, their local support libraries and the data-only `scripts/motion_sources.py`. Source servers, memory collection, external installers, stored-provider agents and bulk exports stay inactive. File hashes, exclusions and redistribution holds are in `docs/motion-source-admission/` and each library inventory.

Generated sprite acting: `skills/create-motion-graphics/references/generated-sprite-animation.md` extends the existing generated-assets owner. Storyboards carry the action ledger; motion owns referenced strips, extraction/registration and assembly; QA verifies semantics and encoded transitions. `scripts/preview_sprite_sequence.py` and `video_workflow/sprite_sequence.py` check hash-bound registered poses and complete frame accounting; `tests/test_sprite_sequence.py` covers failures. Pets remains an optional method source with its lifecycle untouched.
