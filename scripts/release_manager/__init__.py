"""Read-only release evidence, version selection, and package change planning."""

from .catalog import SemVer, select_current, validate_catalog
from .changes import changed_products, propose_version, evidence_notes
from .inventory import expected_package_files
from .versions import version_edits


def import_history(*args, **kwargs):
    """Load the network importer only when requested, including CLI execution."""
    from .history import import_history as run
    return run(*args, **kwargs)

__all__ = [
    'SemVer', 'select_current', 'validate_catalog', 'changed_products',
    'propose_version', 'evidence_notes', 'import_history',
    'expected_package_files', 'version_edits',
]
