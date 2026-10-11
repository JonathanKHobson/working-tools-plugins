# SPDX-License-Identifier: AGPL-3.0-only
"""Bounded per-scope records. No prompt, workspace, IDs or review prose stored."""
from __future__ import annotations

import contextlib
import fcntl
import hashlib
import json
import os
import stat
import time
from pathlib import Path

from quality_rules import OBLIGATION_ORDER

MAX_BYTES = 64_000
SCHEMA = 1


class StateError(ValueError):
    pass


def scope_key(payload):
    """Prefer session continuity; turn ID is used only without a session ID."""
    if not isinstance(payload, dict):
        return None
    for kind in ('session_id', 'turn_id'):
        value = payload.get(kind)
        if isinstance(value, str) and 0 < len(value.strip()) <= 512:
            return hashlib.sha256((kind + '\0' + value.strip()).encode()).hexdigest()
    return None


def validate_key(key):
    if not isinstance(key, str) or len(key) != 64 or any(c not in '0123456789abcdef' for c in key):
        raise StateError('A scoped identifier is required')


@contextlib.contextmanager
def state_directory(path):
    """Open every component with NOFOLLOW; create only the final directory."""
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts or path == Path('/'):
        raise StateError('State directory must be a dedicated absolute path')
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = os.open('/', flags)
    try:
        for index, part in enumerate(path.parts[1:]):
            try:
                next_fd = os.open(part, flags, dir_fd=fd)
            except FileNotFoundError:
                if index != len(path.parts) - 2:
                    raise StateError('State parent directory must exist')
                try:
                    os.mkdir(part, 0o700, dir_fd=fd)
                except FileExistsError:
                    pass
                next_fd = os.open(part, flags, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        info = os.fstat(fd)
        if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o700:
            raise StateError('State directory must be owned by this user with mode 0700')
        yield fd
    finally:
        os.close(fd)


def open_private_file(directory_fd, name, flags):
    fd = os.open(name, flags | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600, dir_fd=directory_fd)
    try:
        info = os.fstat(fd)
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                or info.st_nlink != 1 or stat.S_IMODE(info.st_mode) != 0o600):
            raise StateError('State file must be an owned private regular file')
        return fd
    except BaseException:
        os.close(fd)
        raise


def validate_record(value):
    if not isinstance(value, dict) or set(value) != {'schema_version', 'updated_at', 'obligations'}:
        raise StateError('Invalid state schema')
    if value['schema_version'] != SCHEMA or not isinstance(value['updated_at'], int):
        raise StateError('Invalid state version')
    obligations = value['obligations']
    if not isinstance(obligations, dict) or any(k not in OBLIGATION_ORDER for k in obligations):
        raise StateError('Invalid obligations')
    for record in obligations.values():
        if not isinstance(record, dict) or record not in (
            {'status': 'pending'}, {'status': 'done', 'attested': True},
            {'status': 'skipped', 'reason_supplied': True},
        ):
            raise StateError('Invalid obligation status')
    return value


class ScopeStore:
    def __init__(self, directory, key):
        validate_key(key)
        self.directory, self.key = directory, key

    @contextlib.contextmanager
    def transaction(self):
        with state_directory(self.directory) as directory_fd:
            lock_fd = open_private_file(directory_fd, self.key + '.lock', os.O_CREAT | os.O_RDWR)
            try:
                # Nonblocking lock keeps a damaged or busy hook from hanging a turn.
                fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                yield directory_fd
            finally:
                os.close(lock_fd)

    def _read(self, directory_fd):
        try:
            fd = open_private_file(directory_fd, self.key + '.json', os.O_RDONLY)
        except FileNotFoundError:
            return None
        try:
            with os.fdopen(fd, 'rb') as handle:
                raw = handle.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise StateError('Oversized state')
            return validate_record(json.loads(raw))
        except (ValueError, UnicodeError, RecursionError) as error:
            raise StateError('Invalid state') from error

    def _write(self, directory_fd, value):
        validate_record(value)
        # Lock serializes a scope. Truncation occurs only after checking the file.
        fd = open_private_file(directory_fd, self.key + '.json', os.O_CREAT | os.O_WRONLY)
        with os.fdopen(fd, 'wb') as handle:
            os.ftruncate(handle.fileno(), 0)
            handle.write(json.dumps(value, sort_keys=True).encode() + b'\n')
            handle.flush()
            os.fsync(handle.fileno())

    def read(self):
        with self.transaction() as directory_fd:
            return self._read(directory_fd)

    def detect(self, obligations):
        value = {'schema_version': SCHEMA, 'updated_at': int(time.time()),
                 'obligations': {name: {'status': 'pending'} for name in obligations}}
        with self.transaction() as directory_fd:
            self._write(directory_fd, value)
        return value

    def update(self, name, status):
        with self.transaction() as directory_fd:
            value = self._read(directory_fd)
            if value is None or name not in value['obligations']:
                raise StateError('Check was not detected in this scope')
            value['obligations'][name] = ({'status': 'done', 'attested': True} if status == 'done'
                                        else {'status': 'skipped', 'reason_supplied': True})
            value['updated_at'] = int(time.time())
            self._write(directory_fd, value)
        return value

    def clear(self):
        with self.transaction() as directory_fd:
            # Validate before unlinking: do not remove a suspicious file.
            if self._read(directory_fd) is not None:
                os.unlink(self.key + '.json', dir_fd=directory_fd)


def pending(value):
    return [name for name in OBLIGATION_ORDER if value and
            value['obligations'].get(name, {}).get('status') == 'pending']
