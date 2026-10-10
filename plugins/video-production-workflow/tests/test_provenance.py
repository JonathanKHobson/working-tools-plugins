from pathlib import Path
from video_workflow.provenance import cache_key, hash_file, inventory_paths


def test_hash_inventory_and_cache_key(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"; a.write_text("alpha")
    b = tmp_path / "b.txt"; b.write_text("beta")
    assert hash_file(a) != hash_file(b)
    rows = inventory_paths([a, b])
    assert {row["name"] for row in rows} == {"a.txt", "b.txt"}
    key1 = cache_key({"x": 1}, files=[a])
    key2 = cache_key({"x": 1}, files=[a])
    assert key1 == key2
    a.write_text("changed")
    assert cache_key({"x": 1}, files=[a]) != key1
