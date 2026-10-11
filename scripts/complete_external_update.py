"""Complete one independently hosted guide update from its owning source repo."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path

from release_manager.legacy import complete_active_external_update, load_external_products


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--product', required=True, help='Registered active guide product ID')
    parser.add_argument('--checkout', required=True, type=Path, help='Owning public source checkout')
    parser.add_argument('--catalog', type=Path, default=Path('catalog/external-products.json'))
    parser.add_argument('--notes-dir', type=Path, default=Path('catalog/external-changes'))
    parser.add_argument('--branch', default='main', help='Owning source publication branch')
    parser.add_argument('--publish', action='store_true', help='Push, publish, verify and advance the ledger')
    args = parser.parse_args()
    if not args.publish:
        parser.error('Publication is explicit; pass --publish after the authored note and source commit are ready')
    original = load_external_products(args.catalog)
    updated = complete_active_external_update(original, args.product, args.checkout,
                                               args.notes_dir, branch=args.branch)
    args.catalog.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.external-products-', suffix='.json', dir=args.catalog.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            json.dump(updated, handle, indent=2, ensure_ascii=False)
            handle.write('\n')
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, args.catalog)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    product = next(p for p in updated['products'] if p['id'] == args.product)
    print(json.dumps({'product_id': args.product, 'source_commit': product['source']['commit'],
                      'distribution': product['disposition'], 'catalog': str(args.catalog)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
