# Resolve round-trip acceptance

Read when an editorial timeline moves into/out of Resolve or a Resolve delivery
must remain editable. Use **edit-davinci-resolve** for app control. Preserve a
frozen cut-map/manifest revision and media hashes alongside the handoff. For an
ordinary native saved-project deliverable, verify save/reopen, source links and
clip editability; an interchange export/reimport is required when crossing tools
or delivering an interchange timeline. Archive restoration is a separate test.

## Choose a representable timeline

The existing command is:

```sh
python -m video_workflow.cli export-timeline project.json --format edl --output work/timeline.edl
```

Use `--format otio` only with the optional interchange runtime installed and
verified. These exporters are deliberately limited implementations:

- CMX3600: video/animation hard cuts, video track only, integer frame-rate
  conversion and non-drop-frame timecode, eight-character reel IDs. Preflight
  for reel-ID collisions. Fractional rates, source start timecode, retimes,
  transitions and separate audio need a verified richer export or explicit
  manual reconstruction; do not silently approximate them.
- OTIO: one sequential picture track including images; record starts are stored
  as metadata, without gap/overlap/transition or audio-track reconstruction.
  Media paths must be resolved through the stable-ID relink map. Use this route
  only for a representable contiguous cut sequence or an independently tested
  adapter; unsupported intent belongs in the handoff notes.

A file with an XML/OTIO extension does not prove compatibility. FCPXML can be a
useful alternative when a separately verified exporter preserves the required
features; this plugin does not currently include an FCPXML exporter. Do not run
an upstream download as a shortcut around review/compatibility testing.

## Prove editability

Use a small copied/synthetic fixture containing repeated source ranges, clip
boundaries and every required track/feature. Verify against the cut map:

1. Import into a disposable project, relink to actual media and inspect the
   timeline's clip order, source in/out, record positions, rate, duration and
   audio/channel placement. Account for inclusive/exclusive end conventions.
2. Inspect captions, transforms, transitions, color and any baked graphics.
   Record which items remain native/editable and which are normalized picture.
3. Save and reopen the project, checking the same source links and state.
4. Export an available supported timeline format from Resolve and import it
   into a fresh project. Repeat the comparison; a rendered MP4 cannot serve as
   this test. Keep a comparison receipt and explicit loss/manual-work list.
5. Only then move the full edit, repeating final source/range/duration checks.

For delivery, include the saved `.drp` or requested timeline file, stable media
map with hashes, rights-safe source/dependency locations, output-timed captions,
unsupported-feature notes and a verified reference render. A `.drp` alone is
not self-contained. If an archive is requested, package a `.dra` or equivalent
authorized media bundle, restore it to a fresh location and check relink/playback
before calling it restorable. Do not package stock/font assets beyond their rights.
