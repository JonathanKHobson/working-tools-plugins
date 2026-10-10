"""Read-only, version-bound Writing Voice Library catalog and handoffs."""
from __future__ import annotations
import hashlib
import json
import re
import stat
import os
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parent
PACKAGE_ROOT = ROOT.parents[1]
DATA_ROOT = Path(os.environ.get('WRITING_TEMPLATES_DATA_ROOT') or PACKAGE_ROOT / 'data/voice-library').expanduser().absolute()
if os.environ.get('WRITING_TEMPLATES_DATA_ROOT') and DATA_ROOT.resolve().is_relative_to(PACKAGE_ROOT):
    raise ValueError('Explicit writing collection must stay outside the installed package')
PUBLIC_BASE = os.environ.get('WRITING_TEMPLATES_PUBLIC_BASE', '')
ID_RE = re.compile(r'(?:V(?:0[1-9]|1[0-9]|2[0-4])|P(?:2[5-9]|[34][0-9]|5[0-3]))\Z')
TYPES = {'legacy_profile', 'voice_candidate', 'module', 'alias', 'merge'}
PUBLIC_FIELDS = ('id', 'name', 'version', 'resource_type', 'description', 'mechanism', 'rhythm', 'tags', 'primary_layer', 'independence_status', 'evidence_status', 'nearest_neighbors', 'neighbor_difference', 'truth_boundary', 'communication_targets', 'task_fit', 'research', 'route', 'skill_name')

class CatalogError(ValueError):
    """An unavailable or unsafe resource cannot be selected."""

def safe_read(root: Path, relative: str) -> bytes:
    """Refuse traversal, symlinks and special files in every relative component."""
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise CatalogError('Resource path is invalid')
    parts = PurePosixPath(relative)
    if parts.is_absolute() or any(p in ('.', '..') for p in relative.split('/')) or '' in relative.split('/'):
        raise CatalogError('Resource path must stay inside the library')
    path = root
    try:
        if not stat.S_ISDIR(root.lstat().st_mode):
            raise CatalogError('Library root must be a real directory')
        for index, part in enumerate(parts.parts):
            path = path / part
            mode = path.lstat().st_mode
            final = index == len(parts.parts) - 1
            if not (stat.S_ISREG(mode) if final else stat.S_ISDIR(mode)):
                raise CatalogError('Resource must be a regular file inside the library')
        path.resolve().relative_to(root.resolve())
        return path.read_bytes()
    except (OSError, ValueError) as exc:
        if isinstance(exc, CatalogError):
            raise
        raise CatalogError('Library resource is missing or unreadable') from exc

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def source_references(ids: list[str], data_root: Path) -> list[dict]:
    expected = approved_sources().get('sourceEditionSha256')
    if not expected:
        return []
    raw = safe_read(data_root, 'source-edition/edition.json')
    if digest(raw) != expected:
        raise CatalogError('Source edition has changed; review it before preparing a handoff')
    edition = json.loads(raw)
    references = []
    paths = dict.fromkeys(path for ident in ids for path in edition['records'][ident]['bundleFiles'])
    for path in paths:
        raw = safe_read(data_root, 'source-edition/' + path)
        if digest(raw) != edition['files'].get(path):
            raise CatalogError('Historical reading or style specification has changed')
        references.append({'path': 'source-edition/' + path, 'sha256': digest(raw), 'text': raw.decode('utf-8')})
    return references

def approved_sources() -> dict:
    try:
        return json.loads(safe_read(DATA_ROOT, 'approved-sources.json'))
    except (OSError, ValueError) as exc:
        raise CatalogError('Approved source manifest is unavailable') from exc

