"""Rebuild all six lossless display WebPs in temporary staging without touching the delivered scene."""
import argparse
import os
from hashlib import sha256
from pathlib import Path
import shutil
import subprocess
import tempfile
from xml.etree import ElementTree as ET

from PIL import Image, features

EXPECTED_RGBA = {'front_detail': '30cc8236111f87c67e016a50e6156ef30df82d1d2314c66c9a14c196fe5d64cb', 'rear_unreconstructed': 'b7c3ab3ae6a417755e9c41aa4240afc5d79bea179f8541f930a6b8fc0dedd5f1', 'top': 'c2f5762dc36b9c3accf836b390c70aae5820e446d4d3e7b45b28bfad516d86ec', 'front': 'a8586a0e606ef74933a1dba5cfdbd136b3981318a180b5b36df06110b07ca35a', 'front_elevation': 'e2a010be9dbf9289e0689569ed4ac4d37ea9df677bacab7c6ad9f63807af89e9', 'observed_short_end': 'cc9fb105d30224c8e73cd2d6f18c4266e8c8cbddb98bf9a0706c6b78415fbcb5'}
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


def export(package, blender, rendered_png_dir, scene_output=None):
    if Image.__version__ != '13.0.0' or features.version('webp') != '1.6.0':
        raise RuntimeError('Use Pillow 13.0.0 with libwebp 1.6.0 for identical output')
    for output in (rendered_png_dir, scene_output):
        if output is not None and output.resolve().is_relative_to(package.resolve()):
            raise ValueError('Write optional PNGs and rebuilt scene outside the package')
    if scene_output is not None and scene_output.suffix.lower() != '.blend':
        raise ValueError('The rebuilt scene output must have a .blend extension')
    manifest = {r['path']: r for r in __import__('json').loads((package / 'manifest.json').read_text())['files']}
    with tempfile.TemporaryDirectory(prefix='nuk-power-station-display-') as scratch:
        staging = Path(scratch)
        for name in ('mesh-data.npz', 'editable-parts.json', 'construction-parts.json', 'render_model.py'):
            shutil.copyfile(package / name, staging / name)
        subprocess.run([blender, '-b', '-t', '4', '--python-exit-code', '19',
                        '-P', str(staging / 'render_model.py'), '--', '--views', ','.join(EXPECTED_RGBA)],
                       cwd=staging, env={**os.environ, "NUK_WEBP_RENDER_STAGING":str(staging)}, check=True)
        for view in EXPECTED_RGBA:
            png = staging / 'previews' / f'{view}.png'
            with Image.open(png) as im:
                if im.size != (1200, 800) or sha256(im.convert('RGBA').tobytes()).hexdigest() != EXPECTED_RGBA[view]:
                    raise ValueError(f'{view}: Blender render did not reproduce the released display pixels')
            p = staging / f'{view}.webp'
            convert(png, p)
            row = manifest[f'previews/{view}.webp']
            if p.stat().st_size != row['bytes'] or sha256(p.read_bytes()).hexdigest() != row['sha256']:
                raise ValueError(f'{view}: reproduced WebP does not match current delivery')
        if rendered_png_dir is not None:
            rendered_png_dir.mkdir(parents=True, exist_ok=True)
        for view in EXPECTED_RGBA:
            shutil.copyfile(staging / f'{view}.webp', package / 'previews' / f'{view}.webp')
            if rendered_png_dir is not None:
                shutil.copyfile(staging / 'previews' / f'{view}.png', rendered_png_dir / f'{view}.png')
        if scene_output is not None:
            scene_output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(staging / 'scene.blend', scene_output)
    print('Six exact WebP files checked and exported without touching delivered geometry.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--blender', default='blender')
    parser.add_argument('--rendered-png-dir', type=Path)
    parser.add_argument('--scene-output', type=Path)
    args = parser.parse_args()
    export(Path(__file__).resolve().parent, args.blender, args.rendered_png_dir, args.scene_output)
