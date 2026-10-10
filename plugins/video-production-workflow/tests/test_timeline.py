from video_workflow.timeline import plan_slideshow


def test_plan_slideshow_uses_all_assets_and_target_duration() -> None:
    assets = ["a.jpg", "b.jpg", "c.jpg", "d.jpg"]
    plan = plan_slideshow(assets, target_duration=12.0, beats=[0.0, 2.0, 4.0, 7.0, 9.0, 12.0])
    assert len(plan) == 4
    assert [item["source"] for item in plan] == assets
    assert abs(max(i["start"] + i["duration"] for i in plan) - 12.0) < 1e-6
    assert all(i["duration"] >= 1.0 for i in plan)


def test_transition_never_exceeds_half_shorter_clip() -> None:
    plan = plan_slideshow(["a", "b"], target_duration=3.0, transition_duration=2.0)
    assert plan[0]["transition"]["duration"] <= 0.75
