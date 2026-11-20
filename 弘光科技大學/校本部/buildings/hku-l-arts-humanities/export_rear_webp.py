"""Rebuild the rear display WebP without leaving scratch PNG/Blend in the checkout."""
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile
from xml.etree import ElementTree as ET

from PIL import Image, features

XNS = 'adobe:ns:meta/'
RNS = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
DNS = 'https://github.com/hplin50643/taiwan-buildings-3d/ns/render/1.0/'
ET.register_namespace('x', XNS)
ET.register_namespace('rdf', RNS)
ET.register_namespace('render', DNS)


def convert(source, destination):
    assert Image.__version__ == '13.0.0' and features.version('webp') == '1.6.0'
    with Image.open(source) as im:
        if im.format != 'PNG':
            raise ValueError('Expected the original rear-view PNG')
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
    with tempfile.TemporaryDirectory(prefix='hku-rear-') as scratch:
        staging = Path(scratch)
        for name in ('model.stl', 'render_preview.py'):
            shutil.copyfile(package / name, staging / name)
        subprocess.run([blender, '-b', '-t', '2', '--python-exit-code', '19',
                        '-P', str(staging / 'render_preview.py')], cwd=staging, check=True)
        webp = staging / 'rear.webp'
        convert(staging / 'previews' / 'rear.png', webp)
        shutil.copyfile(webp, package / 'previews' / 'rear.webp')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--blender', default='blender')
    args = parser.parse_args()
    export(Path(__file__).resolve().parent, args.blender)
