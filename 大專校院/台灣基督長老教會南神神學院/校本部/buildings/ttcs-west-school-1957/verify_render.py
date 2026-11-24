"""Reopen the delivered Blend and verify its front camera using scratch output only."""
import argparse, bpy, hashlib, json, struct, subprocess, sys, tempfile
from pathlib import Path
A=Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument('--image-python',help='Optional Python executable with Pillow for raw RGBA comparison')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
bpy.ops.wm.open_mainfile(filepath=str(A/'scene.blend'),load_ui=False,use_scripts=False)
with tempfile.TemporaryDirectory() as td:
    o=Path(td)/'front.png'
    bpy.context.scene.render.filepath=str(o)
    bpy.ops.render.render(write_still=True)
    raw=o.read_bytes()
    clean=raw[:8]
    pos=8
    while pos<len(raw):
        n=struct.unpack('>I',raw[pos:pos+4])[0]
        if raw[pos+4:pos+8] not in [b'tEXt',b'zTXt',b'iTXt',b'eXIf']:
            clean+=raw[pos:pos+n+12]
        pos+=n+12
    h=hashlib.sha256(clean).hexdigest()
    rep=json.loads((A/'qa/render-reopen-validation.json').read_bytes())
    d=json.loads((A/'display-proof.json').read_bytes())['exterior_webp_validation']['previews/front.png']
    assert rep['scene_front_camera_reopen_render_exact'] and rep['front_sha256']==h==d['historic_png_sha256']
    assert hashlib.sha256((A/d['webp']).read_bytes()).hexdigest()==d['webp_sha256']
    if a.image_python:
        subprocess.run([a.image_python,'-c','from pathlib import Path; import sys; sys.path.insert(0,sys.argv[1]); from verify_webp import verify; assert verify(Path(sys.argv[1]),camera=Path(sys.argv[2]))==5',str(A),str(o)],check=True)
print('Saved front camera proof passes; no checked-in PNG required.')
