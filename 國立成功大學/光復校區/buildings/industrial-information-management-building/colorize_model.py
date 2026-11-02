"""Bounded color on unchanged A039 mesh. No A040/A038 geometry or color borrowed."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='544fcdd5c632d9058aa83e403a96faac386ca3aa6ab4db77e5b4e5fd8184cf3f'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1394
pal=[('Observed entry long-wall brick family','#B5765B'),('Light recess returns stair and portal soffit','#BCBCB1'),('Existing recess shade not asserted all glass','#45534F'),('UNVERIFIED short end side rear roof and portal edges','#A7ABA5')];mat=np.full(len(m.faces),3,dtype=np.int32)
for i,(t,(x,y,z),n)in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 if hi[2]<=3.001:continue
 if abs(y-13)<.003 and ny<-.99:mat[i]=0
 for xx in [-58,-45,-32,-19,-6,7,20,33]:
  for zz in [34,43,52]:
   if lo[0]>=xx-4.251 and hi[0]<=xx+4.251 and lo[1]>=12.999 and hi[1]<=14.201 and lo[2]>=zz-.001 and hi[2]<=zz+5.801:
    mat[i]=2 if abs(y-14.2)<.003 and ny<-.99 else 1
 for xx in [-53,-31,-9,13]:
  if lo[0]>=xx-7.501 and hi[0]<=xx+7.501 and lo[1]>=12.999 and hi[1]<=15.801 and lo[2]>=4.999 and hi[2]<=26.001:
   mat[i]=2 if abs(y-15.8)<.003 and ny<-.99 else 0
 # Two source-confirmed brick posts; broad slab is not automatically the lower gray canopy.
 for xx in [7,35]:
  if lo[0]>=xx-1.751 and hi[0]<=xx+1.751 and lo[1]>=.999 and hi[1]<=11.001 and hi[2]<=30.901:mat[i]=0
 # Neutral whole slab edges/top; pale underside supported by both source overhangs.
 if lo[0]>=5.499 and hi[0]<=36.501 and lo[1]>=-1.501 and hi[1]<=13.501 and lo[2]>=27.999 and hi[2]<=31.001:
  mat[i]=1 if nz<-.99 and abs(z-28)<.003 else 3
 if lo[0]>=-8.001 and hi[0]<=7.701 and lo[1]>=-7.001 and hi[1]<=8.001 and hi[2]<=16.101:mat[i]=1
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int((mat==i).sum())}for i,(a,b)in enumerate(pal)],'geometry_policy':'1394 original triangles unchanged.','limits':['Only photographed entrance long face receives brick/gray/shadow interpretation.','Original tall portal may map high overhang, not low gray canopy; only soffit pale, edges/top neutral.','Short end/external side/rear/roof neutral; no A040/A038 borrowing.','Four labels are not a tested four-filament slicer project.']},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
