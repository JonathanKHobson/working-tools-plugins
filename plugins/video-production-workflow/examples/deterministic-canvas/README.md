# Deterministic canvas example

An original, AI-assisted silent twelve-second canvas scene with a keyboard-seekable preview and an exact-frame browser renderer. It is MIT licensed under this package. No rendered proof or private authoring transcript is included.

Serve this directory with a local HTTP server to inspect `preview.html`. The preview explicitly requests locally installed Arial and reports font-load failure. To render, set `PLAYWRIGHT_MODULE` to an existing reviewed Playwright `index.mjs`, `FFMPEG` and `FFPROBE` to installed executables, then run `node render.mjs /absolute/path/to/new-output-directory`. The output directory must not exist. The command owns and closes its browser, server and encoder.

Playwright/Chromium, Node and Arial are separate dependencies, excluded from this distribution. This example was not browser-rendered during the public release check. Its repeated/shuffled-frame checks support same-environment determinism; they do not certify cross-platform fonts, visual craft or audio.
