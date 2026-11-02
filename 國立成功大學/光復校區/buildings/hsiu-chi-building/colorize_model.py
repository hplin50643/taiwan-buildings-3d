"""Source-bounded color on unchanged original Hsiu Chi mesh; no new geometry."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent
EXPECTED_STL='af1c45a9f03d66cdcd5a5e7077ff996dbc81be95a551d277f4fa58954ab27833'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2104
pal=[('Observed brick color family','#9F5946'),('Observed gray frames and bands','#B0B2A7'),('Opaque opening shadow approximation','#414A48'),('Observed right sloped roof gray','#525957'),('Entry steps gray','#999D95'),('UNVERIFIED neutral surfaces','#A7ABA5'),('Display support only','#ABA8A0')]
mat=np.full(len(m.faces),5,dtype=np.int32)
for i,(t,c,n) in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 lo=t.min(0);hi=t.max(0);x,y,z=c;nx,ny,nz=n
 if hi[2]<=3.001:mat[i]=6;continue
 # Central convex facade only, not side or top. Existing surface curvature is unverified approximation.
 if lo[0]>=-26.002 and hi[0]<=10.002 and hi[1]<=-16.999 and lo[2]>=26.999:
  mat[i]=0
  if lo[2]>=49.999:mat[i]=1
  for zz in [31,40,49]:
   if lo[2]>=zz-.002 and hi[2]<=zz+1.502:mat[i]=1
  if abs(y+17)<.003 and ny<-.9:mat[i]=2
  if nz>.9 and hi[2]>=55.899:mat[i]=5
 # Right frontage only, existing flat faces and window reveals.
 if lo[0]>=10-.002 and hi[0]<=68.002 and lo[1]>=-11.102 and hi[1]<=-5.098 and lo[2]>3:
  mat[i]=0
  if (abs(y+10.1)<.003 or abs(y+5.1)<.003) and ny<-.9:mat[i]=2
  elif abs(ny)<.9:mat[i]=1
 # Right roof's existing front slope, not unknown back slope or tower roof.
 if lo[0]>=10-.002 and lo[2]>=40.999 and hi[2]<=45.001 and hi[1]<=9.001 and .1<nz<.99:mat[i]=3
 # Entrance: existing front frame and recessed dark back. Whole unseparated planes gray.
 if lo[0]>=-23.502 and hi[0]<=7.502 and hi[1]<=-27.999 and lo[2]>=9.999 and hi[2]<=27.001:
  mat[i]=1
  if abs(y+30.6)<.003 and ny<-.9:mat[i]=2

 # Coherent whole original facade planes avoid artificial diagonal paint boundaries.
 if ny<-.99 and (abs(y+11)<.003 or abs(y+6)<.003) and x>10 and z>3:mat[i]=0
 if ny<-.99 and abs(y+32)<.003 and -24<x<8:mat[i]=1
 if abs(z-27)<.003 and nz>.9 and -24<x<8 and y<-18:mat[i]=1
 # Side-window reveals and outside wall remain unverified, including their small corner faces.
 if x>67 and not(abs(y+11)<.003 and ny<-.99):mat[i]=5
 # Far-right high block cannot be uniquely matched in official front photograph.
 if lo[0]>=39.999 and z>3:mat[i]=5
 if hi[1]<-27.9 and lo[2]>=2.999 and hi[2]<=10.201:mat[i]=4
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'palette.json').write_text(json.dumps(pal,ensure_ascii=False,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int((mat==i).sum())}for i,(a,b)in enumerate(pal)],'geometry_policy':'2104 original triangles unchanged; no subdivision.','scope':'Observed central entrance and right frontage color-family interpretation only; left broad arch and rear neutral.','limitations':['Original convex curvature is not revalidated by these photographs.','Paint boundaries coarsened to existing faces; no restoration color precision.','Seven material labels not a verified four-filament slicing project.']},ensure_ascii=False,indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'watertight':bool(m.is_watertight),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
