# Educational Canvas motion template

A local, dependency-light, asset-configured renderer for a silent three-step explanation. The engine contains no project-specific assets or private paths. `project.json` owns the words, colors, image files, checksums, formats and editorial meaning. Each project keeps its own assets beside its JSON.

Run with existing local Node 22, Playwright, FFmpeg and FFprobe. No install, remote request, or package script is used:

```sh
PLAYWRIGHT_MODULE=/absolute/local/playwright/index.mjs FFMPEG=/absolute/local/ffmpeg FFPROBE=/absolute/local/ffprobe node /absolute/generic/render.mjs /absolute/project/project.json /absolute/NEW-output-directory
```

The output directory must not exist. The renderer serves only `preview.html`, `scene.mjs`, `project.json` and named, hash-checked assets from the project. Paths must be relative to the project directory; `..`, symlinks and mismatched SHA-256 values fail before browser launch. The local browser and server close in `finally`.

The `educational-canvas/1` schema currently fixes 12 seconds at 24 fps, three steps and two separately composed formats: 1280 × 720 and 720 × 1280. It accepts two display title parts, three action/why/example/note objects, diagram labels, two takeaway lines, a palette, and logo/character/painted marks through named assets. Each project can replace the teaching text and imagery without changing the renderer; keep phrases near the proof’s lengths and inspect text bounds after editing. All outputs are silent. The frame API is seekable: frame 0–287; phase changes at 0.8, 3.3, 5.8 and 8.3 seconds. The final overview holds from 8.85 seconds to the end. Exports derive every state from the requested frame; preview motion preference affects only preview playback.

`preview.html` begins paused, has Play/Pause, format selection, slider/arrow-key seeking, Space playback, page-hidden pause, and reduced-motion change pause. A static first frame and final overview remain legible without playback. Browser canvas reset clears inherited clip/transform state before every frame.

`checks.json` binds each MP4 to its SHA-256, exact frame count, decoded stream, browser, source and asset hashes. PNG stills and an encoded-video contact sheet support visual review. A human must still inspect continuous playback and the rendered anchor regions before release. Edit the project JSON, create a new output path and rerender; never treat an old hash as approval of changed content.

Keep private project assets and source paths outside redistributed copies of this generic template.

Start from `project.example.json` in a separate project folder. Its asset filenames are placeholders and its zero hashes deliberately fail validation. Supply permitted PNG artwork and local font files, then set each SHA-256 from the exact bytes. The font role keys name the renderer's current face slots; they can point to any permitted font of the supported file type. Replace the example teaching text with a source-backed objective and learner action. This example bundles no brand kit.
