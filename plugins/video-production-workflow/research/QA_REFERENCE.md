# Video Quality Assurance Reference

## Automated evidence

- ffprobe stream/format JSON;
- expected versus actual duration;
- frame rate, time base, resolution, sample rate, channels, codec, pixel format, and color tags;
- black, freeze, silence, clipping, loudness, true-peak, and missing-stream detectors;
- manifest/schema/timeline assertions;
- caption timing, overlaps, reading-speed flags, and file validity;
- hashes and command/tool-version logs.

## Visual evidence

- first and last frames;
- regular contact sheet;
- every cut/transition boundary at adjacent timestamps;
- frames containing dense text or captions;
- each aspect-ratio variant under UI overlays;
- alpha/matte frames for overlays;
- HDR/SDR representative frames on appropriate displays when possible.

## Human/agent watch-through

Watch once for story and emotion without stopping. Watch again for picture. Listen once without looking. Review muted for visual comprehension. View at a small/mobile approximation. Automated checks cannot tell whether a joke lands, a pause breathes, a crop feels disrespectful, or a transition is cheesy.

## Approval record

Approval must bind to exact path, hash, size, duration, date, reviewer, QA report, exceptions, and delivery purpose. Any later re-encode is a new file requiring at least targeted revalidation.
