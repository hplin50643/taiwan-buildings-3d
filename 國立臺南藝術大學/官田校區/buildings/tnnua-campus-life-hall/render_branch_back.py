from pathlib import Path
import bpy,numpy as np,json,sys
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'))
v=np.load(R/'color-mesh.npz')['vertices'];scene=bpy.context.scene;cam=scene.camera
o=bpy.data.objects['TNNUA Campus Life Hall partial color'];caption=bpy.data.objects['HISTORICAL_SCHEME_NOTICE_NOT_PRINT_GEOMETRY'];backing=bpy.data.objects['NOTICE_BACKDROP_NOT_PRINT_GEOMETRY']
ONLY_VIEW=next((x.split('=',1)[1]for x in sys.argv if x.startswith('--only-view=')),None)
views={'preview':(220,-330,230),'rear':(220,330,230),'front':(0,-550,75),'back':(0,550,75),'west':(-550,0,75),'east':(550,0,75),'top':(0,0,550)}
def update_caption():
 sc=cam.data.ortho_scale;caption.location=(-.45*sc,-.29*sc,-10);caption.rotation_euler=(0,0,0);caption.data.size=.026*sc
 backing.location=(-.355*sc,-.322*sc,-10.1);backing.scale=(.23*sc,.090*sc,1);backing.rotation_euler=(0,0,0)
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
 update_caption();framing[name]=bounds;scene.render.filepath=str(R/(name+'.png'));bpy.ops.render.render(write_still=True)
if framing:
 prior=R/'FRAMING-QA.json'
 if ONLY_VIEW and prior.exists():
  old=json.loads(prior.read_text())
  if old.get('mesh_sha256')==o['source_mesh_sha256']:framing={**old['projected_vertex_bounds'],**framing}
 prior.write_text(json.dumps({'status':'PASS','mesh_sha256':o['source_mesh_sha256'],'projected_vertex_bounds':framing},indent=2))

# Three deliberately cropped detail views, not full-model framing claims.
for name,loc,target,ortho in [('entry-detail',(120,-150,85),(42,-20,42),50),('facade-detail',(60,-150,38),(42,-20,42),30),('roof-detail',(-110,160,160),(25,-2,40),100)]:
 if ONLY_VIEW and name!=ONLY_VIEW:continue
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=ortho;update_caption();scene.render.filepath=str(R/(name+'.png'));bpy.ops.render.render(write_still=True)
