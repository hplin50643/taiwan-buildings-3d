"""Bounded same-tower material-family interpretation; exact original triangles."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='9a0984725f7df81d431ebfd23e6039831075bbb4f18799338f910d4c7a8aadb8'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',process=True,force='mesh');assert len(m.faces)==12444
pal=[('Same-tower continuous teal family interpretation','#4B8B85'),('Existing raised facade metal bands','#9AAFA6'),('Existing coin ornaments and spire silver gray','#BAC4B8'),('Original coin-center recess generic shade','#4B615C'),('UNVERIFIED podium barrel roof horizontal surfaces','#A7ABA5')]
a=np.full(len(m.faces),4,np.int32)
for i,(t,c,n) in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 lo=t.min(0);hi=t.max(0);x,y,z=c;dx=t[:,0]-8;dy=t[:,1]+8;nz=n[2]
 # Entire tower domains above obscured podium; below use exact taper surface planes only.
 if lo[2]>=14.399 and hi[2]<=140.001:a[i]=0
 if lo[2]>=2.799 and hi[2]<=36.801:
  w=25.2+(19-25.2)*(t[:,2]-2.7)/(36.8-2.7)
  onside=any(np.max(np.abs(s*v-w/2))<.003 for v in [dx,dy]for s in [-1,1])
  oncorner=any(np.max(np.abs(sx*dx+sy*dy-.9*w))<.003 for sx in [-1,1]for sy in [-1,1])
  if onside or oncorner:a[i]=0
 # Main existing horizontal relief rings, no added floor lines.
 for zz in np.arange(8,36,2.0):
  if lo[2]>=zz-.001 and hi[2]<=zz+.351 and np.max(np.abs(dx))<14 and np.max(np.abs(dy))<14:a[i]=1
 for j in range(8):
  zz=37.3+j*10.75
  if lo[2]>=zz+9.699 and hi[2]<=zz+10.751:a[i]=1
  for k in range(1,8):
   b=zz+k*1.24
   if lo[2]>=b-.001 and hi[2]<=b+.301:a[i]=1
  # Full vertices must belong to one existing sloping corner-pier volume.
  if lo[2]>=zz-.001 and hi[2]<=zz+9.601:
   p=7.85+(9.18-7.85)*(t[:,2]-zz)/9.6
   for sx in [-1,1]:
    for sy in [-1,1]:
     if np.all(np.abs(dx-sx*p)<=.551) and np.all(np.abs(dy-sy*p)<=.551):a[i]=1
  # Stylized ruyi caps already present: only complete small outward cap faces.
  if lo[2]>=zz+9.099 and hi[2]<=zz+10.401:
   for v,u in [(dx,dy),(dy,dx)]:
    if np.max(np.abs(u))<=1.501 and np.min(np.abs(v))>=9.599:a[i]=1
 # Coin components by cylindrical footprint and outward location, not arbitrary z stripe.
 if lo[2]>=34.099 and hi[2]<=39.501:
  for v,u in [(dx,dy),(dy,dx)]:
   if np.all(u*u+(t[:,2]-36.8)**2<=2.701**2) and np.min(np.abs(v))>=9.099 and np.max(np.abs(v))<=10.501:
    a[i]=2
    if np.max(np.abs(u))<=.751 and lo[2]>=36.049 and hi[2]<=37.551:a[i]=3
 # Original crown belts and spire, not night illumination.
 for zz in np.arange(127,135.5,1.25):
  if lo[2]>=zz-.001 and hi[2]<=zz+.351:a[i]=1
 if lo[2]>=135.599 and hi[2]<=136.301:a[i]=1
 if lo[2]>=139.699:a[i]=2
 # Unobserved truly horizontal crown shelves remain neutral; vertical spire tip is tiny original solid.
 if nz>.999 and hi[2]<139.699:a[i]=4
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'geometry_policy':'12444 original triangles and vertices unchanged','limits':['Four-direction same-tower continuous material-family interpretation, not separately photographed directions.','Podium/barrel roofs and unverified horizontal shelves neutral.','No night illumination colors, added floor lines or textures.','Five material labels not a verified multi-filament print.']},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
