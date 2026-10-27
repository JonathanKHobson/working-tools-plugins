"""Descriptor-relative no-follow filesystem boundary for optional local utilities.

Unsupported platforms fail closed instead of substituting race-prone pathname IO.
"""

from contextlib import contextmanager
import os
from pathlib import Path
import stat

SUPPORTED = (os.name == "posix" and hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_DIRECTORY")
             and all(call in os.supports_dir_fd for call in (os.open, os.mkdir, os.rename, os.unlink))
             and os.scandir in os.supports_fd)


def require_supported():
    if not SUPPORTED:
        raise ValueError("safe descriptor-relative filesystem operations are unavailable on this platform")


def parts(relative):
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError("a nonempty relative path without parent traversal is required")
    return path.parts


@contextmanager
def directory_at(parent, relative, *, create=False):
    """Hold a directory inode, refusing symlinks at every path component."""
    require_supported()
    current = os.dup(parent)
    try:
        for name in parts(relative):
            flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
            try:
                child = os.open(name, flags, dir_fd=current)
            except FileNotFoundError:
                if not create:
                    raise
                try:
                    os.mkdir(name, mode=0o700, dir_fd=current)
                except FileExistsError:
                    pass
                child = os.open(name, flags, dir_fd=current)
            os.close(current)
            current = child
        yield current
    finally:
        os.close(current)


@contextmanager
def directory(path, *, create=False):
    require_supported()
    absolute = Path(os.path.abspath(path))
    anchor = os.open(absolute.anchor, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        relative = absolute.relative_to(absolute.anchor)
        if str(relative) == ".":
            yield anchor
        else:
            with directory_at(anchor, relative, create=create) as descriptor:
                yield descriptor
    finally:
        os.close(anchor)


def read_at(parent, relative, limit):
    names = parts(relative)

    def read(descriptor):
        opened = os.open(names[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=descriptor)
        with os.fdopen(opened, "rb") as handle:
            before = os.fstat(handle.fileno())
            if not stat.S_ISREG(before.st_mode):
                raise ValueError("only regular files may be read")
            value = handle.read(limit + 1)
            after = os.fstat(handle.fileno())
            if (before.st_mtime_ns, before.st_size) != (after.st_mtime_ns, after.st_size):
                raise ValueError("file changed while reading")
            return value, after

    if len(names) == 1:
        return read(parent)
    with directory_at(parent, Path(*names[:-1])) as descriptor:
        return read(descriptor)
