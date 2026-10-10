import errno
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from video_workflow import provenance
from video_workflow.provenance import verify_relative_inventory


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_template_bundle.py"


def create_link(link, target, *, hard=False, directory=False):
    try:
        if hard:
            os.link(target, link)
        else:
            link.symlink_to(target, target_is_directory=directory)
    except OSError as exc:
        unsupported = {errno.EACCES, errno.EPERM, errno.ENOSYS, errno.ENOTSUP, errno.EOPNOTSUPP}
        if exc.errno in unsupported or getattr(exc, "winerror", None) == 1314:
            pytest.skip(f"Link creation unavailable on this platform: {exc}")
        raise


def require_case_insensitive(root):
    alias = root.with_name(root.name.upper())
    if not alias.exists() or not alias.samefile(root):
        pytest.skip("Regression requires a case-insensitive filesystem")
    return alias


def entry(root, name):
    path = root / name
    return {
        "path": name,
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def codes(report):
    return {issue["code"] for issue in report["issues"]}


def run_cli(root, manifest, output=None):
    command = [sys.executable, str(SCRIPT), str(root), str(manifest)]
    if output is not None:
        command.extend(["--output", str(output)])
    return subprocess.run(command, capture_output=True, text=True, check=False)


def bundle(tmp_path):
    root = tmp_path / "bundle"
    root.mkdir()
    (root / "scene.js").write_bytes(b"scene")
    (root / "sprite.png").write_bytes(b"asset")
    records = [entry(root, name) for name in ("scene.js", "sprite.png")]
    manifest = tmp_path / "inventory.json"
    manifest.write_text(json.dumps({"files": records}))
    return root, manifest, records


def test_valid_bundle_is_read_only_and_detects_changed_asset(tmp_path):
    root, _, records = bundle(tmp_path)
    before = {path.name: path.read_bytes() for path in root.iterdir()}
    report = verify_relative_inventory(root, records, required_paths=["scene.js", "sprite.png"])
    assert report["passed"]
    assert before == {path.name: path.read_bytes() for path in root.iterdir()}
    (root / "sprite.png").write_bytes(b"other")
    report = verify_relative_inventory(root, records)
    assert not report["passed"]
    assert "hash-mismatch" in codes(report)


def test_required_file_not_declared_and_missing_file(tmp_path):
    (tmp_path / "scene.js").write_bytes(b"scene")
    records = [entry(tmp_path, "scene.js")]
    report = verify_relative_inventory(tmp_path, records, required_paths=["score.wav"])
    assert codes(report) == {"required-entry-missing"}
    (tmp_path / "scene.js").unlink()
    assert codes(verify_relative_inventory(tmp_path, records)) == {"missing-file"}


@pytest.mark.parametrize("bad", ["../outside", "/absolute", "C:\\outside", "a/../../outside"])
def test_nonportable_or_escaping_path_refused(tmp_path, bad):
    report = verify_relative_inventory(tmp_path, [{"path": bad, "sha256": "0" * 64}])
    assert codes(report) == {"unsafe-path"}


def test_external_symlink_refused_without_read(tmp_path, monkeypatch):
    root = tmp_path / "bundle"
    root.mkdir()
    outside = tmp_path / "secret"
    outside.write_bytes(b"private")
    create_link(root / "link", outside)

    def unexpected_read(path):
        pytest.fail(f"Unexpected read of {path}")

    monkeypatch.setattr(provenance, "hash_file", unexpected_read)
    assert codes(verify_relative_inventory(root, [{"path": "link", "sha256": "0" * 64}])) == {"unsafe-path"}


@pytest.mark.parametrize("name", ["Assets/sprite.png", "assets/Sprite.png"])
def test_case_alias_inventory_path_refused_without_read(tmp_path, monkeypatch, name):
    root = tmp_path / "bundle"
    (root / "assets").mkdir(parents=True)
    require_case_insensitive(root)
    (root / "assets" / "sprite.png").write_bytes(b"asset")
    record = {**entry(root, "assets/sprite.png"), "path": name}

    def unexpected_read(path):
        pytest.fail(f"Unexpected read of case alias {path}")

    monkeypatch.setattr(provenance, "hash_file", unexpected_read)
    report = verify_relative_inventory(root, [record])
    assert codes(report) == {"case-mismatch"}
    assert report["verifiedFiles"] == []


@pytest.mark.parametrize("hard", [False, True])
def test_distinct_declared_link_paths_are_valid(tmp_path, hard):
    (tmp_path / "scene.js").write_bytes(b"scene")
    create_link(tmp_path / "scene-copy.js", tmp_path / "scene.js", hard=hard)
    records = [entry(tmp_path, name) for name in ("scene.js", "scene-copy.js")]
    report = verify_relative_inventory(tmp_path, records)
    assert report["passed"]
    assert report["verifiedFiles"] == ["scene.js", "scene-copy.js"]


@pytest.mark.parametrize("error_code", [errno.EACCES, errno.EPERM, errno.ENOSYS, errno.ENOTSUP])
def test_link_setup_skips_only_platform_limitations(tmp_path, monkeypatch, error_code):
    def failed_link(*args):
        raise OSError(error_code, "Fixture platform limitation")

    monkeypatch.setattr(os, "link", failed_link)
    with pytest.raises(pytest.skip.Exception):
        create_link(tmp_path / "link", tmp_path / "target", hard=True)


@pytest.mark.parametrize("error_code", [errno.EEXIST, errno.ENOENT, errno.EIO])
def test_link_setup_propagates_unexpected_errors(tmp_path, monkeypatch, error_code):
    def failed_link(*args):
        raise OSError(error_code, "Fixture unexpected error")

    monkeypatch.setattr(os, "link", failed_link)
    with pytest.raises(OSError) as error:
        create_link(tmp_path / "link", tmp_path / "target", hard=True)
    assert error.value.errno == error_code


def test_duplicate_invalid_digest_and_empty_declaration(tmp_path):
    (tmp_path / "a").write_bytes(b"a")
    record = entry(tmp_path, "a")
    assert codes(verify_relative_inventory(tmp_path, [record, record])) == {"duplicate-entry"}
    assert codes(verify_relative_inventory(tmp_path, [{"path": "a", "sha256": "unknown"}])) == {"invalid-sha256"}
    assert codes(verify_relative_inventory(tmp_path, [])) == {"empty-inventory"}


@pytest.mark.parametrize("records", [None, 7, "files", {"path": "a"}])
def test_invalid_inventory_reports_issue(tmp_path, records):
    assert codes(verify_relative_inventory(tmp_path, records)) == {"invalid-inventory"}


@pytest.mark.parametrize("record", [None, 7, {"path": None}, {"path": ""}, {"path": "."}, {"path": "a\0b"}])
def test_malformed_record_reports_issue(tmp_path, record):
    report = verify_relative_inventory(tmp_path, [record])
    assert not report["passed"]
    assert codes(report) == {"unsafe-path"}
    json.dumps(report)


@pytest.mark.parametrize("size", [True, -1, "5", 5.0, None])
def test_malformed_size_refused(tmp_path, size):
    (tmp_path / "a").write_bytes(b"a")
    record = entry(tmp_path, "a")
    record["bytes"] = size
    assert codes(verify_relative_inventory(tmp_path, [record])) == {"invalid-bytes"}


def test_size_mismatch_does_not_mark_file_verified(tmp_path):
    (tmp_path / "a").write_bytes(b"a")
    record = entry(tmp_path, "a")
    record["bytes"] = 2
    report = verify_relative_inventory(tmp_path, [record])
    assert codes(report) == {"size-mismatch"}
    assert report["verifiedFiles"] == []


@pytest.mark.parametrize("required", [None, "scene.js", 1, {}])
def test_invalid_required_paths_report_issue(tmp_path, required):
    root, _, records = bundle(tmp_path)
    assert codes(verify_relative_inventory(root, records, required_paths=required)) == {"invalid-required-paths"}


def test_required_paths_normalized_and_unsafe_paths_reported(tmp_path):
    root, _, records = bundle(tmp_path)
    assert verify_relative_inventory(root, records, required_paths=["./scene.js"])["passed"]
    assert codes(verify_relative_inventory(root, records, required_paths=["../outside"])) == {"unsafe-required-path"}
    alias = {**records[0], "path": "./scene.js"}
    assert codes(verify_relative_inventory(root, [records[0], alias])) == {"duplicate-entry"}


def test_directory_and_invalid_root_report_issue(tmp_path):
    assert codes(verify_relative_inventory(tmp_path, [{"path": "subdir", "sha256": "0" * 64}])) == {"missing-file"}
    (tmp_path / "subdir").mkdir()
    assert codes(verify_relative_inventory(tmp_path, [{"path": "subdir", "sha256": "0" * 64}])) == {"missing-file"}
    assert codes(verify_relative_inventory(tmp_path / "absent", [])) == {"invalid-root"}


def test_modification_during_hash_is_detected(tmp_path, monkeypatch):
    root, _, records = bundle(tmp_path)
    original_hash = provenance.hash_file

    def mutate_after_hash(path):
        digest = original_hash(path)
        if path.name == "scene.js":
            path.write_bytes(b"changed")
        return digest

    monkeypatch.setattr(provenance, "hash_file", mutate_after_hash)
    report = verify_relative_inventory(root, records)
    assert "changed-during-read" in codes(report)
    assert "scene.js" not in report["verifiedFiles"]


def test_earlier_entry_change_during_later_hash_is_detected(tmp_path, monkeypatch):
    root, _, records = bundle(tmp_path)
    original_hash = provenance.hash_file

    def change_earlier_file(path):
        if path.name == "sprite.png":
            (root / "scene.js").write_bytes(b"other")
        return original_hash(path)

    monkeypatch.setattr(provenance, "hash_file", change_earlier_file)
    report = verify_relative_inventory(root, records)
    assert not report["passed"]
    assert codes(report) == {"changed-during-verification"}
    assert report["verifiedFiles"] == ["sprite.png"]


def test_same_size_change_with_restored_mtime_is_detected(tmp_path, monkeypatch):
    root, _, records = bundle(tmp_path)
    target = root / "scene.js"
    before = target.stat()
    original_hash = provenance.hash_file

    def change_earlier_file(path):
        if path.name == "sprite.png":
            target.write_bytes(b"other")
            os.utime(target, ns=(before.st_atime_ns, before.st_mtime_ns))
        return original_hash(path)

    monkeypatch.setattr(provenance, "hash_file", change_earlier_file)
    assert "changed-during-verification" in codes(verify_relative_inventory(root, records))


def test_hash_io_failure_reports_issue(tmp_path, monkeypatch):
    root, _, records = bundle(tmp_path)

    def failed_read(path):
        raise PermissionError("Fixture read denied")

    monkeypatch.setattr(provenance, "hash_file", failed_read)
    report = verify_relative_inventory(root, records)
    assert not report["passed"]
    assert codes(report) == {"io-error"}
    assert report["verifiedFiles"] == []


def test_file_removed_before_final_recheck_is_detected(tmp_path, monkeypatch):
    root, _, records = bundle(tmp_path)
    original_hash = provenance.hash_file

    def remove_earlier_file(path):
        if path.name == "sprite.png":
            (root / "scene.js").unlink()
        return original_hash(path)

    monkeypatch.setattr(provenance, "hash_file", remove_earlier_file)
    assert "changed-during-verification" in codes(verify_relative_inventory(root, records))


def test_cli_success_and_failed_identity_reports(tmp_path):
    root, manifest, _ = bundle(tmp_path)
    output = tmp_path / "report.json"
    proc = run_cli(root, manifest, output)
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout) == json.loads(output.read_text())
    assert json.loads(proc.stdout)["passed"]
    (root / "scene.js").write_bytes(b"other")
    proc = run_cli(root, manifest)
    assert proc.returncode == 2
    assert "hash-mismatch" in codes(json.loads(proc.stdout))


