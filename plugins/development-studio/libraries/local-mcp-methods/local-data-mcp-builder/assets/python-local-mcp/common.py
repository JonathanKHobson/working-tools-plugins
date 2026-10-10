#!/usr/bin/env python3

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    with Path(path).expanduser().open("r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path: str | Path, value: Any) -> None:
    target = Path(path).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)


def encode_cursor(offset: int) -> str:
    payload = json.dumps({"offset": max(offset, 0)}).encode("utf-8")
    return base64.urlsafe_b64encode(payload).decode("ascii")


def decode_cursor(cursor: str | None) -> int:
    if not cursor:
        return 0
    try:
        payload = base64.urlsafe_b64decode(cursor.encode("ascii"))
        return max(int(json.loads(payload.decode("utf-8")).get("offset", 0)), 0)
    except Exception:
        return 0
