"""Bounded 2013 photo color families assigned only to original complete triangles."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='9c00fda00143f65020271ba536c72e333fd8161b98985343129f76a47f66b6d2';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1988
pal=[('2013 visible cream brick family','#C3B58D'),('Existing restrained brown-gray window members','#706860'),('Actual opening backing shadow','#4C514B'),('Visible narrow reddish brown coping','#705449'),('Documented canopy and exposed stair concrete','#999B94'),('UNVERIFIED mixed plinth wall rear roof neutral','#B8BAB6')];a=np.full(len(m.faces),5,np.int32)
for i,(t,n)in enumerate(zip(m.triangles,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.003 and hi[0]<=x1+.003 and lo[1]>=y0-.003 and hi[1]<=y1+.003 and lo[2]>=z0-.003 and hi[2]<=z1+.003
 def plane(j,v):return np.all(abs(t[:,j]-v)<.003)
 # Entire front/right masonry triangles above the hidden plinth; no synthetic arch rings.
 if plane(1,-15) and inside(-18.5,2.5,-15.01,-14.99,73,86.5):a[i]=0
 # Whole main front/right and left wing masonry planes neutral: continuity crosses plinth.
 # Plane fragments reaching original base are deliberately neutral; do not use centroids.
 # Original front-visible separate roof fascia, horizontal roof/terrace surfaces stay neutral.
 for x,w,z,h,y in [(20,83,73,1.4,-16.5),(-42,47,45,1.4,-16.5),(-8,23,86.5,1.3,-16)]:
  if plane(1,y) and inside(x-w/2,x+w/2,y-.01,y+.01,z,z+h):a[i]=3
 if plane(0,61.5) and inside(61.49,61.51,-16.5,32.5,73,74.4):a[i]=3
 # Low front parapet is itself an existing narrow band, no false brick grid.
 if plane(1,-48.9) and inside(-65,45,-48.91,-48.89,26.5,28.5):a[i]=3
 # True aperture backing planes. Each has explicit source and original cut extent.
 for x in [20,44]:
  if plane(1,-13.5) and inside(x-4.5,x+4.5,-13.51,-13.49,31,69):a[i]=2
  if inside(x-4.75,x+4.75,-15.601,-13.601,60,61):a[i]=1
  if inside(x-.5,x+.5,-15.601,-13.601,50,68):a[i]=1
  if inside(x-4.5,x+4.5,-16.5,-15.001,46,48):a[i]=3
 for x in [-53,-32]:
  if plane(1,-13.5) and inside(x-4,x+4,-13.51,-13.49,30,43):a[i]=2
 for z,h in [(31,12),(54,16)]:
  if plane(1,-13.5) and inside(-10.5,-5.5,-13.51,-13.49,z,z+h):a[i]=2
 # Cylinder cut terminates at y=-14; real circle backing, not surrounding ring.
 if plane(1,-14) and inside(-11.1,-4.9,-14.01,-13.99,77.9,84.1):a[i]=2
 for x in [-52,-25,2,29]:
  if plane(1,-46.5) and inside(x-3.5,x+3.5,-46.51,-46.49,4.5,24.5):a[i]=2
 for y in [-7,9,25]:
  if plane(0,58.5) and inside(58.49,58.51,y-4,y+4,7,69):a[i]=2
  for z in [56,62]:
   if inside(58.251,60.75,y-4.25,y+4.25,z,z+1):a[i]=1
 # Existing concrete canopy, not reproduction of staining/debris.
 if inside(-37.5,-2.5,-57.5,-44.5,20,21.8) and (ny<-.5 or nz>.5):a[i]=4
 if inside(-36,-4,-54.85,-48.95,2.801,5.601) and (nz>.5 or ny<-.5):a[i]=4
 # Exposed roof stairs were photographed; no metal rail geometry added.
 if inside(2,10,-9.1,15.1,74,86) and (nz>.5 or ny<-.5):a[i]=4
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1988 original triangles unchanged','limits':['2013 photographer reference, not current precise condition.','No separately modeled ochre arch rings: not painted on wall triangles.','Unsplit plinth-crossing wall planes, rear and roof field neutral.','Narrow original coping bands are coarse color-family approximations.','Six labels are not a verified four-filament slicer project.']},indent=2)+'\n');q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
