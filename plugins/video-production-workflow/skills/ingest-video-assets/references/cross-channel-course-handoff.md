# Course and workshop cross-channel handoff

Use when the authorized intake includes a wider channel flow. Reuse the reviewed
media and transcript package from [course-video installation](course-video-installation.md);
Social Publishing owns native actions and channel policy. This reference owns the
media/source evidence handoff, not a posting adapter.

For a course or workshop recording authorized for a wider channel flow, reuse this
one source package. Prepare the source-supported derivative set below; a candidate
is not an instruction to publish immediately. Preserve the existing releases and
their URLs. A new handoff does not authorize changing the course itself: record
`instructional_change_requested` and route actual course work to Instructional
Design's course-production handoff only when that instruction exists.

| Derivative | Video's preparation | Downstream owner |
| --- | --- | --- |
| Full/part YouTube lesson or workshop | Reviewed final media, chapters, complete captions and source-supported teaching promise | Social Publishing for authorized native scheduling/readback |
| YouTube Shorts | Self-contained moments with their own payoff; final edit/transcript/timing map and portrait art | Dialogue/conform/QA, then Social Publishing |
| LinkedIn YouTube companion | Real example or lesson, evidence span and takeaway; exact video/course destination | Social/Writing Quality for adaptation and native scheduling |
| Substack article candidate | Substantive teaching argument, worked example, usable steps and limits, supported by the transcript | Social/Writing Quality for article craft and approved release |
| Later LinkedIn native Short/video | Reuse the reviewed edit or prepare an authorized platform variant; keep its lineage to the YouTube source | Social Publishing for a separate release slot |
| Later LinkedIn article | Standalone professional lesson adapted from the evidence, with distinct framing | Social/Writing Quality for article adaptation and approved timing |

Select moments and article angles from exact transcript spans. Label fictional
teaching examples and distinguish interpretation from recorded facts. An article
must teach something useful without requiring the reader to watch a video; do not
pad a transcript or turn an illustrative exercise into an invented success story.
If the source cannot support a useful standalone Short or article, record that gap
instead of manufacturing the derivative. Full-course compilations wait for all
required material and their own reviewed edit; available parts can proceed under
the existing release plan.

Keep a compact project handoff with these fields, reusing existing records:

- `content_id`, `parent_content_id`, media/asset IDs, source span and its timebase.
- Source/final render paths and hashes, complete captions/transcript paths and
  hashes, chapter map, output duration, format-specific art, and review evidence.
- Teaching takeaway, concrete example, claim-to-transcript references, course URL,
  privacy/rights constraints, and `instructional_change_requested`.
- Authorized channels and `authorization_source`: cite the user's applicable
  standing grant or narrower request. A worker assignment carries that scope;
  it does not create a wider publication grant.
- Per-derivative status and candidate/draft location; saved platform IDs, timestamps
  and public-link state only from the downstream publishing receipt.
- Release dependencies, time zone, approved `not_before`/spacing rule and its source;
  an unavailable native scheduling window remains prepared, not scheduled.

These editorial/release fields belong to the project handoff. Do not add article,
post or remote-state roles to `preflight-delivery`, which checks local media and
review freshness only. Pass a small per-item package to each delegate and preserve
stable IDs across adapters; do not make every worker reread the complete source
or independently reconstruct a calendar.

Keep same-day YouTube promotion distinct from a later native LinkedIn video or
article. Read the project's approved spacing policy; when it calls for separation
by weeks, carry its explicit earliest date/dependency to Social Publishing. Do not
pick an immediate slot merely because a file is ready, infer a scheduling guarantee
from a planned timestamp, or move an existing release as a side effect of adding a
new channel. Social Publishing owns cross-channel collision checks and the current
native interface/window. Never claim a scheduled/private YouTube URL is publicly
playable before release readback.

If a native YouTube receipt changes publish time or visibility/status, mark all
dependent companions `reconciliation_required`. Send the shared publishing owner
the stable content ID, old/new timestamps and statuses, and the changed receipt.
That owner reconciles prepared or scheduled LinkedIn/Substack derivatives against
the current platform ledger and authorized spacing policy before clearing the
flag. Do not silently shift companion dates or leave promotions pointing to a
private source. A local plan edit cannot establish a native platform change.

Use analytics to identify a bounded craft question, not to replace learning value,
creative judgment, compassion or critical thinking. Improve truthful pacing,
legibility and accessibility first. Keep performance observations separate from
hypotheses; social/marketing research must provide dated, current evidence before
a trend shapes the copy. Do not promise virality or fabricate performance metrics.
