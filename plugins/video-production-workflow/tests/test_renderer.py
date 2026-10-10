from pathlib import Path
import json
import subprocess

from PIL import Image

from video_workflow.manifest import default_project, save_project
from video_workflow.render import render_project
from video_workflow.probe import probe_media
from video_workflow.utils import require_tool


def test_end_to_end_slideshow_render(tmp_path: Path) -> None:
    img1 = tmp_path / "one.png"
    img2 = tmp_path / "two.png"
    Image.new("RGB", (640, 360), "#203050").save(img1)
    Image.new("RGB", (360, 640), "#803020").save(img2)
    music = tmp_path / "music.wav"
    subprocess.run([
        require_tool("ffmpeg"), "-y", "-f", "lavfi", "-i", "sine=frequency=220:duration=4:sample_rate=48000",
        str(music),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    project = default_project("render-test", width=640, height=360, fps=24)
    project["assets"] = {
        "one": {"path": str(img1), "type": "image"},
        "two": {"path": str(img2), "type": "image"},
        "music": {"path": str(music), "type": "audio"},
    }
    project["timeline"] = [
        {"id": "s1", "kind": "image", "asset": "one", "start": 0.0, "duration": 2.0,
         "motion": "zoom-in", "text": "FIRST", "transition": {"type": "fade", "duration": 0.3}},
        {"id": "s2", "kind": "image", "asset": "two", "start": 1.7, "duration": 2.3,
         "motion": "pan-right", "text": "SECOND", "transition": {"type": "fade", "duration": 0.3}},
    ]
    project["audio"] = {"music": {"asset": "music", "volume": 0.15}, "loudness": {"enabled": False}}
    manifest = tmp_path / "project.json"
    save_project(project, manifest)
    out = tmp_path / "out.mp4"
    render_project(manifest, out, work_dir=tmp_path / "work")
    info = probe_media(out)
    assert info["video"]["width"] == 640
    assert info["video"]["height"] == 360
    assert 3.8 <= info["format"]["duration"] <= 4.2
    assert info["audio"] is not None


def test_contain_motion_preserves_letterbox(tmp_path: Path) -> None:
    from PIL import Image as PILImage
    portrait = tmp_path / "portrait.png"
    image = PILImage.new("RGB", (100, 200), "red")
    for y in range(100, 200):
        for x in range(100):
            image.putpixel((x, y), (0, 0, 255))
    image.save(portrait)
    project = default_project("contain-motion", width=200, height=100, fps=24)
    project["assets"] = {"portrait": {"path": str(portrait), "type": "image"}}
    project["timeline"] = [{"id": "only", "kind": "image", "asset": "portrait", "start": 0, "duration": 1.0, "fit": "contain", "motion": "zoom-in"}]
    project["audio"]["loudness"]["enabled"] = False
    manifest = tmp_path / "project.json"; save_project(project, manifest)
    out = tmp_path / "out.mp4"; render_project(manifest, out, work_dir=tmp_path / "work")
    frame = tmp_path / "frame.png"
    subprocess.run([require_tool("ffmpeg"), "-y", "-v", "error", "-ss", "0.5", "-i", str(out), "-frames:v", "1", str(frame)], check=True)
    with PILImage.open(frame).convert("RGB") as sample:
        left = sample.getpixel((3, 50))
        assert max(left) < 30  # contain mode keeps dark side bars even with motion


def test_default_title_has_visible_glyphs_without_fontconfig(tmp_path: Path) -> None:
    """An available font file must produce visible title pixels, not just a valid MP4."""
    import numpy as np
    project = default_project('portable-title', width=320, height=180, fps=24)
    project['timeline'] = [{'id':'title','kind':'card','start':0,'duration':1,'background':'#000000','text':'VISIBLE TITLE','font_size':25}]
    project['audio']['loudness']['enabled'] = False
    manifest=tmp_path/'project.json';save_project(project,manifest)
    out=tmp_path/'title.mp4';render_project(manifest,out,work_dir=tmp_path/'work')
    frame=tmp_path/'frame.png'
    subprocess.run([require_tool('ffmpeg'),'-y','-v','error','-ss','0.5','-i',str(out),'-frames:v','1',str(frame)],check=True)
    pixels=np.asarray(Image.open(frame).convert('RGB'))
    bright=(pixels[50:130,20:300].min(axis=2)>180).sum()
    assert bright>100, 'Encoded title is blank despite successful FFmpeg exit'
