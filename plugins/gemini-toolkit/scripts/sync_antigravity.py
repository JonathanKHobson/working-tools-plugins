#!/usr/bin/env python3
"""Deterministic, conflict-safe Antigravity source-link synchronization."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

OUT = STATE = GLOBAL = ADAPTERS = ALIASES = NATIVE = None
AGY = None
CONFIG = {}
COMMAND_TIMEOUT = 60


def sha(data):
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    return sha(path.read_bytes()) if path.is_file() else None


def source_skills(packages):
    primary = CONFIG.get('primary_skill_owners', {})
    entries = {}
    by_name = {}
    for pkg in packages:
        owner = pkg['name']
        root = Path(pkg['source']['path'])
        if not root.is_dir():
            raise RuntimeError(f'Missing canonical source: {root}')
        for path in sorted((root / 'skills').glob('*/SKILL.md')):
            content = path.read_text(encoding='utf-8')
            if not content.startswith('---\n') or '\n---\n' not in content[4:]:
                raise RuntimeError(f'Invalid skill frontmatter: {path}')
            head = content.split('\n---\n', 1)[0][4:]
            match = re.search(r'^name:\s*(.+)$', head, flags=re.M)
            if not match:
                raise RuntimeError(f'Missing skill name: {path}')
            name = match.group(1).strip().strip('"\'')
            key = f'{owner}--{name}'
            if key in entries:
                raise RuntimeError(f'Duplicate owner/name: {key}')
            by_name.setdefault(name, []).append(owner)
            entries[key] = {'owner': owner, 'name': name, 'source': str(path),
                            'source_sha256': sha(content.encode()), 'head': head}
    collisions = {k: v for k, v in by_name.items() if len(v) > 1}
    if set(collisions) - set(primary):
        raise RuntimeError(f'New skill-name collision needs an owner decision: {collisions}')
    for name, owners in collisions.items():
        if primary[name] not in owners:
            raise RuntimeError(f'Preferred owner missing for {name}: {owners}')
    desired = {}
    for key, entry in entries.items():
        owner, name = entry['owner'], entry['name']
        alias = name in collisions and owner != primary[name]
        target = (ALIASES / f'{owner}-{name}') if alias else Path(entry['source']).parent
        entry['link'] = str(GLOBAL / key)
        entry['target'] = str(target)
        entry['discovered_name'] = f'{owner}-{name}' if alias else name
        entry['alias'] = alias
        if alias:
            head = re.sub(r'^name:\s*.+$', f'name: {entry["discovered_name"]}',
                          entry['head'], count=1, flags=re.M)
            body = ('---\n' + head + '\n---\n\n# ' + entry['discovered_name'] + '\n\n'
                    + f'Read and follow the complete canonical skill at `{entry["source"]}`. '
                    + 'Read its referenced files relative to that canonical skill directory. '
                    + 'Preserve its full method and project constraints; this alias only resolves a host-wide skill-name collision.\n')
            entry['alias_content'] = body
            entry['alias_sha256'] = sha(body.encode())
        desired[key] = entry
    return desired, collisions


def source_guards(packages):
    guards = {}
    for pkg in packages:
        root = Path(pkg['source']['path'])
        for relative in ['.mcp.json', 'hooks/hooks.json']:
            path = root / relative
            if path.is_file():
                guards[f'{pkg["name"]}/{relative}'] = file_sha(path)
        for path in sorted((root / 'agents').glob('*.md')):
            guards[f'{pkg["name"]}/agents/{path.name}'] = file_sha(path)
    admission = OUT / 'mcp-admission.json'
    if admission.is_file():
        for entry in json.loads(admission.read_text()).get('servers', []):
            if entry.get('state') == 'staged-disabled':
                script = Path(entry['entry']['path'])
                guards[f'executable-mcp/{entry["server"]}'] = file_sha(script)
    for name, path in CONFIG.get('hook_guard_paths', {}).items():
        guards[f'executable-hook/{name}'] = file_sha(Path(path))
    return guards


def manifest(pkg):
    return (json.dumps({'$schema': 'https://antigravity.google/schemas/v1/plugin.json',
                        'name': pkg['name'],
                        'description': f'Shared canonical methods from {pkg["name"]} {pkg["version"]}; global skills link to source.'},
                       indent=2) + '\n').encode()


def live_file_hashes(directory):
    if not directory.is_dir():
        return None
    result = {}
    for path in sorted(directory.rglob('*')):
        relative = str(path.relative_to(directory))
        if path.is_symlink():
            result[relative] = 'symlink:' + os.readlink(path)
        elif path.is_file():
            result[relative] = file_sha(path)
    return result


def run_native(*command):
    try:
        done = subprocess.run([AGY, *command], capture_output=True, text=True,
                              timeout=COMMAND_TIMEOUT, check=False)
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(f'Native command timed out after {COMMAND_TIMEOUT}s: {command}') from error
    if done.returncode:
        raise RuntimeError(f'Native command failed {command}: {done.stdout} {done.stderr}')
    return done


def remove_path(path):
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def copy_path(source, target):
    if source.is_symlink():
        target.symlink_to(os.readlink(source), target_is_directory=True)
    elif source.is_dir():
        shutil.copytree(source, target, symlinks=True)
    elif source.is_file():
        shutil.copy2(source, target)


def snapshot(paths):
    backup = Path(tempfile.mkdtemp(prefix='sync-', dir=OUT / 'rollback'))
    entries = []
    for index, path in enumerate(sorted(paths, key=str)):
        target = backup / str(index)
        exists = path.exists() or path.is_symlink()
        if exists:
            copy_path(path, target)
        entries.append({'path': str(path), 'backup': str(index), 'exists': exists})
    (backup / 'manifest.json').write_text(json.dumps(entries, indent=2) + '\n')
    return backup, entries


def restore(backup, entries):
    for entry in entries:
        path = Path(entry['path'])
        remove_path(path)
        if entry['exists']:
            path.parent.mkdir(parents=True, exist_ok=True)
            copy_path(backup / entry['backup'], path)
    return all((path.exists() or path.is_symlink()) == entry['exists'] and
               (not entry['exists'] or path_fingerprint(path) == path_fingerprint(backup / entry['backup']))
               for entry in entries for path in [Path(entry['path'])])


def path_fingerprint(path):
    if path.is_symlink():
        return ('symlink', os.readlink(path))
    if path.is_dir():
        return ('dir', live_file_hashes(path))
    if path.is_file():
        return ('file', file_sha(path))
    return ('missing', None)


def main():
    global OUT, STATE, GLOBAL, ADAPTERS, ALIASES, NATIVE, AGY, CONFIG, COMMAND_TIMEOUT
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--apply', action='store_true')
    parser.add_argument('--config', type=Path, required=True,
                        help='Private host path binding; keep this outside the portable toolkit')
    parser.add_argument('--inventory', type=Path)
    args = parser.parse_args()
    CONFIG = json.loads(args.config.read_text())
    OUT = Path(CONFIG['state_dir']).resolve(strict=True)
    if not OUT.is_dir() or (CONFIG.get('require_external_volume', True) and
                            not str(OUT).startswith('/Volumes/')):
        raise RuntimeError('Private state must be on a mounted external volume')
    STATE = OUT / 'sync-state.json'
    GLOBAL = Path(CONFIG['global_skills_dir'])
    ADAPTERS = OUT / 'adapters'
    ALIASES = OUT / 'alias-skills'
    NATIVE = Path(CONFIG['native_plugins_dir'])
    AGY = CONFIG['agy']
    COMMAND_TIMEOUT = int(CONFIG.get('command_timeout_seconds', 60))
    if COMMAND_TIMEOUT < 1 or COMMAND_TIMEOUT > 300:
        raise RuntimeError('command_timeout_seconds must be 1..300')
    args.inventory = args.inventory or Path(CONFIG['default_inventory'])
    packages = [x for x in json.loads(args.inventory.read_text())['installed']
                if x.get('marketplaceName') == 'personal' and x.get('source', {}).get('path')]
    by_package = {x['name']: x for x in packages}
    if len(by_package) != len(packages):
        raise RuntimeError('Duplicate personal package names')
    desired, collisions = source_skills(packages)
    guards = source_guards(packages)
    old = json.loads(STATE.read_text()) if STATE.exists() else {'skills': {}, 'packages': {}, 'source_guards': {}}
    conflicts = []
    actions = []
    security_review = [key for key in set(old.get('source_guards', {})) | set(guards)
                       if old.get('source_guards', {}).get(key) != guards.get(key)] if STATE.exists() else []

    for key, entry in desired.items():
        link = Path(entry['link'])
        current = os.readlink(link) if link.is_symlink() else None
        prior = old['skills'].get(key)
        if current is not None and current != entry['target']:
            if prior is None or current != prior['target']:
                conflicts.append(f'Edited skill link: {link}')
            else:
                actions.append(f'relink {key}')
        elif current is None:
            if link.exists():
                conflicts.append(f'Nonlink destination: {link}')
            else:
                actions.append(f'link {key}')
        if entry['alias']:
            alias_file = Path(entry['target']) / 'SKILL.md'
            current_sha = file_sha(alias_file)
            if current_sha != entry['alias_sha256']:
                prior_sha = prior.get('alias_sha256') if prior else None
                if current_sha is not None and current_sha != prior_sha:
                    conflicts.append(f'Edited alias: {alias_file}')
                else:
                    actions.append(f'alias {key}')
        if prior and prior.get('source_sha256') != entry['source_sha256']:
            actions.append(f'source-content {key} (link already shares bytes)')
    for key, prior in old['skills'].items():
        if key in desired:
            continue
        link = Path(prior['link'])
        if link.is_symlink() and os.readlink(link) == prior['target']:
            actions.append(f'unlink {key}')
        elif link.exists() or link.is_symlink():
            conflicts.append(f'Edited stale link: {link}')
        if prior.get('alias'):
            alias_file = Path(prior['target']) / 'SKILL.md'
            current_sha = file_sha(alias_file)
            if current_sha == prior.get('alias_sha256'):
                actions.append(f'remove alias {key}')
            elif current_sha is not None:
                conflicts.append(f'Edited stale alias: {alias_file}')

    next_packages = {}
    for name, pkg in by_package.items():
        adapter = ADAPTERS / name
        native = NATIVE / name
        expected_manifest = manifest(pkg)
        old_pkg = old['packages'].get(name)
        adapter_hashes = live_file_hashes(adapter)
        native_hashes = live_file_hashes(native)
        if adapter_hashes is None and old_pkg:
            conflicts.append(f'Missing owned adapter: {adapter}')
        if native_hashes is None and old_pkg:
            conflicts.append(f'Missing native package: {native}')
        for place, hashes, known in [('adapter', adapter_hashes, old_pkg.get('adapter') if old_pkg else None),
                                     ('native', native_hashes, old_pkg.get('native') if old_pkg else None)]:
            if hashes is not None and known is not None:
                for rel in set(hashes) - set(known):
                    conflicts.append(f'Extra {place} package entry: {name}/{rel}')
                for rel, previous_sha in known.items():
                    if hashes.get(rel) != previous_sha:
                        conflicts.append(f'Edited {place} package file: {name}/{rel}')
            elif hashes is not None and old_pkg is None:
                if place == 'native':
                    if hashes != adapter_hashes:
                        conflicts.append(f'Unowned native package: {name}')
                elif hashes.get('plugin.json') != sha(expected_manifest):
                    conflicts.append(f'Unowned adapter manifest: {name}')
        if old_pkg is None and adapter_hashes is not None and adapter_hashes != {'plugin.json': sha(expected_manifest)}:
            conflicts.append(f'Unowned adapter package: {name}')
        if adapter_hashes is None:
            actions.append(f'create adapter {name}')
            adapter_hashes = {}
        if adapter_hashes.get('plugin.json') != sha(expected_manifest):
            if old_pkg and adapter_hashes.get('plugin.json') == old_pkg['adapter'].get('plugin.json'):
                actions.append(f'update manifest {name}')
            elif old_pkg is None and not adapter_hashes:
                actions.append(f'write manifest {name}')
            else:
                conflicts.append(f'Edited adapter manifest: {name}')
        if native_hashes is None or native_hashes != adapter_hashes:
            actions.append(f'native install {name}')
        next_packages[name] = {'manifest_sha256': sha(expected_manifest)}
    for name, prior in old['packages'].items():
        if name in by_package:
            continue
        if live_file_hashes(ADAPTERS / name) != prior['adapter'] or live_file_hashes(NATIVE / name) != prior['native']:
            conflicts.append(f'Edited removed package: {name}')
        else:
            actions.append(f'uninstall {name}')
    result = {'mode': 'check' if args.check else 'apply', 'packages': len(packages),
              'skills': len(desired), 'collisions': collisions,
              'actions': actions, 'conflicts': sorted(set(conflicts)),
              'security_review_needed': sorted(security_review)}
    if args.check or conflicts or security_review:
        print(json.dumps(result, indent=2))
        if not args.check:
            return 2
        return 1 if conflicts or security_review else 0

    if not actions:
        print(json.dumps(result, indent=2))
        return 0

    managed = {STATE, OUT / 'shared-skills-map.json'}
    if CONFIG.get('native_import_manifest'):
        managed.add(Path(CONFIG['native_import_manifest']))
    managed.update(GLOBAL / key for key in set(desired) | set(old['skills']))
    managed.update(ALIASES / f'{entry["owner"]}-{entry["name"]}' for entry in desired.values() if entry['alias'])
    managed.update(Path(entry['target']) for entry in old['skills'].values() if entry.get('alias'))
    managed.update(ADAPTERS / name for name in set(by_package) | set(old['packages']))
    managed.update(NATIVE / name for name in set(by_package) | set(old['packages']))
    (OUT / 'rollback').mkdir(exist_ok=True)
    backup, entries = snapshot(managed)
    try:
        apply_changes(packages, by_package, desired, old, next_packages, guards, args, collisions, result)
    except Exception as error:
        verified = restore(backup, entries)
        result['rollback'] = {'backup': str(backup), 'verified': verified, 'cause': str(error)}
        print(json.dumps(result, indent=2))
        return 2
    result['rollback_backup'] = str(backup)
    print(json.dumps(result, indent=2))
    return 0


def apply_changes(packages, by_package, desired, old, next_packages, guards, args, collisions, result):

    GLOBAL.mkdir(parents=True, exist_ok=True)
    ALIASES.mkdir(parents=True, exist_ok=True)
    ADAPTERS.mkdir(parents=True, exist_ok=True)
    for key, prior in old['skills'].items():
        if key in desired:
            continue
        link = Path(prior['link'])
        if link.is_symlink():
            link.unlink()
        if prior.get('alias'):
            alias_file = Path(prior['target']) / 'SKILL.md'
            if alias_file.exists():
                alias_file.unlink()
                alias_file.parent.rmdir()
    for name, prior in old['packages'].items():
        if name in by_package:
            continue
        run_native('plugin', 'uninstall', name)
        for path in sorted((ADAPTERS / name).rglob('*'), reverse=True):
            if path.is_file(): path.unlink()
            elif path.is_dir(): path.rmdir()
        (ADAPTERS / name).rmdir()
    for key, entry in desired.items():
        link = Path(entry['link'])
        if entry['alias']:
            alias_file = Path(entry['target']) / 'SKILL.md'
            alias_file.parent.mkdir(parents=True, exist_ok=True)
            if file_sha(alias_file) != entry['alias_sha256']:
                alias_file.write_text(entry['alias_content'])
        if link.is_symlink() and os.readlink(link) != entry['target']:
            link.unlink()
        if not link.is_symlink():
            link.symlink_to(entry['target'], target_is_directory=True)
    for name, pkg in by_package.items():
        adapter = ADAPTERS / name
        adapter.mkdir(exist_ok=True)
        manifest_path = adapter / 'plugin.json'
        if file_sha(manifest_path) != sha(manifest(pkg)):
            manifest_path.write_bytes(manifest(pkg))
        native = NATIVE / name
        if live_file_hashes(native) != live_file_hashes(adapter):
            run_native('plugin', 'validate', str(adapter), '--strict', '--json')
            run_native('plugin', 'install', str(adapter))
            if live_file_hashes(native) != live_file_hashes(adapter):
                raise RuntimeError(f'Native readback differs for {name}')
        next_packages[name] = {'manifest_sha256': sha(manifest(pkg)),
                               'adapter': live_file_hashes(adapter), 'native': live_file_hashes(native)}
    state_skills = {key: {k: value for k, value in entry.items()
                          if k not in {'head', 'alias_content'}} for key, entry in desired.items()}
    state_content = json.dumps({'schema_version': 1, 'inventory': str(args.inventory),
                                'skills': state_skills, 'packages': next_packages,
                                'source_guards': guards}, indent=2) + '\n'
    if not STATE.exists() or STATE.read_text() != state_content:
        STATE.write_text(state_content)
    map_path = OUT / 'shared-skills-map.json'
    map_content = json.dumps({'packages': len(packages), 'skills': len(desired),
                              'collisions': collisions, 'entries': list(state_skills.values())}, indent=2) + '\n'
    if not map_path.exists() or map_path.read_text() != map_content:
        map_path.write_text(map_content)
    return None


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(f'Antigravity sync stopped: {error}', file=sys.stderr)
        sys.exit(2)
