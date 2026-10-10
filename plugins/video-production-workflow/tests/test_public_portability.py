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
    for folder in ('video_workflow','skills','agents','references','docs'):
        for path in (ROOT/folder).rglob('*'):
            if not path.is_file() or path.suffix not in {'.py','.md','.json','.yaml','.sh'}:continue
            text=path.read_text()
            assert not re.search(r'/Users/[A-Za-z0-9_.-]+/(?:plugins|\.codex)', text), str(path.relative_to(ROOT))
            assert not re.search(r'/Volumes/[A-Za-z0-9_.-]+/', text), str(path.relative_to(ROOT))
            assert 'Skysight/segments' not in text, str(path.relative_to(ROOT))

def test_export_contains_no_external_compatibility_symlink_or_launcher():
    assert not (ROOT/'runtime/video-style-library').exists()
    assert not (ROOT/'scripts/video_style_library_mcp.py').exists()
