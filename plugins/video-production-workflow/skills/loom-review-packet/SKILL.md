---
name: loom-review-packet
description: Turn a Loom UX review into a timestamped packet of transcript cues, key frames, and clearly separated observations, questions, and recommendations. Use when reviewing a Loom or similar screen-recorded design walkthrough; do not use for recording or publishing a Loom.
---

# Loom Review Packet

Create a compact, evidence-linked packet that lets a designer or stakeholder move from a UX comment to the exact video moment and frame that supports it.

## Gather the source

Collect the Loom title, author, source URL, transcript, and either a local video file or existing screenshots. Preserve the raw transcript unchanged. If only a Loom URL is available, use the signed-in browser normally; do not bypass access controls or imply that the video was downloaded.

Record the state precisely. A copied transcript is not a captured frame, a captured frame is not an organized packet, and an organized packet is not delivered feedback.

## Extract timestamp cues

Use the helper to convert timestamped transcript text into a reviewable CSV. Resolve `<skill-directory>` to the folder containing this `SKILL.md`:

```bash
python3 <skill-directory>/scripts/loom_review_packet.py extract \
  --transcript /path/to/transcript.txt \
  --output /path/to/timestamps.csv
```

Review the extracted rows and create a cue CSV. Select moments that materially support UX feedback: a new screen or state, a comparison, a stated design question, a confusing interaction, or evidence for a recommendation. Consolidate nearby timestamps when one frame proves the same point.

Read [references/packet-format.md](references/packet-format.md) for the cue schema and output structure.

## Capture key frames

Prefer a local video plus `ffmpeg` when available because it produces repeatable frame timing. If no local video is available, seek to each cue in Loom, pause, wait for the target UI state to settle, and capture the product area needed to understand the feedback. Exclude unrelated windows, notifications, and private content.

Use filesystem-safe timestamp names. On macOS, a filename such as `1:58.png` can fail in Finder; use `01-58` or the helper-generated form instead.

Existing screenshots can be mapped to cues by filename or absolute path. The helper copies source screenshots by default so the originals remain intact.

## Build the packet

```bash
python3 <skill-directory>/scripts/loom_review_packet.py build \
  --title "Fictional library issue review" \
  --author "Demo reviewer" \
  --source-url "https://example.org/fictional-review" \
  --transcript /path/to/transcript.txt \
  --cues /path/to/cues.csv \
  --screenshots-dir /path/to/source-screenshots \
  --output /path/to/loom-review-packet
```

Use `--video /path/to/video.mp4` when cue rows without screenshots should be captured from a local video. This requires `ffmpeg`. The output directory must not already exist. Use `--allow-missing` only to create an explicitly partial staging packet; never describe that result as complete.

## Write UX feedback

Keep these evidence types separate in the cue CSV and generated review:

- `observation`: what is visibly shown or explicitly said.
- `question`: the decision that needs an answer.
- `recommendation`: the proposed UX action and rationale.

Do not convert a speaker's question into a team decision or treat an inference as an observed fact. Edit `ux-feedback.md` after assembly when synthesis is needed, while retaining each timestamp and frame link.

## Verify before signoff

Inspect the rendered packet, not just filenames or extracted text. Check a small set of representative anchors: the opening context, every major screen/state change, the most important question, and the final recommendation. For each, verify that the timestamp, frame content, and written feedback agree.

Confirm that:

- `manifest.json` reports `complete` and its cue and frame counts match;
- every cue links to a readable, relevant frame;
- frame order follows video time;
- filenames contain no colons;
- no source screenshots were moved or overwritten;
- `ux-feedback.md` distinguishes observation, question, and recommendation.

Report the packet as built only after those checks. Report delivery or stakeholder receipt only with separate evidence.
