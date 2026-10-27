"""Behavior checks for the local sticker and meme CLI."""

from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest

from PIL import Image, ImageDraw, ImageFont


SCRIPT = Path(__file__).parents[1] / "scripts" / "compose.py"


class ComposeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def run_cli(self, *args, okay=True):
        result = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, okay, result.stderr)
        return result

    def test_alpha_cutout_trims_and_preserves_subject(self):
        image = Image.new("RGBA", (100, 80), (0, 0, 0, 0))
        ImageDraw.Draw(image).ellipse((20, 10, 79, 69), fill=(220, 40, 30, 255))
        src, dst = self.root / "source.png", self.root / "sticker.png"
        image.save(src)
        self.run_cli("sticker", src, dst, "--padding", "5", "--border", "4")
        with Image.open(dst) as output:
            self.assertEqual(output.size, (78, 78))
            self.assertEqual(output.getpixel((39, 39))[:3], (220, 40, 30))
            self.assertEqual(output.getpixel((0, 0))[3], 0)
            self.assertEqual(output.getpixel((39, 6))[:3], (255, 255, 255))

    def test_meme_export_removes_private_exif(self):
        src, dst = self.root / 'private.png', self.root / 'meme.png'
        exif = Image.Exif()
        exif[315] = 'Private camera owner'
        Image.new('RGB', (600, 400), 'blue').save(src, exif=exif)
        self.run_cli('meme', src, dst, '--top', 'LOCAL CAPTION')
        with Image.open(dst) as output:
            self.assertFalse(output.getexif())

    def test_opaque_requires_explicit_shape_or_mask(self):
        src, mask, dst = (self.root / name for name in ("photo.jpg", "mask.png", "out.png"))
        Image.new("RGB", (80, 60), "blue").save(src)
        result = self.run_cli("sticker", src, dst, okay=False)
        self.assertIn("cutout requires", result.stderr)
        Image.new("L", (80, 60), 0).save(mask)
        with Image.open(mask) as m:
            m.putpixel((30, 20), 255)
            m.save(mask)
        self.run_cli("sticker", src, dst, "--mask", mask, "--border", "0", "--padding", "0")
        with Image.open(dst) as output:
            self.assertEqual(output.size, (1, 1))
            self.assertEqual(output.getpixel((0, 0))[3], 255)

    def test_circle_and_nonoverwrite(self):
        src, dst = self.root / "photo.png", self.root / "circle.png"
        Image.new("RGB", (90, 60), "green").save(src)
        self.run_cli("sticker", src, dst, "--shape", "circle", "--padding", "0", "--border", "0")
        with Image.open(dst) as output:
            self.assertEqual(output.size, (60, 60))
            self.assertEqual(output.getpixel((0, 0))[3], 0)
        self.assertIn("Output exists", self.run_cli("sticker", src, dst, "--shape", "circle", okay=False).stderr)

    def test_circle_preserves_existing_transparency(self):
        src, dst = self.root / "transparent.png", self.root / "circle.png"
        image = Image.new("RGBA", (50, 50), (255, 0, 0, 0))
        ImageDraw.Draw(image).rectangle((20, 20, 30, 30), fill=(255, 0, 0, 255))
        image.save(src)
        self.run_cli("sticker", src, dst, "--shape", "circle", "--padding", "0", "--border", "0")
        with Image.open(dst) as output:
            self.assertEqual(output.getpixel((10, 25))[3], 0)
            self.assertEqual(output.getpixel((25, 25))[3], 255)

    def test_meme_native_dimensions_font_and_overflow(self):
        src, dst = self.root / "photo.png", self.root / "meme.png"
        Image.new("RGB", (600, 400), "#404040").save(src)
        result = self.run_cli("meme", src, dst, "--top", "LOCAL LAYOUT", "--bottom", "NO UPLOADS")
        self.assertIn("font:", result.stdout)
        with Image.open(dst) as output:
            self.assertEqual(output.size, (600, 400))
            self.assertNotEqual(output.convert("RGB").getpixel((300, 20)), (64, 64, 64))
        long = "UNBREAKABLE" * 40
        result = self.run_cli("meme", src, self.root / "bad.png", "--top", long, okay=False)
        self.assertIn("does not fit", result.stderr)

    def test_exact_caption_characters_and_explicit_breaks(self):
        module = runpy.run_path(str(SCRIPT))
        font = ImageFont.truetype(str(module["font_path"](None)), 32)
        canvas = Image.new("RGB", (1000, 200), "black")
        lines = module["wrap_caption"](ImageDraw.Draw(canvas), "FIRST  LINE!\n你好 😀\nLAST?", font, 900, 2)
        self.assertEqual(lines, ["FIRST  LINE!", "你好 😀", "LAST?"])

    def test_rejects_url_svg_and_oversize(self):
        dst = self.root / "out.png"
        self.assertIn("local filesystem path", self.run_cli("sticker", "https://example.com/a.png", dst, okay=False).stderr)
        svg = self.root / "source.svg"
        svg.write_text("<svg></svg>")
        self.assertIn("no SVG", self.run_cli("sticker", svg, dst, okay=False).stderr)
        large = self.root / "large.png"
        Image.new("RGB", (8200, 2), "red").save(large)
        self.assertIn("exceeds", self.run_cli("sticker", large, dst, "--shape", "rectangle", okay=False).stderr)

    def test_exif_orientation_and_mask_size(self):
        src, mask, dst = (self.root / name for name in ("rotated.jpg", "mask.png", "sticker.png"))
        exif = Image.Exif()
        exif[274] = 6  # 90 degrees clockwise: 40x20 becomes 20x40.
        Image.new("RGB", (40, 20), "purple").save(src, exif=exif)
        Image.new("L", (40, 20), 255).save(mask)
        self.assertIn("oriented source", self.run_cli("sticker", src, dst, "--mask", mask, okay=False).stderr)
        Image.new("L", (20, 40), 255).save(mask)
        self.run_cli("sticker", src, dst, "--mask", mask, "--border", "0", "--padding", "0")
        with Image.open(dst) as output:
            self.assertEqual(output.size, (20, 40))

    def test_palette_transparency_and_mask_protection(self):
        src, mask, dst = (self.root / name for name in ("indexed.png", "mask.png", "sticker.png"))
        indexed = Image.new("P", (10, 10), 0)
        indexed.putpalette([0, 0, 0, 255, 0, 0] + [0] * (256 * 3 - 6))
        indexed.info["transparency"] = 0
        indexed.putpixel((5, 5), 1)
        indexed.save(src)
        self.run_cli("sticker", src, dst, "--border", "0", "--padding", "0")
        with Image.open(dst) as output:
            self.assertEqual(output.size, (1, 1))
            self.assertEqual(output.getpixel((0, 0))[:3], (255, 0, 0))
        Image.new("L", (10, 10), 255).save(mask)
        result = self.run_cli("sticker", src, mask, "--mask", mask, "--overwrite", okay=False)
        self.assertIn("differ from source and mask", result.stderr)


if __name__ == "__main__":
    unittest.main()