def validation_references(ids: list[str], data_root: Path) -> dict:
    raw = safe_read(data_root, 'validation/manifest.json')
    if digest(raw) != approved_sources().get('validationManifestSha256'):
        raise CatalogError('Draft QA package has changed; review it before a handoff')
    manifest = json.loads(raw)
    paths = manifest['runtimeFiles'] + ['validation/WORKFLOW.md', 'validation/editorial-companion.md'] + [f'validation/profiles/{ident}.json' for ident in ids]
    texts = []
    for path in paths:
        content = safe_read(data_root, path)
        if digest(content) != manifest['files'].get(path):
            raise CatalogError('Draft QA script, method or profile has changed')
        if path.endswith('.json') and '/profiles/' in path or path in ('validation/WORKFLOW.md', 'validation/editorial-companion.md'):
            texts.append({'path': path, 'sha256': digest(content), 'text': content.decode('utf-8')})
    return {'entrypoint': str(data_root / 'validation/validate.py'),
            'alternateEntrypoint': str(data_root / 'validation/validate.cjs'),
            'requires': 'Node >=20; Python >=3 for optional launcher', 'network': False,
            'profiles': ids, 'references': texts, 'manifestSha256': digest(raw)}

def axis_references(ids: list[str], data_root: Path) -> dict:
    """Return reviewed axis metadata and generated pages for the actual route."""
    raw = safe_read(data_root, 'axes/four-axes.json')
    pins = approved_sources()
    if digest(raw) != pins.get('axesSha256'):
        raise CatalogError('Four-axis profile data has changed; review it before preparing a handoff')
    data = json.loads(raw)
    if data.get('schemaVersion') != 'wvl-axes/1':
        raise CatalogError('Four-axis schema is invalid')
    profiles = {p['id']: p for p in data['profiles']}
    references = []
    for ident in ids:
        if ident not in profiles:
            raise CatalogError('Four-axis profile is missing for a routed resource')
        for name in ('README.md', 'voice.md', 'tone.md', 'style.md', 'format.md', 'profile.json'):
            path = f'styles/{ident}/axes/{name}'
            content = safe_read(data_root, path)
            if digest(content) != pins['files'].get(path):
                raise CatalogError('Four-axis reference has changed; reviewed source required')
            references.append({'path': path, 'sha256': digest(content), 'text': content.decode('utf-8')})
    return {'schemaVersion': 'wvl-axes/1', 'framework': data['framework'],
            'levels': data['levels'], 'profiles': [profiles[ident] for ident in ids],
            'references': references}

def load_catalog(data_root: Path = DATA_ROOT) -> list[dict]:
    raw = safe_read(data_root, 'records/catalog.json')
    manifest = approved_sources()
    if digest(raw) != manifest['catalogSha256']:
        raise CatalogError('Catalog has changed; review it before preparing a handoff')
    try:
        document = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise CatalogError('Catalog is invalid') from exc
    records = document.get('records')
    if document.get('schema_version') != 'wvl-catalog/2.0.0' or not isinstance(records, list) or document.get('private_included') is not False:
        raise CatalogError('Catalog schema or privacy boundary is invalid')
    ids = set()
    for record in records:
        if not isinstance(record, dict) or not ID_RE.fullmatch(record.get('id', '')) or record['id'] in ids:
            raise CatalogError('Catalog contains an invalid or duplicate ID')
        ids.add(record['id'])
        if record.get('resource_type') not in TYPES or not isinstance(record.get('version'), str):
            raise CatalogError('Resource type or version is invalid')
        route = record.get('route', {})
        if route.get('selected_resource_id') != record['id'] or not ID_RE.fullmatch(route.get('base_profile_id', '')) or not isinstance(route.get('module_ids'), list):
            raise CatalogError('Catalog route is invalid')
    for record in records:
        route = record['route']
        if route['base_profile_id'] not in ids or any(m not in ids for m in route['module_ids']):
            raise CatalogError('Catalog route references an unknown resource')
    return records

def verified_file(data_root: Path, path: str, expected: str | None = None) -> bytes:
    raw = safe_read(data_root, path)
    pinned = approved_sources()['files'].get(path)
    if not pinned or digest(raw) != pinned or (expected is not None and pinned != expected):
        raise CatalogError('Resource has changed; reviewed source required')
    return raw

