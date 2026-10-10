# Optional Renderer Adapters

The core plugin renders with FFmpeg. These folders define isolated integration boundaries for specialist engines; they are not installed automatically.

- `ffmpeg/` — baseline full-project adapter.
- `hyperframes/` — browser-native HTML/CSS/JS slots.
- `motion-canvas/` — TypeScript explanatory animation.
- `manim/` — Python mathematical/diagram animation.
- `blender/` — 3D/VFX/compositing/VSE slots.
- `remotion/` — React video slots; current license review required.

Each adapter should consume `schemas/animation-slot.schema.json` or the shared project manifest, write a normalized media file, and emit a render log/probe/contact sheet.
