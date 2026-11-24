"""Verify the published lossless WebP preview and its frozen rendering lineage."""
import argparse
import hashlib
import io
import json
from pathlib import Path

from PIL import Image

def sha(b):
    return hashlib.sha256(b).hexdigest()

def need(condition, name):
    if not condition:
        raise ValueError(name)

def verify(root, samples=None):
    load = lambda path: json.loads((root / path).read_bytes())
    proof = load("display-proof.json")
    for f, h in proof["model_sha256"].items():
        need(sha((root / f).read_bytes()) == h, f)
    manifest = load("render-manifest.json")["views"]
    historical = {x["view"]:x for x in load("RENDER-BINDING-QA.json")["checks"]}
    framing = load("FRAMING-QA.json")
    views = proof["views"]
    need(set(views) == set(historical) == set(framing["views"]) == {x["name"] for x in manifest}, "view set")
    for view in manifest:
        n = view["name"]
        r = views[n]
        need(r["preview"] == f"previews/{n}-current.webp", n + " file")
        sidecar = load(f"previews/{n}.render.json")
        need(sidecar["view"] == n and all(sidecar[k] == view[k] for k in ("camera","target","ortho_scale")), n + " camera")
        need(sidecar["mesh_sha256"] == proof["model_sha256"]["mesh-data.npz"], n + " mesh")
        need(sidecar["renderer_script_sha256"] == proof["model_sha256"]["render_model.py"], n + " renderer")
        need(historical[n]["passed"] is True and all(historical[n]["checks"].values()) and sidecar["png_sha256"] == historical[n]["png_sha256"] == r["png_sha256"], n + " historic provenance")
        need(framing["passed"] and framing["views"][n]["detail_crop_allowed"] == r["detail_view"], n + " framing")
        raw = (root / r["preview"]).read_bytes()
        need(len(raw) == r["webp_bytes"] and sha(raw) == r["webp_sha256"], n + " file SHA256")
        with Image.open(io.BytesIO(raw)) as im:
            need(im.format == "WEBP" and raw[12:16] == b"VP8L" and not getattr(im, "is_animated", False), n + " lossless WebP")
            need(list(im.size) == r["dimensions"] == sidecar["resolution"], n + " dimensions")
            need(sha(im.convert("RGBA").tobytes()) == r["decoded_rgba_sha256"], n + " decoded RGBA SHA256")
        if samples is not None:
            with Image.open(samples / f"{n}.png") as im:
                need(list(im.size) == r["dimensions"] and sha(im.convert("RGBA").tobytes()) == r["decoded_rgba_sha256"], n + " freshly rendered RGBA")
    return len(views)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch-png-dir", type=Path, help="Optional output directory of a fresh render, not checked-in PNGs")
    a = parser.parse_args()
    print(f"{verify(Path(__file__).resolve().parent, a.scratch_png_dir)} lossless WebP previews verified")
