import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import re
import subprocess

from PIL import Image

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/interactive-depth-cards/scripts/build_depth_card.py'
spec = importlib.util.spec_from_file_location('depth_cards', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DepthCardsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        Image.new('RGBA', (64, 48), (30, 70, 110, 255)).save(self.root / 'scene.png')
        self.brief = {'title': 'Example', 'layers': [{'path': 'scene.png', 'alt': 'Scene', 'depth': 20}]}

    def run_brief(self, **kwargs):
        source = self.root / 'brief.json'
        source.write_text(json.dumps(self.brief))
        return module.build(source, self.root / 'card.html', **kwargs)

    def test_offline_embedded_and_text_escaped(self):
        self.brief['title'] = '<script>alert(1)</script> __BODY__'
        self.brief['body'] = 'Body'
        with patch('socket.socket', side_effect=AssertionError('network forbidden')):
            self.run_brief()
        output = (self.root / 'card.html').read_text()
        self.assertIn('&lt;script&gt;', output)
        self.assertIn('__BODY__</h1>', output)
        self.assertIn('data:image/png;base64,', output)
        self.assertNotIn('<script>alert(1)', output)
        self.assertIn("default-src 'none'", output)

    def test_existing_output_is_preserved(self):
        self.run_brief()
        before = (self.root / 'card.html').read_bytes()
        with self.assertRaises(FileExistsError): self.run_brief()
        self.assertEqual(before, (self.root / 'card.html').read_bytes())

    def test_remote_image_refused(self):
        self.brief['layers'][0]['path'] = 'https://example.invalid/photo.png'
        with self.assertRaisesRegex(ValueError, 'local image'): self.run_brief()

    def test_nonfinite_depth_and_missing_alt_refused(self):
        self.brief['layers'][0]['depth'] = float('nan')
        with self.assertRaisesRegex(ValueError, 'finite'): self.run_brief()
        self.brief['layers'][0]['depth'] = 0
        del self.brief['layers'][0]['alt']
        with self.assertRaisesRegex(ValueError, 'alt'): self.run_brief()

    def test_facts_require_sources(self):
        self.brief['facts'] = [{'label': 'Claim', 'value': 'Unverified'}]
        with self.assertRaisesRegex(ValueError, 'source'): self.run_brief()

    def test_svg_and_false_extension_refused(self):
        (self.root / 'x.svg').write_text('<svg/>')
        self.brief['layers'][0]['path'] = 'x.svg'
        with self.assertRaisesRegex(ValueError, 'raster'): self.run_brief()
        (self.root / 'x.png').write_text('<svg/>')
        self.brief['layers'][0]['path'] = 'x.png'
        with self.assertRaises(OSError): self.run_brief()

    def test_normalized_image_drops_exif(self):
        image = Image.new('RGB', (64, 48), 'white')
        exif = Image.Exif()
        exif[315] = 'Private camera owner'
        image.save(self.root / 'private.png', exif=exif)
        normalized = module.encode_image(self.root / 'private.png')
        with Image.open(io.BytesIO(normalized)) as result:
            self.assertFalse(result.getexif())

    def test_complete_local_card_controls_and_planes(self):
        Image.new('RGBA', (64, 48), (220, 80, 20, 0)).save(self.root / 'subject.png')
        self.brief.update({'finish': 'gold', 'card_depth': 50, 'foil': False,
                           'auto_rotate': True, 'exploded': True,
                           'card_text': ['Level <12>'],
                           'sparkles': 12,
                           'layers': [{'path': 'scene.png', 'alt': 'Background', 'depth': 8, 'role': 'background'},
                                      {'path': 'subject.png', 'alt': 'Subject', 'depth': 45, 'role': 'foreground'}],
                           'back': {'title': 'Reverse', 'body': 'Live reverse text'}})
        self.run_brief()
        output = (self.root / 'card.html').read_text()
        self.assertIn('role-background', output)
        self.assertIn('role-foreground', output)
        self.assertIn('--shift:-6.000px', output)
        self.assertIn('--shift:16.200px', output)
        self.assertIn('Show back', output)
        self.assertIn('Reverse', output)
        self.assertIn('Level &lt;12&gt;', output)
        self.assertEqual(output.count('animation-delay:-'), 12)
        self.assertIn('aria-hidden="true"', output)
        self.assertIn('finish-gold', output)
        self.assertIn('calc(.08 + var(--lift,0) * .35)', output)
        self.assertIn('depth/100', output)
        self.assertIn('document.hidden', output)
        self.assertIn('pointercancel', output)
        self.assertIn('prefers-reduced-motion', output)
        self.assertNotIn('__CONFIG__', output)
        script = re.search(r'<script>(.*?)</script>', output, re.S).group(1)
        checked = subprocess.run(['node', '--check'], input=script, text=True, capture_output=True)
        self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_feature_inputs_are_bounded(self):
        self.brief['finish'] = 'unknown'
        with self.assertRaisesRegex(ValueError, 'finish'): self.run_brief()
        self.brief['finish'] = 'gold'
        self.brief['card_depth'] = float('nan')
        with self.assertRaisesRegex(ValueError, 'card_depth'): self.run_brief()
        self.brief['card_depth'] = 50
        self.brief['auto_rotate'] = 'yes'
        with self.assertRaisesRegex(ValueError, 'auto_rotate'): self.run_brief()
        del self.brief['auto_rotate']
        self.brief['back'] = {'title': ''}
        with self.assertRaisesRegex(ValueError, 'title'): self.run_brief()
        self.brief['back'] = {'title': 'Back'}
        self.brief['sparkles'] = 25
        with self.assertRaisesRegex(ValueError, 'sparkles'): self.run_brief()


if __name__ == '__main__': unittest.main()
