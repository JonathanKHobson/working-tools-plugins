# Video Studio efficiency audit — 2026-10-01

This is a dated first-party method and test account. Referenced run reports and project-specific media remain in the author's private archive; the narrative does not prove a receiving host's runtime, account or current platform behavior.

The YouTube teaching-video flow exposed missing portrait covers, repeated asset
inventory, and uncertainty about which exact export/caption/art bytes had passed
review. Native thumbnail Save, card controls and publication eligibility are
already documented by Social Publishing. This update keeps those ownership
boundaries and improves the media preparation stage.

## Implemented

- The shared CLI now offers `preflight-delivery`: one read-only batch check for
  final render, captions, transcript, cover and optional square course-card art.
  It reports all missing, changed or mismatched artifacts with outstanding actions.
- Actual ffprobe/Pillow measurements, file hashes, recipient-supplied size/pixel
  limits and format-specific aspects are checked together. There is no hardcoded
  upload-size limit or claimed universal native thumbnail behavior.
- Review attestations bind the exact render, text and art hashes. Replacing a file
  invalidates its dependent review; updating its expected file hash cannot make
  an old review current. A transcript and a square card cannot slip through as
  unreviewed extras.
- Shared artifacts are hashed/probed once per invocation. A regression verifies
  two deliveries sharing four files use one probe and four hashes. Files changing
  during inspection or later in the batch are reported; no persistent stale cache
  is trusted.
- Conform, Shorts and QA guidance now covers faithful portrait artwork, final-edit
  captions, source resolution versus platform processing, honest listening status,
  and reuse of valid stages. Approved wide artwork and held exports remain intact.
- Planning routes already specified work directly to the owning stage. Full
  procedures and retained source libraries remain conditional; no new skill,
  background job, publishing adapter or provider was introduced.

## Before/after evidence

Before: `probe_media` measured a file, `qa` checked media, and course sidecar
packaging validated declared durations/hashes. None aggregated finished variants
or compared all current artifacts with their review attestations. The new test
module initially failed to import the absent delivery capability. After:
21 targeted preflight regressions pass, including wrong-aspect cover, missing
assets, stale render/text/art reviews, duplicate delivery ID, changing shared
file, explicit limits, and a real ffprobe/CLI read-only check. The complete suite
contains 101 passing tests; release-gate evidence is under `release/`.

Independent review found two false-ready paths in the first draft: transcript
freshness and optional card review. Both were corrected and regression tested.
The next worker receives the per-item manifest/check result, not full conversation
history or a new calendar reconstruction.

Static Plugin Eval reports are in `baseline-evals/delivery-preflight-plugin-*.json`.
Its score remains 0 and estimated discovery cost remains 949 tokens: the rubric
flags retained support-library budgets and public-distribution policy URLs.
These reports are static estimates, not measured task usage or a successful
model-routing benchmark. No actual token, billing or elapsed-time saving is
claimed. The demonstrated improvement is fewer repeated probe/hash operations
and a deterministic checklist replacing per-item reconstruction.

The evaluator also flags cross-skill links with fragment anchors; direct file and
heading checks confirm those targets exist. No source is deleted to satisfy a
static size score. The native release gate now runs an existing static evaluator
when available through PATH or `VIDEO_WORKFLOW_PLUGIN_EVAL`; its result is advisory
and availability is recorded accurately. It never installs this optional tool.

## Still requires review or platform action

Editorial clip selection, truthful emphasis, pacing, small-screen readability,
audio listening, caption-speech alignment and visual anchors remain actual review
work. The CLI checks hash freshness of human attestations; it cannot authenticate
their evidence text or perform the underlying review. Cue structure/timing uses
the existing caption/package tools, followed by review against the final render.

Social Publishing retains account IDs, playlist and card destinations, A/B test
eligibility, native crop checks, asynchronous Save recovery, upload/schedule
readback and public playback. Existing course media and the release ledger were
not mutated by this plugin update. No timer or automatic publishing was added.

Keep a new persistent cache, automated clip scoring and richer motion templates
deferred until actual repeated workloads justify them. The requested craft
upgrade can be integrated into the existing dialogue/editing owner when supplied.

## Cross-channel handoff audit — 2026-10-02

