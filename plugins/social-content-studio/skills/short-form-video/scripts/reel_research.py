#!/usr/bin/env python3
"""Validate manually collected Reel research without global ranking.

Input is a JSON array of rows with source_url, account, platform, views,
baseline_views, metric, window, and cohort. Numeric values are finite,
nonnegative numbers; missing baselines remain missing and zero baselines remain
zero. The tool computes a descriptive within-row multiple only when defined,
preserves denominator provenance, and never ranks incomparable rows. It reads
files or stdin, emits JSON, and performs no network, subprocess, or writes.
"""
from __future__ import annotations
import argparse, json, math, sys
from pathlib import Path

REQUIRED = ("source_url", "account", "platform", "views", "baseline_views", "metric", "window", "cohort")

def _number(value, name, *, required=True):
    if value is None and not required: return None
    try:
        finite = math.isfinite(value)
    except (OverflowError, TypeError):
        finite = False
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not finite or value < 0:
        suffix = " or null" if not required else ""
        raise ValueError(f"{name} must be a finite nonnegative number{suffix}")
    return float(value)

def _stable_median(values):
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    low, high = ordered[middle - 1], ordered[middle]
    result = low + (high - low) / 2
    if not math.isfinite(result):
        raise ValueError("baseline_samples median is unavailable due to numeric overflow")
    return result

def analyse(rows):
    if not isinstance(rows, list): raise ValueError("expected a JSON array of research rows")
    seen_urls, seen_ids, output = set(), set(), []
    for index, row in enumerate(rows):
        if not isinstance(row, dict): raise ValueError(f"row {index} must be an object")
        for key in REQUIRED:
            if key not in row: raise ValueError(f"row {index} missing {key}")
            if key not in ("views", "baseline_views") and (not isinstance(row[key], str) or not row[key].strip()):
                raise ValueError(f"row {index} {key} must be a nonempty string")
        url = row["source_url"]
        if url in seen_urls: raise ValueError(f"duplicate source_url: {url}")
        seen_urls.add(url)
        if row.get("id") is not None:
            if not isinstance(row["id"], str) or not row["id"].strip(): raise ValueError(f"row {index} id must be nonempty")
            if row["id"] in seen_ids: raise ValueError(f"duplicate id: {row['id']}")
            seen_ids.add(row["id"])
        views = _number(row["views"], f"row {index} views", required=False)
        baseline = _number(row["baseline_views"], f"row {index} baseline_views", required=False)
        samples = row.get("baseline_samples")
        if samples is not None:
            if not isinstance(samples, list) or not samples:
                raise ValueError(f"row {index} baseline_samples must be a nonempty array when supplied")
            samples = [_number(value, f"row {index} baseline_samples") for value in samples]
            if baseline is not None:
                raise ValueError(f"row {index} cannot provide baseline_samples with explicit baseline_views")
            baseline = _stable_median(samples)
        supplied_count = row.get("baseline_count")
        if supplied_count is not None and (isinstance(supplied_count, bool) or not isinstance(supplied_count, int) or supplied_count < 0):
            raise ValueError(f"row {index} baseline_count must be a nonnegative integer")
        baseline_count = len(samples) if samples is not None else supplied_count
        for field in ("baseline_source", "baseline_window"):
            if field in row and row[field] is not None and (not isinstance(row[field], str) or not row[field].strip()):
                raise ValueError(f"row {index} {field} must be a nonempty string when supplied")
        baseline_source = row.get("baseline_source")
        baseline_window = row.get("baseline_window")
        status = "missing baseline" if baseline is None else ("zero baseline" if baseline == 0 else "defined")
        try:
            raw_multiple = views / baseline if views is not None and baseline not in (None, 0) else None
            multiple = round(raw_multiple, 6) if raw_multiple is not None and math.isfinite(raw_multiple) else None
            if raw_multiple is not None and not math.isfinite(raw_multiple):
                status = "ratio unavailable (overflow)"
        except (OverflowError, ZeroDivisionError):
            multiple = None
            status = "ratio unavailable (overflow)"
        item = dict(row)
        item.update({"views": views, "views_status": "missing views" if views is None else "defined", "baseline_views": baseline, "baseline_count": baseline_count, "baseline_source": baseline_source, "baseline_window": baseline_window, "relative_multiple": multiple, "baseline_status": status})
        output.append(item)
    groups = {}
    for item in output:
        key = (item["platform"], item["metric"], item["window"], item["cohort"])
        group = groups.setdefault(key, {"platform": item["platform"], "metric": item["metric"], "window": item["window"], "cohort": item["cohort"], "row_count": 0})
        group["row_count"] += 1
    warnings = []
    if any(x["relative_multiple"] is None for x in output): warnings.append("views or baseline missing, zero, or ratio unavailable: relative multiple is undefined")
    if any(x["baseline_source"] is None or x["baseline_window"] is None for x in output): warnings.append("baseline source or window is unknown for at least one manual observation")
    if any(x["baseline_count"] == 0 and x["baseline_status"] == "defined" for x in output): warnings.append("baseline_count is zero despite a defined baseline value")
    return {"schema_version": 1, "claim_boundary": "Descriptive manually supplied observations; no incomparable global ranking, winner, causal, reach, or virality claim.", "row_count": len(output), "rows": output, "comparable_groups": list(groups.values()), "ranking": None, "warnings": warnings}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument("input", nargs="?", default="-"); args = ap.parse_args(argv)
    try:
        raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
        print(json.dumps(analyse(json.loads(raw)), ensure_ascii=False, allow_nan=False)); return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr); return 2
if __name__ == "__main__": raise SystemExit(main())
