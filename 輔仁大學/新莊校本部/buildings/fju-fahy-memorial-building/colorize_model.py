"""Existing Fahy front color interpretation; geometry unchanged."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='e65d94ce49d6829333d26e0dcb9984fc473104e8e072333bee52482b45d5d932'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==4982
pal=[('Observed front gray wall family','#A2A59B'),('Central blue teal reflected glass approximation','#4D8C9D'),('Existing warm gray mullions','#B5B7A9'),('Small window dark recess','#4B5350'),('UNVERIFIED entrance roof sides and rear','#A9ADA6'),('Display support','#AAA79E')];mat=np.full(len(m.faces),4,dtype=np.int32)
tri=m.triangles.copy();tri[:,:,0]/=.88;c=m.triangles_center.copy();c[:,0]/=.88
for i,(t,(x,y,z),n)in enumerate(zip(tri,c,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 if hi[2]<=3.001:mat[i]=5;continue
 # Whole actual front planes: no centroids splitting a continuous wall into diagonal paint.
 if ny<-.99 and (abs(y+16)<.003 or abs(y+22.5)<.003 or abs(y+17.5)<.003):mat[i]=0
 # Source-matched upper front window domains, transformed x coordinates only for classification.
 if lo[0]>=-14.001 and hi[0]<=14.001 and lo[2]>=29.999 and hi[2]<=120.001 and lo[1]>=-24.901 and hi[1]<=-21.249:
  mat[i]=2
  if ny<-.99 and abs(y+21.25)<.003:mat[i]=1
 if ((lo[0]>=34.999 and hi[0]<=53.001)or(lo[0]>=-53.001 and hi[0]<=-34.999)) and lo[2]>=39.999 and hi[2]<=115.001 and lo[1]>=-18.801 and hi[1]<=-14.249:
  mat[i]=2
  if ny<-.99 and abs(y+14.25)<.003:mat[i]=3
 if lo[2]>=127.999 and hi[2]<=135.001 and lo[1]>=-17.501 and hi[1]<=-15.499:
  mat[i]=0
  if ny<-.99 and abs(y+15.5)<.003:mat[i]=3
 # Original blank name plaque, no gold text or additional geometry.
 if lo[0]>=-16.501 and hi[0]<=16.501 and lo[2]>=110.999 and hi[2]<=123.001 and hi[1]<=-21.999:mat[i]=0
 # Existing side-front ledges only, not roofhorizontal or obscured portico.
 if lo[2]>=37.999 and hi[2]<=112.001 and hi[1]<=-15.499 and lo[1]>=-20.501 and abs(x)>32.5:mat[i]=0 if nz>.9 else mat[i]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat);(R/'palette.json').write_text(json.dumps(pal,ensure_ascii=False,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int((mat==i).sum())}for i,(a,b)in enumerate(pal)],'geometry_policy':'4982 original triangles unchanged, original x*.88 transform preserved.','limits':['Photo-supported front color families, not precise dated paint.','Main flat wall color generalized coherently through foliage-hidden portions; entrance portico remains neutral.','Rear, sidewalls, horizontal roof tops and semicircular lower entrance unknown.','Six materials not verified four-filament slicing project.']},ensure_ascii=False,indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'watertight':bool(m.is_watertight),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
