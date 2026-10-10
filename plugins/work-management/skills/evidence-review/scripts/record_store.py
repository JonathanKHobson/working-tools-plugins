"""Confirmation-gated immutable revisions in an explicitly selected project directory."""
import json
import os
import tempfile
from pathlib import Path
from card_model import canonical, digest, require, validate_card


def checked_store(project_root, store):
    root = Path(project_root).expanduser().resolve(strict=True)
    require(root.is_dir(), 'Project root must be an existing directory')
    target = Path(store).expanduser().absolute()
    root_argument = Path(project_root).expanduser().absolute()
    if target.is_relative_to(root_argument):
        target = root / target.relative_to(root_argument)
    elif not target.is_relative_to(root):
        # A system path alias may spell the selected root differently, e.g. /var.
        for ancestor in target.parents:
            if ancestor.exists() and ancestor.resolve() == root:
                target = root / target.relative_to(ancestor)
                break
    require(target.is_relative_to(root) and target != root, 'Store must be inside the selected project')
    relative = target.relative_to(root)
    current = root
    for part in relative.parts:
        require(part not in {'.', '..'}, 'Invalid store path')
        current = current / part
        require(not current.is_symlink(), 'Symlinked record store refused')
        if current.exists():
            require(current.is_dir(), 'Record store parent is not a directory')
    return target


def atomic_write(path, value):
    descriptor, temp = tempfile.mkstemp(prefix='.pending-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'w') as stream:
            stream.write(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def save(card, project_root, store, opt_in=False, confirm=False):
    require(confirm is True, 'Saving a private record requires confirmation')
    card = validate_card(card, opt_in)
    target = checked_store(project_root, store)
    target.mkdir(parents=True, exist_ok=True, mode=0o700)
    checked_store(project_root, target)
    os.chmod(target, 0o700)
    lock = target / '.evidence-review.lock'
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
    except FileExistsError as error:
        raise ValueError('Record store is busy; inspect an interrupted owned lock before retrying') from error
    try:
        with os.fdopen(fd, 'w') as stream:
            stream.write(str(os.getpid()))
        folder = target / card['card_id']
        require(not folder.is_symlink(), 'Symlinked card directory refused')
        folder.mkdir(exist_ok=True, mode=0o700)
        revision = digest(card)
        path = folder / (revision + '.json')
        pointer = folder / 'latest.json'
        require(not path.is_symlink() and not pointer.is_symlink(), 'Symlinked record refused')
        if path.exists():
            require(json.loads(path.read_text()) == card, 'Stored revision integrity mismatch')
            return {'status': 'already_saved', 'record': str(path), 'card_id': card['card_id'], 'revision': revision}
        atomic_write(path, card)
        atomic_write(pointer, {'card_id': card['card_id'], 'revision': revision, 'record': path.name})
        return {'status': 'saved', 'record': str(path), 'card_id': card['card_id'], 'revision': revision}
    finally:
        lock.unlink(missing_ok=True)
