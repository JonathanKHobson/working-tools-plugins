# Deterministic canvas example

A silent 12-second explanation of reference → storyboard → render. Use it to learn the exact-frame contract or start a small canvas animation, not as a required visual style. `scene.mjs` exports beat data, state-at-frame and drawing; `preview.html` adds a paused, keyboard-seekable player; `render.mjs` checks repeated/out-of-order frames and captures an MP4 with explicit local dependencies.

The original scene was AI-assisted and then locally reviewed and corrected. The private authoring exchange is retained in the author's archive rather than distributed. Integration replaced an unverified font stack with an explicitly loaded local Arial face, reset the owned canvas to clear inherited clips, and raised future-step label contrast. The module intentionally owns and resets its canvas context; it does not preserve arbitrary caller state. It produces no audio and makes no external requests. Prior MIT permissions remain in the package's prior-grant record; current first-party file scope is stated in `LICENSE-SCOPE.json`.

## Run

Serve this directory with an existing local HTTP server to inspect `preview.html`. The preview requires local Arial; font-load failure is visible. It never silently substitutes a face. The renderer uses the same page and blocks requests outside its own loopback server.

Set `PLAYWRIGHT_MODULE` to an absolute existing reviewed Playwright `index.mjs`, `FFMPEG` and `FFPROBE` to absolute installed executable paths, then run:

```sh
node render.mjs /absolute/path/to/new-output-directory
```

The output directory must not exist. No dependency installation is performed. The command owns and closes its headless browser, loopback server and encoder. It renders frames 0–287 at 24 fps into `preview.mp4`, saves selected PNG frames and `checks.json`, then probes and fully decodes the result. A 60-fps delivery would need the wrapper/export settings changed together; `sceneAt` itself is tested at 24, 25, 30 and 60 fps.

Checks include shuffled repeated-frame equality, prior clip/transform/alpha contamination, reduced-motion export parity, text width, boundary validation, frame count and duration. Equality covers PNG pixel output within one browser environment, not cross-platform fonts or byte-identical video encoders. Color tags are declared Rec.709 for the MP4; this example has no calibrated color-pipeline acceptance. Independent rendered and temporal review remains required. The example is not evidence that the retained Animate or HyperFrames runtimes execute successfully.
