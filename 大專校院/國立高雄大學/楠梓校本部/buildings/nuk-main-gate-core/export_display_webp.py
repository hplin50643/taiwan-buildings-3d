"""Rebuild the three lossless display WebPs without touching the delivered scene or any other preview."""
import argparse
from hashlib import sha256
from pathlib import Path
import shutil
import subprocess
import tempfile
from xml.etree import ElementTree as ET

from PIL import Image, features

EXPECTED_RGBA = {'observed_side': 'e5be0edf81f4191e62118d110a5678c8d3e24846740185bc1ec13bb00929f6c9', 'neutral_rear': '08023446307d5f68d5a46a83fdd420a608bfcce0a782bf4929be85d73448390d', 'top': '88966ea1f81664f2e428bae34ac56347c8f863275c27f10e3172368796ad52f2'}
NS = {
    'x': 'adobe:ns:meta/',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'render': 'https://github.com/hplin50643/taiwan-buildings-3d/ns/render/1.0/',
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def convert(source, destination):
    with Image.open(source) as im:
        im.load()
        meta = {key: im.info[key] for key in ('icc_profile', 'exif') if key in im.info}
        root = ET.Element(f"{{{NS['x']}}}xmpmeta")
        rdf = ET.SubElement(root, f"{{{NS['rdf']}}}RDF")
        desc = ET.SubElement(rdf, f"{{{NS['rdf']}}}Description", {f"{{{NS['rdf']}}}about": ''})
        for key in ('dpi', 'Time', 'Frame', 'Camera', 'Scene'):
            if key in im.info:
                value = im.info[key]
                ET.SubElement(desc, f"{{{NS['render']}}}{key}").text = (
                    ','.join(map(str, value)) if isinstance(value, tuple) else str(value)
                )
        meta['xmp'] = ET.tostring(root, encoding='utf-8')
        im.save(destination, 'WEBP', lossless=True, method=6, exact=True, **meta)
        with Image.open(destination) as check:
            if im.size != check.size or check.convert('RGBA').tobytes() != im.convert('RGBA').tobytes():
                raise ValueError('Lossless WebP failed the full-resolution RGBA comparison')


def export(package, blender, rendered_png_dir):
    if Image.__version__ != '13.0.0' or features.version('webp') != '1.6.0':
        raise RuntimeError('Use Pillow 13.0.0 with libwebp 1.6.0 for identical output')
    if rendered_png_dir is not None and rendered_png_dir.resolve() == (package / 'previews').resolve():
        raise ValueError('Write archival PNGs outside the tracked preview directory')
    with tempfile.TemporaryDirectory(prefix='nuk-main-gate-display-') as scratch:
        staging = Path(scratch)
        for name in ('mesh-data.npz', 'editable-parts.json', 'construction-parts.json', 'render_model.py'):
            shutil.copyfile(package / name, staging / name)
        subprocess.run([blender, '-b', '-t', '4', '--python-exit-code', '19',
                        '-P', str(staging / 'render_model.py'), '--', '--views', ','.join(EXPECTED_RGBA)],
                       cwd=staging, check=True)
        for view in EXPECTED_RGBA:
            png = staging / 'previews' / f'{view}.png'
            with Image.open(png) as im:
                if im.size != (1200, 900) or sha256(im.convert('RGBA').tobytes()).hexdigest() != EXPECTED_RGBA[view]:
                    raise ValueError(f'{view}: Blender render did not reproduce the released display pixels')
            convert(png, staging / f'{view}.webp')
        if rendered_png_dir is not None:
            rendered_png_dir.mkdir(parents=True, exist_ok=True)
        for view in EXPECTED_RGBA:
            shutil.copyfile(staging / f'{view}.webp', package / 'previews' / f'{view}.webp')
            if rendered_png_dir is not None:
                shutil.copyfile(staging / 'previews' / f'{view}.png', rendered_png_dir / f'{view}.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--blender', default='blender')
    parser.add_argument('--rendered-png-dir', type=Path)
    args = parser.parse_args()
    export(Path(__file__).resolve().parent, args.blender, args.rendered_png_dir)
