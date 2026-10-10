# Gap Analysis and Contribution Strategy

## 1. Editorial intermediate representation

**Observed gap:** Many workflows jump from prompt/transcript directly to FFmpeg commands or a renderer-specific composition.

**Contribution:** `schemas/video-project.schema.json`, the `video_workflow.manifest` API, and a renderer-neutral timeline carrying assets, source ranges, output timing, text, motion intent, audio, captions, delivery, QA, and provenance.

## 2. Music semantics

**Observed gap:** “Waveform” and “beat sync” are often treated as sufficient.

**Contribution:** Layered signal/pulse/phrase/energy/editorial reasoning, confidence-aware cut windows, alternate tempo interpretation, and pacing modes that preserve story and reading time.

## 3. Video design

**Observed gap:** Layout and typography are frequently embedded as hardcoded renderer templates.

**Contribution:** Design tokens, temporal hierarchy, local/dynamic contrast, responsive composition, text measurement, safe-zone review, semantic motion, localization, and reduced-motion thinking.

## 4. Renderer pluralism

**Observed gap:** Skills tend to overfit FFmpeg or Remotion.

**Contribution:** FFmpeg baseline plus isolated slots for PIL, HyperFrames, Motion Canvas, Manim, Blender, Remotion, MoviePy, PyAV, or future adapters. The manifest refers to rendered assets, not renderer implementation details.

## 5. Editing breadth

**Observed gap:** Slideshow tools, shorts tools, and talking-head tools are separate.

**Contribution:** Explicit routing for montage, dialogue/multi-take, typography, motion, audio, conform, interchange, and QA under one project model.

## 6. Interchange and escape hatch

**Observed gap:** Generated workflows can trap a project in code.

**Contribution:** CMX3600 and OTIO exports, media maps, handoff notes, and documented loss boundaries for finishing in a nonlinear editor.

## 7. Provenance and licensing

**Observed gap:** Tools and assets are installed or downloaded without a coherent rights model.

**Contribution:** Source lockfile, per-skill source cards, explicit usage classes, immutable source hashes, asset lineage, font caution, platform review dates, and isolation of copyleft/custom-licensed tools.

## 8. Quality evidence

**Observed gap:** A successful command is mistaken for a successful video.

**Contribution:** Structural probe, duration/stream assertions, contact sheets, cut-boundary views, waveform, caption checks, audio measurement, full watch-through, issue severity, exact-file approval, and capped self-iteration.

## 9. Continuous learning

**Observed gap:** Project lessons remain in chat history or become overgeneralized rules.

**Contribution:** `evolve-video-workflow` separates recurring failures from one-off taste, requires baseline scenarios, updates cross-references, runs tests/evaluation, and documents migration.
