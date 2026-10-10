# Loom Review Packet Format

## Cue CSV

The cue file must contain a `timestamp` column. These optional columns improve the packet:

| Column | Purpose |
| --- | --- |
| `timestamp` | Loom/video time as `M:SS` or `H:MM:SS`. |
| `topic` | Short filesystem-safe label for the moment. |
| `screenshot` | Existing image filename under `--screenshots-dir`, or an absolute path. Leave blank to capture from `--video`. |
| `observation` | What is visibly shown or explicitly said. |
| `question` | The unresolved UX/product decision. |
| `recommendation` | Proposed action and rationale. |

Example:

```csv
timestamp,topic,screenshot,observation,question,recommendation
0:23,mobile issue card,0-23.png,"Comments and media are shown in the issue card.","Should they remain visible before opening the issue?","Keep the collapsed card scannable; reveal the thread after opening."
1:58,edit open issue,1-58.png,"The edit state includes description and follow-up fields.","Can add and edit use the same field order?","Use one field order unless a required creation-only field prevents it."
```

Keep observation, question, and recommendation distinct. Empty cells are preferable to invented evidence.

## Transcript parsing

The extractor accepts timestamps embedded in copied Loom transcript text. It creates:

```text
sequence,timestamp,seconds,transcript
```

It preserves transcript wording while collapsing whitespace in the derivative CSV. The raw transcript remains the source of truth.

## Output

```text
loom-review-packet/
|-- manifest.json
|-- ux-feedback.md
|-- transcript/
|   |-- raw.txt
|   `-- timestamps.csv
`-- frames/
    |-- 001-00-23-mobile-issue-card.png
    `-- 002-01-58-edit-open-issue.png
```

`manifest.json` records packet status, source metadata, cue count, frame count, per-frame source, and SHA-256 hashes. `complete` means every cue has a frame. `partial` means one or more cues are missing frames and is only produced when `--allow-missing` is explicitly used.

## Frame choice

Choose the smallest set of frames that proves the feedback. Capture another frame when the UX claim depends on a different state, screen, or comparison. Avoid near-duplicates that add no evidence.

When capturing manually from Loom, keep the exact cue timestamp in the cue CSV even if the player lands a second away. Note a meaningful discrepancy in the observation instead of silently changing the evidence.
