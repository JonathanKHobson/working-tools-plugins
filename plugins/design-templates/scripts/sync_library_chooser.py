#!/usr/bin/env python3
"""Project the canonical chooser without copying adapters or host configuration."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = ('index.html', 'styles.css', 'bridge.js', 'app.js')
PEERS = (
    'ux-design-toolkit/runtime/library-chooser',
    'ux-design-toolkit/runtime/design-library/ui',
    'writing-templates/runtime/writing-voice-library/ui',
    'prompt-playbook-studio/runtime/framework-builder/shared',
    'brand-templates/runtime/brand-library/ui',
    'activities-templates/runtime/studio_library/ui',
    'video-templates/runtime/video-library/ui',
    'video-templates/runtime/library-chooser',
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--peer-root', type=Path, help='Optional host plugin source root')
    parser.add_argument('--target', type=Path, action='append', default=[])
    parser.add_argument('--include-atlas', action='store_true', help='Use optional external Atlas binding')
    args = parser.parse_args()
    targets = [ROOT / 'runtime/design-library/ui', *args.target]
    if args.peer_root:
        targets.extend(args.peer_root.expanduser() / rel for rel in PEERS if (args.peer_root.expanduser() / rel).is_dir())
    if args.include_atlas:
        binding = Path.home() / '.config/studio-tools/atlas-library.json'
        config = json.loads(binding.read_text())
        server = Path(config['server']).expanduser().resolve(strict=True)
        if server.name != 'server.py' or server.parent.name != 'studio_library':
            raise ValueError('Atlas binding must name the studio_library server')
        targets.append(server.parent / 'ui')
    drift = []
    for folder in targets:
        if not folder.is_dir():
            raise ValueError('Configured UI target is missing')
        for name in FILES:
            target = folder / name
            expected = (ROOT / 'runtime/library-chooser' / name).read_bytes()
            if target.is_file() and target.read_bytes() == expected:
                continue
            drift.append(str(target))
            if not args.check:
                target.write_bytes(expected)
    print(json.dumps({'checkedTargets':len(targets),'drift':drift,'mode':'check' if args.check else 'sync'}))
    return int(bool(drift) and args.check)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f'Chooser synchronization failed: {exc}', file=sys.stderr)
        raise SystemExit(2)
