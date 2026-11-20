"""Read saved scene, render original ten views without replacing world/materials or saving camera changes."""
from pathlib import Path
import bpy,numpy as np,json,sys,struct
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'))
scene=bpy.context.scene;cam=scene.camera;o=bpy.data.objects['Zhiben Science Engineering partial color'];v=[x.co[:]for x in o.data.vertices]
scene.render.threads_mode='FIXED';scene.render.threads=1
ONLY_VIEW=next((x.split('=',1)[1]for x in sys.argv if x.startswith('--only-view=')),None)
views={'preview':(220,-330,180),'rear':(220,330,230),'front':(0,-550,75),'back':(0,550,75),'west':(-550,0,75),'east':(550,0,75),'top':(0,0,550)}
framing={}
def render(name):
 path=R/(name+'.png');scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
 raw=path.read_bytes();out=bytearray(raw[:8]);offset=8
 while offset<len(raw):
  n=int.from_bytes(raw[offset:offset+4],'big');typ=raw[offset+4:offset+8];chunk=raw[offset:offset+n+12]
  if typ not in [b'tEXt',b'zTXt',b'iTXt']:out.extend(chunk)
  offset+=n+12
 path.write_bytes(out)
for name,loc in views.items():
 if ONLY_VIEW and name!=ONLY_VIEW:continue
 cam.location=loc;cam.rotation_euler=(Vector((0,0,33))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=190;bpy.context.view_layer.update()
 for _ in range(20):
  pts=[world_to_camera_view(scene,cam,Vector(x))for x in v];bb=[min(p.x for p in pts),max(p.x for p in pts),min(p.y for p in pts),max(p.y for p in pts)]
  if bb[0]>.03 and bb[1]<.97 and bb[2]>.14 and bb[3]<.97:break
  cam.data.ortho_scale*=1.08;bpy.context.view_layer.update()
 assert bb[0]>.03 and bb[1]<.97 and bb[2]>.14 and bb[3]<.97
 framing[name]={'projected_vertex_bounds':bb,'ortho_scale':cam.data.ortho_scale,'camera':loc};render(name)
for name,loc,target,ortho in [('entry-detail',(-125,-160,70),(-52,-22,26),60),('facade-detail',(-52,-150,29),(-52,-24,27),45),('roof-detail',(100,-130,160),(0,0,35),150)]:
 if ONLY_VIEW and name!=ONLY_VIEW:continue
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=ortho;framing[name]={'scope':'Deliberately cropped original detail, not full building','camera':loc,'target':target,'ortho_scale':ortho};render(name)
(R/'preview-framing.json').write_text(json.dumps(framing,indent=2)+'\n')
