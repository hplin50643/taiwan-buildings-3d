import bpy,json,sys,hashlib
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
from pathlib import Path
D=Path(sys.argv[sys.argv.index('--')+1]); D.mkdir(exist_ok=True,parents=True)
s=bpy.context.scene; cam=s.camera
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=32;s.cycles.seed=0;s.cycles.use_denoising=False
s.render.resolution_x=1200;s.render.resolution_y=900;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.use_stamp=False
source_sha=hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()
m=next(o for o in s.objects if o.type=='MESH' and len(o.data.polygons)==2336)
vertices=[m.matrix_world@v.co for v in m.data.vertices]
poses={}
for n,loc in {'preview':None,'rear':(220,330,230),'front':(0,-550,75),'back':(0,550,75),'west':(-550,0,75),'east':(550,0,75),'top':(0,0,550)}.items():
 if loc:
  cam.location=loc;cam.rotation_euler=(Vector((0,0,56))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=190
  for _ in range(18):
   bpy.context.view_layer.update()
   vv=[world_to_camera_view(s,cam,v) for v in vertices]
   if all(.035<v.x<.965 and .035<v.y<.965 and v.z>0 for v in vv):break
   cam.data.ortho_scale*=1.08
  else: raise RuntimeError(n)
 bpy.context.view_layer.update()
 pts=[world_to_camera_view(s,cam,v) for v in vertices]
 assert all(0<v.x<1 and 0<v.y<1 and v.z>0 for v in pts)
 poses[n]={'matrix':[list(x) for x in cam.matrix_world],'ortho_scale':cam.data.ortho_scale,'ndc_bounds':[min(v.x for v in pts),min(v.y for v in pts),max(v.x for v in pts),max(v.y for v in pts)]}
 s.render.filepath=str(D/(n+'.png'));bpy.ops.render.render(write_still=True)
(D/'poses.json').write_text(json.dumps({'source_sha256':source_sha,'camera':poses,'settings':'Cycles CPU 32 samples seed 0, no denoising/no stamp; original saved camera matrix for preview; Blender 4.3.2'},indent=2)+'\n')
