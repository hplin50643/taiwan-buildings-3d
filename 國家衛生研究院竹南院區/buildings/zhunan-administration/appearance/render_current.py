"""Render a single declared current-model view from published scene without saving."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
mode,out=sys.argv[sys.argv.index('--')+1:]
out=Path(out);s=bpy.context.scene;cam=s.camera
views={'front':None,'rear':((-180,240,155),(0,0,21),225),'elevation':((0,-290,21),(0,0,21),185),'top':((0,0,350),(0,0,0),180)}
assert mode in views and cam.data.type=='ORTHO'
assert not bpy.data.libraries and not bpy.data.texts and not any(i.source=='FILE' and i.filepath for i in bpy.data.images)
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=48;s.cycles.seed=0;s.cycles.use_denoising=False
s.render.resolution_x=1200;s.render.resolution_y=1200;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.use_stamp=False
if views[mode]:
 p,aim,scale=views[mode];cam.location=p;cam.rotation_euler=(Vector(aim)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
m=next(o for o in s.objects if o.type=='MESH' and len(o.data.polygons)==3622)
bpy.context.view_layer.update()
v=[world_to_camera_view(s,cam,m.matrix_world@x.co) for x in m.data.vertices]
assert all(.035<r.x<.965 and .035<r.y<.965 and r.z>0 for r in v)
s.render.filepath=str(out);bpy.ops.render.render(write_still=True)
proof={'camera_matrix':[list(r) for r in cam.matrix_world],'ortho_scale':cam.data.ortho_scale,'bounds':[min(r.x for r in v),max(r.x for r in v),min(r.y for r in v),max(r.y for r in v)],'source_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'settings':'Blender 4.3.2 Cycles CPU, 48 samples seed 0, no denoising and stamp, 1200x1200 RGBA'}
out.with_suffix('.json').write_text(json.dumps(proof,indent=2)+'\n')
