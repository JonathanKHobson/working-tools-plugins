# Video template design contract

Source anchors are the existing Video Library HTML/UI and the shared chooser snapshot, carried forward with package-relative loading. The final Design Templates shared chooser merge restores relatedLink support while retaining its existing blurFill/cover behavior; the Video domain adapter and storyboard UI are unchanged. Lead review must inspect the exported library and storyboard at the same viewport before any visual acceptance claim.

| ID | Source / approximate region | Observed fact | Intended action |
| --- | --- | --- | --- |
| V1 | `runtime/library-chooser/index.html`, top controls | Chooser renders search and library cards from embedded JSON | Preserve shared control structure |
| V2 | `runtime/video-style-library/ui/adapter.js`, family card | Family identity has selectable exact examples, master hash and reviews | Preserve 30 family / 38 example identity |
| V3 | `runtime/video-style-library/ui/video.css`, preview/detail | Domain styling extends shared chooser CSS | Preserve CSS bytes |
| V4 | `runtime/video-style-library/ui/previews/`, method card | Seven exported JPEG previews derive from the pinned MIT sample PNGs | Record derivative hashes and preserve staged status |
| V5 | `runtime/video-style-library/ui/storyboard.html`, compact/editor views | Inline summary expands into ordered editable shot cards | Preserve view and save behavior |
| V6 | `runtime/video-style-library/ui/storyboard.js`, reload/save | Revision checks, media hydration and explicit Draw handoff | Preserve user edits and conflict handling |

Change: package ownership and portable defaults. Keep: interface IDs, public URL filtering, catalog identities/hashes, source UI, revisioned storyboard behavior and external private DB default. The public catalog omits creative narrative and asset bodies; method thumbnails derive from the licensed sample PNGs. Defer: native installation, native-host widget proof, published package and film reproduction. Lead-rendered inspection remains separate from automated source/behavior checks.
