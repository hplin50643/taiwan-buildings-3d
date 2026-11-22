"""Reopen exact current Taipei 101 model; render the prior angles without saving."""
import bpy,json,sys
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
name,output=sys.argv[sys.argv.index('--')+1:]
s=bpy.context.scene;cam=s.camera
assert cam.data.type=='ORTHO' and tuple(cam.location)==(220.,-330.,240.)
assert not bpy.data.libraries and not bpy.data.texts and not bpy.data.movieclips
assert not any(x.source=='FILE' for x in bpy.data.images)
assert all(o.hide_render for o in s.objects if o.type in ('FONT','CURVE') or 'NOTICE' in o.name)
s.render.resolution_x=1200;s.render.resolution_y=900;s.render.resolution_percentage=100
s.render.use_stamp=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
assert s.render.engine=='CYCLES' and s.cycles.samples==48 and not s.cycles.use_denoising
s.cycles.seed=0;s.cycles.device='CPU'
o=next(x for x in s.objects if x.type=='MESH' and len(x.data.polygons)==19150)
v=[o.matrix_world @ x.co for x in o.data.vertices]
def box():
 pts=[world_to_camera_view(s,cam,x) for x in v]
 return [min(p.x for p in pts),max(p.x for p in pts),min(p.y for p in pts),max(p.y for p in pts)]
views={'preview':(220,-330,240),'rear':(-220,330,240),'front':(0,-550,25),'back':(0,550,25),'west':(-550,0,25),'east':(550,0,25),'top':(0,0,550)}
details={'entry-detail':((85,-170,95),(0,-43,24),90),'corridor-detail':((65,-140,72),(0,-45,33),65),'roof-detail':((90,-100,95),(0,-29,43),80)}
if name in views: loc,target,scale=views[name],(0,0,24),190
else: loc,target,scale=details[name]
cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
bpy.context.view_layer.update()
if name in views:
 for _ in range(20):
  a=box()
  if a[0]>.03 and a[1]<.97 and a[2]>.14 and a[3]<.97:break
  cam.data.ortho_scale*=1.08;bpy.context.view_layer.update()
 assert a[0]>.03 and a[1]<.97 and a[2]>.14 and a[3]<.97
print('CURRENT_VIEW',json.dumps(dict(location=loc,target=target,scale=cam.data.ortho_scale,coordinates=box(),rotation=list(cam.rotation_euler))))
s.render.filepath=output;bpy.ops.render.render(write_still=True)
if name=='preview':
 Path(output+'.native.json').write_text(json.dumps({'vertices':[[*x] for x in v],'faces':[[*f.vertices] for f in o.data.polygons],'material':[f.material_index for f in o.data.polygons]},separators=(',',':')))
