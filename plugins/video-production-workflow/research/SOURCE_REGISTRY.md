# Source Registry

**Reviewed:** 2026-07-22  
**Policy:** Sources are evidence and inspiration, not an invitation to blend code with incompatible or absent licenses. URLs and license notes must be rechecked before redistribution or commercial use.

| ID | Source | License/status | Approved use | Research contribution |
|---|---|---|---|---|
| `agent-skills-spec` | Agent Skills specification | documentation-terms | architecture-reference | Skill folder, frontmatter, progressive disclosure, and portability conventions. |
| `openai-skills` | OpenAI Skills repository | mixed-per-skill | architecture-reference | Official Codex skill-creator and plugin-creator patterns; verify each subdirectory license. |
| `anthropic-skills` | Anthropic Skills repository | mixed-per-skill | architecture-reference | Cross-harness skill examples and authoring conventions; no code copied automatically. |
| `video-use` | browser-use/video-use | MIT | adapt-ideas-with-attribution | Conversation-driven editing, word-level transcript workflow, EDL, staged FFmpeg render, self-QA. |
| `claude-video-watch` | bradautomates/claude-video | MIT | adapt-ideas-with-attribution | Video understanding through captions, scene-aware frame extraction, detail budgets, and setup checks. |
| `claude-shorts` | AgriciDaniel/claude-shorts | MIT | adapt-ideas-with-attribution | Longform-to-shorts pipeline, scoring, word/silence boundary snapping, reframing, captions, export validation. |
| `remotion-superpowers` | DojoCodingLabs/remotion-superpowers | MIT | adapt-ideas-with-attribution | Modular Remotion production rules, audio-first timing, media generation, review and CI rendering patterns. |
| `remotion-skills` | remotion-dev/skills | not-found-at-review-time | research-only-no-copy | Useful internal workflow ideas; absence of a repository license means do not copy or redistribute content. |
| `remotion` | Remotion | custom-source-available | optional-integration-only | React-based programmatic video renderer. Verify current commercial license before adoption. |
| `hyperframes` | HyperFrames | Apache-2.0 | optional-integration | HTML/CSS/JavaScript frame-accurate renderer suited to UI motion and kinetic typography. |
| `motion-canvas` | Motion Canvas | MIT | optional-integration | TypeScript generator-based animation for explanatory motion graphics. |
| `manim` | Manim Community | MIT | optional-integration | Python mathematical and diagram animation engine. |
| `blender` | Blender Video Sequence Editor and Python API | GPL-3.0-or-later | invoke-external-tool-no-code-copy | Heavyweight VSE, compositing, 3D and scripting; keep Blender code/process isolated from permissive plugin code. |
| `ffmpeg` | FFmpeg documentation | LGPL-2.1-or-later-or-GPL-build-dependent | invoke-external-tool | Baseline media probe, decode, filter, encode, mux, loudness, subtitles, transitions and quality checks. |
| `ffprobe` | ffprobe documentation | LGPL-2.1-or-later-or-GPL-build-dependent | invoke-external-tool | Machine-readable stream, format, duration, color and codec inspection. |
| `moviepy` | MoviePy | MIT | optional-integration | Python composition convenience layer; prefer FFmpeg for fragile, high-volume, or codec-sensitive stages. |
| `pyav` | PyAV | BSD-3-Clause | optional-integration | Pythonic FFmpeg bindings for frame/packet-level analysis and custom processing. |
| `opentimelineio` | OpenTimelineIO | Apache-2.0 | optional-integration | Editorial timeline interchange model and adapters; media remains external. |
| `pyscenedetect` | PySceneDetect | BSD-3-Clause | optional-integration | Shot-change detection, scene lists, splitting and CLI workflows. |
| `faster-whisper` | faster-whisper | MIT | optional-integration | Local Whisper transcription via CTranslate2, including word-level timestamps. |
| `whisper` | OpenAI Whisper | MIT | optional-integration | Automatic speech recognition baseline and timestamped transcription. |
| `whisperx` | WhisperX | BSD-style-verify-current | optional-integration | Forced alignment and diarization options for more precise word timing. |
| `librosa` | librosa | ISC | runtime-dependency-optional | Beat tracking, onset strength, RMS energy, spectral and temporal music features. |
| `essentia` | Essentia | AGPL-3.0-or-commercial | invoke-or-optional-separate-environment | Advanced music descriptors and structure; keep licensing implications explicit. |
| `aubio` | aubio | GPL-3.0 | invoke-external-tool-no-code-copy | Low-latency onset, beat, tempo and pitch analysis. |
| `pyloudnorm` | pyloudnorm | MIT | runtime-dependency-optional | Python implementation of ITU-R BS.1770 loudness measurement and normalization helpers. |
| `mediapipe` | MediaPipe Tasks Vision | Apache-2.0 | optional-integration | Face and object detection for subject-aware reframing and crop suggestions. |
| `opencv` | OpenCV | Apache-2.0 | optional-integration | Frame sampling, optical flow, blur/exposure analysis, tracking, and image transforms. |
| `pillow` | Pillow | HPND | runtime-dependency | Image normalization, title cards, contact sheets, simple animation frames, and text measurement. |
| `fonttools` | fontTools | MIT | optional-integration | Font metadata, subsetting and variable-font inspection; does not grant font redistribution rights. |
| `wcag-captions` | W3C captions guidance | W3C-document-license | accessibility-reference | Captions provide synchronized text for speech and meaningful non-speech audio. |
| `wcag-contrast` | WCAG contrast guidance | W3C-document-license | accessibility-reference | Contrast criteria and rationale for readable text; video overlays still require contextual judgment. |
| `itu-bs1770` | ITU-R BS.1770 | standards-terms | audio-reference | Algorithms for programme loudness and true-peak audio measurement. |
| `ebu-r128` | EBU R 128 | documentation-terms | audio-reference | Broadcast loudness normalization guidance built on BS.1770. |
| `youtube-upload` | YouTube recommended upload encoding settings | site-terms | delivery-reference-reverify | Container, codec, frame rate, aspect ratio and audio recommendations; recheck before final delivery. |
| `youtube-aspect` | YouTube aspect ratio guidance | site-terms | delivery-reference-reverify | Player adaptation and native aspect-ratio guidance. |
| `tiktok-specs` | TikTok business video specifications | site-terms | delivery-reference-reverify | Official advertising specs used as a cautious technical proxy; organic product UI may differ. |
| `meta-reels` | Meta Reels creative and technical guidance | site-terms | delivery-reference-reverify | Reels aspect, media and creative guidance; user-interface overlays change over time. |
| `linkedin-video` | LinkedIn video specifications | site-terms | delivery-reference-reverify | Supported video formats and constraints; recheck before export. |
| `yt-dlp` | yt-dlp | Unlicense | optional-integration | Media acquisition only when the user has rights and the site permits access. |
| `editly` | Editly | MIT | research-and-optional-integration | Declarative JSON/JavaScript video editing patterns and transitions. |
| `mlt` | MLT Multimedia Framework | LGPL-2.1-or-later | optional-integration | Timeline-based multimedia engine used by nonlinear editors; candidate for future adapter. |
| `frei0r` | frei0r video effects | GPL-2.0-or-later | invoke-through-compatible-host | Portable video effects plugins; verify host and distribution implications. |

| `mediainfo` | MediaInfo | BSD-2-Clause | optional-integration | Detailed container, stream, codec, color, HDR, timecode and metadata inspection beyond the baseline ffprobe report. |
| `exiftool` | ExifTool | Artistic-1.0-Perl-or-GPL-1.0-or-later | invoke-external-tool-no-code-copy | Broad camera, image, audio and video metadata inspection and cautious metadata editing. |
| `vmaf` | Netflix VMAF | BSD-2-Clause-Patent | optional-integration | Full-reference perceptual comparison of encodes and delivery variants. |
| `shaka-packager` | Shaka Packager | BSD-3-Clause | optional-integration | DASH/HLS packaging and encryption after editorial mastering. |

| `mediaconch` | MediaConch | BSD-2-Clause-verify-current-components | invoke-external-tool | Policy and implementation conformance checking for audiovisual containers. |
| `qctools` | QCTools | GPL-3.0-program-and-BSD-3-Clause-BAVC-code | invoke-external-tool-no-code-copy | Signal-level plots, scopes and temporal artifact analysis for difficult masters and archival QC. |
