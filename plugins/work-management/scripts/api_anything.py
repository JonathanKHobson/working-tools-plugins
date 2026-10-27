#!/usr/bin/env python3
"""Set up and run the bundled API Anything revision. No implicit downloads."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'libraries/api-anything'
MANIFEST = ROOT / 'docs/api-anything-source.json'
BINDING = Path.home() / '.config/work-management/api-anything.json'
RECEIPT = '.work-management-runtime.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_files(root, files):
    root = root.resolve()
    for name, expected in files.items():
        rel = Path(name)
        if rel.is_absolute() or '..' in rel.parts:
            raise ValueError('Unsafe manifest path: ' + name)
        path = root / rel
        if any(p.is_symlink() for p in [path, *path.parents] if p != root and root in p.parents):
            raise ValueError('Source symlink refused: ' + name)
        if not path.is_file() or digest(path) != expected:
            raise ValueError('Source integrity mismatch: ' + name)


def verify_source():
    manifest = json.loads(MANIFEST.read_text())
    verify_files(SOURCE, manifest['files'])
    actual = {str(p.relative_to(SOURCE)) for p in SOURCE.rglob('*') if p.is_file()}
    if actual != set(manifest['files']):
        raise ValueError('Source integrity mismatch: unexpected files')
    return manifest


def supported_node(version):
    match = re.fullmatch(r'v?(\d+)\.(\d+)\.(\d+)', version.strip())
    return bool(match and tuple(map(int, match.groups())) >= (22, 13, 0))


def environment():
    env = os.environ.copy()
    for key in ('NODE_OPTIONS', 'NODE_PATH'):
        env.pop(key, None)
    return env


def verify_runtime(runtime):
    manifest = verify_source()
    receipt_path = runtime / RECEIPT
    if not receipt_path.is_file():
        raise ValueError('Runtime is missing; run setup with an empty --runtime directory first')
    receipt = json.loads(receipt_path.read_text())
    if receipt.get('commit') != manifest['commit'] or receipt.get('manifest_sha256') != digest(MANIFEST):
        raise ValueError('Runtime revision differs; run setup in a new empty directory')
    verify_files(runtime, manifest['files'])
    verify_files(runtime, receipt['built_files'])
    check_startup(runtime)
    return receipt


def check_startup(runtime):
    package = json.loads((runtime/'package.json').read_text())
    for name in package['dependencies']:
        if not (runtime/'node_modules'/name/'package.json').is_file():
            raise ValueError('Runtime dependencies missing ('+name+'); run setup in a new empty directory')
    node = shutil.which('node')
    if not node:
        raise ValueError('Node >=22.13 is required')
    env = environment()
    version = subprocess.run([node, '--version'], capture_output=True, text=True, env=env, check=True).stdout
    if not supported_node(version):
        raise ValueError('Node >=22.13 is required')
    # --help loads CLI dependencies but performs no operation, login or fetch.
    result = subprocess.run([node, str(runtime/'dist/cli.js'), '--help'],
                            capture_output=True, text=True, env=env, timeout=30)
    if result.returncode:
        raise ValueError('Runtime startup failed; inspect dependencies or set up a new runtime: '
                         + result.stderr[:1000])


def state_path(raw, runtime):
    runtime = runtime.resolve()
    path = Path(raw).expanduser().resolve()
    if path == ROOT or ROOT in path.parents or path == runtime or runtime in path.parents:
        raise ValueError('Private state must stay outside the plugin and runtime directories')
    return path


def setup(runtime):
    if runtime.exists() and any(runtime.iterdir()):
        if (runtime/RECEIPT).is_file():
            verify_runtime(runtime)
            return
        raise ValueError('Setup requires an empty runtime directory; existing files were preserved')
    if runtime == ROOT or ROOT in runtime.parents or runtime in ROOT.parents:
        raise ValueError('Runtime must be outside the plugin directory')
    manifest = verify_source()
    node = shutil.which('node'); npm = shutil.which('npm')
    if not node or not npm:
        raise ValueError('Node >=22.13 and npm are required; install them using your host setup')
    env = environment()
    version = subprocess.run([node, '--version'], check=True, capture_output=True, text=True, env=env).stdout
    if not supported_node(version):
        raise ValueError('Node >=22.13 is required; found ' + version.strip())
    runtime.mkdir(parents=True, exist_ok=True, mode=0o700)
    for name in manifest['files']:
        target = runtime / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE/name, target)
    # All package lifecycle hooks stay disabled. Only the reviewed tsc build runs.
    env['npm_config_cache'] = str(runtime/'.npm-cache')
    env['npm_config_update_notifier'] = 'false'
    subprocess.run([npm, 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=runtime, env=env, check=True)
    subprocess.run([node, str(runtime/'node_modules/typescript/bin/tsc'), '-p', 'tsconfig.build.json'],
                   cwd=runtime, env=env, check=True)
    verify_files(runtime, manifest['files'])
    built = {str(p.relative_to(runtime)):digest(p) for p in sorted((runtime/'dist').rglob('*')) if p.is_file()}
    if 'dist/cli.js' not in built:
        raise ValueError('Build did not produce dist/cli.js; setup is incomplete')
    receipt = {'commit':manifest['commit'], 'manifest_sha256':digest(MANIFEST),
               'node':version.strip(), 'built_files':built}
    (runtime/RECEIPT).write_text(json.dumps(receipt, indent=2)+'\n')
    (runtime/RECEIPT).chmod(0o600)


def binding():
    return json.loads(BINDING.read_text()) if BINDING.exists() else {}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', type=Path, help='Explicit runtime directory outside this plugin')
    parser.add_argument('--state', type=Path, help='Private session/spec directory outside this plugin')
    parser.add_argument('--remember', action='store_true', help='Save these local paths after successful setup')
    parser.add_argument('command', choices=['setup', 'status', 'run', 'mcp'])
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    try:
        config = binding()
        raw = args.runtime or os.environ.get('WORK_MANAGEMENT_API_ANYTHING_RUNTIME') or config.get('runtime')
        if not raw:
            raise ValueError('No runtime selected; use --runtime /your/storage/api-anything setup')
        runtime = Path(raw).expanduser().resolve()
        private = state_path(args.state or os.environ.get('API_ANYTHING_HOME') or config.get('state')
                             or Path.home()/'.local/share/work-management/api-anything', runtime)
        if args.command == 'setup':
            if args.args:
                raise ValueError('Setup takes no trailing arguments')
            setup(runtime)
            if args.remember:
                BINDING.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                temporary = BINDING.with_suffix('.tmp')
                fd = os.open(temporary, os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600)
                with os.fdopen(fd, 'w') as stream:
                    json.dump({'runtime':str(runtime), 'state':str(private)}, stream, indent=2)
                    stream.write('\n')
                os.replace(temporary, BINDING)
        receipt = verify_runtime(runtime)
        if args.command in ('setup','status'):
            print(json.dumps({'ready':True,'commit':receipt['commit'],'runtime':str(runtime),
                              'state':str(private),'network_used':args.command == 'setup'}))
            return 0
        node = shutil.which('node')
        if not node:
            raise ValueError('Node >=22.13 is required')
        env = environment(); env['API_ANYTHING_HOME'] = str(private)
        rest = args.args[1:] if args.args[:1] == ['--'] else args.args
        command = ['mcp', *rest] if args.command == 'mcp' else rest
        if not command:
            raise ValueError('run needs an API Anything command, such as sites')
        # Replace this process: stdio is untouched and the host owns MCP lifetime.
        os.execve(node, [node, str(runtime/'dist/cli.js'), *command], env)
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print('API Anything: '+str(exc), file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
