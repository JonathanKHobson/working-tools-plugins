#!/usr/bin/env python3
"""Offline checker for this package's deliberately simple metadata format.

Uses only Python's standard library. It is not a general YAML parser, Codex
compatibility certification, link-availability checker, or live Figma evaluator.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

NAME = 'figma-ui-operator'
REQUIRED = (
    'SKILL.md', 'agents/openai.yaml', 'references/runtime.md',
    'references/stitch-to-figma.md', 'references/import-and-presentation.md',
    'references/design-direction.md', 'docs/project-map.md',
    'references/interface-map.md', 'references/action-loop.md',
    'references/create-and-edit.md', 'references/auto-layout.md',
    'references/components-and-variables.md', 'references/prototypes.md',
    'references/collaboration-and-export.md', 'references/recovery.md',
    'references/shortcuts.md', 'references/recipes.md',
    'references/acceptance-tests.md', 'references/sources.md',
    'references/sources.json', 'evals/evals.json',
    'assets/session-template.md', 'assets/ui-calibration-template.md',
    'assets/eval-result-template.json', 'scripts/validate_skill.py',
)
LINK = re.compile(r'\[[^\]\n]*\]\(([^)\n]+)\)')


def files_for_install(root: Path) -> list[Path]:
    """Return ordinary source files; generated Python cache files are excluded."""
    return sorted(p for p in root.rglob('*')
                  if '__pycache__' not in p.relative_to(root).parts
                  and p.suffix != '.pyc' and p.is_file())


def _plain_frontmatter(text: str) -> dict[str, str]:
    """Read the two one-line scalar keys used here; reject ambiguous YAML."""
    lines = text.splitlines()
    if not lines or lines[0] != '---':
        raise ValueError('SKILL.md must start with YAML frontmatter')
    try:
        end = lines.index('---', 1)
    except ValueError as exc:
        raise ValueError('frontmatter has no closing delimiter') from exc
    result: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        match = re.fullmatch(r'(name|description):\s*(.*)', line)
        if not match or match.group(1) in result:
            raise ValueError('expected unique, single-line name and description keys')
        key, value = match.groups()
        if value.startswith('"'):
            value = json.loads(value)
        elif value.startswith("'") or value.startswith(('|', '>')):
            raise ValueError('checker supports plain or double-quoted one-line scalars')
        if not isinstance(value, str):
            raise ValueError(f'{key} must be a string')
        result[key] = value.strip()
    return result


def validate(root: Path) -> list[str]:
    """Return human-readable errors, or an empty list for a valid package."""
    root = Path(root)
    errors: list[str] = []
    if root.is_symlink():
        return ['source skill directory must not be a symlink']
    if not root.is_dir():
        return [f'skill directory does not exist: {root}']
    if root.name != NAME:
        errors.append(f'skill directory must be named {NAME}')
    for p in root.rglob('*'):
        if p.is_symlink():
            errors.append(f'symlink rejected: {p.relative_to(root)}')
        elif not (p.is_dir() or p.is_file()):
            errors.append(f'non-regular file rejected: {p.relative_to(root)}')
    if any('rejected:' in e for e in errors):
        return errors  # Never follow a source link to inspect private content.
    for rel in REQUIRED:
        if not (root / rel).is_file():
            errors.append(f'missing required file: {rel}')
    if errors:
        return errors
    try:
        text = (root / 'SKILL.md').read_text(encoding='utf-8')
        meta = _plain_frontmatter(text)
        if meta.get('name') != NAME:
            errors.append(f'frontmatter name must be {NAME}')
        description = meta.get('description', '')
        if not 1 <= len(description) <= 1024:
            errors.append('description must contain 1–1024 characters')
        if description and not description.startswith('Use when'):
            errors.append('description should start with Use when')
        if len(text.split()) > 900:
            errors.append('entry point exceeds the portable package budget of 900 words')
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(f'frontmatter: {exc}')
    try:
        agent = (root / 'agents/openai.yaml').read_text(encoding='utf-8')
        for key in ('display_name', 'short_description', 'default_prompt'):
            match = re.search(rf'^  {key}:\s*(".*")\s*$', agent, re.M)
            value = json.loads(match.group(1)) if match else None
            if not isinstance(value, str) or not value.strip():
                errors.append(f'agent metadata requires a quoted {key}')
        if '$figma-ui-operator' not in agent:
            errors.append('default prompt must explicitly name the skill')
        if re.search(r'^\s*model\s*:', agent, re.M):
            errors.append('do not hardcode a model in agent metadata')
        if '  allow_implicit_invocation: true' not in agent:
            errors.append('implicit invocation policy missing or unexpected')
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(f'agent metadata: {exc}')
    root_resolved = root.resolve()
    plugin_root = root.parent.parent.resolve()
    # Four heads intentionally share complete guides and a package README.
    # Permit only the enclosing declared plugin, never arbitrary ancestors.
    manifest = plugin_root / '.codex-plugin/plugin.json'
    if manifest.is_file():
        metadata = json.loads(manifest.read_text(encoding='utf-8'))
        if metadata.get('name') == 'figma-design-workflow' and metadata.get('skills') == './skills/':
            root_resolved = plugin_root
    for doc in root.rglob('*.md'):
        try:
            for raw in LINK.findall(doc.read_text(encoding='utf-8')):
                target = raw.strip().strip('<>')
                parsed = urlsplit(target)
                if parsed.scheme or target.startswith(('#', '//')):
                    continue
                path = unquote(parsed.path)
                if not path:
                    continue
                resolved = (doc.parent / path).resolve()
                if not resolved.is_relative_to(root_resolved):
                    errors.append(f'link escapes declared package: {doc.relative_to(root)} -> {target}')
                elif not resolved.exists():
                    errors.append(f'broken internal file link: {doc.relative_to(root)} -> {target}')
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f'cannot check {doc.relative_to(root)}: {exc}')
    try:
        data = json.loads((root / 'evals/evals.json').read_text(encoding='utf-8'))
        scenarios = data.get('scenarios', [])
        if not isinstance(scenarios, list) or len(scenarios) < 12:
            errors.append('evaluation set must include at least 12 scenarios')
        seen: set[str] = set()
        for item in scenarios if isinstance(scenarios, list) else []:
            if not isinstance(item, dict):
                errors.append('scenario must be an object'); continue
            ident = item.get('id')
            if not isinstance(ident, str) or not ident or ident in seen:
                errors.append('scenario IDs must be nonempty and unique')
            if isinstance(ident, str):
                seen.add(ident)
            for key in ('fixture', 'prompt'):
                if not isinstance(item.get(key), str) or not item[key].strip():
                    errors.append(f'{ident}: nonempty {key} required')
            for key in ('must_do', 'must_not_do'):
                value = item.get(key)
                if not isinstance(value, list) or not value or not all(isinstance(v, str) and v for v in value):
                    errors.append(f'{ident}: {key} must be a nonempty list of strings')
            if item.get('category') not in {'positive', 'negative', 'blocked', 'recovery', 'adversarial'}:
                errors.append(f'{ident}: unexpected category')
            if item.get('status') != 'not_run':
                errors.append(f'{ident}: keep fixture status not_run; record results separately')
    except (OSError, UnicodeError, ValueError, AttributeError) as exc:
        errors.append(f'evaluation JSON: {exc}')
    try:
        ledger = json.loads((root / 'references/sources.json').read_text(encoding='utf-8'))
        sources = ledger.get('sources', [])
        ids = [s.get('id') for s in sources]
        if len(ids) != len(set(ids)) or len(sources) < 20:
            errors.append('source ledger must contain unique IDs and at least 20 entries')
        for source in sources:
            host = urlsplit(source.get('url', '')).hostname
            if host not in {'learn.chatgpt.com', 'help.figma.com', 'www.youtube.com'}:
                errors.append(f'unexpected source host: {host}')
        for doc in (root / 'references').glob('*.md'):
            for sid in re.findall(r'\[(S\d{2})\]', doc.read_text(encoding='utf-8')):
                if sid not in ids:
                    errors.append(f'unknown source {sid} in {doc.name}')
    except (OSError, UnicodeError, ValueError, AttributeError, TypeError) as exc:
        errors.append(f'source ledger: {exc}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('skill_dir', nargs='?', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json', action='store_true', help='Print a machine-readable report.')
    args = parser.parse_args()
    errors = validate(args.skill_dir)
    report = {'valid': not errors, 'skill': NAME, 'errors': errors,
              'scope': 'offline package structure only; GUI and agent behavior not tested'}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print('VALID' if not errors else 'INVALID')
        for error in errors:
            print(f'- {error}')
        print(report['scope'])
    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(main())
