from video_workflow.toolchain import check_toolchain


def test_check_toolchain_reports_production_inspection_and_ffmpeg_capabilities():
    report = check_toolchain()
    assert {"mediainfo", "exiftool", "packager"}.issubset(report["binaries"])
    assert "ffmpeg_capabilities" in report
    caps = report["ffmpeg_capabilities"]
    assert {"filters", "encoders", "hardware_acceleration"}.issubset(caps)
    assert isinstance(caps["filters"], dict)
    assert "libvmaf" in caps["filters"]
    assert "subtitles" in caps["filters"]
