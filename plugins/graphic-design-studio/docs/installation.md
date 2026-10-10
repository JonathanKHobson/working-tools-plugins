# Install Graphic Design Studio

Install this package using the [public platform guide](https://github.com/JonathanKHobson/working-tools-plugins/blob/main/docs/install.md). Skill instructions work without a Python environment. For the actual local MCP, use Python 3.10 or newer to create `.runtime/venv` under this package, then install `requirements.txt`. The manifest command `python3` only bootstraps the launcher; it can be an older host Python. For an external environment, set `IMAGE_WORKFLOWS_PYTHON` to its absolute interpreter path. The launcher preserves venv executable symlinks and never installs dependencies. When no package runtime or `IMAGE_WORKFLOWS_PYTHON` is selected, it can reuse the current user’s existing `~/.config/studio-tools/design-library.json` interpreter binding; that binding is never distributed.

```sh
python3.12 -m venv .runtime/venv
.runtime/venv/bin/python -m pip install -r requirements.txt
```

Install public `design-templates`. When packages are sibling folders, the chooser is detected. Otherwise set `DESIGN_TEMPLATES_ROOT` to the installed Design Templates package root in your host's MCP environment. Search, read and prepare work independently; the app resource and `--export-html` need that four-file chooser. The server does not install, configure or mutate the other package.

For PDF mechanics, install `requirements-preflight.txt` in an explicitly selected environment. PyMuPDF carries AGPL/commercial terms, separately from these scripts; review those terms for your own usage. Pillow and zxing-cpp are needed only for requested QR decoding. Use the preflight CLI with an explicitly supplied PDF and report/render destinations. It does not modify the input PDF. The Iconify helper requires only Python standard library and makes explicit public GET requests; individual icon collection rights must be inspected.

Portable plugin/mcp manifests and native Codex/Claude identities are bundled. Windows may require replacing the bootstrap command with the installed Python command; the launcher recognizes a local Windows venv. Native installation/discovery and MCP App host messaging require separate host acceptance; subprocess and standalone preview checks do not establish them.
