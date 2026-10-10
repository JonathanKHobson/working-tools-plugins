# Resolve control and finishing

Read for setup, import or edits inside Resolve. Record live capabilities in the
project's existing setup record/profile: edition/build, OS, application and
media/cache/proxy paths, frame-rate/color defaults, keyboard preset, permitted
control route and last smoke-test evidence. Resolve's About screen and installed
documentation take precedence over an old profile. Discover the existing profile
through the owning project; do not create a second catalog or runtime registry.

## Edition boundary and substitutions

Reviewed 2026-10-07: Blackmagic's 21.1 release catalogue assigns assistant
integration to Studio. The pack's inspected vendor documentation and the
community MCP maintainer agree that Python scripting moved to Studio in 21.1.
Use the [route sources](resolve-routes.md) for exact references and limits.
Recheck after editor updates; no local install or successful edit is implied.

| Requested capability | Free route |
| --- | --- |
| Assemble reviewed source ranges | Import a suitable timeline file and verify clips/media in the editor |
| Tighten speech or remove silence | Reviewed local transcription plus manual/UI trims; preserve meaning and learning pauses |
| Captions | Generate reviewed output-timed SRT externally and import; style through available controls |
| Reframe | Inspector transform/keyframes and visual review of the subject or demonstrated UI |
| Dialogue cleanup | Available Fairlight gain/EQ/dynamics and the approved external audio route; verify availability before use |
| Color and compositing | Available Color/Fusion controls; normalize inputs and inspect temporal edges |

Do not select Studio-only transcription, IntelliCut, automatic audio subtitles,
Voice Isolation, Magic Mask or Smart Reframe as Free dependencies. For a missing
feature, use a supported substitute or report the finishing limit. Do not
purchase, downgrade or modify a scripting gate to make a route fit.

The external community project is
[`samuelgursky/davinci-resolve-mcp`](https://github.com/samuelgursky/davinci-resolve-mcp),
separate from the editing pack and the vendor's bundled `ResolveMCP`. Its README
limits the measured Free bridge to 21.0.x and leaves Free 21.1 Python Console
support unconfirmed. It is not a Free 21.1 setup instruction. If another edition
has an authorized supported MCP, verify status and a read-only project request
before mutations; installation or a tool list does not prove connection.

## Minimal app proof before real media

Reuse proof for the same edition/build, import format and required feature set
when the media/runtime bindings are still valid. Run or extend the smoke test
when proof is absent, stale or the route changed; an ordinary finishing task in
an existing native project does not need a new disposable import project.

Use the existing verified FFmpeg/ffprobe to prepare tiny synthetic picture and
audio with visible frame/clip identities. Put them in the project's work/test
area, preserving user sources. In a disposable Resolve project:

1. Set the timeline frame rate deliberately; verify playback and delivery rates.
2. Import a few source ranges including two separate ranges from one asset.
3. Read clip identities, in/out positions, track placement and total duration;
   verify intended audio without duplicate playback.
4. Save, reopen, export a short test and probe its actual media streams.
5. For an editable handoff, perform the linked round-trip acceptance procedure.

Keep the project until proof is collected or the user wants it; clean up only
task-owned disposable files/projects. If app access is absent, prepare the
timeline/cut sheet and identify the remaining import/verification step honestly.

## Precise finishing

Confirm project/timeline identity after dialogs and page switches. Inspect
Keyboard Customization before relying on shortcut examples. Lock or exclude
unaffected music, graphics and caption tracks from ripple operations. Check
linked audio/video selection and intended trim mode.

Move by timecode, frame controls or verified keyboard commands for exact edits;
dragging edges at a wide zoom cannot establish one-frame accuracy. Inspect the
Edit Index/Inspector or zoomed timeline after each small mutation. Reconcile an
uncertain action before retrying so an extra delete or trim cannot compound it.

Match color management to actual source tags and intended output. Adjust
exposure/white balance before a creative look and compare adjoining shots. Use
room tone, restrained fades and J/L cuts where the brief calls for continuity.
Caption timing follows the completed edit; manual reframe review must protect
the subject, meaningful screen controls and readable text at delivery size.

Use proxies/cache only when needed, outside originals, and verify final render
uses the intended quality/media. Save the editable project and preserve the
reviewed master before making an independently named derivative timeline.
