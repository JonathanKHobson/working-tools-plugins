"""Plan synchronized registry and host-manifest version edits in memory."""

from __future__ import annotations

import json
from pathlib import Path

from .catalog import SemVer


def version_edits(root: Path, product_id: str, version: str) -> dict[str, str]:
    """Return exact updated JSON text for the registry and three manifests.

    The caller must validate the complete transaction before writing. This
    function never mutates source files or marketplace projections.
    """
    SemVer(version)
    root = Path(root)
    locations = ['catalog/packages.json', f'plugins/{product_id}/plugin.json',
                 f'plugins/{product_id}/.codex-plugin/plugin.json',
                 f'plugins/{product_id}/.claude-plugin/plugin.json']
    documents = {name: json.loads((root/name).read_text()) for name in locations}
    rows = [row for row in documents[locations[0]]['packages'] if row['id'] == product_id]
    if len(rows) != 1:
        raise ValueError(f'{product_id}: registry identity missing or duplicated')
    old = rows[0]['version']
    if SemVer(version) <= SemVer(old):
        raise ValueError(f'{product_id}: version must increase from {old}')
    for name in locations[1:]:
        document = documents[name]
        if document.get('name') != product_id or document.get('version') != old:
            raise ValueError(f'{name}: identity or baseline version mismatch')
        document['version'] = version
    rows[0]['version'] = version
    return {name: json.dumps(document, indent=2, ensure_ascii=False) + '\n'
            for name, document in documents.items()}