def specimen_text(raw: bytes) -> str:
    try:
        text = raw.decode('utf-8')
        start, end = '<!-- specimen:start -->', '<!-- specimen:end -->'
        if text.count(start) != 1 or text.count(end) != 1:
            raise CatalogError('Sample lacks an unambiguous specimen')
        return text.split(start, 1)[1].split(end, 1)[0].strip()
    except UnicodeError as exc:
        raise CatalogError('Sample must be UTF-8 text') from exc

def item_status(record: dict, data_root: Path) -> tuple[str, list[dict]]:
    try:
        verified_file(data_root, record['guide_path'])
        examples = []
        for sample in record['examples']:
            text = specimen_text(verified_file(data_root, sample['path'], sample['sha256']))
            examples.append({k: sample[k] for k in ('id', 'brief_id', 'sha256')} | {'text': text})
        return 'ready', examples
    except (CatalogError, KeyError):
        return 'unavailable', []

def public_item(record: dict, data_root: Path, *, samples: bool = False) -> dict:
    status, examples = item_status(record, data_root)
    result = {k: record[k] for k in PUBLIC_FIELDS if k in record}
    result.update(availability=status, sourceUri=(PUBLIC_BASE + '#voice=' + record['id']) if PUBLIC_BASE else '')
    if samples:
        result['examples'] = examples
    return result

def browse(query: str = '', type: str = 'all', *, data_root: Path = DATA_ROOT) -> dict:
    if not isinstance(query, str) or len(query) > 500 or not isinstance(type, str) or type not in TYPES | {'all'}:
        raise CatalogError('Use a query under 500 characters and a registered resource type')
    terms = query.casefold().split()
    items = []
    for record in load_catalog(data_root):
        haystack = ' '.join(str(record.get(k, '')) for k in ('id', 'name', 'description', 'tags', 'mechanism', 'primary_layer')).casefold()
        if (type == 'all' or record['resource_type'] == type) and all(term in haystack for term in terms):
            item = public_item(record, data_root)
            # Tool fallback remains compact; full specimen prose belongs in the UI resource.
            items.append({k: item[k] for k in ('id', 'name', 'version', 'resource_type', 'description', 'route', 'availability', 'sourceUri')})
    return {'schemaVersion': 1, 'owner': 'Writing Templates', 'query': query, 'type': type, 'items': items}

