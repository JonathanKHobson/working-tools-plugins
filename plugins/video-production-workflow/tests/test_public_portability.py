"""Public identity and isolation regressions observed in the canonical payload."""
from pathlib import Path
import json
import re
from video_workflow import __version__

ROOT = Path(__file__).resolve().parents[1]

def test_public_identity_is_consistent_and_does_not_advertise_external_mcp():
    manifests=[json.loads((ROOT/path).read_text()) for path in ('plugin.json','.codex-plugin/plugin.json','.claude-plugin/plugin.json')]
    assert all(item['name']=='video-production-workflow' for item in manifests)
    assert {item['version'] for item in manifests}=={__version__}
    assert all(not item.get('mcpServers') for item in manifests)
    text=(ROOT/'pyproject.toml').read_text()
    assert re.search(r'^version = "'+re.escape(__version__)+'"$',text,re.M)

def test_active_methods_have_no_private_host_or_event_bindings():
    public = {row['path'] for row in json.loads((ROOT/'PUBLIC_FILE_MANIFEST.json').read_text())['files']}
    assert 'skills/create-motion-graphics/SKILL.md' in public
    for folder in ('video_workflow','skills','agents','references','docs'):
        for path in (ROOT/folder).rglob('*'):
            if not path.is_file() or path.suffix not in {'.py','.md','.json','.yaml','.sh'}:continue
            # Historical private receipts stay outside the reviewed export.
            if path.relative_to(ROOT).as_posix() not in public:continue
            text=path.read_text()
            assert not re.search(r'/' + r'Users/[A-Za-z0-9_.-]+/(?:plugins|\.codex)', text), str(path.relative_to(ROOT))
            assert not re.search(r'/' + r'Volumes/[A-Za-z0-9_.-]+/', text), str(path.relative_to(ROOT))
            assert 'Skysight/segments' not in text, str(path.relative_to(ROOT))

def test_export_contains_no_external_compatibility_symlink_or_launcher():
    manifest = json.loads((ROOT/'PUBLIC_FILE_MANIFEST.json').read_text())
    assert not any(row['path'] == 'runtime/video-style-library' or row['path'].startswith('runtime/video-style-library/') for row in manifest['files'])
    launcher = ROOT/'scripts/video_style_library_mcp.py'
    assert launcher.is_file()
    assert 'VIDEO_TEMPLATES_ROOT' in launcher.read_text()


def test_packager_accepts_manifest_output_hash_and_rejects_changed_bytes(tmp_path, monkeypatch):
    import importlib.util
    import sys
    import hashlib
    from zipfile import ZipFile
    import pytest
    spec = importlib.util.spec_from_file_location("package_public_under_test", ROOT/"scripts/package_public.py")
    packager = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(packager)
    payload = tmp_path/"source"
    payload.mkdir()
    data = b"reviewed source\n"
    (payload/"README.md").write_bytes(data)
    (payload/"PUBLIC_FILE_MANIFEST.json").write_text(json.dumps({"files":[{"path":"README.md","output_sha256":hashlib.sha256(data).hexdigest()}]}))
    monkeypatch.setattr(packager, "ROOT", payload)
    archive = tmp_path/"package.zip"
    monkeypatch.setattr(sys, "argv", ["package_public.py", str(archive)])
    assert packager.main() == 0
    with ZipFile(archive) as z:
        assert z.read("video-production-workflow/README.md") == data
    (payload/"README.md").write_text("changed")
    monkeypatch.setattr(sys, "argv", ["package_public.py", str(tmp_path/"changed.zip")])
    with pytest.raises(SystemExit):
        packager.main()
    assert not (tmp_path/"changed.zip").exists()
