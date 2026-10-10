# Toolchain Decision Guide

## Baseline

| Need | Default | Why |
|---|---|---|
| Probe media | ffprobe JSON | Stable machine-readable stream/format metadata |
| Decode/filter/encode/mux | FFmpeg | Broad format and filter coverage; CLI is scriptable and inspectable |
| Orchestration | Python | Strong file/data tooling, testing, audio/image ecosystem |
| Images/cards | Pillow + FFmpeg | Deterministic and lightweight |
| Project contract | JSON/YAML + JSON Schema | Human and machine editable; renderer neutral |
| QA | ffprobe + FFmpeg detectors + frame artifacts + watch-through | Combines structure, evidence, and judgment |

## Optional analyzers

| Tool | Use when | Do not default when |
|---|---|---|
| librosa | Beat/onset/energy features and local Python analysis | Environment must stay dependency-minimal |
| Essentia | Advanced music descriptors/structure | License obligations or deployment conflict |
| aubio | Lightweight/real-time beat, onset, pitch | Vendoring GPL code would conflict |
| PySceneDetect | Shot boundaries and scene lists | Cuts are already known or footage is extremely short |
| MediaInfo / ExifTool | Deep container, camera, color, timecode and tag inspection | ffprobe already answers the question or metadata edits would create risk |
| VMAF | Compare an encode to a trusted aligned reference master | No reference exists, content differs, or the question is artistic quality |
| MediaConch / QCTools | Conformance policies and signal-level forensic QC | Ordinary social output only needs baseline QA |
| faster-whisper | Local fast transcription | GPU/runtime burden exceeds need or native captions suffice |
| WhisperX | Word alignment/diarization precision | Setup complexity is not justified |
| MediaPipe/OpenCV | Subject-aware crop, tracking, frame quality | A manual anchor is more reliable and cheaper |
| pyloudnorm | Python loudness analysis | FFmpeg loudnorm already covers the required pipeline |

## Optional renderers

| Engine | Best fit | Trade-offs |
|---|---|---|
| FFmpeg/Pillow | Assembly, transforms, cards, overlays, subtitles, utility animation | Complex motion can become unreadable filter graphs |
| HyperFrames | HTML/CSS/JS, UI/product motion, kinetic typography | Browser runtime and project-local Node setup |
| Motion Canvas | Explanatory TypeScript animation and diagrams | Separate ecosystem and render pipeline |
| Manim | Mathematical/formal diagrams and graph morphs | Not a general editorial renderer |
| Blender | 3D, tracking, VFX, particles, compositing | Heavy setup; GPL application; longer render/debug loop |
| Remotion | Reusable React component systems | Custom source-available/commercial license must fit |
| MoviePy | Convenient small Python compositions | Lower-level control/performance may be insufficient |
| PyAV | Frame/packet-level custom processing | Requires codec/time-base expertise |
| MLT | NLE-style timeline engine and future adapter | Additional framework boundary and integration work |
| Shaka Packager | DASH/HLS packaging after final encode | The task is editorial composition rather than streaming delivery |

## Selection heuristic

Choose the lowest-complexity tool that can produce the required output deterministically, legally, and with acceptable review latency. A tool is not “free” merely because it is already installed: every additional runtime expands failure modes, cache keys, licensing, and maintenance.

## Installation reference

See `RECOMMENDED_INSTALLS.md` for tiered, license-aware local setup and current package-manager starting points.
