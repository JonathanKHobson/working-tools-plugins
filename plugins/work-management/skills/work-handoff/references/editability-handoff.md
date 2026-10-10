# What remains editable after export

Use this small addition when handing off a visual, presentation, video or interactive artifact whose recipient may revise it. Put the result in the existing delivery note; do not create a separate system or inventory for a trivial export.

Identify the delivered artifact, editable master, required application/runtime, linked assets/data/fonts and the recipient's intended next edit. State actual verification and any missing access or dependency. A file extension alone does not establish editability.

For a simple graphic, one sentence can suffice: “The SVG source retains text and vector shapes; the PNG is flattened. The original photograph remains a raster image. Opened and checked in [actual app].” For a mixed artifact use a short table:

| Part | Editable in delivered file? | Where to change it | Verified or limitation |
| --- | --- | --- | --- |
| Text/notes | Native text, raster, or unknown | Master / destination app | Font substitutions, overflow and notes checked? |
| Shapes/diagrams/charts | Native objects, vector group, image, or unknown | Source, source data, or destination app | Separate geometry/data edits tested? |
| Images | Replace/crop versus edit internal content | Original asset / authorized image tool | Resolution and source included? |
| Motion/audio/timing | Timeline/keyframes versus rendered stream | Actual project/source and editor | Effects, media and fonts available? |
| Interaction/data | Source code/data versus static snapshot | HTML/SVG/source files | Offline behavior and dependencies checked? |

Only include relevant rows. Use **unverified** where no round trip was performed. Distinguish “source is editable” from “this export preserves editable objects.” SVG text may have been converted to paths; a PPTX may consist of screenshot slides; an HTML file may depend on remote assets; MP4 contains rendered video/audio, not the original timeline. A saved canvas may still require its original service.

When the requested outcome depends on destination editing, open the export in that application or available compatible tool and test one representative edit from each consequential object type. Reopen saved source/export as relevant. If that application is unavailable, provide the master and say destination editability is unverified; do not claim a passed check from inspecting the archive alone. Keep the approved original intact when using a test copy.

For generated or exported presentations report native text, shapes, charts, pictures and notes separately. For a video deliverable distinguish captions/transcript, editable motion/project source and the final render. Include reproduction instructions only to the extent they are needed; preserve existing authorized workflows and do not install extra software merely to make the handoff look complete.
