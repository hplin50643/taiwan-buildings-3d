"""Appearance-only mapping to original 3894 faces; no new geometry or textures."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED='d51b147e4cc926c06637b684d2057a83952d32f732abd28a26e98059f8649ef6'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED
m=trimesh.load(R/'model.stl',process=True,force='mesh');assert len(m.faces)==3894 and m.is_watertight
pal=[('Approximate verified courtyard brick','#A66553'),('Approximate gray balconies and bay panels','#A3A59C'),('Existing recess shade NOT all glazing','#46524F'),('UNVERIFIED other facades roof and base neutral','#A7ABA5')]
t=m.triangles;c=m.triangles_center;mat=np.full(len(c),3,np.int32)
for i,(x,y,z) in enumerate(c):
 if z<=3.001:continue
 # Only the uniquely matched courtyard-entry wing; other outer/north facades unverified.
 if -33.601<=x<=-32.499 and -29.001<=y<=37.001 and z<59.899:mat[i]=0
 if t[i,:,0].min()>=-33.001 and t[i,:,0].max()<=-28.999 and t[i,:,1].min()>=-9.001 and t[i,:,1].max()<=11.001 and z<56.901:mat[i]=0
 # Existing recess backs: generic deep shade rather than fabricated windows/door leafs.
 if abs(x+33.6)<.002 and any(abs(y-a)<3.501 for a in [-21,-10,12,23]) and any(a-.001<z<a+5.501 for a in [7,16,25,34,43,52]):mat[i]=2
 if abs(x+30.2)<.002 and abs(y-1)<6.501 and (5.999<z<14.001 or any(a-.001<z<a+4.801 for a in [32,41,50])):mat[i]=2
 # Round shallow motif above entry remains shade/neutral, never declared glass.
 if t[i,:,0].min()>=-29.701 and t[i,:,0].max()<=-28.999 and np.all(abs(t[i,:,1]-1)<=2.401) and np.all(abs(t[i,:,2]-22)<=2.401):mat[i]=2
 # Original curved balconies plus their existing slab/block, all-vertex domain.
 if t[i,:,0].max()>-32.499 and t[i,:,0].min()>=-34.501 and np.all(abs(t[i,:,1]-1)<=9.001) and any(t[i,:,2].min()>=a-.001 and t[i,:,2].max()<=a+4.501 for a in [27,36,45]):mat[i]=1
 # Gray spandrels only actual bay-wise protrusions, not a belt across brick piers.
 if t[i,:,0].min()>=-33.101 and t[i,:,0].max()<=-31.699 and any(np.all(abs(t[i,:,1]-a)<=4.301) for a in [-21,-10,12,23]) and any(t[i,:,2].min()>=a-.001 and t[i,:,2].max()<=a+2.301 for a in [14,23,32,41,50]):mat[i]=1
 # Existing entry steps; not coloring large shared wall triangles.
 if t[i,:,0].min()>=-26.501 and t[i,:,0].max()<=-18.699 and t[i,:,2].max()<=6.601 and np.all(abs(t[i,:,1]-1)<=12.501):mat[i]=1
 if z>=59.899:mat[i]=3
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');assert len(np.unique(mat))==4
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int(np.sum(mat==i))}for i,(a,b)in enumerate(pal)],'geometry_policy':'3894 original triangles unchanged.','limits':'Only uniquely matched courtyard-entry face colored; unverified exterior/north/roof neutral. Gray bay panels do not span brick piers. Round motif is not glazing.','printing':'Four appearance labels are not a validated four-filament slicer project.'},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'bounds_mm':m.bounds.tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
