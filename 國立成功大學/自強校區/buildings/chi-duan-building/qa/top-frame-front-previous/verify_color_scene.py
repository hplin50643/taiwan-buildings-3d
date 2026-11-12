from pathlib import Path
import bpy,numpy as np,json,hashlib
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'))
d=np.load(R/'color-mesh.npz');objects=[x for x in bpy.data.objects if x.type=='MESH' and x.name.startswith('NCKU Chi Duan') and x.get('source_mesh_sha256')];assert len(objects)==1;o=objects[0]
assert o is not None
v=np.array([x.co[:] for x in o.data.vertices]);f=np.array([x.vertices[:] for x in o.data.polygons]);sha=hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()
checks={'object_identity':o.name.startswith('NCKU Chi Duan'),'mesh_vertices_match':bool(np.allclose(v,d['vertices'],atol=1e-5)),'mesh_faces_exact':bool(np.array_equal(f,d['faces'])),'mesh_sha_property_matches':o.get('source_mesh_sha256')==sha,'scale_property':o.get('scale')=='independent150mm','camera_exists':bpy.context.scene.camera is not None,'triangulated':all(len(p.vertices)==3 for p in o.data.polygons)}
pal=json.loads((R/'palette.json').read_text());checks['seven_actual_material_slots']=len(o.data.materials)==len(pal)==7
checks['actual_shader_palette']=all(np.allclose(mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value[:3],[(q/12.92 if q<=.04045 else ((q+.055)/1.055)**2.4)for q in [int(col[j:j+2],16)/255 for j in (1,3,5)]],atol=1e-6)for mat,(_,col)in zip(o.data.materials,pal))
checks['historical_notice_exists']=bpy.data.objects.get('HISTORICAL_SCHEME_NOTICE_NOT_PRINT_GEOMETRY') is not None
checks['material_indices_match']=bool(np.array_equal(np.array([p.material_index for p in o.data.polygons]),d['materials']))
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
scene=bpy.context.scene;cam=scene.camera;bpy.context.view_layer.update();pts=[world_to_camera_view(scene,cam,Vector(x)) for x in v];bounds=[min(p.x for p in pts),max(p.x for p in pts),min(p.y for p in pts),max(p.y for p in pts)];checks['saved_camera_full_model_margin']=bool(bounds[0]>.03 and bounds[1]<.97 and bounds[2]>.03 and bounds[3]<.97)
q={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'mesh_sha256':sha};(R/'SCENE-QA.json').write_text(json.dumps(q,indent=2));print(q);assert all(checks.values())
