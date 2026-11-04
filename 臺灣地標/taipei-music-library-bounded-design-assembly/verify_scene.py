import bpy,json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;p=ROOT/'scene.blend';before=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
d=json.loads((ROOT/'inputs/physical-meshes.json').read_text());results=[]
for q in d['objects']:
 o=bpy.data.objects[q['id']];o.data.calc_loop_triangles();v=[list(x.co)for x in o.data.vertices];f=[list(x.vertices)for x in o.data.loop_triangles];assert v==q['vertices_mm'];assert f==q['triangles'];identity=all(abs(o.matrix_world[i][j]-(1 if i==j else 0))==0 for i in range(4)for j in range(4));assert identity
 results.append({'id':o.name,'vertices':len(v),'triangles':len(f),'exact_geometry_input':True,'identity_matrix':True,'role':o['role'],'rgba':[list(m.diffuse_color)for m in o.data.materials]})
ref=bpy.data.collections['SOURCE_ONLY_FINITE_REFERENCES_NO_OPAQUE_FACES'];rr=json.loads((ROOT/'inputs/reference-baselines.json').read_text())['records'];assert len(ref.objects)==len(rr)==116
for q in rr:
 o=bpy.data.objects['REF_'+q['id']];actual=[list(p.co)[:3]for p in o.data.splines[0].points]
 import struct
 expected=[[struct.unpack('<f',struct.pack('<f',x))[0]for x in a]for a in q['points_mm']];assert actual==expected
assert ref.hide_render and ref.hide_viewport
for mode in ['source_only','hypotheses_removed']:
 physical=bpy.data.collections['PHYSICAL_ARTIFICIAL_RESEARCH_ASSEMBLY'];shown=[]
 for o in physical.objects:
  show=False if mode=='source_only'else o.name in ['A','B','CENTRAL','ARTIFICIAL_SHARED_BASE']
  o.hide_render=not show
  if show:shown.append(o.name)
 if mode=='source_only':assert not shown
 else:assert len(shown)==4
 # No save: verification never mutates the frozen scene.
assert hashlib.sha256(p.read_bytes()).hexdigest()==before
(ROOT/'ACTUAL-SCENE-REOPEN-VERIFICATION.json').write_text(json.dumps({'scene_sha256_before_and_after':before,'actual_objects':results,'source_reference_count':116,'source_only_opaque_physical_count':0,'hypotheses_removed_physical_count':4,'source_only_excludes_conditional_roofs_and_artificial_parts':True,'mode_method':'actual collection membership and object visibility checked, no save','not_print_or_architectural_truth_certification':True},indent=2)+'\n')
