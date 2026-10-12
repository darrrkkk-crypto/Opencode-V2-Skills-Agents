#!/usr/bin/env python3
"""Deterministic project-local variants of Manus catalog PNG members."""
import argparse
import hashlib
import io
import json
from pathlib import PurePosixPath
import re
import sys
import warnings
import xml.etree.ElementTree as ET

import retrieve as r

VERSION = 1
RECEIPT_VERSION = 2
MAX_INPUT = 16 * 1024 * 1024
MAX_PIXELS = 4_000_000
MAX_OUTPUT = 32 * 1024 * 1024
MAX_RECIPE = 64 * 1024


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode() + b"\n"


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            r.fail("invalid_recipe", "Recipe JSON must not contain duplicate fields.")
        result[key] = value
    return result


def keys(value, required):
    if not isinstance(value, dict) or set(value) != set(required):
        r.fail("invalid_recipe", "Use exactly the documented fields for this operation.")


def identity(value, archive=False):
    required = ["member", "sha256"] + (["collection", "archiveSha256"] if archive else [])
    keys(value, required)
    r.relative_name(value["member"])
    r.hash_value(value["sha256"])
    if archive:
        r.relative_name(value["collection"])
        r.hash_value(value["archiveSha256"])


def parse_recipe(recipe):
    if not isinstance(recipe, dict) or type(recipe.get("schemaVersion")) is not int or recipe.get("schemaVersion") != VERSION:
        r.fail("invalid_recipe", "Use recipe schemaVersion 1.")
    operation = recipe.get("operation")
    if operation not in ("slice", "palette"):
        r.fail("unsupported_operation", "Choose authored XML slicing or exact RGB palette mapping.")
    keys(recipe, ["schemaVersion", "operation", "source"] + (["atlas", "frames"] if operation == "slice" else ["mapping"]))
    identity(recipe["source"], archive=True)
    if operation == "slice":
        identity(recipe["atlas"])
        frames = recipe["frames"]
        if not isinstance(frames, list) or not 1 <= len(frames) <= 64:
            r.fail("invalid_recipe", "Select between 1 and 64 exact authored frame names.")
        for frame in frames:
            r.relative_name(frame)
        if len(set(frames)) != len(frames):
            r.fail("invalid_recipe", "Select each authored frame name only once.")
    else:
        mapping = recipe["mapping"]
        if not isinstance(mapping, dict) or not 1 <= len(mapping) <= 64:
            r.fail("invalid_recipe", "Provide 1 to 64 distinct RGB replacements.")
        for old, new in mapping.items():
            if not isinstance(new, str) or not re.fullmatch(r"#[0-9a-f]{6}", old) or not re.fullmatch(r"#[0-9a-f]{6}", new) or old == new:
                r.fail("invalid_recipe", "Use distinct lowercase #rrggbb colors; alpha is preserved.")
    return recipe


def verified_bytes(path, expected, limit):
    raw = r.metadata_bytes(path, limit)
    if hashlib.sha256(raw).hexdigest() != expected:
        r.fail("integrity_failed", "The local input differs from its expected member SHA-256.")
    return raw


def pillow():
    try:
        from PIL import Image, __version__
    except ImportError:
        r.fail("image_dependency_unavailable", "Use a Python environment with Pillow already available.")
    return Image, __version__


def load_png(raw):
    Image, version = pillow()
    if raw[:8] != b"\x89PNG\r\n\x1a\n" or len(raw) < 29 or raw[24] == 16:
        r.fail("unsupported_image", "Use a single-frame PNG with at most 8 bits per channel.")
    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)
        try:
            with Image.open(io.BytesIO(raw)) as image:
                if image.format != "PNG" or getattr(image, "n_frames", 1) != 1:
                    r.fail("unsupported_image", "Use a single-frame PNG.")
                if image.width * image.height > MAX_PIXELS:
                    r.fail("image_budget_exceeded", "Use an image with at most 4 million pixels.")
                if image.mode not in ("1", "L", "LA", "P", "RGB", "RGBA"):
                    r.fail("unsupported_image", "Use an 8-bit color or indexed PNG.")
                result = image.convert("RGBA")
                result.info.clear()
                return result, version
        except (Image.DecompressionBombWarning, Image.DecompressionBombError):
            r.fail("image_budget_exceeded", "Use an image with at most 4 million pixels.")
        except (OSError, ValueError):
            r.fail("invalid_image", "The PNG could not be decoded.")


