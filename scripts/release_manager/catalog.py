"""Validate the durable release catalog and select verified stable releases."""

from __future__ import annotations

from functools import total_ordering
import re

SCHEMA_VERSION = 'working-tools.releases.v1'
_SEMVER = re.compile(r'^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$')
_DIGEST = re.compile(r'^[0-9a-f]{64}$')


@total_ordering
class SemVer:
    """SemVer 2.0 precedence; build metadata never affects ordering."""

    def __init__(self, value: str):
        if not isinstance(value, str) or not (match := _SEMVER.fullmatch(value)):
            raise ValueError(f'invalid SemVer: {value!r}')
        major, minor, patch, pre, build = match.groups()
        if pre and any(part.isdigit() and len(part) > 1 and part[0] == '0' for part in pre.split('.')):
            raise ValueError(f'invalid SemVer numeric prerelease identifier: {value!r}')
        self.value = value
        self.major, self.minor, self.patch = int(major), int(minor), int(patch)
        self.prerelease = tuple(pre.split('.')) if pre else ()
        self.build = tuple(build.split('.')) if build else ()

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'SemVer({self.value!r})'

    def __eq__(self, other):
        if not isinstance(other, SemVer):
            return NotImplemented
        return self._precedence() == other._precedence()

    def __lt__(self, other):
        if not isinstance(other, SemVer):
            return NotImplemented
        a, b = self._precedence(), other._precedence()
        if a[:3] != b[:3]:
            return a[:3] < b[:3]
        ap, bp = a[3], b[3]
        if not ap:
            return False
        if not bp:
            return True
        for left, right in zip(ap, bp):
            if left == right:
                continue
            ln, rn = left.isdigit(), right.isdigit()
            if ln != rn:
                return ln
            return int(left) < int(right) if ln else left < right
        return len(ap) < len(bp)

    def _precedence(self):
        return self.major, self.minor, self.patch, self.prerelease


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _valid_digest(value):
    return isinstance(value, str) and bool(_DIGEST.fullmatch(value))


def _complete_verified(release: dict) -> bool:
    verification = release.get('verification', {})
    assets = release.get('assets')
    return (isinstance(verification, dict) and isinstance(assets, list)
            and all(isinstance(asset, dict) for asset in assets)
            and verification.get('archive_verified') is True
            and verification.get('layout_verified') is True
            and bool(assets)
            and any(asset.get('role') == 'installation' and asset.get('name') ==
                    f'{release.get("product_id")}-{release.get("version")}.zip'
                    for asset in assets)
            and all(_nonempty(asset.get('url')) and type(asset.get('size')) is int
                    and asset['size'] > 0 and _valid_digest(asset.get('sha256'))
                    for asset in assets))


def _eligible(release: dict) -> bool:
    try:
        version = SemVer(release['version'])
    except (KeyError, ValueError, TypeError):
        return False
    return (not version.prerelease and release.get('channel') == 'stable'
            and release.get('distribution_status') == 'available'
            and _complete_verified(release))


def select_current(product: dict) -> dict | None:
    """Highest eligible SemVer, regardless of publication order or backports."""
    if product.get('kind') == 'external':
        return None
    records=product.get('releases')
    if not isinstance(records,list):
        return None
    releases = [row for row in records if isinstance(row, dict) and _eligible(row)]
    return max(releases, key=lambda row: (SemVer(row['version']), str(row.get('published_at') or ''), str(row.get('release_key') or '')), default=None)


