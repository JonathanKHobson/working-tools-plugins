# Video Project Manifest Reference

A batch of finished course, workshop or Short deliverables uses the separate local
[delivery preflight contract](../skills/conform-video-delivery/references/delivery-preflight.md).
This keeps final artifact/review hashes separate from editorial timeline semantics;
existing project and course-package manifests remain compatible.

The manifest is a renderer-neutral editorial contract. The JSON Schema is `schemas/video-project.schema.json`.

## Top-level sections

- `version`: schema version.
- `project`: ID, title, intent, audience, status.
- `delivery`: dimensions, frame rate, aspect, codec, pixel format, color, container, and optional platform.
- `style`: palette, font, asymmetric safe area, reading model, copy constraints, motion intensity, and optional tokens.
- `assets`: stable IDs to paths, types, hashes, rights, metadata, subject anchors.
- `timeline`: output-timeline items with source ranges, duration, layout, text, motion, transition, and reasoning.
- `audio`: voiceover/music/stems, gains, timing, ducking, loudness policy.
- `captions`: source, format, burn-in/sidecar policy, style.
- `render`: quality, cache, renderer/slot settings.
- `qa`: required checks and approved exceptions.
- `provenance`: source and decision lineage.

## Editorial constraints

- `style.safe_area` supports independent left, right, top, and bottom percentages plus platform, review date, and source.
- `style.reading` controls words-per-second and minimum text hold checks.
- `style.copy_constraints.disallowed_characters` records project-specific punctuation or character restrictions.
- `qa.max_asset_uses_per_video` enables a within-video source-reuse ceiling.
- `qa.minimum_cta_hold_s` applies to timeline items with `role: "cta"`.
- Trimmed music uses `audio.music.start`, `end`, and `boundary_review`.
- Timeline text supports `text_align`, `text_position`, and `text_max_width_px`.

## Timeline coordinates

`start` and `duration` describe the output timeline. `source_start` and optional `source_duration` describe source media. Transition overlap must be reflected in output starts. Caption words from source clips must be remapped into output time.

## Asset references

Use stable IDs. Relative paths resolve from the manifest directory. Do not store secrets. External/generated assets should include rights, source URL/provider/model, prompt/record, hash, and parent lineage.
