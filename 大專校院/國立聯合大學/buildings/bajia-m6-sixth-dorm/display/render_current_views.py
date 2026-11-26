"""Render the exact published fascia Blender scene at the four historical cameras."""
import bpy,json,sys
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(sys.argv[sys.argv.index('--')+1]).resolve()
P.mkdir(parents=True,exist_ok=True)
A=Path(__file__).resolve().parent
source=A.parent/'gable-fascia-20261120/scene.blend'
assert Path(bpy.data.filepath).resolve()==source.resolve()
proof=json.loads((A/'render-proof.json').read_text());s=bpy.context.scene;cam=s.camera
mesh=[o for o in s.objects if o.type=='MESH']; assert len(mesh)==1 and len(mesh[0].data.polygons)==7000 and len(mesh[0].data.materials)==6
assert all(mesh[0].data.polygons[i].material_index==3 for i in (6993,6999))
assert s.render.engine=='CYCLES' and s.cycles.samples==48 and s.render.resolution_x==s.render.resolution_y==1200
for v in proof['views']:
 cam.location=v['camera'];cam.rotation_euler=(Vector(v['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=v['ortho_scale'];bpy.context.view_layer.update()
 for vertex in mesh[0].data.vertices:
  p=world_to_camera_view(s,cam,mesh[0].matrix_world@vertex.co);assert .035<p.x<.965 and .035<p.y<.965 and p.z>0
 s.render.filepath=str(P/Path(v['source_path']).name)
 bpy.ops.render.render(write_still=True)
