# Repeatable course-video installation

Use for recorded lesson clips that must become one course video with chapters,
source-timed captions, an interactive transcript, a concise guide and task materials.
This is a conditional route through the existing video workflow, not another editor
or course system. Read the target project's media runbook for its service adapter.

## Start or resume

Read the current project map, latest relevant media receipt, and current user scope.
Identify the owning checkout and exact course/lesson/page/activity IDs. Reuse the
existing player and editable media fields. Do not copy a historical course snapshot
over current author edits. A new course or a missing page needs explicit placement;
never infer it from an old task number.

Keep one private job directory with the input manifest, original probes/captions,
delivery copies, review evidence and separate upload/save/publish receipts. Original
recordings are immutable. Keep credentials outside it and out of delegated briefs.
Recover the latest completed stage from bytes and receipts, not a previous agent's
claim. Do not rerender or retranscribe matching verified inputs merely to resume.

| Stage | Deterministic work | Judgment / evidence still needed |
| --- | --- | --- |
| Ingest | Existing inventory/probe tools; hashes and stream discovery | Verify clip order, alternate takes and separate bonus steps |
| Timing | Extract embedded timed captions first; offset by probed clip durations | Sample actual speech; scripts are context, not verbatim evidence |
| Delivery | Existing renderer/conform tools; fast-start web copy, codec/size/decode checks | Inspect privacy, both sides of joins, readable screen actions and audio |
| Package | `scripts/package_course_media.py` below | Review exact caption corrections, chapter titles and guide fidelity |
| Integrate | Project adapter; schema validation and narrow candidate diff | Placement, existing materials, next step and future-task wording |
| Release | Existing authorized upload/save/publish API with guarded readbacks | Actual learner playback, seeking, downloads and navigation |

## Prepare the media

Reuse the toolchain already configured by this plugin or the project. Inspect it
before installing dependencies. Limit render concurrency under machine pressure;
independent transcript analysis can run separately without parallel encoders.

Probe streams before choosing captions. For embedded subtitles, select the observed
stream index and extract to a new file, for example:

```sh
ffmpeg -nostdin -n -i input.mp4 -map 0:2 -c:s srt captions/part-a.srt
```

`0:2` is an example, not a fixed subtitle stream. If captions are absent or inaccurate,
use actual audio for transcription/alignment and record the method. Never create
timestamps from a script or guess them. Transcription quality needs sampling even
when timestamps came from the recording. Transcribe repetitions and intentional pauses
faithfully; an authorized editorial pass may remove them and must retime its captions.

Use the existing render/conform path for concatenation or encode. Review private UI
details before upload; masks and crops are editorial decisions and must preserve the
demonstrated task. Bind the final delivery to its hash and QA evidence. If a trim,
speed change, overlap or reordered excerpt changes timing, first produce a verified
timing map and matching sidecars: the helper below only supports untrimmed consecutive
clips. Do not represent edited durations as if they were untouched sources.

For joined delivery files, check stream start/end times and packet timestamps as well
as container duration. Decode the full file and inspect the first/last spoken words
and joins; a matching duration can conceal broken timestamps. Review proper names
and technical caption terms against the audio before freezing sidecars for upload.

## Package sidecars once

Run from the installed or maintained plugin root. This helper uses only Python's
standard library; it does not require the optional render/ASR dependencies.

```sh
python3 scripts/package_course_media.py /absolute/job/package.json
python3 scripts/package_course_media.py /absolute/job/package.json --output /absolute/job/package
```

The first command is a read-only dry run. The second creates cues, chapters, VTT,
plain-text transcript and a hash receipt. Exact reruns preserve existing bytes;
conflicting outputs fail before writing. Use a new output directory after an
intentional source/correction change. There is no upload or publish command here.

Minimal input (paths resolve relative to the manifest):

```json
{
  "schemaVersion": 1,
  "id": "task-05",
  "clips": [
    {
      "id": "part-a",
      "title": "Your Turn",
      "source": "sources/part-a.mp4",
      "sha256": "REPLACE_WITH_ACTUAL_SHA256",
      "durationSeconds": 120.125,
      "captions": "captions/part-a.srt"
    }
  ]
}
```

Durations must come from the actual probe. Optional `corrections` entries contain
`clipId`, zero-based `cueIndex`, exact `before`, `after`, and a review `reason`.
Only those explicit corrections change transcript wording. Optional `delivery`
contains `path`, `sha256`, `maxBytes`, `durationSeconds`; use the currently verified
destination limit, not a historical universal preset. The helper compares declared
delivery duration to the sum and hashes bytes; it does **not** decode or independently
probe the delivery. Keep that evidence from the media QA stage.

