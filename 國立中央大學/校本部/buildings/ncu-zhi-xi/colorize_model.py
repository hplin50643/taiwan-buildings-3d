"""Bounded front-only color interpretation, existing 2013 approximate mesh unchanged."""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
R=Path(__file__).resolve().parent;EXPECTED_STL='0fa6acf0e73b9e82a5d754c464a55a8382046211707b552052ce9eb219569330'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2524 and m.is_watertight
pal=[('Photographed front tower gray, approximate','#979B97'),('Photographed front wing warm gray beige, disputed hue disclosed','#B1A995'),('Existing front mullions pale gray','#D0D2CA'),('Opaque dark window and entrance recess','#414D4B'),('Approximate entry step gray','#A3A59F'),('UNVERIFIED upper tower, cylinders, sides, rear, roof and support','#A7ABA5')]
mat=np.full(len(m.faces),5,dtype=np.int32);tri=m.triangles.copy();tri[:,:,2]/=.76;c=m.triangles_center.copy();c[:,2]/=.76
for i,(t,(x,y,z),n)in enumerate(zip(tri,c,m.face_normals)):
 lo=t.min(axis=0);hi=t.max(axis=0);nx,ny,nz=n
 if hi[2]<=3.001:continue
 # Only whole existing triangles entirely inside the source-supported front domains.
 central=lo[0]>=-23.501 and hi[0]<=23.501 and lo[1]>=-31.601 and hi[1]<=-28.399 and hi[2]<=109.001
 wing=((lo[0]>=23.499 and hi[0]<=62.501)or(lo[0]>=-62.501 and hi[0]<=-23.499))and lo[1]>=-18.001 and hi[1]<=-16.499 and hi[2]<=106.001
 if central:
  mat[i]=0
  # True recessed back faces; no painted grid or new panes.
  if abs(y+28.5)<.003 and ny<-.9:mat[i]=3
  # Five existing sets of relief mullions, original exact domains.
  for zz in [42,57,71,85,99]:
   if lo[2]>=zz-.002 and hi[2]<=zz+10.002 and any(lo[0]>=xx-.602 and hi[0]<=xx+.602 for xx in [-17,-6,6,17]):mat[i]=2
 if wing:
  mat[i]=1
  if abs(y+16.5)<.003 and ny<-.9:mat[i]=3
 # Whole wing front plane kept neutral because original large triangles cross the evidence ceiling.
 if abs(y+18)<.003 and ny<-.9 and abs(x)>23.49:mat[i]=5
 if hi[1]<-34 and lo[2]>=2.799 and hi[2]<=5.101:mat[i]=4
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'palette.json').write_text(json.dumps(pal,ensure_ascii=False,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int(np.count_nonzero(mat==i))}for i,(a,b)in enumerate(pal)],'geometry_policy':'2524 original triangles unchanged, no added or subdivided faces.','source_scope':'Original 2013 approximate geometry plus later obtained official photograph of unstated shooting date. Not one-year reconstruction.','bounds':'Original code z109 central / z106 wings, exported by z*.76; entire crossing triangles remain neutral.','limits':['Official text brick-red differs from low-saturation photograph gray-beige; no claim this resolves period or color balance.','Tower top/loggias/cylindrical cores/sides/rear/roof neutral.','Six material labels not a tested four-filament slicing project.']},ensure_ascii=False,indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'watertight':bool(m.is_watertight),'bounds_mm':m.bounds.tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};assert len(np.unique(mat))==6;(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
