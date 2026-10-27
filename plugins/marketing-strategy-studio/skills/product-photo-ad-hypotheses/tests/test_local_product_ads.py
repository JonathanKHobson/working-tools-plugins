import base64
import importlib.util
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "local_product_ads.py"
spec = importlib.util.spec_from_file_location("local_product_ads", SCRIPT)
ads = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ads)


class ProductAdsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        Image.new("RGB", (320, 400), "#8a998a").save(self.root / "product.jpg")
        Image.new("RGB", (320, 400), "#b9a7a0").save(self.root / "preview.png")
        self.brief = {
            "product_name": "Sample <item>",
            "audience": "Gift shoppers",
            "destination_label": "Explore options",
            "photos": [
                {"path": "product.jpg", "role": "product", "observations": ["A green object on a plain background."]},
                {"path": "preview.png", "role": "personalization_preview", "observations": ["A name appears on the object."]},
            ],
            "hypotheses": [
                {"angle": "Green outline", "premise": "For gift shoppers, the green outline may improve recognition of the item.", "competing_explanation": "The plain background may cause attention instead.", "observation_refs": ["P1-O1"], "falsifier": "Qualified detail visits do not improve against a control.", "metric": "Qualified detail-visit rate", "headline": "Notice the green outline", "caption": "The supplied photo shows a green object on a plain background."},
                {"angle": "Name placement", "premise": "A visible name placement may encourage gift shoppers to explore personalization.", "competing_explanation": "The alternate photo color may cause attention instead.", "observation_refs": ["P2-O1"], "falsifier": "Preview starts do not improve against a control.", "metric": "Preview-start rate", "headline": "Picture a name here", "caption": "The supplied preview shows a name on the object."},
                {"angle": "Side-by-side clarity", "premise": "Showing the item and preview together may clarify their relationship.", "competing_explanation": "Two images may attract attention regardless of clarity.", "observation_refs": ["P1-O1", "P2-O1"], "falsifier": "Qualified visits do not improve against a control.", "metric": "Qualified visit rate", "headline": "See item and preview", "caption": "Compare the green object photo with the name preview."},
            ],
            "claims": [{"text": "Lasts forever", "source": "Unverified sample", "status": "unverified"}],
            "best_first_hypothesis": 2,
            "first_test_assumption": "The name preview may prompt exploration.",
        }
        for index, idea in enumerate(self.brief["hypotheses"], 1):
            idea.update({"tension_or_desire": f"A shopper wants to understand view {index}.", "interpretation": f"View {index} may clarify the item.", "confidence": 45 + index, "confidence_rationale": "The view is visible, but buyer motive is unknown.", "opening": "Begin with the supplied view.", "reveal": "Show the item at a readable scale.", "hook": "Look closer", "proposed_extension": "An additional product gallery view.", "extension_status": "proposed", "small_test": "Compare qualified visits with a current control.", "fact_refs": []})

    def write_brief(self):
        path = self.root / "brief.json"
        path.write_text(json.dumps(self.brief), encoding="utf-8")
        return path

    def test_three_linked_creatives_and_safe_markup(self):
        output = self.root / "result"
        ads.build(self.write_brief(), output)
        self.assertEqual(sorted(p.name for p in output.iterdir()), ["ad-1.svg", "ad-2.svg", "ad-3.svg", "manifest.json", "review.html"])
        manifest = json.loads((output / "manifest.json").read_text())
        self.assertEqual(len(manifest["hypotheses"]), 3)
        self.assertEqual([h["observation_refs"] for h in manifest["hypotheses"]], [["P1-O1"], ["P2-O1"], ["P1-O1", "P2-O1"]])
        self.assertEqual({h["angle"] for h in manifest["hypotheses"]}, {"Green outline", "Name placement", "Side-by-side clarity"})
        self.assertTrue(all(h["falsifier"] and h["metric"] for h in manifest["hypotheses"]))
        self.assertEqual(manifest["hypotheses"][0]["competing_explanation"], "The plain background may cause attention instead.")
        self.assertEqual(len(manifest["observations"][0]["source_sha256"]), 64)
        self.assertIn("&lt;item&gt;", (output / "review.html").read_text())
        for i in range(1, 4):
            svg = (output / f"ad-{i}.svg").read_text()
            self.assertIn('width="1080" height="1440"', svg)
            self.assertIn("data:image/png;base64,", svg)
            self.assertNotIn("Lasts forever", svg)
            self.assertNotIn("<item>", svg)
            self.assertNotIn("AD HYPOTHESIS", svg)
            self.assertNotIn("P1-O1", svg)
            self.assertNotIn("P2-O1", svg)
        self.assertIn("Notice the green outline", (output / "ad-1.svg").read_text())
        self.assertIn("PERSONALIZATION PREVIEW", (output / "ad-2.svg").read_text())
        with self.assertRaisesRegex(ads.BriefError, "already exists"):
            ads.build(self.write_brief(), output)

    def test_rejects_remote_and_svg_sources(self):
        for bad in ("https://example.com/a.png", "file:///tmp/a.png", "art.svg"):
            with self.subTest(bad=bad):
                self.brief["photos"][0]["path"] = bad
                with self.assertRaises(ads.BriefError):
                    ads.build(self.write_brief(), self.root / "result")
                self.assertFalse((self.root / "result").exists())

    def test_rejects_missing_photo_or_target(self):
        self.brief["photos"][0]["path"] = "absent.jpg"
        with self.assertRaisesRegex(ads.BriefError, "missing photo"):
            ads.build(self.write_brief(), self.root / "result")
        self.brief["photos"][0]["path"] = "product.jpg"
        self.brief["photos"][0]["role"] = "style_reference"
        self.brief["photos"][1]["role"] = "style_reference"
        with self.assertRaisesRegex(ads.BriefError, "at least one product"):
            ads.build(self.write_brief(), self.root / "result")

    def test_rejects_bad_json_and_fake_raster(self):
        path = self.root / "brief.json"
        path.write_text("{broken", encoding="utf-8")
        with self.assertRaisesRegex(ads.BriefError, "malformed"):
            ads.build(path, self.root / "result")
        (self.root / "product.jpg").write_text("<svg/>", encoding="utf-8")
        with self.assertRaisesRegex(ads.BriefError, "unreadable raster"):
            ads.build(self.write_brief(), self.root / "result")

    def test_rejects_untrusted_control_text(self):
        self.brief["product_name"] = "Bad\x00name"
        with self.assertRaisesRegex(ads.BriefError, "controls"):
            ads.build(self.write_brief(), self.root / "result")
        self.brief["product_name"] = "Bad\ud800name"
        with self.assertRaisesRegex(ads.BriefError, "invalid Unicode"):
            ads.build(self.write_brief(), self.root / "result")

    def test_rejects_unsupported_observation_ref(self):
        self.brief["photos"][1]["role"] = "style_reference"
        with self.assertRaisesRegex(ads.BriefError, "not style references alone"):
            ads.build(self.write_brief(), self.root / "result")
        self.brief["photos"][1]["role"] = "personalization_preview"
        self.brief["hypotheses"][1]["observation_refs"] = ["P9-O9"]
        with self.assertRaisesRegex(ads.BriefError, "unsupported observation ref"):
            ads.build(self.write_brief(), self.root / "result")

    def test_requires_three_distinct_authored_hypotheses(self):
        third = self.brief["hypotheses"][2]
        self.brief["hypotheses"] = self.brief["hypotheses"][:2]
        with self.assertRaisesRegex(ads.BriefError, "exactly three authored"):
            ads.build(self.write_brief(), self.root / "result")
        third["angle"] = self.brief["hypotheses"][0]["angle"]
        self.brief["hypotheses"].append(third)
        with self.assertRaisesRegex(ads.BriefError, "distinct angles"):
            ads.build(self.write_brief(), self.root / "result")

    def test_confidence_and_fact_refs_are_bounded(self):
        self.brief["hypotheses"][0]["confidence"] = 101
        with self.assertRaisesRegex(ads.BriefError, "confidence must"):
            ads.build(self.write_brief(), self.root / "result")
        self.brief["hypotheses"][0]["confidence"] = 46
        self.brief["hypotheses"][0]["fact_refs"] = ["C1"]
        with self.assertRaisesRegex(ads.BriefError, "unapproved fact ref"):
            ads.build(self.write_brief(), self.root / "result")
        self.brief["claims"][0]["status"] = "approved"
        ads.build(self.write_brief(), self.root / "result")
        self.assertEqual(json.loads((self.root / "result" / "manifest.json").read_text())["hypotheses"][0]["fact_refs"], ["C1"])

    def test_rejects_overflow_without_truncation(self):
        self.brief["hypotheses"][0]["headline"] = "longword" * 12
        with self.assertRaisesRegex(ads.BriefError, "does not fit"):
            ads.build(self.write_brief(), self.root / "result")
        self.assertFalse((self.root / "result").exists())
        self.brief["hypotheses"][0]["headline"] = "漢" * 80
        with self.assertRaises(ads.BriefError):
            ads.build(self.write_brief(), self.root / "result")

    def test_embedded_pixels_strip_source_metadata(self):
        source = Image.new("RGB", (320, 400), "#8a998a")
        exif = Image.Exif()
        exif[270] = "PRIVATE_SOURCE_NOTE"
        source.save(self.root / "product.jpg", exif=exif)
        output = self.root / "result"
        ads.build(self.write_brief(), output)
        svg = (output / "ad-1.svg").read_text()
        encoded = re.search(r"data:image/png;base64,([A-Za-z0-9+/=]+)", svg).group(1)
        with Image.open(io.BytesIO(base64.b64decode(encoded))) as embedded:
            self.assertNotIn("exif", embedded.info)
            self.assertNotIn("icc_profile", embedded.info)
        manifest = json.loads((output / "manifest.json").read_text())
        self.assertEqual(len(manifest["observations"][0]["source_sha256"]), 64)

    def test_cli_success_and_non_overwrite_error(self):
        brief = self.write_brief()
        output = self.root / "cli-output"
        command = [sys.executable, str(SCRIPT), str(brief), str(output)]
        first = subprocess.run(command, text=True, capture_output=True, check=False)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertTrue((output / "review.html").is_file())
        second = subprocess.run(command, text=True, capture_output=True, check=False)
        self.assertEqual(second.returncode, 2)
        self.assertIn("already exists", second.stderr)

    def test_single_mockup_image_still_supports_three_concepts(self):
        self.brief["photos"] = self.brief["photos"][:1]
        self.brief["photos"][0]["role"] = "mockup"
        for idea in self.brief["hypotheses"]:
            idea["observation_refs"] = ["P1-O1"]
        output = self.root / "one-image"
        ads.build(self.write_brief(), output)
        self.assertEqual(len(list(output.glob("ad-*.svg"))), 3)
        self.assertIn("PRODUCT MOCKUP", (output / "ad-2.svg").read_text())
        self.assertEqual(json.loads((output / "manifest.json").read_text())["hypotheses"][2]["photo_refs"], ["P1"])

    def test_insights_only_cli_creates_no_render(self):
        brief = self.write_brief()
        command = [sys.executable, str(SCRIPT), str(brief), "--insights-only"]
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "insights only; no render")
        self.assertEqual(payload["best_first_hypothesis"], 2)
        self.assertEqual(len(payload["hypotheses"]), 3)
        self.assertNotIn("creative", payload["hypotheses"][0])
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ["brief.json", "preview.png", "product.jpg"])


if __name__ == "__main__":
    unittest.main()
