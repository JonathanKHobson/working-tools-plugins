from pathlib import Path
import json


def test_source_registry_is_license_aware() -> None:
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "research/sources.lock.json").read_text())
    assert len(data["sources"]) >= 25
    assert all("license" in source and "usage" in source for source in data["sources"])
    remotion = next(s for s in data["sources"] if s["id"] == "remotion")
    assert remotion["license"] == "custom-source-available"
    assert remotion["usage"] == "optional-integration-only"
