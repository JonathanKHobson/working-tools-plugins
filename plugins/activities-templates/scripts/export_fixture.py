#!/usr/bin/env python3
"""Export a synthetic scoped chooser for rendered checks without private data."""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
from fixtures import make_fixture
from catalog import Catalog, DOMAINS
from server import export_html


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--domain', choices=list(DOMAINS), default='facilitation')
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output.is_relative_to(ROOT):
        parser.error('Put fixture evidence outside the package')
    output.mkdir(parents=True, exist_ok=True)
    _, db = make_fixture(output / 'fixture-data')
    print(export_html(Catalog(db, args.domain), output / ('activities-' + args.domain + '-fixture.html')))


if __name__ == '__main__':
    main()
