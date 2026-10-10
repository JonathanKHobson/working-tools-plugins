#!/usr/bin/env python3
"""Build an allowlisted public plugin, sharing references and QA across catalog templates."""
import argparse
from collections import Counter
import hashlib
import json
import re
from pathlib import Path
from build_voice_public import zip_bytes, safe_check
from build_style_entries import entries as style_entries

ROOT = Path(__file__).resolve().parents[1]


def catalog_type_summary(rows):
    labels = (
        ('legacy_profile', 'retained profile', 'retained profiles'),
        ('voice_candidate', 'voice candidate', 'voice candidates'),
        ('module', 'module', 'modules'),
        ('alias', 'alias', 'aliases'),
        ('merge', 'merged extension', 'merged extensions'),
    )
    counts = Counter(row['resource_type'] for row in rows)
    if set(counts) != {kind for kind, _, _ in labels}:
        raise ValueError('Unexpected resource types in catalog')
    parts = [f'{counts[kind]} {single if counts[kind] == 1 else plural}'
             for kind, single, plural in labels]
    return ', '.join(parts[:-1]) + ' and ' + parts[-1]


def build():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    for ident, expected in style_entries(ROOT / 'library/voice-library'):
        if (ROOT / 'library/voice-library/styles' / ident / 'STYLE.md').read_text() != expected:
            raise ValueError('Stale STYLE.md ' + ident)
    from build_axis_references import write_references
    template_count = write_references(ROOT / 'library/voice-library', check=True)
    catalog = json.loads((ROOT / 'library/voice-library/records/catalog.json').read_text())
    if catalog['record_count'] != template_count or len(catalog['records']) != template_count:
        raise ValueError('Catalog count does not match checked template references')
    type_summary = catalog_type_summary(catalog['records'])
    files = {}
    # Deliberate allowlist: never ship the private Writing Quality Studio owner,
    # original import archive, host config, caches, tests or research attachments.
    for directory in ('library/voice-library', 'runtime/writing-voice-library'):
        for path in sorted((ROOT / directory).rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts and not path.name.startswith('.'):
                text = path.read_text(encoding='utf-8')
                safe_check(text)
                files[path.relative_to(ROOT).as_posix()] = text
    for rel in ('scripts/writing_voice_library_mcp.py', 'skills/writing-templates/SKILL.md'):
        files[rel] = (ROOT / rel).read_text()
    files['skills/writing-templates/SKILL.md'] = re.sub(
        r'\n<!-- BEGIN PROFESSIONAL-AGENTS -->[\s\S]*?<!-- END PROFESSIONAL-AGENTS -->\n?',
        '\n', files['skills/writing-templates/SKILL.md'])
    for path in sorted((ROOT / 'templates').glob('*/SKILL.md')):
        files[path.relative_to(ROOT).as_posix()] = path.read_text()
    for rel in ('docs/writing-voice-library-app.md', 'references/library-search.md'):
        path = ROOT / rel
        if path.exists():
            files[rel] = path.read_text()
    files['requirements.txt'] = 'mcp==1.27.0\n'
    manifest = {
        'name': 'writing-templates',
        'version': json.loads((ROOT / '.codex-plugin/plugin.json').read_text())['version'],
        'description': f'Choose from {template_count} writing templates with complete guides, four-axis references, examples, Humanizer Light and offline draft QA.',
        'author': {'name': 'Kyle Hobson'}, 'skills': './skills/',
        'mcpServers': './.mcp.codex.json',
        'interface': {'displayName': 'Writing Templates', 'shortDescription': 'Choose a voice. Load one template. Check the draft.'}}
    files['.codex-plugin/plugin.json'] = json.dumps(manifest, indent=2) + '\n'
    marketplace = {'name': 'writing-templates', 'interface': {'displayName': 'Writing Templates'},
                   'plugins': [{'name': 'writing-templates', 'source': {'source': 'local', 'path': './'},
                                'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'},
                                'category': 'Productivity'}]}
    files['.agents/plugins/marketplace.json'] = json.dumps(marketplace, indent=2) + '\n'
    claude = {k: manifest[k] for k in ('name', 'version', 'description', 'author', 'skills')}
    claude['mcpServers'] = './.mcp.claude.json'
    files['.claude-plugin/plugin.json'] = json.dumps(claude, indent=2) + '\n'
    server = {'command': 'python3', 'args': ['scripts/writing_voice_library_mcp.py'],
              'cwd': '.', 'env': {'PYTHONDONTWRITEBYTECODE': '1'}}
    files['.mcp.codex.json'] = json.dumps({'mcpServers': {'writing-voice-library': server}}, indent=2) + '\n'
    server = {'command': 'python3', 'args': ['${CLAUDE_PLUGIN_ROOT}/scripts/writing_voice_library_mcp.py'],
              'env': {'PYTHONDONTWRITEBYTECODE': '1'}}
    files['.mcp.claude.json'] = json.dumps({'mcpServers': {'writing-voice-library': server}}, indent=2) + '\n'
    files['SKILL.md'] = '''---
name: writing-templates
description: "Select and apply a writing template, with four-axis references, examples, an editorial pass and draft QA."
---

# Writing Templates

Read the [selector](skills/writing-templates/SKILL.md), then load the selected `library/voice-library/styles/{ID}/STYLE.md`, complete guide, routed base/module guides, four-axis references and relevant examples. Keep this entire folder together when installing it as a regular skill. Plugin hosts discover the single selector under `skills/`; the individual template references stay outside skill discovery.
'''
    files['README.md'] = f'''# Writing Templates

{template_count} writing templates in one package. Choose a template by purpose or name, load its STYLE.md entry, complete selected/base and routed module guides, then its four-axis references and relevant examples. Draft with your own facts, apply Humanizer Light, then run draft QA. The STYLE.md entry is a generated, source-linked digest; the complete guide remains the specification. Four-axis levels describe editorial prominence, not statistical thresholds. One discovered skill loads only the selected template's material.

## Start here

- **Codex:** run `codex plugin marketplace add /absolute/path/to/writing-templates`, then `codex plugin add writing-templates@writing-templates`. Replace the path with the extracted folder. The included local marketplace exposes only this plugin. Start a fresh chat to use the installed entrypoint and tools.
- **Claude Code:** load the extracted folder with `claude --plugin-dir /absolute/path/to/writing-templates`, or use your existing plugin marketplace workflow. The Claude manifest is `.claude-plugin/plugin.json`.
- **Skill or file-based assistants:** keep the complete folder together and use the root `SKILL.md`. Attach the ZIP or selected guide and references in hosts that support files. File attachment does not install a native plugin or provide an executable runtime.

Try “Use Writing Templates to find a voice for a clear recommendation,” or “Apply V19 to these facts.” Ordinary editing and personal-voice work can stay in Writing Quality Studio; that separate plugin is not required here.

## Optional searchable picker

The package includes `browse_writing_voice_library`, `prepare_writing_voice_handoff` and a gallery resource. MCP Apps-capable hosts can display the picker; other hosts can use the same tools or the local catalog. The tools search names, descriptions, tags and mechanisms before loading a selection. They do not scan or activate {template_count} skill heads.

The MCP server needs Python 3.10+ with `mcp==1.27.0` installed in its runtime. Use your normal environment setup, for example `python3 -m pip install -r requirements.txt` in a dedicated environment, and set `WRITING_TEMPLATES_PYTHON` to its interpreter if needed. Startup never downloads dependencies. An existing local Studio runtime binding may be reused. Missing MCP support does not block reading and applying the templates.

## Included checks

Every selection references `library/voice-library/validation/editorial-companion.md` and its own QA profile. Run `python3 library/voice-library/validation/validate.py --input draft.md --profile library/voice-library/validation/profiles/V19.json` from the extracted root; substitute the selected ID. The original measurement engine requires **Node 20+**; Python is an optional launcher. The pinned Markdown parser is bundled. No network is used by draft validation.

Humanizer Light checks stock framing, unsupported claims and empty repetition while preserving intentional punctuation, fragments, cadence and structure. The full **Humanizer Deep Audit** is an optional companion when separately installed through Writing Quality Studio. Its private source corpus is not included here.

## Package and source boundaries

The library contains {type_summary}. All {template_count} IDs keep their actual base/module routes. The package includes current demonstrations, attributed historical readings, detailed style specifications, four-axis editorial references, separate APA/MLA format references, numeric QA profiles and the original measurement method. Historical readings illustrate techniques; they are not generated-output validation runs.

Follow the selected guide's constraints and the supplied brief. Do not widen a constraint to make a draft pass. Observed sample measurements remain descriptive unless a reviewed acceptance limit is explicitly supplied. A successful script exit does not replace review of meaning or style.

Only generic library material is distributed. Original library guidance and demonstrations are supplied for reuse in writing workflows. External excerpts, linked authorities and the Markdown parser retain their source-specific rights, credits and notices. See `library/voice-library/source-edition/` and `library/voice-library/validation/vendor/marked/LICENSE.md`. No private personal voice samples, credentials or full Humanizer research archive are included. This ZIP is a download, not an installation or a promise that every host supports plugins, MCP Apps or scripts.
'''
    # Verify local Markdown links inside the public package (ordinary inline links).
    import posixpath
    broken = []
    for name, text in files.items():
        safe_check(text)
        if not name.endswith('.md'):
            continue
        for link in re.findall(r'\]\(([^\n)]+)\)', text):
            link = link.strip('<>').split('#')[0]
            if link and ':' not in link:
                target = posixpath.normpath(posixpath.join(posixpath.dirname(name), link))
                if target not in files and not any(p.startswith(target.rstrip('/') + '/') for p in files):
                    broken.append((name, link))
    # Provenance/research records may point outside the minimal executable package;
    # active entrypoints and operational references must be closed.
    active_broken = [x for x in broken if x[0].startswith(('skills/', 'templates/')) or x[0] == 'SKILL.md']
    if active_broken:
        raise ValueError('Broken active package links: ' + repr(active_broken))
    archive = zip_bytes({'writing-templates/' + p: text for p, text in files.items()})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(archive)
    evidence = {'schema': 'writing-templates-distribution/1', 'templates': template_count, 'discoveredSkills': 1,
                'bytes': len(archive), 'sha256': hashlib.sha256(archive).hexdigest(),
                'files': {p: hashlib.sha256(text.encode()).hexdigest() for p, text in files.items()},
                'historicalReferenceLinksOutsidePackage': broken}
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps({k: evidence[k] for k in ('templates', 'discoveredSkills', 'bytes', 'sha256')}))


if __name__ == '__main__':
    build()
