"""Check four-axis source coverage, generated references and portable closure."""
import io
import json
import re
import sys
import unittest
import zipfile
from pathlib import Path
from posixpath import dirname, normpath, join


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'runtime/writing-voice-library'))
from build_axis_references import AXES, augment_archive, augment_directory, load_profiles, render_files, write_references  # noqa: E402
import catalog  # noqa: E402


class FourAxisTests(unittest.TestCase):
    def test_profiles_cover_catalog_and_generated_pages(self):
        library = ROOT / 'library/voice-library'
        doc, profiles = load_profiles(library)
        catalog = json.loads((library / 'records/catalog.json').read_text())
        self.assertEqual(set(profiles), {row['id'] for row in catalog['records']})
        self.assertEqual(len(profiles), 53)
        self.assertEqual(write_references(library, check=True), 53)
        for ident, profile in profiles.items():
            self.assertEqual(set(profile['axes']), set(AXES))
            rendered = render_files(doc, profile)
            self.assertEqual(set(rendered), {'README.md', 'profile.json', *(f'{axis}.md' for axis in AXES)})
            for name, content in rendered.items():
                if not name.endswith('.md'):
                    continue
                for target in re.findall(r'\]\(([^)]+)\)', content):
                    if '://' not in target:
                        path = library / 'styles' / ident / 'axes' / name
                        self.assertTrue((path.parent / target.split('#')[0]).resolve().is_file(), (ident, name, target))
            self.assertTrue((library / 'styles' / ident / 'STYLE.md').is_file())

    def test_augmented_archive_preserves_route_and_adds_reading_order(self):
        doc, profiles = load_profiles(require_complete=False)
        profile = profiles['P28']
        manifest = {'schema': 'wvl-portable-agent/1', 'resourceId': 'P28',
                    'baseProfileId': 'V01', 'moduleIds': ['P28'], 'entrypoint': 'SKILL.md'}
        source = io.BytesIO()
        with zipfile.ZipFile(source, 'w') as archive:
            archive.writestr('writing-resource-p28/SKILL.md', '# P28\n\nRead selected and base guides.\n')
            archive.writestr('writing-resource-p28/STYLE.md', '# P28 style\n')
            archive.writestr('writing-resource-p28/agent-manifest.json', json.dumps(manifest))
            archive.writestr('writing-resource-p28/references/guide.md', 'Guide fixture')
            archive.writestr('writing-resource-p28/axes/four-axes.json', json.dumps({'profiles': []}))
        result = augment_archive(source.getvalue(), doc, profile)
        with zipfile.ZipFile(io.BytesIO(result)) as archive:
            names = set(archive.namelist())
            prefix = 'writing-resource-p28/'
            self.assertIn(prefix + 'axes/profile.json', names)
            self.assertTrue(all(prefix + f'axes/{axis}.md' in names for axis in AXES))
            self.assertIn(prefix + 'axes/README.md', names)
            self.assertEqual(archive.read(prefix + 'references/guide.md'), b'Guide fixture')
            result_manifest = json.loads(archive.read(prefix + 'agent-manifest.json'))
            self.assertEqual(result_manifest['baseProfileId'], 'V01')
            self.assertEqual(result_manifest['moduleIds'], ['P28'])
            self.assertEqual(result_manifest['axesProfile'], 'axes/profile.json')
            self.assertEqual(len(json.loads(archive.read(prefix + 'axes/four-axes.json'))['profiles']), 53)
            scoped = json.loads(archive.read(prefix + 'axes/profile.json'))
            self.assertEqual(scoped['profile']['id'], 'P28')
            skill = archive.read(prefix + 'SKILL.md').decode()
            self.assertIn('After reading the selected complete guide', skill)
            self.assertIn('before drafting', skill)
            self.assertIn('measured QA', skill)
            self.assertIn('[Four-axis editorial reference](axes/README.md)', archive.read(prefix + 'STYLE.md').decode())
            for name in names:
                if not name.startswith(prefix + 'axes/') or not name.endswith('.md'):
                    continue
                for target in re.findall(r'\]\(([^)]+)\)', archive.read(name).decode()):
                    if '://' not in target:
                        self.assertIn(normpath(join(dirname(name), target)), names)

    def test_archive_rejects_mismatched_resource(self):
        doc, profiles = load_profiles(require_complete=False)
        source = io.BytesIO()
        with zipfile.ZipFile(source, 'w') as archive:
            archive.writestr('one/SKILL.md', '# One')
            archive.writestr('one/STYLE.md', '# One style')
            archive.writestr('one/agent-manifest.json', json.dumps({'resourceId': 'V01'}))
        with self.assertRaisesRegex(ValueError, 'does not match'):
            augment_archive(source.getvalue(), doc, profiles['P28'])

    def test_archive_output_cannot_replace_sources(self):
        with self.assertRaisesRegex(ValueError, 'outside'):
            augment_directory(ROOT / 'library/voice-library', ROOT / 'library/voice-library', ids=['V01'])

    def test_native_handoff_uses_actual_route_and_checked_axes(self):
        result = catalog.handoff('P28', 'Explain a proposed decision.')
        self.assertEqual(result['route'], {'selected_resource_id': 'P28', 'base_profile_id': 'V01', 'module_ids': ['P28']})
        self.assertEqual([p['id'] for p in result['fourAxes']['profiles']], ['P28', 'V01'])
        self.assertIn('styles/P28/axes/voice.md', result['handoffText'])
        self.assertIn('styles/V01/axes/format.md', result['handoffText'])
        self.assertIn('not statistical thresholds', result['instructions'])


if __name__ == '__main__':
    unittest.main()
