"""Rebuild the rear, top, and elevation display WebPs without updating the Blender scene."""
# Uses the same lossless encoding and stable metadata as the HKU L display exporter.
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile
from xml.etree import ElementTree as ET

from PIL import Image, features

XNS = 'adobe:ns:meta/'
RNS = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
VIEWS = ('rear', 'top', 'elevation')
DNS = 'https://github.com/hplin50643/taiwan-buildings-3d/ns/render/1.0/'
ET.register_namespace('x', XNS)
ET.register_namespace('rdf', RNS)
ET.register_namespace('render', DNS)


def convert(source, destination):
    if Image.__version__ != '13.0.0' or features.version('webp') != '1.6.0':
        raise RuntimeError('Install Pillow 13.0.0 with libwebp 1.6.0 for identical output')
    with Image.open(source) as im:
        if im.format != 'PNG':
            raise ValueError('Expected an original Blender PNG')
        im.load()
        meta = {k: im.info[k] for k in ('icc_profile', 'exif') if k in im.info}
        root = ET.Element(f'{{{XNS}}}xmpmeta')
        rdf = ET.SubElement(root, f'{{{RNS}}}RDF')
        desc = ET.SubElement(rdf, f'{{{RNS}}}Description', {f'{{{RNS}}}about': ''})
        for key in ('dpi', 'File', 'Time', 'Frame', 'Camera', 'Scene'):
            if key in im.info:
                value = im.info[key]
                ET.SubElement(desc, f'{{{DNS}}}{key}').text = (
                    ','.join(map(str, value)) if isinstance(value, tuple) else str(value)
                )
        meta['xmp'] = ET.tostring(root, encoding='utf-8')
        im.save(destination, 'WEBP', lossless=True, method=6, exact=True, **meta)
        with Image.open(destination) as check:
            if check.convert('RGBA').tobytes() != im.convert('RGBA').tobytes():
                raise RuntimeError('WebP failed exact full-resolution RGBA roundtrip')


def export(package, blender):
    with tempfile.TemporaryDirectory(prefix='yuntech-display-') as scratch:
        staging = Path(scratch)
        for name in ('model.stl', 'render_preview.py'):
            shutil.copyfile(package / name, staging / name)
        subprocess.run([blender, '-b', '-t', '2', '--python-exit-code', '19',
                        '-P', str(staging / 'render_preview.py')], cwd=staging, check=True)
        for view in VIEWS:
            convert(staging / 'previews' / f'{view}.png', staging / f'{view}.webp')
        for view in VIEWS:
            shutil.copyfile(staging / f'{view}.webp', package / 'previews' / f'{view}.webp')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--blender', default='blender')
    args = parser.parse_args()
    export(Path(__file__).resolve().parent, args.blender)
