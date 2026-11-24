from pathlib import Path
import numpy as np,trimesh,json,hashlib,collections
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='281e48a2d40fb7fec7e4eef243ca709fa89ab38a89eea04f2ed18e9094514277'
assert H(R/'model.stl')==expected
d=np.load(R/'mesh.npz');m=trimesh.Trimesh(d['vertices'],d['faces'],process=False);t=m.triangles;a=d['materials'].copy();old=a.copy();assert len(t)==16568
whole=np.max(abs(t[:,:,2]-(3.20+.70)*1000/350),axis=1)<1e-5
assert whole.sum()==102
fields=[]
for gi in range(4):
 for aa,bb in [(0,5.9),(10.5,16.4)]:
  low=(np.array([gi*22.63+aa-.115,4.45,3.20])+[-42.25,-4.55,.70])*1000/350
  high=(np.array([gi*22.63+bb+.115,9.615,3.20])+[-42.25,-4.55,.70])*1000/350
  low=low.astype('f4').astype(float);high=high.astype('f4').astype(float)
  finite=whole & np.all((t>=low-1e-5)&(t<=high+1e-5),axis=(1,2));fields.append(finite)
sel=np.logical_or.reduce(fields);assert sel.sum()==85 and np.all(old[sel]==1)
# Coplanar adjacency verifies each selected domain is complete. Original material seams are historical and not altered.
p=np.arange(len(t))
def root(i):
 while p[i]!=i:p[i]=p[p[i]];i=p[i]
 return i
for i,j in m.face_adjacency:
 if np.dot(m.face_normals[i],m.face_normals[j])>.999999:p[root(i)]=root(j)
g={}
for i in range(len(t)):g.setdefault(root(i),[]).append(i)
assert all(not sel[ids].any() or sel[ids].all() for ids in g.values())
assert len({root(i) for i in np.flatnonzero(sel)})==8
a[sel]=7;assert np.array_equal(a[~sel],old[~sel])
pal=[('illustrative plaster','#DDD6C5'),('illustrative concrete','#B5B5AC'),('illustrative roof finish','#7B817D'),('print-thickened metal frame','#9FAAAA'),('authored display support not terrain','#A3AA9B'),('opaque glazing illustration','#6D929B'),('illustrative timber door','#94765B'),('NUPS 1983 A1 nominal red square tile DESIGN only','#A45F4C')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
report={'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':{'selected_complete_terrace_faces':85,'whole_z_candidates':102,'excluded_column_tops':17,'selected_components':8,'per_rectangle':[int(x.sum())for x in fields],'coplanar_domains':len(g)},'partial_color_incomplete':True,'fully_colored_exterior':False,'design_color_only':True,'geometry_policy':'16568 original triangles and original ordering unchanged','limitations':['1983 A1 nominal red square tile DESIGN family,not water/asbuilt/current color.','A1 terrace says尺二紅方磚; A2 says尺三磁方磚; discrepancy retained,not red缸磚 platform text.','85 original mat1 terrace upper faces changed to appended mat7 only;16483 original seven illustrative assignments and RGB remain EXACT,not newly certified.','Original four paired groups/eightunits oneengineeringpackage/count0; no newtilejoints or geometry.','All original height contradictions,printthickening,derivedshortcanopies and untested manufacturing limitations retained.']}
(R/'appearance-materials.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':16568,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz'),'only_85_assignments_changed':True,'remaining_original_material_assignments_exact':True},indent=2));print(np.unique(a,return_counts=True),report['domains'])
