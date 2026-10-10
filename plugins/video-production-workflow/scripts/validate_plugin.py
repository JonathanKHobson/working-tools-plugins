#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
errors = []
manifest_path = root / '.codex-plugin' / 'plugin.json'
try:
    manifest = json.loads(manifest_path.read_text())
except Exception as exc:
    raise SystemExit(f'Invalid plugin manifest: {exc}')
if manifest.get('name') != root.name:
    errors.append(f"plugin name {manifest.get('name')!r} does not match folder {root.name!r}")
skills_root = root / 'skills'
if not skills_root.is_dir():
    errors.append('missing skills directory')
else:
    for skill in sorted(skills_root.iterdir()):
        if not skill.is_dir():
            continue
        required = [skill / 'SKILL.md', skill / 'agents' / 'openai.yaml', skill / 'references' / 'sources' / 'source-index.md']
        for path in required:
            if not path.exists():
                errors.append(f'missing {path.relative_to(root)}')
        text = (skill / 'SKILL.md').read_text() if (skill / 'SKILL.md').exists() else ''
        if not text.startswith('---\nname:'):
            errors.append(f'invalid frontmatter in {skill.name}')
if errors:
    print('\n'.join(f'ERROR: {e}' for e in errors))
    raise SystemExit(2)
print(f'Validated {len([p for p in skills_root.iterdir() if p.is_dir()])} skill directories and plugin manifest.')
