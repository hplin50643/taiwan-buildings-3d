"""Render five publishable WebP previews from the delivered model, isolated from native files."""
from PIL import Image, features
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, tempfile

PACKAGE = Path(__file__).resolve().parent
sha256 = lambda data: hashlib.sha256(data).hexdigest()

def export(blender, archive_dir=None, scene_output=None):
    if Image.__version__ != '13.0.0' or features.version('webp') != '1.6.0':
        raise RuntimeError('Use Pillow 13.0.0 with libwebp 1.6.0 for identical output')
    for dest in (archive_dir, scene_output):
        if dest is not None and dest.resolve().is_relative_to(PACKAGE.resolve()):
            raise ValueError('Write optional archival PNGs and rebuilt scene outside the package')
    if scene_output is not None and scene_output.suffix.lower() != '.blend':
        raise ValueError('The rebuilt scene output must have a .blend extension')
    manifest = json.loads((PACKAGE/'qa/render-manifest.json').read_text())
    with tempfile.TemporaryDirectory(prefix='nsysu-bridge-display-') as tmp:
        stage = Path(tmp)
        for n in ('model.stl','model.3mf','palette.json','render_model.py'):
            shutil.copyfile(PACKAGE/n, stage/n)
        for n in ('previews','qa'):
            (stage/n).mkdir()
        subprocess.run([blender,'-b','--threads','6','--python-exit-code','19','--python',str(stage/'render_model.py')],
                       cwd=stage, env={**os.environ,'NSYSU_BRIDGE_RENDER_STAGING':str(stage)}, check=True)
        for v in manifest['files']:
            archive = v['archival_png']
            source = stage/archive['path']
            raw = source.read_bytes()
            if len(raw) != archive['bytes'] or sha256(raw) != archive['sha256']:
                raise ValueError(f"{archive['path']}: rerender failed archived PNG byte check")
            dest = stage/v['path']
            with Image.open(source) as im:
                rgba = im.convert('RGBA')
                if list(rgba.size) != manifest['resolution'] or sha256(rgba.tobytes()) != v['rgba_sha256']:
                    raise ValueError(f'{source.name}: source pixel or resolution mismatch')
                rgba.save(dest,'WEBP',lossless=True,method=6,exact=True)
                with Image.open(dest) as check:
                    if check.size != rgba.size or check.convert('RGBA').tobytes() != rgba.tobytes():
                        raise ValueError(f'{dest.name}: WebP does not preserve original RGBA')
            packed = dest.read_bytes()
            if len(packed) != v['bytes'] or sha256(packed) != v['sha256']:
                raise ValueError(f'{dest.name}: exact encoded WebP differs from current manifest')
        for v in manifest['files']:
            shutil.copyfile(stage/v['path'], PACKAGE/v['path'])
            if archive_dir is not None:
                archive_dir.mkdir(parents=True, exist_ok=True)
                previous = v['archival_png']['path']
                shutil.copyfile(stage/previous, archive_dir/Path(previous).name)
        if scene_output is not None:
            scene_output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(stage/'scene.blend',scene_output)
    print('All five WebP bytes, decoded pixels, and archived PNG digests match.')

if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__)
    p.add_argument('--blender',default='blender')
    p.add_argument('--archive-png-dir',type=Path)
    p.add_argument('--scene-output',type=Path)
    a=p.parse_args();export(a.blender,a.archive_png_dir,a.scene_output)