def validate_catalog(catalog: dict) -> list[str]:
    """Return all catalog errors. No caller should replace a catalog on errors."""
    errors = []
    if not isinstance(catalog, dict) or catalog.get('schema_version') != SCHEMA_VERSION:
        return [f'schema_version must be {SCHEMA_VERSION}']
    products = catalog.get('products')
    if not isinstance(products, list):
        return ['products must be an array']
    ids, keys = set(), set()
    for i, product in enumerate(products):
        label = f'products[{i}]'
        if not isinstance(product, dict):
            errors.append(f'{label}: must be an object'); continue
        if product.get('kind') == 'external':
            errors.extend(_validate_external(product, label))
            ident = product.get('id')
            if isinstance(ident,str):
                if ident in ids:
                    errors.append(f'{label}: duplicate product id {ident}')
                ids.add(ident)
            for j, release in enumerate(product.get('releases', []) if isinstance(product.get('releases'),list) else []):
                if not isinstance(release,dict):
                    continue
                key=release.get('release_key')
                if not _nonempty(key):
                    errors.append(f'{label}.releases[{j}]: release_key must be nonempty text')
                elif key in keys:
                    errors.append(f'{label}.releases[{j}]: duplicate release_key {key}')
                else:
                    keys.add(key)
            continue
        for field in ('id', 'name', 'kind', 'repository', 'compatibility', 'upgrade_guidance'):
            if not _nonempty(product.get(field)):
                errors.append(f'{label}: {field} must be nonempty text')
        ident = product.get('id')
        if isinstance(ident,str):
            if ident in ids:
                errors.append(f'{label}: duplicate product id {ident}')
            ids.add(ident)
        releases = product.get('releases')
        if not isinstance(releases, list):
            errors.append(f'{label}: releases must be an array'); continue
        for j, release in enumerate(releases):
            at = f'{label}.releases[{j}]'
            if not isinstance(release, dict):
                errors.append(f'{at}: must be an object'); continue
            for field in ('release_key', 'product_id', 'version', 'git_tag', 'source_commit',
                          'published_at', 'release_url', 'channel', 'distribution_status',
                          'summary', 'notes', 'notes_provenance', 'compatibility', 'upgrade_guidance'):
                if not _nonempty(release.get(field)):
                    errors.append(f'{at}: {field} must be nonempty text')
            key = release.get('release_key')
            if isinstance(key,str):
                if key in keys:
                    errors.append(f'{at}: duplicate release_key {key}')
                keys.add(key)
            if release.get('product_id') != ident:
                errors.append(f'{at}: wrong product_id')
            try:
                SemVer(release.get('version'))
            except (ValueError, TypeError) as exc:
                errors.append(f'{at}: {exc}')
            if release.get('channel') not in ('stable', 'prerelease', 'draft'):
                errors.append(f'{at}: invalid channel')
            elif release.get('channel') == 'stable':
                try:
                    if SemVer(release.get('version')).prerelease:
                        errors.append(f'{at}: prerelease SemVer cannot use stable channel')
                except (ValueError, TypeError):
                    pass
            if release.get('distribution_status') not in ('available', 'prepared', 'draft', 'withdrawn', 'unavailable'):
                errors.append(f'{at}: invalid distribution_status')
            if not isinstance(release.get('assets'), list):
                errors.append(f'{at}: assets must be an array')
            else:
                asset_names = set()
                for k, asset in enumerate(release['assets']):
                    dest = f'{at}.assets[{k}]'
                    if not isinstance(asset, dict):
                        errors.append(f'{dest}: must be an object'); continue
                    for field in ('role', 'name', 'url'):
                        if not _nonempty(asset.get(field)):
                            errors.append(f'{dest}: {field} must be nonempty text')
                    if type(asset.get('size')) is not int or asset['size'] < 0:
                        errors.append(f'{dest}: invalid size')
                    if not _valid_digest(asset.get('sha256')):
                        errors.append(f'{dest}: invalid sha256')
                    name=asset.get('name')
                    if isinstance(name,str):
                        if name in asset_names:
                            errors.append(f'{dest}: duplicate asset name')
                        asset_names.add(name)
            verification = release.get('verification')
            if not isinstance(verification, dict) or any(type(verification.get(k)) is not bool for k in ('archive_verified', 'layout_verified')):
                errors.append(f'{at}: verification requires archive_verified and layout_verified booleans')
            if release.get('distribution_status') == 'available' and not _complete_verified(release):
                errors.append(f'{at}: available record lacks verified distribution evidence')
        current = select_current(product)
        expected = current['release_key'] if current else None
        if product.get('current_release_key') != expected:
            errors.append(f'{label}: current_release_key must be {expected!r}')
    return errors


def _validate_external(product: dict, label: str) -> list[str]:
    """External history is factual but never an installable current plugin."""
    errors = []
    for field in ('id', 'name'):
        if not _nonempty(product.get(field)):
            errors.append(f'{label}: {field} must be nonempty text')
    if product.get('channel') != 'legacy':
        errors.append(f'{label}: external channel must be legacy')
    if product.get('current_release_key') is not None:
        errors.append(f'{label}: external product cannot have current_release_key')
    releases = product.get('releases')
    if not isinstance(releases, list):
        return errors + [f'{label}: releases must be an array']
    for i, release in enumerate(releases):
        at = f'{label}.releases[{i}]'
        if not isinstance(release, dict):
            errors.append(f'{at}: must be an object'); continue
        scheme, value = release.get('version_scheme'), release.get('version')
        if scheme not in ('semver', 'revision', 'tag', 'unversioned'):
            errors.append(f'{at}: invalid version_scheme')
        elif scheme == 'semver':
            try:
                SemVer(value)
            except (ValueError, TypeError) as exc:
                errors.append(f'{at}: {exc}')
        elif value is not None and not _nonempty(value):
            errors.append(f'{at}: invalid version')
        if release.get('distribution_status') not in ('available', 'page-only', 'unavailable', 'withdrawn'):
            errors.append(f'{at}: invalid distribution_status')
        commit = release.get('source_commit')
        if commit is not None and (not isinstance(commit, str) or not re.fullmatch(r'[0-9a-f]{40}', commit)):
            errors.append(f'{at}: invalid source_commit')
        verification = release.get('verification')
        if not isinstance(verification, dict) or type(verification.get('download_verified')) is not bool or not _nonempty(verification.get('provenance')):
            errors.append(f'{at}: invalid verification')
        assets = release.get('assets')
        if not isinstance(assets, list):
            errors.append(f'{at}: assets must be an array'); continue
        for j, asset in enumerate(assets):
            dest = f'{at}.assets[{j}]'
            if not isinstance(asset, dict) or any(not _nonempty(asset.get(k)) for k in ('name', 'role', 'url')):
                errors.append(f'{dest}: name, role and url are required'); continue
            digest = asset.get('sha256')
            if digest is not None and not _valid_digest(digest):
                errors.append(f'{dest}: invalid sha256')
            if isinstance(verification, dict) and verification.get('download_verified') is True and digest is None:
                errors.append(f'{dest}: verified download requires sha256')
    return errors