Output contract: `ID.cues.json` is an array of
`{id, startSeconds, endSeconds, text}`; `ID.chapters.json` is an array of
`{id, title, startSeconds}`. Times are on the combined timeline. `ID.txt` and `ID.vtt`
derive from the same cues. `package-receipt.json` records input/output hashes and
mechanical validation, not editorial approval or publication. The website adapter
maps these fields to its own schema. Do not embed course IDs or credentials here.

## Integrate without recreating the lesson

Instructional Design Studio's existing `course-production-handoff` skill owns
instructional alignment and learner launch review. Its `course-media-integration`
reference covers guide/material consistency. Keep that ownership; this reference
does not duplicate a curriculum design process.

The adapter should consume a freshly saved snapshot, exact IDs, package, hosted
asset mapping, canonical guide and explicit authored-content placement. Preserve
resources, copyable email/prompts, question/assignment placement, stable page IDs,
approved objectives and neighboring lessons. Review planned/available wording and
roadmap placement separately rather than adding fuzzy text replacement to automation.

Prefer a content-only update when the existing runtime supports it. A new app/Sites
deployment is needed only for an actual application change. Keep service upload,
course save, course publish and runtime deploy as distinct operations and receipts.
Before any authorized save/publish, compare a fresh server record with the expected
revision/document. On conflict, rebuild the narrow patch against the new record.
On an uncertain write response, reconcile remote state before retrying; do not create
duplicate assets or revisions blindly. Verify saved and released documents exactly.

## Reuse the intake for authorized social publishing

When the user's scope includes both course installation and social release, this
same video handoff triggers the publishing lane. Read its existing project brief
and release ledger rather than rebuilding a calendar from chat history. Pass the
verified delivery path/hash, final captions, chapter map, transcript, course URL,
and explicit release constraints to `social-content-studio:social-publishing`.
Use `edit-dialogue-footage` for separately authorized Shorts from those sources.

For an authorized wider channel flow, use the conditional [course/workshop
cross-channel handoff](cross-channel-course-handoff.md). It connects source-backed
YouTube full/parts and Shorts, LinkedIn companions, substantive Substack article
candidates and later LinkedIn native video/article adaptations. Preserve existing
releases and pass the approved spacing constraints to Social Publishing; course
modification still requires its own actual instruction.

Finish any required writing review before freezing copy. Keep account IDs, cadence,
time zone, pending posts, and review holds in the project. Recheck locally prepared
posts against the live scheduling window during this handoff when authorized;
outside-window copy remains prepared until the platform accepts and confirms it.
Do not create a recurring event merely to resume this flow. A user-requested timer
is a separate action. Reuse verified media and receipts; do not reupload matching
assets or revise held videos as a side effect of adopting new editing defaults.

## Bounded delegation

Give each worker the explicit source paths, output directory, manifest/schema,
permitted side effects, checks and stopping conditions. Do not send the whole thread.

- **Luna or equivalent:** inventory, source/caption extraction, package checks and
  receipt comparisons. Return counts, hashes, command results and anomalies; no
  editorial decisions, credentials or production mutation.
- **Sol or equivalent:** bounded script/adapter work, tests, transcript-supported
  guide draft. Preserve authored voice and flag uncertainty; no new curriculum.
- **Astra lead:** clip order, privacy and instructional decisions, guide approval,
  current-state reconciliation, authorized release and final learner QA.

Use one or two independent lanes, not several models repeating the same audit.
Claude subscription/local-model offload can use the existing Work Management route
when it has verified capability; it is optional, not a new dependency. Do not claim
token or cost savings without usage evidence. Scripts reduce repeated generation
and context loading; measure those reductions separately from actual billing.

## Completion and recovery

Return exact files/hashes and separately mark prepared, uploaded, saved, published
and learner-verified. Exercise playback, chapter and transcript seeking, current
highlight, captions, guide, copying, real downloads, mobile layout and Next/Back.
Use actual download bytes, not only a click event or success toast. If browser
automation misses a blob download, inspect a newly created file and compare bytes;
otherwise state the gap. Do not certify a full listening pass from technical checks.

The next conversation should receive the project runbook, job manifest and latest
stage receipt. No broad history reconstruction should be needed. Keep unresolved
decisions in the project record; keep reusable mechanics here.

## YouTube description chapter export

When the same reviewed course delivery is authorized for YouTube, read [description
chapter handoff](youtube-description-chapters.md). It uses the existing package's
`ID.chapters.json` and `package-receipt.json`, verifies the actual final-render hash,
and exports a description block. It does not infer new chapter boundaries or publish.
