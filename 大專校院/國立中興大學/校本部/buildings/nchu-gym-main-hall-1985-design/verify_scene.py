from pathlib import Path
import bpy,numpy as np,json,hashlib
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'))
d=np.load(R/'mesh.npz');o=bpy.data.objects.get('NCHU main gym March1985 revised historical design')
assert o is not None
v=np.array([x.co[:] for x in o.data.vertices]);f=np.array([x.vertices[:] for x in o.data.polygons]);sha=hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()
checks={'mesh_vertices_match':bool(np.allclose(v,d['vertices'],atol=1e-5)),'mesh_faces_exact':bool(np.array_equal(f,d['faces'])),'mesh_sha_property_matches':o.get('source_mesh_sha256')==sha,'scale_property':o.get('scale')=='1:300','camera_exists':bpy.context.scene.camera is not None,'triangulated':all(len(p.vertices)==3 for p in o.data.polygons)}
checks['material_indices_match']=bool(np.array_equal(np.array([p.material_index for p in o.data.polygons]),d['materials']))
q={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'mesh_sha256':sha};(R/'SCENE-QA.json').write_text(json.dumps(q,indent=2));print(q);assert all(checks.values())
