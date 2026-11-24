"""Check published display bytes and pixels without requiring archived PNGs."""
from hashlib import sha256
from pathlib import Path
import json, sys
from PIL import Image

root = Path(__file__).resolve().parent
proof = json.loads((root / "DISPLAY-RENDER-PROOF.json").read_text())
scratch = Path(sys.argv[1]) if len(sys.argv) == 2 else None
if len(sys.argv) > 2:
    raise SystemExit("usage: verify_display_webp.py [scratch-render-directory]")

def check(condition, name):
    if not condition:
        raise SystemExit("FAIL: " + name)

def decoded(file, expected_format):
    with Image.open(file) as image:
        check(image.format == expected_format and list(image.size) == proof["resolution"], str(file) + " format/size")
        return image.convert("RGBA").tobytes()

for name, row in proof["views"].items():
    path = root / row["webp"]
    check(sha256(path.read_bytes()).hexdigest() == row["webp_sha256"], path.name + " file SHA-256")
    pixels = decoded(path, "WEBP")
    check(sha256(pixels).hexdigest() == row["rgba_sha256"], path.name + " RGBA SHA-256")
    if scratch is not None:
        check(decoded(scratch / (name + ".png"), "PNG") == pixels, name + " scratch pixel comparison")
print(f"PASS: {len(proof['views'])} WebP files" + (" and scratch render comparisons" if scratch else ""))
