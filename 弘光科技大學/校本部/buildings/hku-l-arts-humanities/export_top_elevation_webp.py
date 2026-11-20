"""Rebuild only the two non-front display WebPs using the frozen rear exporter encoder."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
from export_rear_webp import convert

VIEWS = ('top', 'elevation')


def export(package, blender):
    with tempfile.TemporaryDirectory(prefix='hku-display-') as scratch:
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
