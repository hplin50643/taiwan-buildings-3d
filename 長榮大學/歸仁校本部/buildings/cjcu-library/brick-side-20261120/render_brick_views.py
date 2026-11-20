"""Render original view recipes directly from edited scene; no persistent scene mutation."""
import bpy,sys
from pathlib import Path
from mathutils import Vector
P=Path(sys.argv[sys.argv.index('--')+1]).resolve()
bpy.ops.wm.open_mainfile(filepath=str(P/'scene.blend'))
sc=bpy.context.scene; cam=sc.camera; model=bpy.data.objects['Printable_CJCU']
assert (sc.render.resolution_x,sc.render.resolution_y)==(1000,800)
z=(min(v.co.z for v in model.data.vertices)+max(v.co.z for v in model.data.vertices))/2
prev=P/'previews';prev.mkdir(exist_ok=True)
for name,loc,aim in [('front',(195,-220,155),(0,0,z)),('rear',(-195,230,160),(0,0,z)),('elevation',(0,-260,z),(0,0,z)),('top',(0,0,300),(0,0,0)),('right-side',(260,0,z),(0,0,z))]:
 cam.location=loc;cam.rotation_euler=(Vector(aim)-cam.location).to_track_quat('-Z','Y').to_euler()
 inv=cam.rotation_euler.to_matrix().transposed(); pts=[inv@(model.matrix_world@Vector(c)-cam.location) for c in model.bound_box]
 w=max(v.x for v in pts)-min(v.x for v in pts);h=max(v.y for v in pts)-min(v.y for v in pts)
 cam.data.ortho_scale=max(w,h*sc.render.resolution_x/sc.render.resolution_y)*1.18
 sc.render.filepath=str(prev/(name+'.png'));bpy.ops.render.render(write_still=True)