def xml_frames(raw, recipe, size):
    if b"<!" in raw or b"\x00" in raw:
        r.fail("unsupported_atlas", "Use a plain UTF-8 TextureAtlas XML without declarations or entities.")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        r.fail("invalid_atlas", "The authored atlas XML could not be parsed.")
    if root.tag != "TextureAtlas" or set(root.attrib) != {"imagePath"} or len(root) > 10000:
        r.fail("unsupported_atlas", "Use a TextureAtlas with imagePath and at most 10000 SubTexture entries.")
    image_path = r.relative_name(root.attrib["imagePath"])
    bound_member = str(PurePosixPath(recipe["atlas"]["member"]).parent / image_path)
    if bound_member != recipe["source"]["member"]:
        r.fail("atlas_source_mismatch", "The authored imagePath must identify the exact source member.")
    selected, seen = {}, set()
    for frame in root:
        if frame.tag != "SubTexture" or list(frame):
            r.fail("unsupported_atlas", "Use flat SubTexture entries.")
        name = frame.get("name")
        if not name or name in seen:
            r.fail("invalid_atlas", "Every authored frame must have a unique name.")
        seen.add(name)
        if name not in recipe["frames"]:
            continue
        if set(frame.attrib) != {"name", "x", "y", "width", "height"}:
            r.fail("unsupported_frame_geometry", "This slicer requires untrimmed, unrotated frames; preserve other authored geometry with the engine importer.")
        values = [frame.get(key) for key in ("x", "y", "width", "height")]
        if any(not re.fullmatch(r"[0-9]{1,8}", value) for value in values):
            r.fail("invalid_atlas", "Authored rectangles must use nonnegative integer pixels.")
        x, y, width, height = map(int, values)
        if width < 1 or height < 1 or x + width > size[0] or y + height > size[1]:
            r.fail("invalid_atlas", "An authored rectangle lies outside the source image.")
        selected[name] = [x, y, width, height]
    if set(selected) != set(recipe["frames"]):
        r.fail("frame_not_found", "An exact selected frame is absent from the authored atlas.")
    if sum(rect[2] * rect[3] for rect in selected.values()) > MAX_PIXELS:
        r.fail("image_budget_exceeded", "Selected frames exceed the 4 million output pixel limit.")
    return [(name, selected[name]) for name in recipe["frames"]]


def palette(image, mapping):
    convert = lambda color: tuple(bytes.fromhex(color[1:]))
    replacements = {convert(old): convert(new) for old, new in mapping.items()}
    found = set()
    raw = bytearray(image.tobytes())
    for offset in range(0, len(raw), 4):
        color = tuple(raw[offset:offset + 3])
        if color in replacements and raw[offset + 3] > 0:
            found.add(color)
            raw[offset:offset + 3] = bytes(replacements[color])
    if found != set(replacements):
        r.fail("palette_color_absent", "Every requested source color must occur in a nontransparent pixel.")
    image.frombytes(bytes(raw))
    return image


def write_file(path, data, created):
    r.no_symlinks(path)
    if path.exists():
        if not path.is_file() or path.stat().st_size != len(data) or r.digest(path) != hashlib.sha256(data).hexdigest():
            r.fail("destination_conflict", "An existing output differs; choose a separate destination.")
        return True
    with path.open("xb") as writer:
        created.append(path)
        writer.write(data)
    if r.digest(path) != hashlib.sha256(data).hexdigest():
        r.fail("integrity_failed", "The new output did not verify.")
    return False


