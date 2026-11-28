"""Reopen the delivered scene in Blender and verify its saved front camera."""
import bpy, os, subprocess, tempfile
from pathlib import Path
A=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(A/'scene.blend'))
with tempfile.TemporaryDirectory() as td:
    p=Path(td)/'front.png'
    bpy.context.scene.render.filepath=str(p)
    bpy.ops.render.render(write_still=True)
    subprocess.run([os.environ.get('MODEL_VERIFY_PYTHON','python3'),'-B',str(A/'verify_front_pixels.py'),str(p)],check=True)
