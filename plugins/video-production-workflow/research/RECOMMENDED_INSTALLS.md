# Recommended Local Toolchain

**Reviewed:** 2026-07-22  
**Principle:** install the smallest reproducible stack that can complete the current job. Every extra renderer, codec build, model, and package manager expands the failure surface and the licensing surface.

## Tier 0 — required baseline

| Tool | Role | Why it belongs in the baseline |
|---|---|---|
| Python 3.10+ | Orchestration, manifests, analysis and tests | Portable scripting and strong media-analysis ecosystem |
| FFmpeg + ffprobe | Decode, normalize, filter, composite, encode, mux and inspect | The most dependable cross-platform assembly spine |
| Git | Versioning plugin, manifests and generated code | Makes iterative agent edits reviewable and reversible |
| A virtual environment | Isolate Python dependencies | Prevents project tools from silently changing the global interpreter |

A baseline FFmpeg build should expose the filters and encoders the project actually needs. Check rather than assume:

```bash
python scripts/check_environment.py > toolchain-report.json
ffmpeg -hide_banner -filters
ffmpeg -hide_banner -encoders
ffmpeg -hide_banner -hwaccels
```

At minimum, ordinary productions benefit from `subtitles` or `ass`, `loudnorm`, `xfade`, `acrossfade`, `blackdetect`, `freezedetect`, `silencedetect`, `showwavespic`, and H.264/AAC encoders. HDR work additionally needs a verified color-management path such as `zscale` and `tonemap`.

## Tier 1 — recommended production utilities

| Tool | Role | Installation posture |
|---|---|---|
| MediaInfo | Second opinion on container, stream, color, HDR, timecode and tag metadata | Recommended; BSD-2-Clause |
| ExifTool | Camera/image/video metadata inventory and cautious metadata edits | Recommended as an external utility; Perl Artistic/GPL choice |
| ImageMagick | Batch image normalization, inspection and asset preparation | Optional but useful for image-heavy work |
| SoX | Audio utility processing and independent measurement | Optional second opinion for audio workflows |
| Node.js + npm | HyperFrames, Motion Canvas, Remotion and browser-native renderers | Install only when a chosen animation slot needs it |
| yt-dlp | Acquire user-authorized online media | Rights-sensitive; never equate technical access with permission |

## Tier 2 — analysis and quality control

| Tool | Use it for | Limits and cautions |
|---|---|---|
| librosa | Beats, onset strength, RMS, spectral/temporal features | Beat detection is evidence, not editorial taste |
| pyloudnorm | Python BS.1770 loudness measurement | FFmpeg `loudnorm` may already cover the pipeline |
| PySceneDetect | Candidate shot boundaries and scene lists | Do not blindly convert every detected change into a cut |
| faster-whisper / WhisperX | Local transcription, word timing, optional alignment/diarization | Model downloads, GPU/CPU cost and transcript error review remain necessary |
| MediaPipe / OpenCV | Subject tracking, face landmarks, crop anchors and frame diagnostics | Confidence thresholds and manual override are mandatory |
| Netflix VMAF | Full-reference comparison of encodes against a trusted master | Not a no-reference taste score; alignment and identical content are prerequisites |
| MediaConch | Policy and implementation conformance checks | Verify current package/component licenses and author a project-specific policy |
| QCTools | Signal-level plots, scopes, broadcast range and temporal artifact investigation | External GPL application; powerful evidence, not an automatic approval stamp |

## Tier 3 — specialized renderers

| Renderer | Choose it when | Avoid defaulting to it when |
|---|---|---|
| FFmpeg + Pillow | Slideshows, cards, reframing, overlays, captions, delivery and utility motion | The filter graph would become an unmaintainable motion-design program |
| HyperFrames | HTML/CSS/JavaScript UI motion and kinetic typography | A Python/FFmpeg card is sufficient |
| Motion Canvas | TypeScript explanatory animation and diagrams | The project does not need its separate runtime |
| Manim | Mathematics, state diagrams, graphs and formal transformations | General editorial assembly is the main task |
| Blender | 3D, tracking, particles, compositing or VSE automation | Setup and render latency outweigh the visual requirement |
| Remotion | A reusable React component system is strategically valuable | Its current source-available/commercial license has not been checked for the use case |
| MoviePy | Small Python-native compositions and prototypes | Codec precision, speed or complex filter behavior is critical |
| PyAV | Packet/frame-level Python access and custom analysis | The team does not understand time bases, seeking and codec behavior |

Each specialized renderer should produce a bounded media asset—preferably an overlay or clip with a declared duration, dimensions, frame rate, alpha behavior, codec and color assumptions—then return to the shared editorial manifest.

## Tier 4 — interchange, streaming and preservation

| Tool | Role |
|---|---|
| OpenTimelineIO | Exchange editorial structure and references without embedding media |
| CMX3600 EDL | Lowest-common-denominator cut-list escape hatch |
| Shaka Packager | Package finished encodes as DASH/HLS and add supported encryption; not an editor |
| MLT | Future NLE-style timeline adapter where its engine model is useful |
| FFV1/Matroska + MediaConch policies | Preservation-oriented mezzanine/conformance workflows where required |

## macOS/Homebrew starting points

Package availability changes. These commands were checked on 2026-07-22; inspect the plan before executing it.

```bash
# Core
brew install ffmpeg python git

# Production inspection and utilities
brew install media-info exiftool imagemagick sox

# Optional conformance and signal QC
brew install mediaconch libvmaf
brew install --cask qctools

# Browser/React/TypeScript renderers
brew install node
```

Homebrew's current `ffmpeg` formula includes `libvmaf`, but a different FFmpeg build may not. Always confirm with `ffmpeg -filters`.

Shaka Packager is best installed from an official release or a controlled container when no trusted system package exists. Record its version and checksum in project provenance.

## Linux starting points

Package names and feature flags differ by distribution. A conservative Debian/Ubuntu baseline is:

```bash
sudo apt-get update
sudo apt-get install -y ffmpeg python3 python3-venv python3-pip git \
  mediainfo libimage-exiftool-perl imagemagick sox
```

Install Node, MediaConch, QCTools, VMAF-enabled FFmpeg and Shaka Packager from the distribution, vendor repository, official release, or a pinned container only after verifying the package and license. A package named `ffmpeg` is not proof that every needed filter or encoder is enabled.

## Windows starting points

Use a trusted package manager or official releases for Python, Git, FFmpeg, Node, MediaInfo and ExifTool. After installation, run the plugin's environment check from the same shell Codex will use. Windows Store Python aliases, multiple FFmpeg copies and PATH ordering are common causes of “installed but unavailable” failures.

## Python environment profiles

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -e .
pip install -e '.[audio]'
pip install -e '.[analysis]'
pip install -e '.[interchange]'
pip install -e '.[python-renderer]'
pip install -e '.[dev]'
```

Do not install every optional group by reflex. Faster-Whisper, MediaPipe and some video libraries can introduce large model/runtime downloads and platform-specific binary conflicts.

## Reproducibility checklist

1. Save `video-workflow check --output toolchain-report.json`.
2. Save `ffmpeg -version`, build configuration, filters and encoders.
3. Lock Python dependencies and Node lockfiles per renderer slot.
4. Record hashes for source assets, generated assets and final masters.
5. Record model names, revisions, prompts, seeds and provider terms for generated media.
6. Cache immutable analyses by source hash plus tool/configuration version.
7. Keep originals read-only; write normalized media, proxies and renders elsewhere.
8. Recheck platform specifications and source-available/commercial licenses immediately before delivery or redistribution.
