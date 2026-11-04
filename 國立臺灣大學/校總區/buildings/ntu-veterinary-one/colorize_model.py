"""2010 bounded original-face color; inseparable brick/gray wall fields neutral."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='ade92b267f98af2e978b84006326fe36940dde4ebe0a1e9fc977547877ab970b';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2890
pal=[('2010 observed gray bands frames and parapet','#858984'),('Existing original gray-green window backing','#61736F'),('True entrance aperture shadow','#414845'),('UNVERIFIED mixed brick-gray field and rear roof','#B8BAB6')];a=np.full(len(m.faces),3,np.int32)
for i,(t,n)in enumerate(zip(m.triangles,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.003 and hi[0]<=x1+.003 and lo[1]>=y0-.003 and hi[1]<=y1+.003 and lo[2]>=z0-.003 and hi[2]<=z1+.003
 def plane(j,v):return np.all(abs(t[:,j]-v)<.003)
 # Whole mixed brick/gray facade fields neutral. Only independently modeled bands gray.
 for z in [18,33,48,62]:
  if inside(-68,68,-20.05,-18.551,z,z+2):a[i]=0
 for x in [-13,13]:
  if inside(x-.65,x+.65,-20.7,-19.001,3,66):a[i]=0
 # Front existing stepped cap: solid gray family, never paint a false brick zigzag.
 if plane(1,-20) and inside(-24,24,-20.01,-19.99,63,71.5):a[i]=0
 # Original narrow front roof fascia, not horizontal rooftop.
 if plane(1,-20) and inside(-69,69,-20.01,-19.99,63,64.5):a[i]=0
 for x in [-56,-34,34,56]:
  for z in [7,22,37,52]:
   for xx in [x-3.7,x+3.7]:
    if plane(1,-17.75) and inside(xx-2.75,xx+2.75,-17.76,-17.74,z,z+8.5):a[i]=1
    if inside(xx-2.75,xx+2.75,-19.55,-17.85,z+4.05,z+4.95):a[i]=0
 for x in [-21,21]:
  for z in [7,22,37,52]:
   if plane(1,-17.75) and inside(x-2.5,x+2.5,-17.76,-17.74,z,z+8.5):a[i]=1
 for z in [17,32,47]:
  if plane(1,-17.75) and inside(-11,11,-17.76,-17.74,z,z+4.8):a[i]=1
  for x in [-7,0,7]:
   if inside(x-.45,x+.45,-19.55,-17.85,z,z+4.8):a[i]=0
 # Documented right original window bands, no green foliage masquerading as paint.
 for y in [-12,4,20]:
  for z in [7,22,37,52]:
   if plane(0,66.75) and inside(66.74,66.76,y-4,y+4,z,z+8.5):a[i]=1
   if inside(66.85,68.55,y-4,y+4,z+4.05,z+4.95):a[i]=0
 if inside(-13.5,13.5,-24.5,-19.001,13,14.6):a[i]=0
 if plane(1,-17.5) and inside(-9.5,9.5,-17.51,-17.49,3.5,13.5):a[i]=2
 if inside(-15,15,-30.85,-24.95,2.801,5.601) and (nz>.5 or ny<-.5):a[i]=0
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'geometry_policy':'2890 original triangles unchanged','limits':['2010 original source family not current precision.','Mixed brick/gray wall fields without distinct original boundaries neutral, no false brick zigzag.','Gray original bands and canopy, actual discrete window backing; vines not wall color.','Unknown left/rear/roof neutral.','Four labels not a verified four-filament slicer project.']},indent=2)+'\n');q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
