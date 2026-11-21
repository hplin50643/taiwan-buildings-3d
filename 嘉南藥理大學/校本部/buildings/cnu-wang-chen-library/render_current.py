"""Render three controlled views of the current model; no scene edits are saved."""
from pathlib import Path
import bpy,sys,json,hashlib
from mathutils import Vector,Matrix
from bpy_extras.object_utils import world_to_camera_view
args=sys.argv[sys.argv.index('--')+1:]
mode,out=args[:2]; out=Path(out)
s=bpy.context.scene;c=s.camera
def props(cam):
 return dict(matrix=[list(r) for r in cam.matrix_world],type=cam.data.type,ortho_scale=cam.data.ortho_scale,shift=[cam.data.shift_x,cam.data.shift_y],clip=[cam.data.clip_start,cam.data.clip_end])
bpy.context.view_layer.update()
if mode=='export-original-camera':
 out.write_text(json.dumps(props(c),indent=2)+'\n')
else:
 assert mode in ('homepage','school','rear')
 assert not bpy.data.libraries and not any(i.source=='FILE' and i.filepath for i in bpy.data.images)
 assert all(x.hide_render for x in s.objects if 'NOTICE' in x.name)
 if mode=='homepage':
  p=json.loads(Path(args[2]).read_text())
  assert p['type']=='ORTHO'
  c.matrix_world=Matrix(p['matrix'])
  c.data.ortho_scale=p['ortho_scale']
  c.data.shift_x,c.data.shift_y=p['shift']
  c.data.clip_start,c.data.clip_end=p['clip']
 m=next(o for o in s.objects if o.type=='MESH' and len(o.data.polygons)==65686)
 s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=36;s.cycles.seed=0;s.cycles.use_denoising=False
 s.render.resolution_x=1200;s.render.resolution_y=900;s.render.resolution_percentage=100
 s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.use_stamp=False
 if mode=='rear':
  c.location=(-220,330,210);c.rotation_euler=(Vector((0,0,40))-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=190
 v=[m.matrix_world@r.co for r in m.data.vertices]
 def bounds():
  bpy.context.view_layer.update();p=[world_to_camera_view(s,c,x) for x in v]
  return [min(x.x for x in p),max(x.x for x in p),min(x.y for x in p),max(x.y for x in p)]
 b=bounds()
 if mode=='rear':
  for _ in range(20):
   if b[0]>.03 and b[1]<.97 and b[2]>.14 and b[3]<.97:break
   c.data.ortho_scale*=1.08;b=bounds()
 assert b[0]>0 and b[1]<1 and b[2]>0 and b[3]<1,b
 s.render.filepath=str(out);bpy.ops.render.render(write_still=True)
 proof=props(c)|{'bounds':b,'source_blend_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'settings':'1200x900 RGBA; Cycles CPU seed 0, 36 samples, denoising disabled, no stamp'}
 out.with_suffix('.json').write_text(json.dumps(proof,indent=2)+'\n')
