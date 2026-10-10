from video_workflow.audit import audit_project
from video_workflow.manifest import default_project


def _project_with_asset() -> dict:
    project = default_project("audit", width=1080, height=1920, fps=30)
    project["delivery"]["platform"] = "tiktok"
    project["assets"] = {
        "portrait": {"path": "portrait.png", "type": "image"},
        "music": {"path": "music.mp3", "type": "audio"},
    }
    return project


def test_audit_flags_repeated_sources_short_text_and_unreviewed_music_cut() -> None:
    project = _project_with_asset()
    project["style"]["safe_area"] = {
        "left_pct": 0.056,
        "right_pct": 0.20,
        "top_pct": 0.08,
        "bottom_pct": 0.18,
    }
    project["style"]["copy_constraints"] = {"disallowed_characters": ["—"]}
    project["qa"]["max_asset_uses_per_video"] = 1
    project["timeline"] = [
        {
            "id": "one",
            "kind": "image",
            "asset": "portrait",
            "start": 0.0,
            "duration": 1.0,
            "text": "This sentence is much too long to read in one second — especially on a phone.",
        },
        {
            "id": "two",
            "kind": "image",
            "asset": "portrait",
            "start": 1.0,
            "duration": 3.0,
        },
    ]
    project["audio"]["music"] = {"asset": "music", "start": 12.0, "end": 24.0}

    codes = {issue["code"] for issue in audit_project(project)["issues"]}
    assert {
        "platform-safe-area-unreviewed",
        "asset-reuse-exceeded",
        "text-hold-too-short",
        "copy-constraint",
        "music-boundary-review-missing",
    } <= codes


def test_audit_accepts_reviewed_safe_area_unique_assets_and_phrase_review() -> None:
    project = _project_with_asset()
    project["assets"]["second"] = {"path": "second.png", "type": "image"}
    project["style"]["safe_area"] = {
        "left_pct": 0.056,
        "right_pct": 0.20,
        "top_pct": 0.08,
        "bottom_pct": 0.18,
        "platform": "tiktok",
        "reviewed_at": "2026-07-22",
        "source": "project overlay review",
    }
    project["qa"]["max_asset_uses_per_video"] = 1
    project["timeline"] = [
        {
            "id": "one",
            "kind": "image",
            "asset": "portrait",
            "start": 0.0,
            "duration": 4.0,
            "text": "Meet the courier.",
        },
        {
            "id": "two",
            "kind": "image",
            "asset": "second",
            "start": 4.0,
            "duration": 3.0,
        },
    ]
    project["audio"]["music"] = {
        "asset": "music",
        "start": 12.0,
        "end": 24.0,
        "boundary_review": {
            "start_natural": True,
            "end_natural": True,
            "method": "listened with transcript and waveform",
        },
    }

    codes = {issue["code"] for issue in audit_project(project)["issues"]}
    assert "platform-safe-area-unreviewed" not in codes
    assert "asset-reuse-exceeded" not in codes
    assert "text-hold-too-short" not in codes
    assert "music-boundary-review-missing" not in codes


def test_audit_enforces_publishable_cta_hold() -> None:
    project = _project_with_asset()
    project["qa"]["minimum_cta_hold_s"] = 2.5
    project["timeline"] = [
        {
            "id": "cta",
            "kind": "card",
            "role": "cta",
            "start": 0.0,
            "duration": 1.8,
            "text": "Learn more",
        }
    ]
    codes = {issue["code"] for issue in audit_project(project)["issues"]}
    assert "cta-hold-too-short" in codes
