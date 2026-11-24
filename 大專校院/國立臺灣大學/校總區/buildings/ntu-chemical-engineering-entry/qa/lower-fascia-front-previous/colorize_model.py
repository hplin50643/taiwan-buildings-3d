"""Original 4262 faces; source-bounded partial color, no invented spandrels."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='65cfa3d66df2bc9e0243229ab612e9623ff7681207b4a638d904a40f1efdde2f';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==4262
pal=[('Observed curved hoods sills and portico mineral gray','#A5A8A1'),('Discrete original glazing and aperture shadow','#4D5956'),('Observed narrow gray framing','#858E88'),('UNVERIFIED mixed brick-spandrel wall and rear roof','#B6B8B2')];a=np.full(len(m.faces),3,np.int32)
for i,(t,n)in enumerate(zip(m.triangles,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.003 and hi[0]<=x1+.003 and lo[1]>=y0-.003 and hi[1]<=y1+.003 and lo[2]>=z0-.003 and hi[2]<=z1+.003
 def plane(j,v):return np.all(abs(t[:,j]-v)<.003)
 for x in [-64,-53,-42,-31,-20,-9,2,13,24,35,64]:
  for z in [6,25]:
   # Solid hood protrusion only, no wall plane extension.
   if inside(x-4,x+4,-14,-11.001,z+13,z+15.4):a[i]=0
   if plane(1,-9.5) and inside(x-2.85,x+2.85,-9.51,-9.49,z,z+13):a[i]=1
   if inside(x-2.65,x+2.65,-11.5,-9.5,z+8,z+9):a[i]=2
  for z in [5,24]:
   if inside(x-3.65,x+3.65,-12.2,-11.001,z,z+1):a[i]=0
 for x in [-69.5,-58.5,-47.5,-36.5,-25.5,-14.5,-3.5,7.5,18.5,29.5,40.5,69.5]:
  if inside(x-.6,x+.6,-12.3,-11.001,3,44):a[i]=2
 # Three-arch front beam and piers are fully gray concrete, not the connected brick wall.
 if inside(-10,36,-37.55,-34.45,3,26.5):a[i]=0
 # Portal canopy vertical sides and underside gray, unseen top/rear neutral.
 if inside(-9,35,-37,-9,24,26.5) and nz<.5 and not plane(1,-9):a[i]=0
 if plane(1,-9) and inside(-5.5,31.5,-9.01,-8.99,3,22):a[i]=1
 for x in [2,13,24]:
  if inside(x-.6,x+.6,-11.95,-9.65,3,22):a[i]=2
 # Explicit original entrance stairs, no adjoining base recoloring.
 if inside(-7.5,33.5,-38.9,-31.1,3,6.25):a[i]=0
 for x in [-61,-43,-25,-7,11,29,47,65]:
  if plane(1,-9.65) and inside(x-6.5,x+6.5,-9.66,-9.64,46,48.4):a[i]=1
 # Semantic connected facade plane is mixed brick/gray real spandrels and has no mesh split.
 if plane(1,-11):a[i]=3
 if plane(2,26.5) and inside(-10,36,-37.55,-9,26.49,26.51):a[i]=3
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'geometry_policy':'4262 original triangles unchanged','partial_color_incomplete':True,'fully_colored_exterior':False,'limits':['Source page published 2026-09-29, photo capture date unknown.','Whole connected main facade neutral: unmodeled gray spandrels cannot be painted onto brick triangles.','Separate original hoods sills piers portico and discrete windows only.','Unknown end/rear/roof neutral.','Four labels not a verified four-filament slicer project.']},indent=2)+'\n');q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q);print(np.unique(a,return_counts=True))
