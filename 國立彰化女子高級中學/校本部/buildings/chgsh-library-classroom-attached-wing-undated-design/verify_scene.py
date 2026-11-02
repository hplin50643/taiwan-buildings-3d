from pathlib import Path
import bpy,numpy as np,json,hashlib
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'))
d=np.load(R/'mesh.npz');o=bpy.data.objects.get('CHGSH library classroom historical attached wing')
assert o is not None
v=np.array([x.co[:] for x in o.data.vertices]);f=np.array([x.vertices[:] for x in o.data.polygons]);sha=hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()
checks={'mesh_vertices_match':bool(np.allclose(v,d['vertices'],atol=1e-5)),'mesh_faces_exact':bool(np.array_equal(f,d['faces'])),'mesh_sha_property_matches':o.get('source_mesh_sha256')==sha,'scale_property':o.get('scale')=='1:150','camera_exists':bpy.context.scene.camera is not None,'triangulated':all(len(p.vertices)==3 for p in o.data.polygons)}
checks['historical_notice_exists']=bpy.data.objects.get('HISTORICAL_SCHEME_NOTICE_NOT_PRINT_GEOMETRY') is not None
checks['material_indices_match']=bool(np.array_equal(np.array([p.material_index for p in o.data.polygons]),d['materials']))
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
scene=bpy.context.scene;cam=scene.camera;bpy.context.view_layer.update();pts=[world_to_camera_view(scene,cam,Vector(x)) for x in v];bounds=[min(p.x for p in pts),max(p.x for p in pts),min(p.y for p in pts),max(p.y for p in pts)];checks['saved_camera_full_model_margin']=bool(bounds[0]>.03 and bounds[1]<.97 and bounds[2]>.03 and bounds[3]<.97)
q={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'mesh_sha256':sha};(R/'SCENE-QA.json').write_text(json.dumps(q,indent=2));print(q);assert all(checks.values())
