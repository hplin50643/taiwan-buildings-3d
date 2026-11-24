"""Original 1092 triangles; coherent source-bounded faces, not subdivided."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='5bc3c76a42c666bd6360ab1af6abe5a70795dc6eab512843b66e2e7a4587d85f'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1092
pal=[('Photo-bounded brick return','#AE7F6C'),('Concrete portico stair and circular aperture','#A8ADA6'),('Observed lower wing light wall','#D0D3CB'),('Existing discrete window shade','#475B56'),('Coarse existing balcony and recess metal family','#9FAFA7'),('Grass reference only original slope upper face','#758656'),('UNVERIFIED or topology-crossing full plane neutral','#A7ABA5')]
mat=np.full(len(m.faces),6,dtype=np.int32)
for i,(t,(x,y,z),n)in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 if hi[2]<=3.001:continue
 # Entire main front is neutral: its large original faces cross upper brick/lower gray.
 if abs(x+17)<.003 and nx<-.99 and lo[2]>=26.499 and lo[1]>=-27.001 and hi[1]<=-22.499:mat[i]=0
 # Existing lower-wing photographed faces only, no roof/rear extrapolation.
 if abs(x+55.5)<.003 and nx<-.99:mat[i]=2
 if abs(y+14.5)<.003 and ny<-.99 and hi[0]<=-16.499:mat[i]=2
 # Existing entrance portico components, all gray concrete; do not borrow bridge.
 if lo[0]>=-63.501 and hi[0]<=19.501 and lo[1]>=-43.501 and hi[1]<=-20.499 and lo[2]>=23.999 and hi[2]<=26.501:mat[i]=1
 if lo[0]>=-63.001 and hi[0]<=-58.999 and lo[1]>=-43.501 and hi[1]<=-20.499 and hi[2]<=26.001:mat[i]=1
 if lo[0]>=-24.001 and hi[0]<=-19.999 and lo[1]>=-25.501 and hi[1]<=-20.499 and hi[2]<=26.001:mat[i]=1
 if lo[0]>=-62.001 and hi[0]<=20.001 and lo[1]>=-49.851 and hi[1]<=-41.149 and hi[2]<=7.001:mat[i]=1
 # Existing gray balcony lips and parapets (coarse originals, no fine railings added).
 for zz in [26,37,48,59]:
  if lo[0]>=-21.001 and hi[0]<=-14.999 and lo[1]>=-22.501 and hi[1]<=40.501 and lo[2]>=zz-.001 and hi[2]<=zz+4.201:mat[i]=4
 # Main front existing recessed window backs/returns; no new front material boundary.
 if lo[1]>=-27.001 and hi[1]<=-26.099 and abs(ny)<.99:mat[i]=4
 if abs(y+26.1)<.003 and ny<-.99:mat[i]=3
 # Lower wing existing cut backs, returns bounded to original wall thickness.
 if abs(x+54.7)<.003 and nx<-.99:mat[i]=3
 if lo[0]>=-55.501 and hi[0]<=-54.699 and abs(nx)<.99:mat[i]=2
 # Roof greenery only sloping top of the original wedge, not any vertical wall.
 if lo[0]>=-60.501 and hi[0]<=-11.499 and lo[1]>=38.999 and hi[1]<=59.001 and lo[2]>=2.899 and hi[2]<=15.901 and .5<nz<.999:mat[i]=5
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int((mat==i).sum())}for i,(a,b)in enumerate(pal)],'geometry_policy':'1092 original triangles unchanged.','limits':['Main front full plane neutral because original triangles cross upper brick/lower frame boundary.','No added bridge/railings/sunshade blades.','Green only sloped top; unknown far side/back/flat roofs neutral.','Seven labels are not a tested multi-filament project.']},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