def adapt(source_file, recipe, destination, atlas_file=None):
    recipe = parse_recipe(recipe)
    target = r.destination_path(destination)
    image, pillow_version = load_png(verified_bytes(source_file, recipe["source"]["sha256"], MAX_INPUT))
    source_size = list(image.size)
    frames = [(None, [0, 0, *image.size])]
    if recipe["operation"] == "slice":
        if atlas_file is None:
            r.fail("atlas_required", "Supply --atlas-file for the hash-bound authored descriptor.")
        frames = xml_frames(verified_bytes(atlas_file, recipe["atlas"]["sha256"], 1024 * 1024), recipe, image.size)
    elif atlas_file is not None:
        r.fail("invalid_recipe", "--atlas-file is only used by the slice operation.")
    else:
        image = palette(image, recipe["mapping"])
    recipe_sha = hashlib.sha256(canonical(recipe)).hexdigest()
    payloads, records, total = [], [], 0
    for index, (name, rect) in enumerate(frames):
        x, y, width, height = rect
        output = image.crop((x, y, x + width, y + height))
        stream = io.BytesIO()
        output.save(stream, format="PNG", optimize=False, compress_level=9)
        raw = stream.getvalue()
        total += len(raw)
        if total > MAX_OUTPUT:
            r.fail("output_budget_exceeded", "PNG outputs exceed the 32 MiB output budget.")
        filename = f"{recipe_sha[:16]}-{index:03d}.png"
        payloads.append((target / filename, raw))
        records.append({"path": filename, "sha256": hashlib.sha256(raw).hexdigest(), "sizeBytes": len(raw),
                        "sourceFrame": name, "sourceRect": rect, "size": [width, height]})
    receipt = {"schemaVersion": RECEIPT_VERSION, "tool": "catalog-adapt", "toolVersion": RECEIPT_VERSION,
               "pillowVersion": pillow_version, "recipeSha256": recipe_sha, "recipe": recipe,
               "sourceSize": source_size, "outputs": records, "alpha": "preserved",
               "coordinateConvention": "top-left origin; integer pixels; half-open rectangles",
               "archiveIdentity": "caller_supplied",
               "geometry": "authored-untrimmed-rectangles" if recipe["operation"] == "slice" else "unchanged",
               "limitations": ["No pivot, animation order, ground contact or runtime fit is inferred.",
                               "Reproducible PNG bytes require the recorded Pillow version; PNG ancillary metadata is not copied."]}
    receipt_path = target / f".catalog-adaptation-{recipe_sha[:16]}-v{RECEIPT_VERSION}.json"
    payloads.append((receipt_path, canonical(receipt)))
    verified_bytes(source_file, recipe["source"]["sha256"], MAX_INPUT)
    if atlas_file is not None:
        verified_bytes(atlas_file, recipe["atlas"]["sha256"], 1024 * 1024)
    target.mkdir(parents=True, exist_ok=True)
    created, reused = [], True
    with r.lease(r.no_symlinks(target / ".catalog-adaptation.lock")):
        try:
            for path, raw in payloads:
                reused = write_file(path, raw, created) and reused
        except BaseException:
            for path in reversed(created):
                path.unlink(missing_ok=True)
            raise
    root = r.provenance_project(target)
    provenance = {"status": "unbound"}
    if root is not None:
        source = {"catalogPath": recipe["source"]["collection"] + "/assets.zip", "memberPath": recipe["source"]["member"]}
        input_record = {"sha256": recipe["source"]["sha256"], "source": source}
        try:
            input_record["path"] = r.no_symlinks(source_file).relative_to(root).as_posix()
        except (ValueError, r.CatalogError):
            pass
        events = [{"kind": "asset", "path": (target / record["path"]).relative_to(root).as_posix(),
                   "origin": "derivative", "sha256": record["sha256"], "source": source,
                   "inputs": [input_record, {"sha256": recipe["source"]["archiveSha256"],
                                             "source": {"catalogPath": source["catalogPath"]}}],
                   "transformations": [{"operation": recipe["operation"], "tool": "catalog-adapt",
                                         "description": "Recipe " + recipe_sha + "; Pillow " + pillow_version
                                             + "; source rectangle " + json.dumps(record["sourceRect"], separators=(",", ":"))
                                             + ("; frame " + record["sourceFrame"] if record["sourceFrame"] else "")}]}
                  for record in records]
        provenance = r.record_provenance(events, root)
    return {"ok": True, "operation": recipe["operation"], "outputCount": len(records), "sizeBytes": total,
            "reused": reused, "receipt": str(receipt_path), "provenance": provenance}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-file", required=True)
    parser.add_argument("--recipe-file", required=True)
    parser.add_argument("--destination", required=True)
    parser.add_argument("--atlas-file")
    args = parser.parse_args()
    try:
        recipe = json.loads(r.metadata_bytes(args.recipe_file, MAX_RECIPE), object_pairs_hook=unique_object)
        result = adapt(args.source_file, recipe, args.destination, args.atlas_file)
    except r.CatalogError as error:
        result = error.result
    except (OSError, ValueError, TypeError, OverflowError):
        result = {"ok": False, "code": "adaptation_failed", "message": "Check the bounded recipe, input files and writable destination."}
    print(json.dumps(result, separators=(",", ":")))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
