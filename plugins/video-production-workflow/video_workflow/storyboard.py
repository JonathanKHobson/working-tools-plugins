from __future__ import annotations

from pathlib import Path

from .manifest import load_project


def write_storyboard(manifest: str | Path, output: str | Path) -> Path:
    project = load_project(manifest)
    lines = [f"# Storyboard — {project['project'].get('title', project['project']['id'])}", "", "| Time | ID | Kind | Visual | Audio / intent |", "|---:|---|---|---|---|"]
    for item in sorted(project["timeline"], key=lambda entry: float(entry["start"])):
        start = float(item["start"])
        end = start + float(item["duration"])
        visual = item.get("text") or item.get("asset") or item.get("background") or ""
        intent = item.get("intent") or item.get("note") or ""
        lines.append(f"| {start:.2f}–{end:.2f}s | {item['id']} | {item['kind']} | {visual} | {intent} |")
    lines.extend(["", "## Editorial checks", "", "- Does each visual beat earn its screen time?", "- Are information-dense cards readable at 1× playback?", "- Do cuts support meaning rather than merely following every beat?", "- Are captions and essential visuals kept clear of overlays and platform UI?", "- Does the ending hold long enough to register?"])
    Path(output).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return Path(output)
