"""Verify active preview bytes and decoded RGBA; optionally compare a new scratch render."""
from hashlib import sha256
from pathlib import Path
import json
import sys
from PIL import Image

root = Path(__file__).resolve().parent
manifest = json.loads((root / "preview-webp-proof.json").read_text())
scratch = Path(sys.argv[1]) if len(sys.argv) == 2 else None
if len(sys.argv) > 2:
    raise SystemExit("usage: verify_preview_webp.py [scratch-previews-directory]")

def require(value, reason):
    if not value:
        raise SystemExit("FAIL " + reason)

def digest(data):
    return sha256(data).hexdigest()

def rgba(path, kind, dimensions):
    with Image.open(path) as image:
        require(image.format == kind and list(image.size) == dimensions, str(path) + " format/dimensions")
        return image.convert("RGBA").tobytes()

for file, expected in manifest["source_sha256"].items():
    require(digest((root / file).read_bytes()) == expected, file + " source SHA-256")
for row in manifest["views"]:
    p = root / row["webp"]
    require(digest(p.read_bytes()) == row["webp_sha256"], p.name + " file SHA-256")
    pixels = rgba(p, "WEBP", row["dimensions"])
    require(digest(pixels) == row["rgba_sha256"], p.name + " decoded RGBA SHA-256")
    if scratch is not None:
        png = scratch / Path(row["original_path"]).name
        require(rgba(png, "PNG", row["dimensions"]) == pixels, png.name + " scratch RGBA")
print(f"PASS: {len(manifest['views'])} previews" + (" and scratch RGBA" if scratch is not None else ""))
