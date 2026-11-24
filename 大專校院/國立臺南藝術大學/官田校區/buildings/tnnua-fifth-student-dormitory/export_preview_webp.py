"""Rebuild the signed lossless preview WebPs without touching the released scene or STL."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from PIL import Image, features

VIEWS = ('elevation', 'front', 'rear')


def decode(path):
    with Image.open(path) as image:
        meta = {k: image.info[k] for k in ('exif', 'icc_profile') if k in image.info}
        return image.convert('RGBA'), meta


def encode(source, target, legacy_display=False):
    rgba, meta = decode(source)
    if legacy_display:
        rgba.convert('RGB').save(target, 'WEBP', lossless=True, method=6, quality=100, exact=True)
    else:
        rgba.save(target, 'WEBP', lossless=True, method=6, exact=True, **meta)
    if decode(target)[0].tobytes() != rgba.tobytes():
        raise ValueError(f'Lossless pixel mismatch: {target.name}')


def export(package, blender):
    if Image.__version__ != '13.0.0' or features.version('webp') != '1.6.0':
        raise RuntimeError('Use Pillow 13.0.0 with libwebp 1.6.0')
    expected = {r['path']: r for r in json.loads((package / 'hash-manifest.json').read_text())}
    for name in ('model.stl', 'render_preview.py'):
        data = (package / name).read_bytes()
        if len(data) != expected[name]['bytes'] or sha256(data).hexdigest() != expected[name]['sha256']:
            raise ValueError(f'{name}: differs from verified release')
    with tempfile.TemporaryDirectory(prefix='preview-webp-') as temp:
        stage = Path(temp)
        for name in ('model.stl', 'render_preview.py'):
            shutil.copyfile(package / name, stage / name)
        subprocess.run([blender, '-b', '-t', '4', '--python-exit-code', '19',
                        '-P', str(stage / 'render_preview.py')], cwd=stage, check=True)
        folder='display' if all(f'display/{view}.webp' in expected for view in VIEWS) else 'previews'
        for view in VIEWS:
            target = stage / f'{view}.webp'
            encode(stage / 'previews' / f'{view}.png', target, legacy_display=(folder=='display'))
            sig = expected[f'{folder}/{target.name}']
            data = target.read_bytes()
            if len(data) != sig['bytes'] or sha256(data).hexdigest() != sig['sha256']:
                raise ValueError(f'{view}: rerender WebP differs from verified release')
        for view in VIEWS:
            name = f'{view}.webp'
            shutil.copyfile(stage / name, package / folder / name)


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--blender', default='blender')
    export(Path(__file__).resolve().parent, cli.parse_args().blender)
