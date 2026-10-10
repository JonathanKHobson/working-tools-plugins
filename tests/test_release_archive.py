"""Unit tests for scripts/release_archive.py.

The module under test is imported by file path via importlib, relative to
this test file's location, as required for this repository layout.
"""

import hashlib
import importlib.util
import io
import pathlib
import stat
import struct
import tempfile
import unittest
import zipfile
from unittest import mock

_THIS_FILE = pathlib.Path(__file__).resolve()
_REPO_ROOT = _THIS_FILE.parent.parent
_MODULE_PATH = _REPO_ROOT / 'scripts' / 'release_archive.py'

_spec = importlib.util.spec_from_file_location('release_archive', _MODULE_PATH)
release_archive = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(release_archive)


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _make_zip(path: pathlib.Path, files: dict, *, extra_setup=None) -> None:
    """Write a zip to path with the given {name: bytes} content.

    extra_setup, if given, is called with the open ZipFile before closing,
    allowing tests to tweak individual ZipInfo entries (e.g. symlink mode
    bits or declared sizes) without writing giant payloads.
    """
    with zipfile.ZipFile(path, 'w') as zf:
        for name, data in files.items():
            zf.writestr(name, data)
        if extra_setup is not None:
            extra_setup(zf)


class VerifyArchiveTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmpdir = pathlib.Path(self._tmpdir.name)

    def tearDown(self):
        self._tmpdir.cleanup()

    def test_synthetic_success(self):
        zip_path = self.tmpdir / 'release.zip'
        payload_a = b'print("hello plugin")\n'
        payload_b = b'{"name": "plugin"}'
        _make_zip(zip_path, {'main.py': payload_a, 'manifest.json': payload_b})

        expected_files = {
            'main.py': _sha256_hex(payload_a),
            'manifest.json': _sha256_hex(payload_b),
        }
        result = release_archive.verify_archive(zip_path, expected_files)
        self.assertTrue(result['passed'], result['errors'])
        self.assertEqual(result['errors'], [])
        self.assertTrue(len(result['sha256']) == 64)

    def test_changed_expected_payload(self):
        zip_path = self.tmpdir / 'release.zip'
        payload = b'original content'
        _make_zip(zip_path, {'main.py': payload})

        expected_files = {'main.py': _sha256_hex(b'different content')}
        result = release_archive.verify_archive(zip_path, expected_files)
        self.assertFalse(result['passed'])
        self.assertTrue(any('content hash mismatch' in e for e in result['errors']))

    def test_missing_required_reference(self):
        zip_path = self.tmpdir / 'release.zip'
        payload = b'content'
        _make_zip(zip_path, {'main.py': payload})

        expected_files = {
            'main.py': _sha256_hex(payload),
            'required.txt': _sha256_hex(b'anything'),
        }
        result = release_archive.verify_archive(zip_path, expected_files)
        self.assertFalse(result['passed'])
        self.assertTrue(any('missing required file' in e for e in result['errors']))

    def test_unexpected_member(self):
        zip_path = self.tmpdir / 'release.zip'
        payload = b'content'
        extra = b'sneaky'
        _make_zip(zip_path, {'main.py': payload, 'extra.py': extra})

        expected_files = {'main.py': _sha256_hex(payload)}
        result = release_archive.verify_archive(zip_path, expected_files)
        self.assertFalse(result['passed'])
        self.assertTrue(any('unexpected member' in e for e in result['errors']))

    def test_wrong_archive_hash(self):
        zip_path = self.tmpdir / 'release.zip'
        payload = b'content'
        _make_zip(zip_path, {'main.py': payload})

        expected_files = {'main.py': _sha256_hex(payload)}
        wrong_archive_hash = '0' * 64
        result = release_archive.verify_archive(zip_path, expected_files, wrong_archive_hash)
        self.assertFalse(result['passed'])
        self.assertTrue(any('archive sha256 mismatch' in e for e in result['errors']))

    def test_duplicate_member(self):
        zip_path = self.tmpdir / 'release.zip'
        payload = b'content'
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr('main.py', payload)
            zf.writestr('main.py', payload)

        expected_files = {'main.py': _sha256_hex(payload)}
        result = release_archive.verify_archive(zip_path, expected_files)
        self.assertFalse(result['passed'])
        self.assertTrue(any('duplicate member name' in e for e in result['errors']))

    def test_path_traversal(self):
        zip_path = self.tmpdir / 'release.zip'
        payload = b'content'
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr('../escape.py', payload)

        expected_files = {'../escape.py': _sha256_hex(payload)}
        result = release_archive.verify_archive(zip_path, expected_files)
        self.assertFalse(result['passed'])
        # The manifest itself is also invalid since it contains a traversal path.
        self.assertTrue(any('traversal' in e for e in result['errors']))

    def test_path_traversal_in_archive_only(self):
        zip_path = self.tmpdir / 'release.zip'
        payload = b'content'
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr('good.py', payload)
            zf.writestr('../escape.py', b'malicious')

        expected_files = {'good.py': _sha256_hex(payload)}
        result = release_archive.verify_archive(zip_path, expected_files)
        self.assertFalse(result['passed'])
        self.assertTrue(any('traversal' in e for e in result['errors']))

    def test_symlink_member(self):
        zip_path = self.tmpdir / 'release.zip'
        payload = b'content'

        def add_symlink(zf):
            info = zipfile.ZipInfo('link.py')
            mode = (stat.S_IFLNK | 0o777) << 16
            info.external_attr = mode
            zf.writestr(info, b'/etc/passwd')

        _make_zip(zip_path, {'main.py': payload}, extra_setup=add_symlink)

        expected_files = {'main.py': _sha256_hex(payload)}
        result = release_archive.verify_archive(zip_path, expected_files)
        self.assertFalse(result['passed'])
        self.assertTrue(any('symbolic link' in e for e in result['errors']))

    def test_corrupt_zip(self):
        zip_path = self.tmpdir / 'release.zip'
        zip_path.write_bytes(b'this is not a valid zip file at all')

        expected_files = {'main.py': _sha256_hex(b'content')}
        result = release_archive.verify_archive(zip_path, expected_files)
        self.assertFalse(result['passed'])
        self.assertTrue(any('not a valid zip' in e for e in result['errors']))

    def test_invalid_expected_digest(self):
        zip_path = self.tmpdir / 'release.zip'
        payload = b'content'
        _make_zip(zip_path, {'main.py': payload})

        expected_files = {'main.py': 'not-a-valid-hex-digest'}
        result = release_archive.verify_archive(zip_path, expected_files)
        self.assertFalse(result['passed'])
        self.assertTrue(any('invalid expected digest' in e for e in result['errors']))

    def test_declared_oversized_member_without_giant_payload(self):
        zip_path = self.tmpdir / 'release.zip'
        small_payload = b'tiny'

        def inflate_declared_size(zf):
            # Patch the declared uncompressed size after writing a tiny
            # payload, so no large allocation ever occurs in this test.
            for info in zf.infolist():
                if info.filename == 'big.py':
                    info.file_size = release_archive.MAX_FILE_UNCOMPRESSED_BYTES + 1

        _make_zip(zip_path, {'big.py': small_payload}, extra_setup=inflate_declared_size)

        expected_files = {'big.py': _sha256_hex(small_payload)}
        result = release_archive.verify_archive(zip_path, expected_files)
        self.assertFalse(result['passed'])
        self.assertTrue(any('exceeds per-file size limit' in e for e in result['errors']))

    def test_nonexistent_archive(self):
        missing_path = self.tmpdir / 'does_not_exist.zip'
        expected_files = {'main.py': _sha256_hex(b'content')}
        result = release_archive.verify_archive(missing_path, expected_files)
        self.assertFalse(result['passed'])
        self.assertTrue(any('does not exist' in e for e in result['errors']))

    def test_backslash_separator_rejected(self):
        zip_path = self.tmpdir / 'release.zip'
        payload = b'content'
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr('dir\\file.py', payload)

        expected_files = {'dir\\file.py': _sha256_hex(payload)}
        result = release_archive.verify_archive(zip_path, expected_files)
        self.assertFalse(result['passed'])
        self.assertTrue(any('backslash' in e for e in result['errors']))

    def test_directory_entry_rejected(self):
        zip_path = self.tmpdir / 'release.zip'
        payload = b'content'
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr('somedir/', b'')
            zf.writestr('somedir/main.py', payload)

        expected_files = {'somedir/main.py': _sha256_hex(payload)}
        result = release_archive.verify_archive(zip_path, expected_files)
        self.assertFalse(result['passed'])
        self.assertTrue(any('directory entry' in e for e in result['errors']))

    def test_encrypted_member_rejected(self):
        zip_path = self.tmpdir / 'release.zip'
        _make_zip(zip_path, {'main.py': b'content'})
        # Python's ZIP writer does not encrypt. Alter both real headers so
        # the reader sees a declared encrypted member without any secret data.
        data = bytearray(zip_path.read_bytes())
        local = data.index(b'PK\x03\x04')
        central = data.index(b'PK\x01\x02')
        data[local + 6] |= 1
        data[central + 8] |= 1
        zip_path.write_bytes(data)

        expected_files = {'main.py': _sha256_hex(b'content')}
        result = release_archive.verify_archive(zip_path, expected_files)
        self.assertFalse(result['passed'])
        self.assertTrue(any('encrypted' in e for e in result['errors']))

    def test_trailing_newline_digest_is_invalid(self):
        path = self.tmpdir / 'release.zip'
        _make_zip(path, {'main.py': b'content'})
        result = release_archive.verify_archive(path, {'main.py': _sha256_hex(b'content') + '\n'})
        self.assertFalse(result['passed'])

    def test_windows_drive_path_is_invalid(self):
        path = self.tmpdir / 'release.zip'
        _make_zip(path, {'C:/outside.py': b'content'})
        result = release_archive.verify_archive(path, {'C:/outside.py': _sha256_hex(b'content')})
        self.assertFalse(result['passed'])

    def test_directory_mode_without_slash_is_rejected(self):
        path = self.tmpdir / 'release.zip'
        info = zipfile.ZipInfo('pretend.py')
        info.create_system = 3
        info.external_attr = (stat.S_IFDIR | 0o755) << 16
        with zipfile.ZipFile(path, 'w') as archive:
            archive.writestr(info, b'content')
        result = release_archive.verify_archive(path, {'pretend.py': _sha256_hex(b'content')})
        self.assertFalse(result['passed'])


if __name__ == '__main__':
    unittest.main()
