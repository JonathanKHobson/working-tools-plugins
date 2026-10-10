"""Synthetic fixture export must never inherit held collection profiles or prose."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('fixture_boundary', ROOT/'scripts/create_sample_collection.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)

class FixtureBoundaryTests(unittest.TestCase):
    def test_unrelated_held_profiles_and_prose_never_copy(self):
        with tempfile.TemporaryDirectory() as folder:
            base=Path(folder); owner=base/'owner'; library=owner/'library/voice-library'
            for rel in fixture.ENGINE_FILES:
                dest=library/rel;dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/'library/voice-library'/rel,dest)
            sentinel='UNGRANTED-COLLECTION-SENTINEL-8e4be558'
            for rel in ('validation/profiles/held-sentinel.json','validation/private-companion.md','metrics/unregistered.cjs'):
                dest=library/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(sentinel)
            with patch.object(fixture,'ROOT',owner):output=fixture.build(base/'external')
            self.assertEqual({p.stem for p in (output/'validation/profiles').glob('*.json')},{'V01','V02','P28','P29'})
            for path in output.rglob('*'):
                if path.is_file():self.assertNotIn(sentinel,path.read_text())
            for rel in fixture.ENGINE_FILES:
                self.assertEqual((library/rel).read_bytes(),(output/rel).read_bytes(),rel)
            self.assertFalse((output/'metrics/unregistered.cjs').exists())
            self.assertFalse((output/'validation/private-companion.md').exists())

if __name__=='__main__':unittest.main()
