"""2010 limited source color, original topology preserved. Cross-plinth planes neutral."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='34622c157322ad7bb3ab6ae6d1f5c51672b7466aaafe259bc1ee17f1bbaf7c78';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==6318
pal=[('2010 observed brick family on bounded upper details and returns','#A17C6F'),('Observed gray original window bands and caps','#727B7A'),('Actual recessed window glass backing','#596E70'),('Actual original entrance shadow','#3F4747'),('UNVERIFIED or inseparable plinth-crossing whole plane','#B8BAB6')];a=np.full(len(m.faces),4,np.int32)
for i,(t,n)in enumerate(zip(m.triangles,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.003 and hi[0]<=x1+.003 and lo[1]>=y0-.003 and hi[1]<=y1+.003 and lo[2]>=z0-.003 and hi[2]<=z1+.003
 def plane(j,v):return np.all(np.abs(t[:,j]-v)<.003)
 # Large front/end wall and full-height projecting pilasters deliberately neutral:
 # no original horizontal boundary separates photographed gray plinth and brick.
 # Upper parapet bodies only, no unseen horizontal roof.
 if inside(-68,68,-21.75,-19.05,64,69) and ny<-.5:a[i]=0
 # Window original reveal returns, backing and existing band relief.
 for x in [-58,-40,-22,22,40,58]:
  for xx in [x-3,x+3]:
   for z in [8,21,34,47]:
    if inside(xx-2.251,xx+2.251,-19.501,-18.199,z,z+(12 if z==47 else 9)) and (abs(nx)>.5 or nz<-.5):a[i]=0
    if plane(1,-18.2) and inside(xx-2.25,xx+2.25,-18.21,-18.19,z,z+(12 if z==47 else 9)):a[i]=2
    if inside(xx-2.45,xx+2.45,-20.05,-18.35,z+4.55,z+5.45):a[i]=1
 # Documented left-end original apertures; no entire end wall recolor.
 for y in [-11,3,17,27]:
  for z in [8,21,34,47]:
   if plane(0,-67) and inside(-67.01,-66.99,y-3,y+3,z,z+(12 if z==47 else 9)):a[i]=2
   if inside(-69.1,-67.1,y-3.25,y+3.25,z+4.55,z+5.45):a[i]=1
 # Central real recessed glazing and original mullions; not entire front blue.
 if plane(1,-17.8) and inside(-10.5,10.5,-17.81,-17.79,19,60):a[i]=2
 for z in [19,29,39,49,59]:
  if inside(-11,11,-20.7,-18.1,z,z+1.8):a[i]=1
 for x in [-8,-4,0,4,8]:
  if inside(x-.45,x+.45,-19.15,-17.25,19,60):a[i]=1
 # High central cap recess, actual cut only.
 if plane(1,-18.5) and inside(-7.5,7.5,-18.51,-18.49,60.5,64.2):a[i]=1
 # Existing upper curved porch cap front can match brick; broad portal face stays neutral.
 if inside(-12.5,12.5,-30.01,-29.99,17,22) and ny<-.99:a[i]=0
 if plane(1,-28.35) and inside(-14.5,14.5,-28.36,-28.34,3.5,14.5):a[i]=3
 # Original small stairs, not broad plinth/sidewalk.
 if inside(-18,18,-35.85,-29.95,2.801,5.601) and (nz>.5 or ny<-.5):a[i]=1
 # Narrow known front cap fascia, no top/side/back extension.
 if plane(1,-20.5) and inside(-69.5,69.5,-20.51,-20.49,64,65.3):a[i]=1
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'geometry_policy':'6318 original triangles unchanged','limits':['2010 photographs, not current precise colors.','Front and left full wall planes and full-height pilasters crossing gray plinth remain neutral.','Original central triangular gable not repaired to photographed shallow arch.','Unknown back/right/roof neutral; no air conditioners or gold labels added.','Five appearance labels are not a verified four-filament slicer project.']},indent=2)+'\n');q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
