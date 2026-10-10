from __future__ import annotations

from typing import Any, Iterable


def project_duration(project: dict[str, Any]) -> float:
    return max((float(item["start"]) + float(item["duration"]) for item in project.get("timeline", [])), default=0.0)


def _nearest_boundaries(targets: list[float], beats: list[float], total: float, min_duration: float) -> list[float]:
    boundaries = [0.0]
    for target in targets[1:-1]:
        candidates = [beat for beat in beats if boundaries[-1] + min_duration <= beat <= total - min_duration]
        if candidates:
            chosen = min(candidates, key=lambda value: abs(value - target))
        else:
            chosen = target
        if chosen - boundaries[-1] < min_duration:
            chosen = boundaries[-1] + min_duration
        boundaries.append(min(chosen, total))
    boundaries.append(total)
    # Backward repair for an undersized final clip.
    for index in range(len(boundaries) - 2, 0, -1):
        if boundaries[index + 1] - boundaries[index] < min_duration:
            boundaries[index] = max(boundaries[index - 1] + min_duration, boundaries[index + 1] - min_duration)
    return boundaries


def plan_slideshow(
    assets: Iterable[str],
    *,
    target_duration: float,
    beats: Iterable[float] | None = None,
    min_duration: float = 1.0,
    transition: str = "fade",
    transition_duration: float = 0.4,
) -> list[dict[str, Any]]:
    sources = list(assets)
    if not sources:
        return []
    if target_duration < min_duration * len(sources):
        min_duration = target_duration / len(sources)
    equal_targets = [target_duration * i / len(sources) for i in range(len(sources) + 1)]
    beat_values = sorted({max(0.0, min(target_duration, float(x))) for x in (beats or [])})
    boundaries = _nearest_boundaries(equal_targets, beat_values, target_duration, min_duration) if beat_values else equal_targets
    durations = [boundaries[i + 1] - boundaries[i] for i in range(len(sources))]
    result: list[dict[str, Any]] = []
    for index, (source, start, duration) in enumerate(zip(sources, boundaries[:-1], durations)):
        next_duration = durations[index + 1] if index + 1 < len(durations) else duration
        max_transition = max(0.0, min(duration, next_duration) / 2.0)
        td = min(float(transition_duration), max_transition)
        item = {
            "id": f"slide-{index + 1:03d}",
            "kind": "image",
            "source": source,
            "start": round(start, 6),
            "duration": round(duration, 6),
            "motion": ["zoom-in", "pan-right", "zoom-out", "pan-left"][index % 4],
            "transition": {"type": transition if index < len(sources) - 1 else "cut", "duration": round(td if index < len(sources) - 1 else 0.0, 6)},
        }
        result.append(item)
    return result


def normalize_timeline(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sort timeline and fill starts from previous overlaps when missing."""
    cursor = 0.0
    normalized = []
    for item in items:
        current = dict(item)
        current.setdefault("start", cursor)
        current.setdefault("duration", 3.0)
        transition = current.get("transition") or {"type": "cut", "duration": 0.0}
        current["transition"] = transition
        cursor = float(current["start"]) + float(current["duration"]) - float(transition.get("duration", 0.0))
        normalized.append(current)
    return sorted(normalized, key=lambda entry: float(entry["start"]))
