# Analyze Video Content: Source Index

These are the sources directly used to shape this skill. The plugin-wide registry and policy live in `../../../../research/sources.lock.json`.

- [bradautomates/claude-video](./claude-video-watch.md) — adapt-ideas-with-attribution; Video understanding through captions, scene-aware frame extraction, detail budgets, and setup checks.
- [browser-use/video-use](./video-use.md) — adapt-ideas-with-attribution; Conversation-driven editing, word-level transcript workflow, EDL, staged FFmpeg render, self-QA.
- [PySceneDetect](./pyscenedetect.md) — optional-integration; Shot-change detection, scene lists, splitting and CLI workflows.
- [faster-whisper](./faster-whisper.md) — optional-integration; Local Whisper transcription via CTranslate2, including word-level timestamps.
- [OpenAI Whisper](./whisper.md) — optional-integration; Automatic speech recognition baseline and timestamped transcription.
- [WhisperX](./whisperx.md) — optional-integration; Forced alignment and diarization options for more precise word timing.
- [MediaPipe Tasks Vision](./mediapipe.md) — optional-integration; Face and object detection for subject-aware reframing and crop suggestions.
- [OpenCV](./opencv.md) — optional-integration; Frame sampling, optical flow, blur/exposure analysis, tracking, and image transforms.

No third-party source code is vendored in this skill. Ideas adapted from permissively licensed projects remain attributed; unlicensed or incompatible sources are research-only or invoked as external tools.
