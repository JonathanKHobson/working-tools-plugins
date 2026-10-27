# Upstream and dependency record

Checked 2026-10-19. Runtime acquisition uses npm registry packages; the source repositories were inspected without executing their build scripts.

- Converter: [figitdesign/web-to-figma](https://github.com/figitdesign/web-to-figma), source commit `859efea8d7f8330783c6c4e3e520fd673e877336`, npm `@figit/dom-to-figma@0.2.4`, MIT. Registry integrity `sha512-GAc82UfGueG1xY8m7S7cCrptQWo9m1kx543TpmYbRKD/0VwqCzHFpfvYW1UqLwYfVNidR7793aaCOJgjZi0+sA==`. `runtime/package-lock.json` pins the full selected graph.
- Encoder used for absolute-mode wrapper correction: `@figit/fig-kiwi@0.2.0`, MIT, from the same repository. No replacement conversion engine was implemented.
- Capture/clipboard reference: [dynCode/HTML-to-FIGMA](https://github.com/dynCode/HTML-to-FIGMA), inspected commit `a433b463dbb005df532ea28d34327e3d50aa972b`. Reviewed content/capture.ts, image loading, classification and rename/merge code. Its ClipboardItem-then-rich-copy-event pattern informed the wrapper; no extension is installed and no extension source is bundled.
- Browser/runtime: `playwright@1.64.1`, `esbuild@0.28.2`, exact integrity graph in the lockfile. The default Fontsource CDN loader is replaced with local font resolution. No converter runtime dependencies or downloaded browser are included in the plugin package.
- Optional [divRIOTS clipboard mode](https://docs-code.to.design/clipboard-mode) and [API](https://docs-code.to.design/api/~endpoints) were checked; no hosted conversion or credit use occurred during validation.

The wrapper and diagnostic fixture are newly authored. Upstream library grants remain MIT. No affiliation or endorsement by Figma, Figit or divRIOTS is implied.

## Figit license

MIT License

Copyright (c) 2026 Figit

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
