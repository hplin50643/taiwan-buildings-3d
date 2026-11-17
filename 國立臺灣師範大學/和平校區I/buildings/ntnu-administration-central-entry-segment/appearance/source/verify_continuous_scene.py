import bpy,json,struct,numpy as np
from pathlib import Path
A=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(A/'scene.blend'))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(meshes)==1
m=meshes[0].data;b=(A.parent/'model.stl').read_bytes();t=np.array([struct.unpack_from('<9f',b,96+50*i) for i in range(5292)]).reshape(-1,3,3);v=np.array([list(v.co) for v in m.vertices]);f=np.array([list(p.vertices) for p in m.polygons]);assert np.array_equal(t,v[f]);c=[p.material_index for p in m.polygons];assert c==json.loads((A/'face-materials.json').read_text())['face_material_indices'];assert len(m.materials)==6
(A/'qa/continuous-crest-scene.json').write_text(json.dumps({'passed':True,'blender':bpy.app.version_string,'single_mesh':True,'exact_source_triangle_coordinates_order':True,'material_indices_match_3mf':True,'material_slots':6},indent=2)+'\n')
print('CONTINUOUS SCENE QA PASS')
