#!/usr/bin/env python3
"""Scoped offline entry to the incorporated Earshot implementation.

No package installation, model acquisition, hosted uploads, MCP registration,
arbitrary recipes, source replacement or provider configuration is supported.
Run from a Python environment whose dependencies were separately reviewed.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

SOURCE = Path(__file__).resolve().parents[1] / 'libraries' / 'earshot'
OPS = ('measure', 'sfx-list', 'sfx-render', 'kit-render', 'kit-check',
       'describe', 'match', 'find', 'compare', 'ab', 'realness', 'timeline')
PERCEPTION = {'describe', 'match', 'find', 'compare', 'ab', 'realness', 'timeline'}
DEPENDENCIES = ('numpy', 'scipy', 'soundfile', 'soxr', 'librosa', 'pyloudnorm')


def bundled_sound_ids():
    """Read fixed bundled JSON as data; never import an audio/recipe module."""
    ids = set()
    for p in (SOURCE / 'earshot' / 'forge' / 'bank').glob('*.json'):
        if p.is_symlink():
            raise ValueError('bundled bank must not be a symlink')
        ids.update(json.loads(p.read_text(encoding='utf-8'))['entries'])
    return ids


def validate_kit(path):
    """Narrow inert schema: shipped sound IDs, bounded knobs, no path fields.

    The upstream kit validator runs too, but only after this data-only policy
    check. Passing a top-level task path does not authorize nested operands.
    """
    if path.stat().st_size > 1024 * 1024:
        raise ValueError('kit JSON exceeds 1 MiB')

    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate kit JSON key')
            result[key] = value
        return result

    kit = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)
    if (not isinstance(kit, dict) or kit.get('kit') != 1 or
            set(kit) - {'kit', 'name', 'sr', 'note', 'roles', 'off'}):
        raise ValueError('kit accepts only schema, metadata and roles; no external paths or overrides')
    if kit.get('sr', 48000) not in (44100, 48000, 88200, 96000):
        raise ValueError('unsupported kit sample rate')
    roles = kit.get('roles')
    if not isinstance(roles, dict) or not 1 <= len(roles) <= 64:
        raise ValueError('kit needs 1 to 64 bounded roles')
    known = bundled_sound_ids()
    total = 0

    def number(v, lo, hi):
        return (not isinstance(v, bool) and isinstance(v, (int, float)) and
                math.isfinite(v) and lo <= v <= hi)

    def pitch(v):
        return (number(v, 20, 20000) or
                isinstance(v, str) and re.fullmatch(r'[A-Ga-g](?:#|b|s)?-?[0-9]', v) is not None)

    for role, spec in roles.items():
        if not re.fullmatch(r'[a-z][a-z0-9_]*(?:\.[a-z0-9_]+)*', role) or len(role) > 64:
            raise ValueError('invalid kit role identity')
        if spec is None:
            continue
        if (not isinstance(spec, dict) or set(spec) -
                {'sound', 'takes', 'seed', 'edits', 'pitches', 'align', 'max_s', 'level_db', 'note'}):
            raise ValueError('kit role has unsupported keys; recipes, files and output paths are excluded')
        if not isinstance(spec.get('sound'), str) or spec['sound'] not in known:
            raise ValueError('kit sound must be a bundled bank identity')
        takes = spec.get('takes', 1)
        if isinstance(takes, bool) or not isinstance(takes, int) or not 1 <= takes <= 32:
            raise ValueError('kit takes must be 1 to 32')
        if 'seed' in spec and (isinstance(spec['seed'], bool) or not isinstance(spec['seed'], int)):
            raise ValueError('kit seed must be an integer')
        edits = spec.get('edits') or {}
        if not isinstance(edits, dict) or set(edits) - {'dur', 'apex', 'pitch'}:
            raise ValueError('kit edits allow only bounded duration, apex and pitch')
        for key in ('dur', 'apex'):
            if key in edits and not number(edits[key], 0.001, 10):
                raise ValueError('kit duration/apex must be 0.001 to 10 seconds')
        if 'pitch' in edits and not pitch(edits['pitch']):
            raise ValueError('invalid kit pitch')
        pitches = spec.get('pitches', [None])
        if not isinstance(pitches, list) or not 1 <= len(pitches) <= 32:
            raise ValueError('kit pitches must be a bounded list')
        if 'pitches' in spec and (any(not pitch(p) for p in pitches) or 'pitch' in edits):
            raise ValueError('invalid or conflicting kit pitches')
        if 'max_s' in spec and not number(spec['max_s'], 0.01, 10):
            raise ValueError('kit max_s must be 0.01 to 10 seconds')
        if 'level_db' in spec and not number(spec['level_db'], -80, 0):
            raise ValueError('kit level must be -80 to 0 dB')
        if 'align' in spec and spec['align'] not in ('onset', 'peak', 'end'):
            raise ValueError('invalid kit alignment')
        total += takes * len(pitches)
        if total > 256:
            raise ValueError('kit exceeds 256 rendered takes; split it into bounded tasks')
    return kit


def scoped(value, root, *, exists=False, fresh=False):
    p = Path(value).expanduser().resolve()
    if not p.is_relative_to(root):
        raise ValueError(f'path leaves the declared task workspace: {p}')
    if exists and not p.is_file():
        raise ValueError(f'input must be an existing task file: {p}')
    if fresh and p.exists():
        raise ValueError(f'output must be new; preserve existing media: {p}')
    return p


def missing_dependencies(finder=importlib.util.find_spec, perception=False):
    names = DEPENDENCIES + (('torch', 'transformers', 'sklearn') if perception else ())
    return [name for name in names if finder(name) is None]


def build_plan(operation, workspace, scratch, *, input_path=None, output=None,
               sound=None, query=None, cached_models=False, parent_env=None,
               references=None, second=None):
    if operation not in OPS:
        raise ValueError('unsupported operation; uploads, model acquisition, servers and Python recipes are excluded')
    root = Path(workspace).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError('workspace must be an existing task directory')
    cache = scoped(scratch, root)
    if cache == root:
        raise ValueError('scratch must be a task subdirectory')
    if operation in PERCEPTION and not cached_models:
        raise ValueError('perception requires --cached-models after reviewing existing pinned safetensors; no download is enabled')
    args = []
    if operation == 'sfx-list':
        args = ['sfx', 'list']
    elif operation == 'sfx-render':
        if not sound or sound not in bundled_sound_ids():
            raise ValueError('sound must be a bundled bank id, not a recipe path')
        if not output:
            raise ValueError('sfx-render requires a fresh --output WAV path')
        args = ['sfx', 'render', sound, '-o', str(scoped(output, root, fresh=True))]
    elif operation in ('kit-render', 'kit-check'):
        if not input_path:
            raise ValueError('kit operation requires --input task kit JSON')
        kit_path = scoped(input_path, root, exists=True)
        validate_kit(kit_path)
        args = ['kit', operation.split('-')[1], str(kit_path)]
        if operation == 'kit-render':
            if not output:
                raise ValueError('kit-render requires a fresh --output directory')
            args += ['--out', str(scoped(output, root, fresh=True))]
    else:
        if not input_path:
            raise ValueError('operation requires --input task media')
        args = [operation, str(scoped(input_path, root, exists=True))]
        if operation in ('match', 'find'):
            if not query:
                raise ValueError('match/find requires --query describing the sound')
            args.append(query)
        if operation == 'compare':
            if not references:
                raise ValueError('compare requires --reference existing task media')
            args += ['--refs', *[str(scoped(p, root, exists=True)) for p in references]]
        if operation == 'ab':
            if not second:
                raise ValueError('ab requires --second existing task media')
            args.append(str(scoped(second, root, exists=True)))
            if query:
                args += ['--query', query]
            if references:
                args += ['--refs', *[str(scoped(p, root, exists=True)) for p in references]]
    # Keep only ordinary process essentials. No provider credentials, inherited
    # models/banks/refsets, proxies, Python path injection or HF tokens are passed.
    inherited = os.environ if parent_env is None else parent_env
    env = {k: v for k, v in inherited.items() if k in (
        'PATH', 'HOME', 'USERPROFILE', 'SYSTEMROOT', 'WINDIR', 'LANG', 'LC_ALL')}
    env.update(EARSHOT_HOME=str(cache / 'earshot'), EARSHOT_OFFLINE='1',
               HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
               HF_HUB_DISABLE_TELEMETRY='1', DO_NOT_TRACK='1',
               EARSHOT_THREADS='2', OMP_NUM_THREADS='2', MKL_NUM_THREADS='2',
               TMPDIR=str(cache / 'tmp'), TEMP=str(cache / 'tmp'), TMP=str(cache / 'tmp'))
    # Explicit revisions disable hub.resolve()'s legacy pickle fallback. Only
    # existing safetensors at the source-reviewed default pins are eligible.
    env.update(EARSHOT_CLAP_REVISION='16c8cc3159a3c8a31e8ff5ef1f66b0d9ab3667db',
               EARSHOT_AST_REVISION='f826b80d28226b62986cc218e5cec390b1096902')
    # Fixed reviewed bootstrap, not user-generated code. -I blocks cwd/PYTHONPATH
    # shadowing; add only this incorporated source tree for the known module.
    loader = "import runpy,sys; sys.path.insert(0,sys.argv.pop(1)); runpy.run_module('earshot',run_name='__main__')"
    return {'argv': [sys.executable, '-I', '-c', loader, str(SOURCE), *args],
            'env': env, 'cwd': str(root), 'scratch': str(cache),
            'perception': operation in PERCEPTION}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('operation', choices=OPS)
    ap.add_argument('--workspace', required=True)
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--input', dest='input_path')
    ap.add_argument('--output')
    ap.add_argument('--sound')
    ap.add_argument('--query')
    ap.add_argument('--reference', dest='references', action='append', help='one task reference media file; repeat as needed')
    ap.add_argument('--second', help='second task media file for ab')
    ap.add_argument('--cached-models', action='store_true')
    ap.add_argument('--plan', action='store_true', help='print a no-import execution plan; do not execute Earshot')
    a = ap.parse_args(argv)
    try:
        p = build_plan(a.operation, a.workspace, a.scratch, input_path=a.input_path,
                       output=a.output, sound=a.sound, query=a.query, cached_models=a.cached_models,
                       references=a.references, second=a.second)
        if a.plan:
            print(json.dumps(p, indent=2))
            return 0
        missing = missing_dependencies(perception=p['perception'])
        if missing:
            raise ValueError('execution unavailable; missing reviewed runtime dependencies: ' + ', '.join(missing))
        if not (SOURCE / 'earshot' / '__main__.py').is_file():
            raise ValueError('incorporated Earshot source is missing; restore complete package support')
        cache = Path(p['scratch'])
        (cache / 'tmp').mkdir(parents=True, exist_ok=True)
        # Bounded process lifetime; this is not a memory or network sandbox.
        return subprocess.run(p['argv'], cwd=p['cwd'], env=p['env'], timeout=180,
                              check=False).returncode
    except (ValueError, OSError, subprocess.TimeoutExpired) as e:
        print(f'earshot adapter: {e}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
