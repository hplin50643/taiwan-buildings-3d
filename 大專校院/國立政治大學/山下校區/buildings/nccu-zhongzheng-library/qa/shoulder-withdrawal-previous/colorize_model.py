"""Color only: original export coordinates and 3930 triangles preserved. No textures."""
from pathlib import Path
import hashlib,json,numpy as np,trimesh
R=Path(__file__).resolve().parent;EXPECTED='c7ad8d7559310965da3dcf737fd335d2dba0387e2bd434b5c6d30761ea62b459'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED
m=trimesh.load(R/'model.stl',process=True,force='mesh');assert m.is_watertight and len(m.faces)==3930
pal=[('Approximate gray-beige opaque spandrels','#A79883'),('Approximate cream crown and visible courtyard walls','#DDDCD0'),('Approximate gray entry structural details','#8E918A'),('Approximate light gray existing corner screen frames','#C7C9BF'),('Opaque dark glazing and existing recess illustration','#465153'),('Aerial-observed gray roof surface approximation','#8C8E87'),('UNVERIFIED rear details and roof-block backs neutral','#A7ABA5'),('Authored display base, not site surfacing','#ABA8A0')]
# Invert original final z90 rotation for classification only. Output stays unchanged.
c=m.triangles_center[:,[1,0,2]].copy();c[:,1]*=-1
n=m.face_normals[:,[1,0,2]].copy();n[:,1]*=-1
poly=np.array([(-44,-67),(-25,-67),(-15,-54),(15,-54),(25,-67),(44,-67),(44,-42),(34,-28),(34,28),(44,42),(44,67),(25,67),(15,54),(-15,54),(-25,67),(-44,67),(-44,42),(-34,28),(-34,-28),(-44,-42)],float)
mat=np.full(len(c),6,dtype=np.int32)
for i,((x,y,z),(nx,ny,nz)) in enumerate(zip(c,n)):
 if z<=3.001:mat[i]=7;continue
 if x<.001:mat[i]=0
 # Both side middle bays have a source-supported facade family; classify their
 # entire coplanar surfaces, not centroid halves that create diagonal patches.
 if abs(abs(y)-54)<.005 and abs(x)<15.01:mat[i]=0
 # Existing top crown seen front/side and aerial. Reveal sidewalls stay light.
 if z>=39.999:mat[i]=1
 # Upper slot backs occur 2.1 mm inside the original perimeter; no invented grid.
 if 39.999<z<48.701:
  for a,b in zip(poly,np.roll(poly,-1,axis=0)):
   u=b-a;L=np.linalg.norm(u);u/=L;rel=np.array([x,y])-a;t=rel@u;dist=abs(u[0]*rel[1]-u[1]*rel[0])
   if 0<=t<=L and abs(dist-2.1)<.005 and abs(np.dot(n[i,:2],u))<.01:mat[i]=4;break
 # Front and partly visible flank horizontal window backs only (not whole bands).
 if x<=.001 and any(z0-.001<z<z0+5.001 for z0 in [8,20,32]):
  if abs(x+32)<.005 and abs(y)<27:mat[i]=4
  if abs(abs(y)-52)<.005 and abs(x)<14.01:mat[i]=4
 if any(z0-.001<z<z0+5.001 for z0 in [8,20,32]) and abs(abs(y)-52)<.005 and abs(x)<14.01:mat[i]=4
 # Front-side corner screen: light ribs, dark actual existing recess backs.
 if x<-42.69 and abs(y)>41.99 and z<39.999:mat[i]=3
 if abs(x+42.7)<.005 and any(abs(abs(y)-a)<2.201 for a in [46,52,58,64]) and any(a-.001<z<a+4.001 for a in [7,13,19,25,31]):mat[i]=4
 # Actual front entrance recess and original integral piers, no new upper columns.
 if abs(x+31)<.005 and abs(y)<25.01 and z<13.001:mat[i]=4
 if x<-31.99 and z<13.201 and any(abs(y-a)<=.751 for a in [-20,-10,0,10,20]):mat[i]=2
 if x<-35.99 and z<7.31:mat[i]=2
 # Unseen lower courtyard wall closure remains neutral on whole planes.
 if z<39.999 and ((abs(abs(x)-13.5)<.005 and abs(y)<20.01) or (abs(abs(y)-20)<.005 and abs(x)<13.51)):mat[i]=6
 # Visible upper courtyard walls / actual recesses. Deep unseen lower walls neutral.
 if z>=39.999 and abs(x)<15.1 and abs(y)<21.1:
  mat[i]=1
  if abs(abs(x)-15)<.005 and 41.999<z<48.001 and any(abs(y-a)<4.501 for a in [-14,0,14]):mat[i]=4
 # Large roof decks and existing roof-block lids genuinely visible in aerial.
 if nz>.999 and (abs(z-52)<.005 or abs(z-57.6)<.005):mat[i]=5
 # Courtyard parapet horizontal top light; roof-block unseen far/back walls neutral.
 if 51.399<z<53.001 and (abs(abs(x)-13.8)<.651 or abs(abs(y)-20.3)<.651):mat[i]=1
 if z>52.001 and z<57.599 and any(abs(x-a)<7.001 for a in [-25,25]) and any(abs(y-a)<7.501 for a in [-48,48]):
  mat[i]=1 if nx<-.1 or ny<-.1 else 6
# Whole-plane fallbacks where original long triangles cross real paint boundaries.
 # No subdivision or fabricated diagonal color edge. Preserve true recess backs.
 if abs(x+44)<.005 and abs(y)>41.99:mat[i]=3
 if abs(x-44)<.005 and abs(y)>41.99:mat[i]=6
 if abs(nx)>.1 and abs(ny)>.1 and abs(nz)<.005 and z>3.001 and mat[i]!=4:mat[i]=2 if x<0 else 6
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int(np.sum(mat==i))}for i,(a,b)in enumerate(pal)],'geometry_policy':'Original 3930 triangles unchanged, only materials.','coordinate_control':'Classification inverse of z90: pre_x=export_y, pre_y=-export_x; exported coordinates unchanged.','four_color_printing':'Eight appearance labels are not a tested four-filament slicer project.','limits':'Rear lower surfaces and unobserved roof-block backs neutral; broad roof gray supported by aerial. No source photo textures.'},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'bounds_mm':m.bounds.tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};assert len(np.unique(mat))==8;(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