The same incoming course/workshop can support several channel derivatives.
Rebuilding an inventory, transcript argument and calendar for every adapter adds
coordination work and makes source or schedule drift harder to detect.

Implemented in the conditional
[course/workshop handoff](../../skills/ingest-video-assets/references/cross-channel-course-handoff.md):

- Reuse one reviewed media/transcript package, stable content/parent IDs, exact
  source spans and current artifact hashes. Pass only the relevant per-item
  evidence to each worker rather than full history or repeated source extraction.
- Prepare a source-supported derivative matrix and record weak-source gaps.
  This avoids padded articles, invented case-study outcomes and unnecessary
  renders of the same reviewed edit.
- Carry the applicable channel grant, approved spacing/dependencies and native
  receipt state. Same-day YouTube promotion and later LinkedIn native video or
  article are distinct derivatives; file readiness cannot select a release date.
- A native YouTube time/status change marks downstream companions for
  reconciliation, with old/new receipt facts and the stable ID passed to the
  shared publishing owner. This makes stale companion schedules visible without
  silently changing them.
- Keep source preparation in Video and article/platform policy in Social/Writing
  Quality. Keep project IDs, release dates and account state out of shared plugin
  defaults. Actual course modification remains conditional on an instruction.

No new adapter, recurring job, provider, clip scorer or permanent cache was added.
Automatic article publication and native schedule mutation are outside this
preparation audit. The deterministic delivery checks are covered by the existing
101-test suite; the new handoff cases are evaluation fixtures, not measured model
benchmarks. No token or timing saving is claimed without a measured comparison.

## Caption reuse and thumbnail meaning — 2026-10-02

The remaining repeat work was converting a reviewed combined cue package into
part and full-video SRT files, then rebuilding timing for Short cuts and speed
changes. The package helper emitted combined cues, VTT and text; the earlier CLI
converted SRT to ASS. The new caption-export regression first failed because
variant export did not exist.

Implemented `export-captions` in the existing CLI. One manifest exports a batch
from one hash-bound cue file and the approved ordered edit spans and speeds.
The default is read-only; explicit output writes SRT files and a receipt,
refuses partial cues and changed outputs, and makes an identical rerun a no-op.
It does not probe media or transcribe again. Variable-speed ramps, transitions
that change duration, word-level splitting, audio alignment and creative judgment
remain outside this command.

The 19 targeted checks cover offsets, joins, speed, preserved text/line breaks,
hash drift, malformed cues, unsafe destinations, millisecond precision and safe
reruns. An independent worker completed a fresh part/combined/1.1× Short request
through the CLI and confirmed that a fine cut inside a cue failed without
generating a truncated SRT.

An isolated comparison of an existing reviewed 857-cue package reproduced all
743 part-one, 114 part-two and 857 full-video cues, including exact text and
millisecond timestamps. Output hashes differ only in the final blank line.
Approved caption files were untouched. This calculation read the cue file once,
performed zero media probes and took about 0.012 seconds locally. That is one
observed run, not a before/after timing benchmark or an account-token saving.
Evidence is in `baseline-evals/caption-variant-comparison.json`.

Conform's design review now checks visual polish and semantic meaning: labels,
strikeouts, arrows and checkmarks must agree with the narrated example. New art
should have clear hierarchy, credible materials or authentic source imagery,
and restrained accents. Imagegen remains the new-art route; generated polish
does not establish correctness. Existing approved covers remain intact.

### Remaining efficiency decisions

- Reuse reviewed transcripts, source probes and valid review stages by hash;
  align only uncertain spans when needed.
- Give workers relevant cue spans, brief, output target and receipt instead of
  full chats, whole courses or separate calendar reconstructions.
- Pilot an unfamiliar Short treatment before batch rendering. Tighten filler
  and repeated explanations before testing speed or adding emphasis/motion.
- Freeze exact delivery bytes before upload. Preserve stable native IDs and
  saved-state receipts so retries resume without another upload. Social
  Publishing already owns this operation.
- Keep current platform specifications, thumbnail controls, playlists,
  education metadata, cards/end screens, HD processing and A/B availability
  in the Social procedure/project record; inspect live controls when acting.

Automated clip judgment, illustrative semantics and publishing remain deferred
until evidence supports reliable behavior. No recurring task, new skill or paid
runtime was added. All sixteen existing skill boundaries remain intact.
