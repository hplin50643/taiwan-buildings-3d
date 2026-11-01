"""Source-inspection detail; deliberately cropped view, not whole-model framing."""
from pathlib import Path
import bpy,json,hashlib,sys
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'))
meshhash=hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()
objs=[o for o in bpy.data.objects if o.type=='MESH' and 'source_mesh_sha256' in o]
assert len(objs)==1 and objs[0]['source_mesh_sha256']==meshhash
s=bpy.context.scene;c=s.camera;c.location=(70,-5,40);c.rotation_euler=(Vector((0,14,18))-c.location).to_track_quat('-Z','Y').to_euler();c.data.type='PERSP';c.data.lens=32;c.data.clip_start=.1
s.cycles.samples=48;s.render.filepath=str(R/'bridge-detail.png');bpy.ops.render.render(write_still=True)
(R/'BRIDGE-DETAIL-QA.json').write_text(json.dumps({'status':'PASS_RENDER_EXECUTED_PENDING_VISUAL','mesh_sha256':meshhash,'cropped_detail':True,'camera_location':list(c.location),'target':[0,14,18],'camera_type':'PERSP','lens_mm':32,'png_sha256':hashlib.sha256((R/'bridge-detail.png').read_bytes()).hexdigest()},indent=2))

if '--bridge-only' in sys.argv:raise SystemExit(0)
c.data.type='ORTHO'
c.location=(50,-135,25);c.rotation_euler=(Vector((0,-78,5))-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=95
s.render.filepath=str(R/'entrance-detail.png');bpy.ops.render.render(write_still=True)
