"""Small stdlib stdio bridge to a private, on-demand fixed-domain MCP backend."""
from __future__ import annotations

import argparse
import ctypes
import fcntl
import hashlib
import json
import os
from pathlib import Path
import selectors
import socket
import stat
import struct
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
CHUNK = 65536
BUFFER_LIMIT = 4 * CHUNK


def peer_uid(sock):
    """Authenticate Unix socket peers on macOS and Linux; fail closed elsewhere."""
    if hasattr(socket, 'SO_PEERCRED'):
        return struct.unpack('3i', sock.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12))[1]
    uid, gid = ctypes.c_uint(), ctypes.c_uint()
    libc = ctypes.CDLL(None, use_errno=True)
    if not hasattr(libc, 'getpeereid') or libc.getpeereid(sock.fileno(), ctypes.byref(uid), ctypes.byref(gid)):
        raise OSError('Unable to authenticate private socket peer')
    return uid.value


def private_directory():
    path = Path(os.environ.get('ACTIVITIES_BACKEND_SOCKET_DIR', f'/tmp/atl-{os.getuid()}'))
    path.mkdir(mode=0o700, parents=False, exist_ok=True)
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o700:
        raise ValueError('Backend socket directory must be an owned private directory (0700)')
    return path


def locked_file(path):
    fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    info = os.fstat(fd)
    if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o600:
        os.close(fd)
        raise ValueError('Backend lock must be an owned private file (0600)')
    return fd


def lease_available(path):
    """Wait out a retiring owner before spending a bounded backend start attempt."""
    fd = locked_file(path)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except BlockingIOError:
            return False
    finally:
        os.close(fd)


def backend_key(db, domain, misses, interpreter):
    """Hash small immutable sources and bindings once per proxy startup, never per RPC."""
    executable = Path(interpreter).expanduser().absolute()
    info = executable.stat()
    fingerprint = hashlib.sha256(json.dumps({
        'db': str(Path(db).expanduser().resolve()), 'domain': domain,
        'misses': str(Path(misses).expanduser().resolve()), 'interpreter': str(executable),
        'interpreter_stat': [info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns],
        'pythonpath': os.environ.get('PYTHONPATH', ''), 'pythonhome': os.environ.get('PYTHONHOME', ''),
    }, sort_keys=True).encode())
    sources = list(ROOT.glob('*.py')) + [ROOT / 'domains.json'] + list((ROOT / 'ui').glob('*'))
    # Bound virtualenv package metadata identifies dependency upgrades without importing
    # the SDK into each proxy or traversing package source trees.
    for site in (executable.parent.parent / 'lib').glob('python*/site-packages'):
        for package in ('mcp', 'anyio', 'pydantic', 'pydantic_core', 'PyYAML', 'starlette'):
            sources.extend(site.glob(package + '-*.dist-info/METADATA'))
    for source in sorted(sources):
        if source.is_file():
            fingerprint.update(str(source).encode())
            fingerprint.update(source.read_bytes())
    return fingerprint.hexdigest()[:32]


def connect(path):
    info = path.lstat()
    if not stat.S_ISSOCK(info.st_mode) or info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o600:
        raise ValueError('Backend socket must be an owned private socket (0600)')
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect(str(path))
        if peer_uid(sock) != os.getuid():
            raise PermissionError('Backend socket belongs to another user')
        return sock
    except BaseException:
        sock.close()
        raise


