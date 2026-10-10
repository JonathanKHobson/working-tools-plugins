# Repurpose a narrated course lesson as a Short

Read for a course excerpt or screen demonstration destined for a vertical Short. Keep course-specific titles, sequence, assets, and creator preferences in the project plan. This reference was checked against the linked platform guidance on 2026-09-30; verify live controls and rules at publication.

## Select an independent teaching beat

1. Confirm the source version, rights, audio, visual assets, and destination. A host platform's public terms do not establish permission to redistribute a provider's course material. Check the applicable course agreement and any third-party music, imagery, logos, or learner data. [Coursera Terms](https://www.coursera.org/about/terms); [YouTube copyright guidance](https://support.google.com/youtube/answer/2797466?hl=en).
2. Choose one useful answer or demonstrated action that stands alone. Preserve what the instructor actually said and did. Build a concise **context → hook → demonstrated payoff** so a viewer who has never seen the course can follow it. Avoid a teaser that withholds the answer.
3. For a project targeting 15–120 seconds, select the needed source intervals and record why each stays. YouTube currently classifies square or vertical uploads up to three minutes as Shorts; the project target can be shorter. [YouTube three-minute Shorts](https://support.google.com/youtube/answer/15424877?hl=en).
4. Preserve the creator's meaning and recognizable voice; that does not require keeping the recording's original pace. First tighten the dialogue below. A modest 1.05–1.15× speech speed with pitch preservation is an *option* to test afterward, not a batch default. Listen for artifacts, rushed instructions, and whether a learner can follow the on-screen action; revert if either suffers. Do not hide missing context by speeding up.

## Tighten before styling

- Select the clearest version of each idea. Remove meaning-free ums, abandoned starts, duplicate explanations, and empty waiting time. Keep qualifiers, necessary setup, meaningful breaths, and pauses that let the demonstrated action register. Do not remove uncertainty or combine fragments into a claim the instructor did not make.
- Apply these pacing choices only to a newly authorized Short edit. A suggested speed-up, filler cut, repetition cut, or stepped/jump zoom does not reopen a held lesson, export, or previously scheduled Short.
- Record source intervals and keep/cut reasons in the existing edit decision list. Noncontiguous excerpts are useful when their combination remains honest. Preserve the order of dependent UI actions and make omissions understandable. Snap edits to verified word or silence boundaries; inspect both sides, then smooth audio with short fades or room tone as needed.
- Write a short beat plan before choosing a template: hook, necessary context, focused demonstration, visible result. Judge the first few seconds for immediate value and each later beat for new information. A longer clip needs a reason to keep watching; a shorter one still needs a complete takeaway.

## Design the vertical demonstration

- Make a 1080×1920 composition when that is the delivery target. Reframe deliberately around each screen action; show the control, cursor, input, and result at readable size. Use callouts, stepped zooms, or re-created safe visual layouts when necessary. Do not blindly center-crop a desktop recording or imply an action occurred offscreen.
- Change framing when the teaching focus changes: orient the viewer, punch in on the relevant control or prompt, then show the result. Choose layout and transitions for the beat rather than repeating one static letterboxed treatment across every clip. Avoid arbitrary zooms that compete with a spoken instruction.
- For an energetic brief, use readable phrase captions with selective word emphasis, bright accent colors, or timed emoji companions. Animate from actual speech timing; do not estimate word times from character counts. Keep emphasis legible through motion, respect contrast and platform overlays, and retain spoken words in the complete caption track even when a decorative emoji accompanies them.
- Use generated graphics or pop-ups only when they clarify the point. Label illustrative imagery where necessary; never fabricate product UI or imply a screen action occurred. Reuse approved graphics by asset hash. Select from available templates and revise one pilot; a new template library is not a prerequisite for an individual Short.
- Inspect the first frame, each crop/zoom transition, the densest text, the decisive click/typed prompt, and the end frame on a phone-sized viewport. Preserve source order and UI truth. Mask private data on the delivery copy while keeping the demonstrated controls readable.
- Recompute all caption start/end times from the **output timeline** after trims, retimes, and joins. Deliver a complete reviewed SRT, including meaningful non-speech sounds where needed. Burned captions are optional presentation, not a substitute for a timed caption track. Check that both text and timing match the final audible render. [YouTube caption upload](https://support.google.com/youtube/answer/2734796?hl=en); [YouTube automatic-caption review](https://support.google.com/youtube/answer/6373554?hl=en-GBAnd).

For a constant-speed retained segment, map time as `outputOffset + (sourceTime - sourceIn) / speed`. Split or clip cues at the retained boundaries and remove words that were cut; never carry an entire source cue across a deleted interval. Variable-speed edits need the renderer's actual timing map. Recheck alignment after the final encode.

For reviewed whole-cue, ordered constant-speed cuts, use the existing CLI
`export-captions` and [caption variant contract](../../conform-video-delivery/references/caption-variant-export.md).
It batches lesson/part/Short sidecars and refuses partial cues; reviewed split
cues or a different actual renderer timing map are needed for finer edits.

## Shared TikTok media handoff

For every newly made Short, assess a TikTok candidate: selected / defer / unsuitable,
with a reason, standalone payoff, source/output hash, rights state and concrete media
adaptation if needed. Assessment is not automatic posting, a clip quota or a required
second render. Reuse source analysis, alignment and approved clean masters; preserve
the existing YouTube path and held exports. Curated backfill selection and publication
history belong to Social/project policy.

Keep a clean master free of another platform watermark and native music attachment;
preserve separable voice/music/SFX where available. Choose a clean native-caption
variant or locally captioned alternative only when useful. Bind captions to output
time and exact reviewed bytes; SRT is an archive/handoff until native import is verified.
Use current phone/native-preview overlays for UI-safe QA rather than a universal
pixel-safe-area claim. A TikTok-native sound license does not clear YouTube reuse.

Pass source spans, EDL/timing, dimensions/duration, exact hashes, transcript/SRT, chosen
variant, cover-frame output timestamps and media QA limitations to
`social-content-studio:social-publishing` and its conditional
`references/tiktok-manual-publishing.md`. That single owner holds cover/hook/post-caption
craft, live capabilities, sound/disclosures, authorized attended native future
scheduling and separate eventual public receipt. Immediate/Now TikTok posting is
prohibited. Direct source exports and custom adaptations are both supported,
including authorized reuse from another owned account. Record that ownership/reuse
basis, check rights/accuracy and keep distinct variant IDs/hashes/receipts under the
same source without replacing published variants. Reuse/overlap is acceptable; do
not present a reach penalty as fact. Refine subsequent authorized edits incrementally.
Hand off the shared-source public readiness dependency; Social verifies
it before scheduling, checks the existing queue/live horizon and records the future
date/time/timezone/native receipt, with future slots on different account calendar
days and at most one TikTok video per day. Outside that horizon, keep the item prepared for
the next attended handoff. Video adds no publishing adapter or external scheduler
and does not duplicate that handbook.

## Keep iteration small

Reuse transcript, word alignment, probes, and approved assets by source hash. Review uncertain transcript spans against audio and correct names before freezing captions. Do not retranscribe a verified whole lesson to make another excerpt. If new alignment is needed, process the selected spans with enough surrounding context for reliable boundaries.

If the Short needs a cover, route a faithful 9:16 adaptation through `conform-video-delivery`; keep it distinct from the 16:9 lesson cover and square course card. Preserve the approved image and wording, then inspect the intended portrait crop. Native thumbnail controls and saved readback belong to `social-content-studio:social-publishing`.

Render one representative pilot at preview quality to judge pacing, framing, and caption treatment before exporting a batch. Keep independent transcript/copy analysis separate from encoding; throttle expensive renders under machine pressure. Give delegates only the source intervals, relevant transcript, output target, style brief, constraints, and expected receipt. Use separate output paths and one owner for the final edit manifest.

## Validate the actual render

Map 3–8 anchors before visual signoff: anchor ID, source or output viewport/time, approximate region, selector/node if applicable, observed fact, and intended action. Reinspect every changed anchor on the rendered file. Watch and listen to the entire final render at normal speed, then inspect cut boundaries, caption transitions, small-screen legibility, speech clarity, and privacy masks. Record render path, dimensions, duration, caption-track status, and SHA-256 of the exact reviewed file. A prior preview does not validate a newer export.

For joined or retimed exports, compare container duration with stream start/end times and packet timestamps, decode the complete file, and inspect the first and last audible words. A plausible duration alone does not prove valid timestamps or continuous playback. Freeze the exact reviewed video, its complete SRT, hashes, and associated copy before opening an upload flow; replacing any of them invalidates the affected QA and handoff receipt.

Keep the editorial/render receipt distinct from upload, schedule, publication, and public playback receipts. Handoff the exact hash and caption file to `social-content-studio:social-publishing` for platform action. A Short may precede a later full compilation: a Related Video link is optional and may point to an *already* public or unlisted relevant lesson; defer that link if no eligible video exists. [YouTube Related Video eligibility](https://support.google.com/youtube/answer/14075157?hl=en).

Workflow feedback changes the next authorized edit brief. It does not authorize revising already exported, scheduled, or published work when the creator has put that work on hold. Keep any such hold in the project record and respect it across handoffs.
