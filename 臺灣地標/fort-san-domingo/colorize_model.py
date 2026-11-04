"""Bounded photographed main-fort faces only; no new geometry or texture."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='eb970466363f9c20b0dfec609f0e6ab94f619059c0d79869a1f69fd56183d524'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3904
pal=[('Photographed front and left red plaster','#B55F49'),('Observed front terrace and near turret warm masonry','#B78354'),('Observed existing stone coping and base','#B4B3A4'),('Shaded lean-to roof and original recess backs','#4C514B'),('UNVERIFIED rear opposite turret roof terrace','#A7ABA5')]
a=np.full(len(m.faces),4,np.int32)
for i,(t,c,n)in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 x,y,z=c;lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.003 and hi[0]<=x1+.003 and lo[1]>=y0-.003 and hi[1]<=y1+.003 and lo[2]>=z0-.003 and hi[2]<=z1+.003
 def plane(axis,v):return np.all(np.abs(t[:,axis]-v)<.003)
 if hi[2]<=3.001:continue
 if (plane(1,-36)and ny<-.99)or(plane(0,-46)and nx<-.99):a[i]=0
 # Complete front apron/parapet/post regions: masonry distinct from smooth main fort.
 if inside(-47.7,47.7,-62.3,-35,3,42.4):a[i]=1
 # Original masonry base strips in observed front/left only.
 if inside(-47,47,-37,57,3.1,5.1) and (ny<-.99 or nx<-.99):a[i]=2
 # Pale existing front and side parapet caps only, not whole posts.
 for xx in [-42,-28,-14,0,14,28,42]:
  if inside(xx-3.55,xx+3.55,-62.2,-57,41.35,42.35):a[i]=2
 for sx in [-1,1]:
  for yy in [-51,-39]:
   if inside(sx*45-2.65,sx*45+2.65,yy-3.4,yy+3.4,41.1,42.1):a[i]=2
 # Main upper front/left coping blocks, unseen rear/right remain neutral.
 if lo[2]>=63.974 and hi[2]<=65.126 and ((lo[1]>=-36.951 and hi[1]<=-33.049)or(lo[0]>=-46.951 and hi[0]<=-43.049)):a[i]=2
 # Southwest photographed projecting brick turret and corbel; opposite turret unknown.
 if inside(-55.3,-31,-45.3,-21,45,73.101):a[i]=1
 if inside(-55.3,-36.7,-45.3,-26.7,72.849,76.001):a[i]=2
 # Existing front lean-to roof, source shade only, not consulate tile.
 if inside(-22,22,-50,-34.6,45.599,51.001) and abs(nz)>.1:a[i]=3
 # Visible sparse left-wall opening backs only; do not mirror right side.
 for yy,zz,w,h in [(-10,24,8,11),(26,23,7,10),(5,43,6,8)]:
  if inside(-46.001,-44.899,yy-w/2,yy+w/2,zz-h/2,zz+h/2):a[i]=3 if nx<-.99 else 0
 # Original terrace arch recesses and porch discrete aperture backs.
 for xx in [-32,-16,0,16,32]:
  if inside(xx-3.75,xx+3.75,-61.501,-58.899,7,27) and ny<-.99 and y>-59.99:a[i]=3
 for xx in [-11,0,11]:
  if inside(xx-3.4,xx+3.4,-49.6,-46.8,36.05,45.55) and ny<-.99:a[i]=3
 # Turret slit backs. No flags, people, signs, interior or neighbouring consulate.
 if inside(-54.75,-52.999,-37.2,-34.8,65.75,70.25)or inside(-47.2,-44.8,-44.75,-42.999,65.75,70.25):a[i]=3
 # Main roof floor and unseen rear/other side explicitly neutral; narrow horizontal caps remain source-limited above.
 if plane(2,62.2):a[i]=4
# Fused side planes cross plaster/terrace masonry. Entire coherent planes neutral, not triangle wedges.
for i,t in enumerate(m.triangles):
 if np.all(np.abs(t[:,0]-46)<.003) or np.all(np.abs(t[:,0]+46)<.003):a[i]=4
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'geometry_policy':'3904 original vertices and triangles unchanged','limits':['Only main fort, not separate consulate.','Front plaster distinct from front terrace and near turret masonry. Both fused main side planes neutral: existing triangles cross incompatible material domains.','Opposite turret and unseen rear/right/roof terrace neutral.','Five labels not verified multi-filament print.']},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