@pytest.mark.parametrize("target", ["manifest", "manifest-symlink", "manifest-hardlink", "asset", "asset-symlink", "asset-hardlink", "unrelated", "dangling-symlink", "new-inside-root", "parent-alias", "case-alias-parent", "case-alias-ancestor"])
def test_cli_refuses_output_that_could_modify_inputs_or_existing_files(tmp_path, target):
    root, manifest, _ = bundle(tmp_path)
    asset = root / "scene.js"
    output = tmp_path / "report.json"
    if target == "manifest":
        output = manifest
    elif target == "asset":
        output = asset
    elif target.endswith("symlink") and target != "dangling-symlink":
        create_link(output, manifest if target.startswith("manifest") else asset)
    elif target.endswith("hardlink"):
        create_link(output, manifest if target.startswith("manifest") else asset, hard=True)
    elif target == "unrelated":
        output.write_bytes(b"keep this unrelated file")
    elif target == "dangling-symlink":
        create_link(output, tmp_path / "absent")
    elif target == "new-inside-root":
        output = root / "new-report.json"
    elif target == "parent-alias":
        alias = tmp_path / "alias"
        create_link(alias, root, directory=True)
        output = alias / "new-report.json"
    elif target.startswith("case-alias"):
        alias = require_case_insensitive(root)
        if target == "case-alias-ancestor":
            (root / "reports").mkdir()
            alias = alias / "reports"
        output = alias / "new-report.json"
    manifest_before, asset_before = manifest.read_bytes(), asset.read_bytes()
    unrelated_before = output.read_bytes() if target == "unrelated" else None
    proc = run_cli(root, manifest, output)
    assert proc.returncode == 2
    assert "Traceback" not in proc.stderr
    assert manifest.read_bytes() == manifest_before
    assert asset.read_bytes() == asset_before
    if unrelated_before is not None:
        assert output.read_bytes() == unrelated_before
    if target in ("new-inside-root", "parent-alias", "case-alias-parent", "case-alias-ancestor"):
        assert not output.exists()
    if target == "dangling-symlink":
        assert output.is_symlink()
        assert not (tmp_path / "absent").exists()


@pytest.mark.parametrize("contents", ["{", "[]", "{}", '{"files": null}', '{"files": [null]}', '{"files": [], "requiredPaths": 3}'])
def test_cli_malformed_manifest_fails_without_traceback(tmp_path, contents):
    root, manifest, _ = bundle(tmp_path)
    manifest.write_text(contents)
    proc = run_cli(root, manifest)
    assert proc.returncode == 2
    assert "Traceback" not in proc.stderr


def test_cli_missing_manifest_and_output_parent_fail_without_traceback(tmp_path):
    root, manifest, _ = bundle(tmp_path)
    missing = run_cli(root, tmp_path / "missing.json")
    assert missing.returncode == 2
    assert "Traceback" not in missing.stderr
    output = tmp_path / "absent-parent" / "report.json"
    proc = run_cli(root, manifest, output)
    assert proc.returncode == 2
    assert "Traceback" not in proc.stderr
    assert not output.parent.exists()
