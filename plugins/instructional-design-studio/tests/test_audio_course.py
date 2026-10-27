import argparse
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1] / "skills/course-production-handoff/scripts"
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
api = load("audio_course", BASE / "audio_course.py")
guard = load("studio_guard", BASE / "audio_lessons/studio_guard.py")
pack = load("package_class", BASE / "audio_lessons/package_class.py")

class Boundaries(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup); self.ws = Path(self.temp.name).resolve()
    def args(self, **kwargs):
        defaults = dict(workspace=str(self.ws),action="check_lessons",allow_host=[],author=None,script=None,output=None,engine="local",allow_upload=False,max_mb=25);defaults.update(kwargs);return argparse.Namespace(**defaults)
    def test_escape_rejected(self):
        with self.assertRaises(ValueError): api.within(self.ws, "../other")
    def test_symlink_rejected(self):
        (self.ws / "alias").symlink_to(self.ws / "target")
        with self.assertRaises(ValueError): api.command(self.args())
    def test_ambient_key_ignored(self):
        with patch.dict(os.environ, {"ELEVENLABS_API_KEY":"synthetic-test-key"}):
            _,env,_ = api.command(self.args());self.assertNotIn("ELEVENLABS_API_KEY",env)
    def test_cloud_requires_consent(self):
        (self.ws / "script.txt").write_text("A: test")
        with self.assertRaises(ValueError): api.command(self.args(action="render_audio",script="script.txt",output="out.mp3",engine="elevenlabs"))
    def test_render_preserves_existing(self):
        (self.ws / "script.txt").write_text("A: test");(self.ws / "out.mp3").write_bytes(b"old")
        with self.assertRaises(ValueError): api.command(self.args(action="render_audio",script="script.txt",output="out.mp3"))
    def test_scrape_requires_host(self):
        with self.assertRaises(ValueError): api.command(self.args(action="scrape"))
    def test_unlisted_host_before_dns(self):
        with patch.dict(os.environ, {"AUDIO_LESSON_ALLOWED_HOSTS":"example.org"}),patch.object(guard.socket,"getaddrinfo") as dns:
            with self.assertRaises(ValueError): guard.validate_url("https://private.example/")
            dns.assert_not_called()
    def test_private_address_rejected(self):
        with patch.dict(os.environ, {"AUDIO_LESSON_ALLOWED_HOSTS":"example.org"}),patch.object(guard.socket,"getaddrinfo",return_value=[(2,1,6,"",("127.0.0.1",443))]):
            with self.assertRaises(ValueError): guard.validate_url("https://example.org/")
    def test_unsafe_scheme_and_userinfo_rejected(self):
        for url in ["file:///etc/passwd","http://example.org/","https://secret@example.org/"]:
            with self.assertRaises(ValueError): guard.validate_url(url)
    def test_incomplete_class_not_packaged(self):
        with self.assertRaises(ValueError): api.command(self.args(action="package_class"))
    def test_oversized_audio_rejected(self):
        d=self.ws/"class/01-test";d.mkdir(parents=True);(d/"a.mp3").write_bytes(b"a"*1000);out=self.ws/"out";out.mkdir()
        with self.assertRaises(ValueError):pack.zip_audio(self.ws,out,1000)
    def test_multiple_takes_split_without_overwrite(self):
        d=self.ws/"class/01-test";d.mkdir(parents=True);(d/"a.mp3").write_bytes(b"a"*1000);(d/"b.mp3").write_bytes(b"b"*1000);out=self.ws/"out";out.mkdir()
        made=pack.zip_audio(self.ws,out,1500);self.assertEqual(len(made),2);self.assertNotEqual(made[0],made[1]);self.assertTrue(all(x.exists() for x in made))
    def test_no_implicit_document_execution(self):
        d=self.ws/"class/01-test";d.mkdir(parents=True);(d/"card.md").write_text("![data](file:///private/secret)");out=self.ws/"out";out.mkdir()
        with patch.object(pack.subprocess,"run") as run:
            self.assertEqual(pack.combine_cards(self.ws,out),1);run.assert_not_called()
    def test_archive_below_actual_cap(self):
        d=self.ws/"class/01-test";d.mkdir(parents=True);(d/"a.mp3").write_bytes(b"a"*1000);out=self.ws/"out";out.mkdir()
        made=pack.zip_audio(self.ws,out,1500);self.assertEqual(len(made),1);self.assertLessEqual(made[0].stat().st_size,1500)

if __name__ == "__main__":unittest.main()