def connect_backend(db, domain, misses, interpreter):
    directory = private_directory()
    key = backend_key(db, domain, misses, interpreter)
    path = directory / (key + '.sock')
    if len(os.fsencode(path)) > 103:
        raise ValueError('Backend socket directory path is too long')
    fd = locked_file(directory / (key + '.start'))
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        process = None
        starts = 0
        deadline = time.monotonic() + 20
        while True:
            sock = None
            try:
                sock = connect(path)
                # Establish the binding before forwarding any caller MCP bytes.
                sock.settimeout(max(0.1, deadline - time.monotonic()))
                sock.sendall(json.dumps({'key': key, 'domain': domain}).encode() + b'\n')
                greeting = bytearray()
                while not greeting.endswith(b'\n'):
                    chunk = sock.recv(1)
                    if not chunk:
                        raise ConnectionResetError('Backend retired during session startup')
                    if len(greeting) >= 1024:
                        raise RuntimeError('Invalid backend session greeting')
                    greeting.extend(chunk)
                response = json.loads(greeting)
                if response.get('ready') is not True:
                    raise RuntimeError(response.get('error', 'Backend rejected session'))
                sock.settimeout(None)
                return sock
            except (FileNotFoundError, ConnectionRefusedError, ConnectionResetError, BrokenPipeError):
                if sock is not None:
                    sock.close()
                if time.monotonic() >= deadline:
                    raise RuntimeError('Backend startup failed; verify bound interpreter and catalog')
                if process is not None and process.poll() not in (None, 0):
                    raise RuntimeError('Backend startup failed (exit ' + str(process.returncode) + '); verify bound interpreter and catalog')
                if starts < 2 and (process is None or process.poll() is not None) and lease_available(path.with_suffix('.lease')):
                    process = subprocess.Popen([
                        str(interpreter), '-B', str(ROOT / 'shared_backend.py'),
                        '--db', str(db), '--domain', domain, '--misses', str(misses),
                        '--socket', str(path), '--key', key,
                    ], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL, start_new_session=True, close_fds=True)
                    starts += 1
                time.sleep(0.05)
            except BaseException:
                if sock is not None:
                    sock.close()
                raise
    finally:
        os.close(fd)


def bridge(sock, stdin_fd=0, stdout_fd=1):
    """Bounded byte forwarding, including half-close and response drain on stdin EOF."""
    incoming, outgoing = bytearray(), bytearray()
    input_open = network_open = True
    input_shutdown = False
    sock.setblocking(False)
    original = {fd: os.get_blocking(fd) for fd in (stdin_fd, stdout_fd)}
    for fd in original:
        os.set_blocking(fd, False)
    selector = selectors.DefaultSelector()
    try:
        while network_open or outgoing:
            desired = {}
            if input_open and network_open and len(incoming) < BUFFER_LIMIT:
                desired[stdin_fd] = selectors.EVENT_READ
            if outgoing:
                desired[stdout_fd] = selectors.EVENT_WRITE
            events = (selectors.EVENT_READ if network_open and len(outgoing) < BUFFER_LIMIT else 0)
            if incoming and network_open:
                events |= selectors.EVENT_WRITE
            if events:
                desired[sock] = events
            for registered in list(selector.get_map().values()):
                if registered.fileobj not in desired:
                    selector.unregister(registered.fileobj)
            for fileobj, mask in desired.items():
                if fileobj in selector.get_map():
                    selector.modify(fileobj, mask)
                else:
                    selector.register(fileobj, mask)
            if not input_open and not incoming and not input_shutdown and network_open:
                sock.shutdown(socket.SHUT_WR)
                input_shutdown = True
            for selected, ready in selector.select():
                if selected.fileobj == stdin_fd:
                    data = os.read(stdin_fd, min(CHUNK, BUFFER_LIMIT - len(incoming)))
                    if data:
                        incoming.extend(data)
                    else:
                        input_open = False
                elif selected.fileobj == stdout_fd:
                    try:
                        written = os.write(stdout_fd, outgoing[:CHUNK])
                        del outgoing[:written]
                    except BlockingIOError:
                        pass
                else:
                    if ready & selectors.EVENT_READ:
                        try:
                            data = sock.recv(min(CHUNK, BUFFER_LIMIT - len(outgoing)))
                            if data:
                                outgoing.extend(data)
                            else:
                                network_open = False
                                incoming.clear()
                        except BlockingIOError:
                            pass
                    if ready & selectors.EVENT_WRITE and network_open and incoming:
                        try:
                            written = sock.send(incoming[:CHUNK])
                            del incoming[:written]
                        except BlockingIOError:
                            pass
        if input_open:
            raise RuntimeError('Backend disconnected before stdin EOF; pending request outcome is unknown')
    finally:
        selector.close()
        for fd, blocking in original.items():
            os.set_blocking(fd, blocking)
        sock.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', type=Path, required=True)
    parser.add_argument('--domain', required=True)
    parser.add_argument('--misses', type=Path, required=True)
    parser.add_argument('--interpreter', type=Path, required=True)
    args = parser.parse_args()
    try:
        bridge(connect_backend(args.db, args.domain, args.misses, args.interpreter))
    except (OSError, ValueError, RuntimeError) as exc:
        print('Activities Templates transport unavailable: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
