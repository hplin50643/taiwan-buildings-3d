from pathlib import Path
import bpy,numpy as np,json,sys,hashlib,struct
from mathutils import Vector
R=Path(__file__).resolve().parent
ONLY_VIEW=next((x.split('=',1)[1] for x in sys.argv if x.startswith('--only-view=')),None)
source=R/'scene.blend';sha=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;cam=scene.camera;o=bpy.data.objects['TNNUA Art History Cultural Heritage partial color'];v=[x.co[:]for x in o.data.vertices]
views={'preview':(220,-330,230),'rear':(220,330,230),'front':(0,-550,75),'back':(0,550,75),'west':(-550,0,75),'east':(550,0,75),'top':(0,0,550)}
from bpy_extras.object_utils import world_to_camera_view
framing={}
for name,loc in views.items():
 if ONLY_VIEW and name!=ONLY_VIEW:continue
 cam.location=loc;target=Vector((0,0,33));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=190
 bpy.context.view_layer.update()
 for _ in range(20):
  pts=[world_to_camera_view(scene,cam,Vector(x)) for x in v];bounds=[min(p.x for p in pts),max(p.x for p in pts),min(p.y for p in pts),max(p.y for p in pts)]
  if bounds[0]>.03 and bounds[1]<.97 and bounds[2]>.14 and bounds[3]<.97:break
  cam.data.ortho_scale*=1.08;bpy.context.view_layer.update()
 assert bounds[0]>.03 and bounds[1]<.97 and bounds[2]>.14 and bounds[3]<.97,(name,bounds)
 framing[name]=bounds;scene.render.filepath=str(R/(name+'.png'));bpy.ops.render.render(write_still=True)
if framing:
 prior=R/'FRAMING-QA.json'
 if ONLY_VIEW and prior.exists():
  old=json.loads(prior.read_text())
  if old.get('mesh_sha256')==o['source_mesh_sha256']:framing={**old['projected_vertex_bounds'],**framing}
 prior.write_text(json.dumps({'status':'PASS','mesh_sha256':o['source_mesh_sha256'],'projected_vertex_bounds':framing},indent=2))

# Three deliberately cropped detail views, not full-model framing claims.
for name,loc,target,ortho in [('entry-detail',(-110,-150,80),(-49,-32,43),60),('facade-detail',(85,-150,85),(12,-27,49),85),('roof-detail',(-110,150,145),(0,4,48),120)]:
 if ONLY_VIEW and name!=ONLY_VIEW:continue
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=ortho;scene.render.filepath=str(R/(name+'.png'));bpy.ops.render.render(write_still=True)
assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
for p in R.glob('*.png'):
 data=p.read_bytes();out=data[:8];off=8
 while off<len(data):
  n=struct.unpack_from('>I',data,off)[0];kind=data[off+4:off+8]
  if kind not in [b'tEXt',b'zTXt',b'iTXt',b'eXIf']:out+=data[off:off+n+12]
  off+=n+12
 p.write_bytes(out)
