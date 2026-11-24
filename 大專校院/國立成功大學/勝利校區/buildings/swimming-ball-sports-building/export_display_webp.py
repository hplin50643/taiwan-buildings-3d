"""Rebuild the lossless display WebPs from the delivered STL without touching the checked-in scene."""
import argparse
import os
from hashlib import sha256
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
from xml.etree import ElementTree as ET
import zlib

from PIL import Image, features

ARCHIVAL_PNG = {'elevation': 'b18e8b5f9f3ad95f9e6d4bf652bd30c91f5c509860bd773423252ba67d47d451', 'front': '875bd4c445e34c57dddaa102266028e8f987ca55bce11d232c611341a7cc7125', 'rear': '2c4759d23490d5c88d209658f2dd148773588a8b00416776a9797ff500907df8'}
# Original Blender stamps are used only to reconstruct the historical bytes.
ARCHIVAL_STAMPS = {'elevation': {b'Date': b'2026/10/13 14:09:15', b'RenderTime': b'00:00.68'}, 'front': {b'Date': b'2026/10/13 14:09:13', b'RenderTime': b'00:02.80'}, 'rear': {b'Date': b'2026/10/13 14:09:14', b'RenderTime': b'00:00.75'}}
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
NS = {
    'x': 'adobe:ns:meta/',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'render': 'https://github.com/hplin50643/taiwan-buildings-3d/ns/render/1.0/',
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def archival_png(data, view):
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError('Expected a Blender PNG')
    stamps = ARCHIVAL_STAMPS[view]
    chunks = [PNG_SIGNATURE]
    seen = set()
    pos = len(PNG_SIGNATURE)
    while pos < len(data):
        length = struct.unpack_from('>I', data, pos)[0]
        end = pos + length + 12
        kind = data[pos+4:pos+8]
        stamp_key = data[pos+8:end-4].partition(b'\x00')[0] if kind == b'tEXt' else None
        if stamp_key in stamps:
            if stamp_key in seen:
                raise ValueError('Duplicate Blender stamp')
            seen.add(stamp_key)
            payload = stamp_key + b'\x00' + stamps[stamp_key]
            chunks.append(struct.pack('>I', len(payload)) + kind + payload
                          + struct.pack('>I', zlib.crc32(kind + payload)))
        else:
            chunks.append(data[pos:end])
        pos = end
    result = b''.join(chunks)
    if seen != stamps.keys() or sha256(result).hexdigest() != ARCHIVAL_PNG[view]:
        raise ValueError(f'{view}: rerender did not reproduce the archived PNG SHA-256')
    return result


def convert(source, destination):
    with Image.open(source) as im:
        im.load()
        meta = {key: im.info[key] for key in ('icc_profile', 'exif') if key in im.info}
        root = ET.Element(f"{{{NS['x']}}}xmpmeta")
        rdf = ET.SubElement(root, f"{{{NS['rdf']}}}RDF")
        desc = ET.SubElement(rdf, f"{{{NS['rdf']}}}Description", {f"{{{NS['rdf']}}}about": ''})
        for key in ('dpi', 'File', 'Time', 'Frame', 'Camera', 'Scene'):
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


def export(package, blender, archive_dir, scene_output=None):
    if Image.__version__ != '13.0.0' or features.version('webp') != '1.6.0':
        raise RuntimeError('Use Pillow 13.0.0 with libwebp 1.6.0 for identical output')
    for output in (archive_dir, scene_output):
        if output is not None and output.resolve().is_relative_to(package.resolve()):
            raise ValueError('Write optional archival PNGs and rebuilt scene outside the package')
    if scene_output is not None and scene_output.suffix.lower() != '.blend':
        raise ValueError('The rebuilt scene output must have a .blend extension')
    if not (package / 'previews').is_dir():
        raise ValueError('Missing package preview directory')
    with tempfile.TemporaryDirectory(prefix='ncku-swim-display-') as scratch:
        staging = Path(scratch)
        for name in ('model.stl', 'render_preview.py'):
            shutil.copyfile(package / name, staging / name)
        subprocess.run([blender, '-b', '-t', '4', '--python-exit-code', '19',
                        '-P', str(staging / 'render_preview.py')], cwd=staging, check=True,
                       env={**os.environ, 'NCKU_SWIM_RENDER_STAGING': str(staging)})
        for view in ARCHIVAL_PNG:
            png = staging / 'previews' / f'{view}.png'
            png.write_bytes(archival_png(png.read_bytes(), view))
            convert(png, staging / f'{view}.webp')
        if archive_dir is not None:
            archive_dir.mkdir(parents=True, exist_ok=True)
        for view in ARCHIVAL_PNG:
            shutil.copyfile(staging / f'{view}.webp', package / 'previews' / f'{view}.webp')
            if archive_dir is not None:
                shutil.copyfile(staging / 'previews' / f'{view}.png', archive_dir / f'{view}.png')
        if scene_output is not None:
            scene_output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(staging / 'scene.blend', scene_output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--blender', default='blender')
    parser.add_argument('--archive-png-dir', type=Path)
    parser.add_argument('--scene-output', type=Path, help='Optional path outside this package for the rebuilt Blender scene')
    args = parser.parse_args()
    export(Path(__file__).resolve().parent, args.blender, args.archive_png_dir, args.scene_output)
