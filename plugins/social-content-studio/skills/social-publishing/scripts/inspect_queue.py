#!/usr/bin/env python3
"""Read-only ledger checks. Local dates are advisory, never platform receipts."""

import argparse
from collections import Counter, defaultdict
from datetime import date, datetime, time, timedelta, timezone
import json
from pathlib import Path
import re
import sys
from urllib.parse import parse_qs, urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def youtube_url_id(value):
    url = urlparse(value)
    host = (url.hostname or "").lower()
    parts = url.path.strip("/").split("/")
    if url.scheme != "https":
        return None
    if host == "youtu.be" and len(parts) == 1:
        return parts[0]
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        if url.path == "/watch":
            ids = parse_qs(url.query).get("v", [])
            return ids[0] if len(ids) == 1 else None
        if len(parts) == 2 and parts[0] in {"shorts", "embed", "live"}:
            return parts[1]
    return None


def inspect_queue(ledger, as_of, horizon_days=90):
    result = {"valid": False, "advisory_only": True,
              "as_of": as_of.isoformat(), "horizon_days": horizon_days,
              "errors": [], "warnings": [], "state_counts": {},
              "prepared_linkedin_candidates": []}

    def issue(kind, code, release_id=None, **details):
        entry = {"code": code, **details}
        if release_id is not None:
            entry["release_id"] = release_id
        result[kind].append(entry)

    if not isinstance(ledger, dict) or not isinstance(ledger.get("items"), dict):
        issue("errors", "ledger_requires_items_object")
        return result
    try:
        zone = ZoneInfo(ledger["timezone"])
    except (KeyError, TypeError, ValueError, ZoneInfoNotFoundError):
        issue("errors", "invalid_timezone")
        return result
    if not isinstance(horizon_days, int) or isinstance(horizon_days, bool) or horizon_days < 1:
        issue("errors", "invalid_horizon_days")
        return result
    start = datetime.combine(as_of, time.min, zone)
    try:
        boundary = as_of + timedelta(days=horizon_days)
    except OverflowError:
        issue("errors", "invalid_horizon_days", detail="horizon exceeds supported date range")
        return result
    result.update(timezone=ledger["timezone"], advisory_boundary_date=boundary.isoformat())
    ids, dates = defaultdict(list), defaultdict(list)
    counts = {platform: Counter() for platform in ("youtube", "linkedin")}
    candidate_instants = {}

    for release_id, item in ledger["items"].items():
        if not release_id or not isinstance(item, dict):
            issue("errors", "invalid_item", release_id)
            continue
        stamps = {}
        for platform in counts:
            state = item.get(f"{platform}_state")
            if state is not None and (not isinstance(state, str) or not state.strip()):
                issue("errors", "invalid_state", release_id, platform=platform)
                state = None
            counts[platform][state or "unspecified"] += 1
            platform_id = item.get(f"{platform}_id")
            if platform == "linkedin":
                alias = item.get("linkedin_post_id")
                if platform_id and alias and platform_id != alias:
                    issue("errors", "conflicting_linkedin_ids", release_id)
                platform_id = platform_id or alias
            if platform_id is not None:
                if not isinstance(platform_id, str) or not platform_id.strip():
                    issue("errors", "invalid_platform_id", release_id, platform=platform)
                else:
                    ids[(platform, platform_id)].append(release_id)
                    if platform == "youtube" and not re.fullmatch(r"[A-Za-z0-9_-]{11}", platform_id):
                        issue("errors", "invalid_youtube_id", release_id)
            field = f"{platform}_publish_at"
            value = item.get(field)
            if value is None:
                if isinstance(state, str) and state.startswith("scheduled"):
                    issue("warnings", "scheduled_state_missing_timestamp", release_id, platform=platform)
                continue
            try:
                if not isinstance(value, str) or "T" not in value:
                    raise ValueError()
                stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
                if stamp.tzinfo is None or stamp.utcoffset() is None:
                    raise ValueError()
                local_date = stamp.astimezone(zone).date()
                stamp.astimezone(timezone.utc)
            except (ValueError, OverflowError):
                issue("errors", "invalid_aware_timestamp", release_id, field=field)
                continue
            stamps[platform] = stamp
            dates[(platform, local_date.isoformat())].append(release_id)
            if stamp < start:
                issue("warnings", "past_record_recheck_live", release_id, platform=platform)
        url = item.get("youtube_url")
        if url is not None:
            try:
                parsed_id = youtube_url_id(url) if isinstance(url, str) else None
            except ValueError:
                parsed_id = None
            if not parsed_id or not re.fullmatch(r"[A-Za-z0-9_-]{11}", parsed_id):
                issue("errors", "invalid_youtube_url", release_id)
            elif item.get("youtube_id") and parsed_id != item["youtube_id"]:
                issue("errors", "youtube_url_id_mismatch", release_id)
            elif not item.get("youtube_id"):
                issue("warnings", "youtube_url_missing_explicit_id", release_id)
        if "youtube" in stamps and "linkedin" in stamps and stamps["linkedin"] <= stamps["youtube"]:
            issue("errors", "linkedin_must_follow_youtube", release_id)
        state = item.get("linkedin_state")
        if isinstance(state, str) and state.startswith("prepared"):
            target = stamps.get("linkedin")
            future = target or stamps.get("youtube")
            if target is None:
                issue("warnings", "prepared_linkedin_missing_publish_at", release_id)
            if future is not None and future >= start:
                local_date = target.astimezone(zone).date() if target else None
                status = "needs_publish_at"
                if local_date is not None:
                    status = ("boundary_check_live_composer" if local_date == boundary else
                              "within_advisory_window" if local_date < boundary else
                              "outside_advisory_window")
                result["prepared_linkedin_candidates"].append({
                    "release_id": release_id, "state": state,
                    "linkedin_publish_at": item.get("linkedin_publish_at"),
                    "youtube_publish_at": item.get("youtube_publish_at"),
                    "advisory_status": status, "next_check": "check_live_composer"})
                candidate_instants[release_id] = future.astimezone(timezone.utc)
    for (platform, platform_id), releases in sorted(ids.items()):
        if len(releases) > 1:
            issue("errors", "duplicate_platform_id", platform=platform, platform_id=platform_id, release_ids=releases)
    for (platform, local_date), releases in sorted(dates.items()):
        if len(releases) > 1:
            issue("warnings", "platform_date_collision", platform=platform, date=local_date, release_ids=releases)
    result["state_counts"] = {key: dict(sorted(value.items())) for key, value in counts.items()}
    result["prepared_linkedin_candidates"].sort(key=lambda item: (candidate_instants[item["release_id"]], item["release_id"]))
    result["valid"] = not result["errors"]
    return result


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--as-of", required=True, help="YYYY-MM-DD; local midnight, not the current clock")
    parser.add_argument("--horizon-days", default="90", help="advisory date window; live composer decides")
    args = parser.parse_args()
    try:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.as_of):
            raise ValueError("--as-of must be YYYY-MM-DD")
        as_of = date.fromisoformat(args.as_of)
        with args.ledger.open(encoding="utf-8") as source:
            ledger = json.load(source, object_pairs_hook=unique_object)
        result = inspect_queue(ledger, as_of, int(args.horizon_days))
    except (OSError, ValueError, TypeError, RecursionError, OverflowError) as error:
        result = {"valid": False, "advisory_only": True,
                  "errors": [{"code": "invalid_input", "detail": str(error)}]}
    print(json.dumps(result, separators=(",", ":"), ensure_ascii=False))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
