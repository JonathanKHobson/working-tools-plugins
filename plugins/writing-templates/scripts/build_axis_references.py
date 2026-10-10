#!/usr/bin/env python3
"""Validate four-axis data, render per-resource references, and copy augmented ZIPs.

The portable operation always writes new archives outside the input directory.
It never runs the historical public projection or changes existing downloads.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / 'library/voice-library'
AXES = ('voice', 'tone', 'style', 'format')
SCHEMA = 'wvl-axes/1'
LEVELS = {1: 'Occasional', 2: 'Supporting', 3: 'Strong', 4: 'Defining'}
AXIS_INSTRUCTION = (
    'After reading the selected complete guide, base guide and routed module guides, '
    'read [the four-axis reference](axes/README.md) and its voice, tone, style and '
    'format pages before drafting. These are editorial descriptions of prominence, '
    'not statistical thresholds. Preserve the guides and user brief as authority, '
    'including task fit, facts, constraints and format requirements. After drafting, '
    'apply the included editorial companion and measured QA workflow; measurements '
    'do not certify meaning or style.'
)


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must be nonempty text')
    if re.search(r'/(?:Users|Volumes)/|file://', value):
        raise ValueError(f'{label} contains a host path')
    return value.strip()


def _relative(value: object, library: Path) -> str:
    path = _text(value, 'evidence path')
    parts = PurePosixPath(path)
    if parts.is_absolute() or '\\' in path or any(p in ('.', '..', '') for p in path.split('/')):
        raise ValueError(f'Unsafe evidence path: {path}')
    target = library / path
    if not target.is_file() or target.is_symlink():
        raise ValueError(f'Missing evidence file: {path}')
    return path


def load_profiles(library: Path = LIBRARY, *, require_complete: bool = True) -> tuple[dict, dict[str, dict]]:
    doc = json.loads((library / 'axes/four-axes.json').read_text(encoding='utf-8'))
    catalog = json.loads((library / 'records/catalog.json').read_text(encoding='utf-8'))
    ids = {row['id'] for row in catalog['records']}
    if doc.get('schemaVersion') != SCHEMA:
        raise ValueError('Unexpected four-axis schema version')
    framework = doc.get('framework')
    if not isinstance(framework, dict):
        raise ValueError('Missing four-axis framework')
    _text(framework.get('title'), 'framework title')
    _text(framework.get('url'), 'framework URL')
    if _text(framework.get('author'), 'framework author') != 'Jonathan Prisant':
        raise ValueError('Framework author attribution is required')
    if _text(framework.get('publisher'), 'framework publisher') != 'Product on Purpose':
        raise ValueError('Framework publisher attribution is required')
    if _text(framework.get('license'), 'framework license') != 'CC BY 4.0':
        raise ValueError('Framework license attribution is required')
    if not _text(framework.get('commitUrl'), 'framework commit URL').startswith('https://'):
        raise ValueError('Framework commit URL must be HTTPS')
    levels = doc.get('levels')
    if not isinstance(levels, list) or len(levels) != 4:
        raise ValueError('Missing levels')
    for number, label in LEVELS.items():
        row = levels[number - 1]
        if not isinstance(row, dict) or row.get('value') != number or row.get('label') != label:
            raise ValueError(f'Invalid level {number}')
        _text(row.get('description'), f'level {number} description')
    axes = doc.get('axes')
    if not isinstance(axes, list) or {a.get('id') for a in axes if isinstance(a, dict)} != set(AXES) or len(axes) != 4:
        raise ValueError('Expected voice, tone, style and format axes')
    for axis in axes:
        _text(axis.get('label'), 'axis label')
        _text(axis.get('question'), 'axis question')
    terms = doc.get('terms')
    if not isinstance(terms, dict) or not terms:
        raise ValueError('Missing axis terms')
    for slug, term in terms.items():
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or not isinstance(term, dict):
            raise ValueError(f'Invalid term: {slug}')
        if _text(term.get('axis'), f'{slug} axis') not in AXES:
            raise ValueError(f'{slug}: unknown axis')
        _text(term.get('label'), f'{slug} label')
        _text(term.get('definition'), f'{slug} definition')
        if 'sourceUrl' in term:
            _text(term['sourceUrl'], f'{slug} sourceUrl')
    profiles = doc.get('profiles')
    if not isinstance(profiles, list) or (require_complete and len(profiles) != len(ids)):
        raise ValueError('One profile per registered resource is required')
    by_id: dict[str, dict] = {}
    for profile in profiles:
        if not isinstance(profile, dict) or profile.get('id') not in ids or profile['id'] in by_id:
            raise ValueError('Invalid or duplicate profile ID')
        ident = profile['id']
        if profile.get('formatPolicy') not in ('fixed', 'task_selected'):
            raise ValueError(f'{ident}: invalid formatPolicy')
        if not isinstance(profile.get('constraints'), list) or any(not isinstance(x, str) or not x.strip() for x in profile['constraints']):
            raise ValueError(f'{ident}: invalid constraints')
        summary = profile.get('summary')
        selections = profile.get('axes')
        if not isinstance(summary, dict) or not isinstance(selections, dict) or set(summary) != set(AXES) or set(selections) != set(AXES):
            raise ValueError(f'{ident}: expected four summaries and selections')
        for axis in AXES:
            _text(summary[axis], f'{ident} {axis} summary')
            if not isinstance(selections[axis], list) or not selections[axis]:
                raise ValueError(f'{ident} {axis}: expected a nonempty list')
            for choice in selections[axis]:
                term_id = choice.get('termId') if isinstance(choice, dict) else None
                if term_id not in terms or choice.get('level') not in LEVELS or isinstance(choice.get('level'), bool):
                    raise ValueError(f'{ident} {axis}: invalid term or level')
                if terms[term_id]['axis'] != axis:
                    raise ValueError(f'{ident} {axis}: term belongs to another axis')
                _text(choice.get('reason'), f'{ident} {axis} reason')
                evidence = choice.get('evidence')
                if not isinstance(evidence, list) or not evidence:
                    raise ValueError(f'{ident} {axis}: evidence required')
                for ref in evidence:
                    if not isinstance(ref, dict):
                        raise ValueError(f'{ident} {axis}: invalid evidence')
                    _relative(ref.get('path'), library)
                    _text(ref.get('section'), f'{ident} {axis} evidence section')
        by_id[ident] = profile
    if require_complete and set(by_id) != ids:
        raise ValueError('Four-axis profiles do not cover the catalog')
    return doc, by_id


def profile_data(doc: dict, profile: dict) -> dict:
    return {
        'schemaVersion': SCHEMA,
        'framework': doc['framework'],
        'levels': doc['levels'],
        'axes': doc['axes'],
        'terms': {term: doc['terms'][term] for axis in AXES for item in profile['axes'][axis] for term in [item['termId']]},
        'profile': profile,
    }


def render_axis(doc: dict, profile: dict, axis: str, *, portable: bool = False) -> str:
    meta = next(item for item in doc['axes'] if item['id'] == axis)
    lines = [f'# {profile["id"]} · {meta["label"]}', '', profile['summary'][axis], '',
             f'**Question:** {meta["question"]}', '',
             'Levels describe editorial prominence in this resource. They are not measured thresholds.', '']
    for item in profile['axes'][axis]:
        term = doc['terms'][item['termId']]
        level = item['level']
        lines += [f'## {term["label"]} · {level} {LEVELS[level]}', '', term['definition'], '',
                  f'**Why it fits:** {item["reason"]}', '', '**Source evidence:**', '']
        if term.get('sourceUrl'):
            lines[-2:-2] = [f'**Term source:** [Reference]({term["sourceUrl"]})', '']
        for ref in item['evidence']:
            path = ref['path']
            if portable:
                lines.append(f'- [{path}](../references/{path}), {ref["section"]}.')
            else:
                lines.append(f'- [{path}](../../../{path}), {ref["section"]}.')
        lines.append('')
    if axis == 'format':
        policy = 'fixed by the guide' if profile['formatPolicy'] == 'fixed' else 'selected for the task and user brief'
        lines += [f'**Format policy:** {policy}.', '']
    lines += ['The complete selected and base guides, routed modules and user brief govern the draft. '
              'Preserve their constraints and run the established editorial and measured QA after drafting.', '']
    return '\n'.join(lines)


def render_readme(doc: dict, profile: dict) -> str:
    ident = profile['id']
    framework = doc['framework']
    lines = [f'# {ident} · Four-axis reading guide', '',
             f'This profile uses [{framework["title"]}]({framework["url"]}) by '
             f'{framework["author"]} / {framework["publisher"]} as an editorial lens. '
             f'The source taxonomy is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) '
             f'and was inspected at [this upstream commit]({framework["commitUrl"]}). '
             'These resource mappings, selections, reasons, evidence and summaries are independently authored local guidance.', '',
             'Read the complete selected guide, base guide and routed module guides first. Then read these four pages before drafting:', '']
    lines += [f'- [{axis.title()}]({axis}.md): {profile["summary"][axis]}' for axis in AXES]
    lines += ['', 'Levels 1–4 describe editorial prominence, not statistical thresholds. '
              'The guides and user brief retain authority over fit, facts, format, exceptions and constraints.', '']
    if profile['constraints']:
        lines += ['## Constraints to preserve', ''] + [f'- {item}' for item in profile['constraints']] + ['']
    lines += ['After drafting, apply the editorial companion and measured QA. Numeric observations describe samples; '
              'they do not establish a style acceptance limit or certify meaning.', '']
    return '\n'.join(lines)


def render_files(doc: dict, profile: dict, *, portable: bool = False) -> dict[str, str]:
    files = {'README.md': render_readme(doc, profile),
             'profile.json': json.dumps(profile_data(doc, profile), ensure_ascii=False, indent=2) + '\n'}
    files.update({f'{axis}.md': render_axis(doc, profile, axis, portable=portable) for axis in AXES})
    return files


def write_references(library: Path = LIBRARY, *, check: bool = False) -> int:
    doc, profiles = load_profiles(library)
    stale = []
    for ident, profile in profiles.items():
        for name, content in render_files(doc, profile).items():
            path = library / 'styles' / ident / 'axes' / name
            if check:
                if not path.is_file() or path.read_text(encoding='utf-8') != content:
                    stale.append(str(path.relative_to(library)))
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding='utf-8')
    if stale:
        raise ValueError('Stale four-axis references: ' + ', '.join(stale[:8]))
    if not check and library.resolve() == LIBRARY.resolve():
        pin_path = ROOT / 'runtime/writing-voice-library/approved-sources.json'
        pins = json.loads(pin_path.read_text(encoding='utf-8'))
        pins['axesSha256'] = hashlib.sha256((library / 'axes/four-axes.json').read_bytes()).hexdigest()
        for ident in profiles:
            for name in ('README.md', 'profile.json', *(f'{axis}.md' for axis in AXES)):
                rel = f'styles/{ident}/axes/{name}'
                pins['files'][rel] = hashlib.sha256((library / rel).read_bytes()).hexdigest()
        pin_path.write_text(json.dumps(pins, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return len(profiles)


def augment_archive(raw: bytes, doc: dict, profile: dict, library: Path = LIBRARY) -> bytes:
    with zipfile.ZipFile(io.BytesIO(raw)) as src:
        members = src.namelist()
        roots = {PurePosixPath(name).parts[0] for name in members if name}
        if len(roots) != 1:
            raise ValueError('Portable archive must have one root')
        root = roots.pop()
        files = {}
        for name in members:
            parts = PurePosixPath(name)
            if name.endswith('/'):
                continue
            if parts.is_absolute() or '..' in parts.parts or '\\' in name or not name.startswith(root + '/'):
                raise ValueError('Unsafe ZIP member')
            files[name] = src.read(name)
    skill_path = root + '/SKILL.md'
    style_path = root + '/STYLE.md'
    manifest_path = root + '/agent-manifest.json'
    if skill_path not in files or style_path not in files or manifest_path not in files:
        raise ValueError('Portable archive lacks skill, STYLE.md or manifest')
    manifest = json.loads(files[manifest_path])
    if manifest.get('resourceId') != profile['id']:
        raise ValueError('Archive resource ID does not match profile')
    skill = files[skill_path].decode('utf-8')
    marker = '## Four-axis guidance'
    if marker not in skill:
        skill += '\n\n' + marker + '\n\n' + AXIS_INSTRUCTION + '\n'
    files[skill_path] = skill.encode('utf-8')
    style = files[style_path].decode('utf-8')
    link = '- [Four-axis editorial reference](axes/README.md)\n'
    if link not in style:
        marker = '## Read before drafting\n\n'
        if marker in style:
            style = style.replace(marker, marker + link, 1)
        else:
            style += '\n\n## Four-axis editorial reference\n\n' + link
    files[style_path] = style.encode('utf-8')
    manifest['axesProfile'] = 'axes/profile.json'
    manifest['axesSchemaVersion'] = SCHEMA
    files[manifest_path] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    full_axes_path = root + '/axes/four-axes.json'
    if full_axes_path in files:
        # The additive P49 source ZIP predates admission and carries a 48-row
        # snapshot. Keep its existing file path but replace that stale snapshot
        # in the new archive with the reviewed current source.
        files[full_axes_path] = (json.dumps(doc, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    for axis in AXES:
        for item in profile['axes'][axis]:
            for ref in item['evidence']:
                path = _relative(ref['path'], library)
                target = root + '/references/' + path
                content = (library / path).read_bytes()
                if target in files and files[target] != content:
                    raise ValueError(f'Portable evidence differs from canonical source: {path}')
                if target not in files:
                    if re.search(rb'/(?:Users|Volumes)/|file://', content):
                        raise ValueError(f'Cannot distribute host path in evidence: {path}')
                    files[target] = content
    for name, content in render_files(doc, profile, portable=True).items():
        files[root + '/axes/' + name] = content.encode('utf-8')
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as dest:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 9, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            dest.writestr(info, content)
    return output.getvalue()


def augment_directory(input_dir: Path, output_dir: Path, library: Path = LIBRARY, *, ids: list[str] | None = None,
                      overrides: dict[str, Path] | None = None) -> int:
    if input_dir.resolve() == output_dir.resolve() or input_dir.resolve() in output_dir.resolve().parents:
        raise ValueError('Output must be outside the existing downloads directory')
    doc, profiles = load_profiles(library, require_complete=ids is None)
    selected = ids if ids is not None else list(profiles)
    if not selected or len(selected) != len(set(selected)) or any(ident not in profiles for ident in selected):
        raise ValueError('Requested IDs must be distinct profiles in four-axes.json')
    overrides = overrides or {}
    if set(overrides) - set(selected):
        raise ValueError('Archive override ID must be selected')
    sources = {}
    for ident in selected:
        source = overrides.get(ident)
        if source is None:
            nested = input_dir / ident / 'bundle.zip'
            flat = input_dir / f'writing-resource-{ident.lower()}.zip'
            source = nested if nested.is_file() else flat
        target = output_dir / f'writing-resource-{ident.lower()}-axes-v1.zip'
        if not source.is_file():
            raise ValueError(f'Missing existing portable archive: {source}')
        if target.exists():
            raise ValueError(f'Refusing to overwrite staged archive: {target}')
        sources[ident] = source
    output_dir.mkdir(parents=True, exist_ok=True)
    for ident in selected:
        profile = profiles[ident]
        source = sources[ident]
        target = output_dir / f'writing-resource-{ident.lower()}-axes-v1.zip'
        target.write_bytes(augment_archive(source.read_bytes(), doc, profile))
    return len(selected)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--library', type=Path, default=LIBRARY)
    parser.add_argument('--check', action='store_true', help='Check generated library references')
    parser.add_argument('--write', action='store_true', help='Write generated library references')
    parser.add_argument('--zip-input-dir', type=Path, help='Existing public downloads directory containing {ID}/bundle.zip')
    parser.add_argument('--zip-output-dir', type=Path, help='Separate directory for new versioned archives')
    parser.add_argument('--ids', help='Comma-separated subset of IDs for staging while another profile is still authored')
    parser.add_argument('--zip-override', action='append', default=[], metavar='ID=PATH',
                        help='Use a specific existing archive for one ID, such as an additive P49 bundle')
    args = parser.parse_args()
    if args.check == args.write and not args.zip_input_dir:
        parser.error('Choose --check, --write, or a ZIP input/output pair')
    if bool(args.zip_input_dir) != bool(args.zip_output_dir):
        parser.error('--zip-input-dir and --zip-output-dir must be used together')
    if args.ids and not args.zip_input_dir:
        parser.error('--ids requires the ZIP input/output pair')
    if args.zip_override and not args.zip_input_dir:
        parser.error('--zip-override requires the ZIP input/output pair')
    if args.write or args.check:
        count = write_references(args.library, check=args.check)
        print(f'{count} four-axis reference sets ' + ('verified' if args.check else 'written'))
    if args.zip_input_dir:
        ids = args.ids.split(',') if args.ids else None
        overrides = {}
        for value in args.zip_override:
            ident, separator, path = value.partition('=')
            if not separator or not ident or not path:
                parser.error('--zip-override must be ID=PATH')
            overrides[ident] = Path(path)
        count = augment_directory(args.zip_input_dir, args.zip_output_dir, args.library, ids=ids,
                                  overrides=overrides)
        print(f'{count} new portable archives staged in {args.zip_output_dir}')


if __name__ == '__main__':
    main()
