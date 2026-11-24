"""Rebuild only the released front WebP without changing the native model or other views."""
import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile
from PIL import Image, features

STL_SHA = 'a58fbb72cc91c3b083562267784816338b2f8ad5ed8e5459eb1eb53a5554b998'
RGBA_SHA = 'fff7b989ae7f98d6b6fb721e35874df605e98aac14f251f4fb866ffbbff63639'
WEBP_SHA = 'd8b77fb73dd966c97defc798046bcbd4af375792caa48d9e6d4e64598a937637'


def rgba(path):
    with Image.open(path) as image:
        if image.size != (1000, 800):
            raise ValueError('Unexpected render dimensions')
        return image.convert('RGBA')


def encode(source, target):
    with Image.open(source) as raw:
        # Preserve stable EXIF/color metadata; render time and date remain in the historical PNG.
        meta = {key: raw.info[key] for key in ('exif', 'icc_profile') if key in raw.info}
        rgba(source).save(target, 'WEBP', lossless=True, method=6, exact=True, **meta)


def export(package, blender):
    if Image.__version__ != '13.0.0' or features.version('webp') != '1.6.0':
        raise RuntimeError('Use Pillow 13.0.0 with libwebp 1.6.0')
    if hashlib.sha256((package / 'model.stl').read_bytes()).hexdigest() != STL_SHA:
        raise ValueError('Current STL differs from the verified release')
    with tempfile.TemporaryDirectory(prefix='front-display-') as directory:
        stage = Path(directory)
        for name in ('model.stl', 'render_preview.py'):
            shutil.copyfile(package / name, stage / name)
        subprocess.run([blender, '-b', '-t', '4', '--python-exit-code', '19',
                        '-P', str(stage / 'render_preview.py')], cwd=stage, check=True)
        pixels = rgba(stage / 'previews/front.png')
        if hashlib.sha256(pixels.tobytes()).hexdigest() != RGBA_SHA:
            raise ValueError('The rerender does not reproduce the verified front view')
        result = stage / 'front.webp'
        encode(stage / 'previews/front.png', result)
        if rgba(result).tobytes() != pixels.tobytes() or hashlib.sha256(result.read_bytes()).hexdigest() != WEBP_SHA:
            raise ValueError('WebP does not match the verified release')
        shutil.copyfile(result, package / 'previews/front.webp')


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--blender', default='blender')
    export(Path(__file__).resolve().parent, cli.parse_args().blender)
