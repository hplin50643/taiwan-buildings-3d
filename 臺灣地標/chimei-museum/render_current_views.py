"""Render the current published scene's original front and rear representative views without saving the scene."""
import bpy,json,sys
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
from pathlib import Path
name,output=sys.argv[sys.argv.index('--')+1:]
s=bpy.context.scene;cam=s.camera
assert name in ('front','rear') and cam.data.type=='ORTHO'
assert not bpy.data.libraries and not any(i.source=='FILE' and i.filepath and not i.packed_file for i in bpy.data.images)
assert all(o.hide_render for o in s.objects if 'NOTICE' in o.name)
assert tuple(cam.location)==(-220.0,-330.0,230.0)
s.render.resolution_x=1200;s.render.resolution_y=900;s.render.resolution_percentage=100
s.render.use_stamp=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
assert s.render.engine=='CYCLES'
s.cycles.samples=48;s.cycles.seed=0;s.cycles.use_denoising=False
o=next(x for x in s.objects if x.type=='MESH' and 'NOTICE' not in x.name and len(x.data.polygons)==17960)
v=[o.matrix_world @ t.co for t in o.data.vertices]
def box():
 pts=[world_to_camera_view(s,cam,x) for x in v]
 return [min(p.x for p in pts),max(p.x for p in pts),min(p.y for p in pts),max(p.y for p in pts)]
if name=='rear':
 cam.location=(220,330,230);cam.rotation_euler=(Vector((0,0,18))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=190
 bpy.context.view_layer.update()
 for _ in range(20):
  a=box()
  if a[0]>.03 and a[1]<.97 and a[2]>.14 and a[3]<.97: break
  cam.data.ortho_scale*=1.08;bpy.context.view_layer.update()
a=box(); assert a[0]>.03 and a[1]<.97 and a[2]>.14 and a[3]<.97
print('CONTROLLED_SAVED_VIEW',json.dumps(dict(camera=list(cam.location),rotation=list(cam.rotation_euler),scale=cam.data.ortho_scale,engine=s.render.engine,frame=s.frame_current,bounds=a)))
s.render.filepath=output;bpy.ops.render.render(write_still=True)