def handoff(profile_id: str, brief: str = '', modifier_ids: list[str] | None = None, *, data_root: Path = DATA_ROOT) -> dict:
    if not isinstance(profile_id, str) or not ID_RE.fullmatch(profile_id):
        raise CatalogError('Choose a registered resource ID')
    if not isinstance(brief, str) or len(brief) > 10000:
        raise CatalogError('Brief must be text under 10,000 characters')
    modifiers = modifier_ids if modifier_ids is not None else []
    if not isinstance(modifiers, list) or len(modifiers) > 6 or any(not isinstance(m, str) or not ID_RE.fullmatch(m) for m in modifiers) or len(set(modifiers)) != len(modifiers):
        raise CatalogError('Choose up to six distinct registered modifier IDs')
    records = {r['id']: r for r in load_catalog(data_root)}
    if profile_id not in records or any(m not in records for m in modifiers):
        raise CatalogError('Choose a registered resource ID')
    selected = records[profile_id]
    base_id = selected['route']['base_profile_id']
    modules = list(selected['route']['module_ids'])
    for modifier_id in modifiers:
        modifier = records[modifier_id]
        if modifier['resource_type'] not in {'module', 'alias', 'merge'} or modifier['route']['base_profile_id'] != base_id:
            raise CatalogError('Modifier must route to the same base profile as the selection')
        for module in modifier['route']['module_ids']:
            if module not in modules:
                modules.append(module)
    resource_ids = list(dict.fromkeys([profile_id, base_id] + modules))
    resources = []
    for resource_id in resource_ids:
        resource = records[resource_id]
        status, _ = item_status(resource, data_root)
        if status != 'ready':
            raise CatalogError(f'{resource_id} source or samples are unavailable or changed')
        raw = verified_file(data_root, resource['guide_path'])
        resources.append({'id': resource_id, 'name': resource['name'], 'version': resource['version'], 'guideRef': resource['guide_path'], 'guideSha256': digest(raw), 'guideText': raw.decode('utf-8'), 'skillName': resource.get('skill_name')})
    route = {'selected_resource_id': profile_id, 'base_profile_id': base_id, 'module_ids': modules}
    supplements = source_references(resource_ids, data_root)
    four_axes = axis_references(resource_ids, data_root)
    validation = validation_references(resource_ids, data_root)
    instructions = ('Apply the verified base guide and selected modules to this brief. Read the style specification and a relevant historical passage alongside the library demonstration. After those authorities, read the four-axis references for the selected resource and its actual base/module route before drafting. Axis levels describe editorial prominence, not statistical thresholds; they do not override template constraints or the user brief. Use the identified technique, not the source author’s identity, distinctive wording or factual claims. Preserve supplied facts, protected spans, uncertainty and authorization. Resolve unsuitable task fit and critical-state overrides before drafting. Library demonstrations are synthetic; historical readings have separate attribution. Neither establishes guaranteed output. APA and MLA are separate optional format conventions; use only the requested one. Selection prepares a writing handoff; it does not generate, send, publish, deploy or install anything.')
    if profile_id == 'P49':
        instructions = instructions.replace('Read the style specification and a relevant historical passage alongside the library demonstration.', 'Read the complete style authority, public source boundaries and a relevant synthetic demonstration. P49 contains no private personal corpus or historical excerpt; its descriptive measurements apply only to the three fictional examples.').replace('Library demonstrations are synthetic; historical readings have separate attribution.', 'Library demonstrations are synthetic; qualitative personal-voice mapping and intended editorial targets are separate from measurements of those examples.')
    route_label = base_id + (' + ' + ' + '.join(modules) if modules else '')
    text = f"Use Writing Voice Library: {selected['name']} ({profile_id}, v{selected['version']}).\nActual route: {route_label}.\nSource: {PUBLIC_BASE}#voice={profile_id}\nBrief: {brief or '(none supplied)'}\n{instructions}\n\n" + '\n\n'.join(f"{r['id']} v{r['version']} — {r['guideRef']}\nSHA-256: {r['guideSha256']}\n{r['guideText']}" for r in resources)
    if supplements:
        text += '\n\nSelected style specification and readings\n\n' + '\n\n'.join(f"{r['path']}\nSHA-256: {r['sha256']}\n{r['text']}" for r in supplements)
    text += '\n\nFour-axis references\n\n' + '\n\n'.join(f"{r['path']}\nSHA-256: {r['sha256']}\n{r['text']}" for r in four_axes['references'])
    instructions += ' After drafting, apply the included Humanizer Light editorial companion, preserving purposeful template mechanics. After any revisions, run the bundled offline QA workflow for the selection and any additional modifiers. Correct explicit violations, retain unknowns, and complete semantic review; observed sample ranges are not acceptance bounds. If executable tools are unavailable, report that automated QA was not run.'
    text += '\n\nDraft QA\n' + instructions + '\n\n' + '\n\n'.join(f"{r['path']}\nSHA-256: {r['sha256']}\n{r['text']}" for r in validation['references'])
    return {'schemaVersion': 1, 'profileId': profile_id, 'name': selected['name'], 'version': selected['version'], 'resourceType': selected['resource_type'], 'catalogSha256': approved_sources()['catalogSha256'], 'route': route, 'resources': resources, 'sourceReferences': supplements, 'fourAxes': four_axes, 'validation': validation, 'brief': brief, 'sourceUri': (PUBLIC_BASE + '#voice=' + profile_id) if PUBLIC_BASE else '', 'instructions': instructions, 'handoffText': text, 'state': 'prepared'}
