#!/usr/bin/env python3
"""Regression tests; synthetic fixtures are not a test of semantic readability.

Run with the available Python 3 interpreter. Requires Pillow.
"""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image, ImageChops, ImageOps

SCRIPT = Path(__file__).resolve().with_name("slice_image.py")
SPEC = importlib.util.spec_from_file_location("slice_image", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ScreeningTests(unittest.TestCase):
    def test_exact_four_to_one_matches(self):
        self.assertIn("longest_side_over_shortest_side_gte_4", MODULE.screening_signals(1600, 400))
        self.assertIn("longest_side_over_shortest_side_gte_4", MODULE.screening_signals(400, 1600))

    def test_below_four_to_one_does_not_match(self):
        self.assertEqual(MODULE.screening_signals(1599, 400), [])

    def test_side_boundary_is_strict(self):
        self.assertEqual(MODULE.screening_signals(4096, 1025), [])
        self.assertIn("side_gt_4096_pixels", MODULE.screening_signals(4097, 1025))

    def test_area_boundary_is_strict(self):
        self.assertEqual(MODULE.screening_signals(4000, 4000), [])
        self.assertEqual(MODULE.screening_signals(4000, 4001), ["area_gt_16000000_pixels"])

    def test_unknown_is_not_a_negative_readability_assessment(self):
        decision = MODULE.preprocessing_decision("unknown", False)
        self.assertIsNone(decision["preprocessing_required"])
        self.assertFalse(decision["tiling_requested"])

    def test_force_does_not_claim_unreadability(self):
        decision = MODULE.preprocessing_decision("unknown", True)
        self.assertIsNone(decision["preprocessing_required"])
        self.assertTrue(decision["tiling_requested"])


class CliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="image tests 中文 ")
        cls.root = Path(cls.temp.name)
        cls.sources = {}
        for name, size in {"wide": (1620, 232), "long": (1440, 20000), "normal": (1200, 900)}.items():
            path = cls.root / f"{name} 原图.png"
            with Image.new("RGB", size, (37, 51, 73)) as image:
                image.putpixel((0, 0), (1, 2, 3))
                image.putpixel((size[0] - 1, size[1] - 1), (4, 5, 6))
                image.save(path)
            cls.sources[name] = path

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def call(self, source="wide", *flags):
        output = self.root / self._testMethodName
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(self.sources[source]), "--output-dir", str(output), *flags],
            text=True, encoding="utf-8", capture_output=True, check=True,
        )
        return json.loads(result.stdout), output

    def assert_no_tiles(self, result, output):
        self.assertFalse(result["tiled"])
        self.assertFalse(output.exists(), "Inspection must not create an output directory")

    def verify_tiles(self, result, output):
        self.assertTrue(result["tiled"])
        manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(result["tiles"], manifest["tiles"])
        self.assertEqual(result["tile_count"], len(result["tiles"]))
        self.assertGreater(result["tile_count"], 1)
        source = ImageOps.exif_transpose(Image.open(result["source"])).convert("RGB")
        width, height = source.size
        tiles = result["tiles"]
        self.assertEqual([t["index"] for t in tiles], list(range(1, len(tiles) + 1)))
        self.assertEqual([(t["y"], t["x"]) for t in tiles], sorted((t["y"], t["x"]) for t in tiles))
        for tile in tiles:
            box = (tile["x"], tile["y"], tile["x"] + tile["pixel_width"], tile["y"] + tile["pixel_height"])
            self.assertLessEqual(box[2], width)
            self.assertLessEqual(box[3], height)
            with Image.open(tile["path"]) as actual:
                self.assertEqual(actual.size, (tile["pixel_width"], tile["pixel_height"]))
                self.assertIsNone(ImageChops.difference(actual.convert("RGB"), source.crop(box)).getbbox())
        for position, span, limit in [("x", "pixel_width", width), ("y", "pixel_height", height)]:
            segments = sorted(set((t[position], t[position] + t[span]) for t in tiles))
            self.assertEqual(segments[0][0], 0)
            self.assertEqual(segments[-1][1], limit)
            for previous, current in zip(segments, segments[1:]):
                self.assertLess(current[0], previous[1], "Adjacent tiles must overlap without gaps")
        source.close()

    def test_wide_unknown_does_not_tile(self):
        result, output = self.call()
        self.assert_no_tiles(result, output)
        self.assertTrue(result["geometry_screening_match"])
        self.assertIsNone(result["preprocessing_required"])

    def test_wide_readable_does_not_tile(self):
        result, output = self.call("wide", "--readability", "readable")
        self.assert_no_tiles(result, output)
        self.assertFalse(result["preprocessing_required"])

    def test_long_unknown_does_not_tile(self):
        result, output = self.call("long")
        self.assert_no_tiles(result, output)
        self.assertEqual(len(result["screening_signals"]), 3)

    def test_long_readable_does_not_tile(self):
        result, output = self.call("long", "--readability", "readable")
        self.assert_no_tiles(result, output)

    def test_ordinary_unknown_does_not_tile(self):
        result, output = self.call("normal")
        self.assert_no_tiles(result, output)
        self.assertFalse(result["geometry_screening_match"])

    def test_mode_alone_does_not_tile(self):
        result, output = self.call("wide", "--mode", "horizontal")
        self.assert_no_tiles(result, output)

    def test_unreadable_long_tiles_vertically(self):
        result, output = self.call("long", "--readability", "unreadable")
        self.assertEqual(result["mode"], "vertical")
        self.assertTrue(result["preprocessing_required"])
        self.verify_tiles(result, output)

    def test_unreadable_ordinary_image_tiles_as_grid(self):
        result, output = self.call("normal", "--readability", "unreadable")
        self.assertEqual(result["mode"], "grid")
        self.assertFalse(result["geometry_screening_match"])
        self.verify_tiles(result, output)

    def test_explicit_force_tiles_horizontally(self):
        result, output = self.call("wide", "--force")
        self.assertEqual(result["mode"], "horizontal")
        self.assertIsNone(result["preprocessing_required"])
        self.verify_tiles(result, output)

    def test_inspect_only_never_tiles_even_with_override(self):
        result, output = self.call("wide", "--force", "--inspect-only")
        self.assert_no_tiles(result, output)
        self.assertEqual(result["operation"], "inspect-only")

    def test_readable_and_force_conflict(self):
        with self.assertRaises(subprocess.CalledProcessError) as raised:
            self.call("wide", "--force", "--readability", "readable")
        self.assertIn("conflicts", raised.exception.stderr)

    def test_invalid_overlap_is_rejected(self):
        with self.assertRaises(subprocess.CalledProcessError):
            self.call("wide", "--overlap", "0.5")

    def test_exif_oriented_header_and_tiles_agree(self):
        path = self.root / "rotated 原图.jpg"
        with Image.new("RGB", (800, 200), (5, 15, 25)) as image:
            exif = Image.Exif()
            exif[274] = 6
            image.save(path, exif=exif)
        self.sources["rotated"] = path
        inspected, output = self.call("rotated", "--inspect-only")
        self.assert_no_tiles(inspected, output)
        self.assertEqual((inspected["pixel_width"], inspected["pixel_height"]), (200, 800))
        result, output = self.call("rotated", "--readability", "unreadable")
        self.assertEqual(result["mode"], "vertical")
        self.verify_tiles(result, output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
