# YouTube description chapter handoff

Use for a prepared course-media package or reviewed output chapter map destined for
YouTube. Chapters are navigation aids: choose titles for the actual section and keep
the learning sequence. Do not infer a new boundary from a pause or keyword alone.

Official [YouTube chapter rules](https://support.google.com/youtube/answer/9884579?hl=en),
verified 2026-10-01: begin with 00:00; list at least three timestamps in ascending order;
every chapter must last at least ten seconds. Check the last chapter through the actual
video end too. Manual chapters override automatic chapters; eligible automatic chapters
are allowed by default for new uploads, but eligibility and displayed chapters must be
verified in the account/player. A valid text block does not prove chapters appeared.
Recheck current official requirements at handoff.

## Prepare and validate

1. Finish the authorized edit and actual rendered QA. Freeze the final render/hash,
   probed duration, output-time captions/transcript and reviewed chapter boundaries.
   Any trim, speed change, reorder or replacement invalidates old chapters: remap,
   regenerate sidecars/receipt and inspect the new render before exporting again.
2. Use `package_course_media.py` for untrimmed consecutive clips as already documented.
   Its `ID.chapters.json` contains `{id, title, startSeconds}`; `package-receipt.json`
   records the chapter hash, total duration and optional `delivery` hash/duration.
   Supply that delivery proof when packaging for this export. The chapter helper
   requires it and rejects a package prepared before the final delivery existed.
   For edited material, use the project's verified output-time map and package adapter;
   do not mislabel it as untrimmed. A prepared map without a bound receipt needs that
   project-level preparation before this helper can accept it.
3. Review titles against speech and screen actions. Name the section's actual useful
   action or topic; retain accurate prerequisites and technical terms. Do not invent
   outcomes, inflate promises or force a title length/number of chapters. If the video
   cannot support three useful sections of ten seconds, omit manual chapters rather
   than fabricate sections. Website chapters can remain valid even when YouTube's
   minimum count is not met.
4. Export from the maintained/installed plugin root using local standard-library code:

   ```sh
   python3 scripts/export_youtube_chapters.py /absolute/job/package/ID.chapters.json /absolute/job/package/package-receipt.json /absolute/job/delivery.mp4
   python3 scripts/export_youtube_chapters.py /absolute/job/package/ID.chapters.json /absolute/job/package/package-receipt.json /absolute/job/delivery.mp4 --json
   ```

   Both commands read local files and print to stdout only. Text output is just the
   copyable chapter block. JSON additionally returns chapter/receipt/render/description
   hashes, duration, and the mechanical validation boundary; retain it in the project's
   handoff receipt. No network, probing, publication or candidate/upstream code execution
   occurs. Whole-second export floors starts; the helper validates both original and
   exported spacing, including the final chapter. Inspect exported boundary precision
   on the render; merge or move a boundary deliberately if conversion makes it invalid.
5. Handoff the block and hash proof to `social-content-studio:social-publishing` with the
   final asset/metadata and existing release constraints. After an authorized save,
   read back the exact description and verify seeking in the actual player. Check
   chapters displayed, titles, first/last and joins. Keep prepared, saved, published
   and player-verified states separate; follow project review holds.

Example only:

```text
00:00 Inspect the source
00:35 Build the first draft
01:12 Check the result
```

The timestamp list is not an upload command. The helper proves hash/structure agreement
and declared timing, not independent duration, content, listening or visual approval.
Keep actual media probe and rendered QA evidence alongside the export receipt.

## Attribution

Chapter validation ideas selectively adapted from Jake Schincariol's `yt-chapters`
at commit `a2feb2104981a375ffd4f87ee04f4f5344ac43c6` (MIT); complete method/helper and
its parser dependency are preserved [inactive](../../../libraries/youtube-agent-methods/PROVENANCE.md).
The local exporter is independently implemented for the existing course package;
no upstream script, keyword-based boundary scorer or mandatory approval question runs.
