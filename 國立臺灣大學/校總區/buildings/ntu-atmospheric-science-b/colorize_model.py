"""Bounded 2010 source color on unchanged B-hall triangles; no false panes."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='08de80d009840bf63d3e1630a64ebb9edfbfeedfecd44a93e1b6b8a4ba3dd4ff';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==4270
pal=[('Observed off-white original frames and members','#DADDD7'),('True portal intrados shaded masonry','#66685E'),('UNVERIFIED mixed plinth walls pane-spandrel backing and roof','#B8BAB6')];a=np.full(len(m.faces),2,np.int32)
for i,(t,n)in enumerate(zip(m.triangles,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.003 and hi[0]<=x1+.003 and lo[1]>=y0-.003 and hi[1]<=y1+.003 and lo[2]>=z0-.003 and hi[2]<=z1+.003
 def plane(j,v):return np.all(abs(t[:,j]-v)<.003)
 # Original continuous front/right wall polygons cross the photographed dark plinth: neutral.
 # Original front relief arches and isolated transverse members correspond to white frame family.
 for x in [-38,-25,-12,25,38]:
  if inside(x-4.6,x+4.6,-24.8,-23.001,7,76):a[i]=0
  for z in [19,31,43,55,67]:
   if inside(x-4,x+4,-23.7,-21.7,z,z+2):a[i]=0
  for xx in [x-2,x,x+2]:
   if inside(xx-.4,xx+.4,-23.5,-21.5,8,23):a[i]=0
 for y in [-7,10,27]:
  for z in [19,31,43,55,67]:
   if inside(63.75,66.25,y-4,y+4,z,z+2):a[i]=0
 # Window cut reveals within true openings: off-white frame, never paint entire continuous backing dark.
 for x in [-38,-25,-12,25,38]:
  if inside(x-3.75,x+3.75,-23,-21.5,8,75) and not plane(1,-21.5) and abs(ny)<.1:a[i]=0
 # Portal internal arch curved intrados are real modeled shaded masonry, not glass.
 if inside(-47,-3,-51.5,-16.5,3.05,32.05) and abs(ny)<.1 and nz<-.05:a[i]=1
 # Portal jamb inner returns below spring point: observed pale masonry, no top coping extrapolation.
 # No uniquely separate beige jamb face survived original union; remain neutral.
 # All portal exterior facade polygons span unmodeled narrow dark coping; keep neutral.
 # All horizontal roofs, terrace and base remain neutral. No unmodeled glazing/spandrel subdivisions.
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'geometry_policy':'4270 original triangles unchanged','limits':['2010 historical source color family, not current precision.','Continuous pane-spandrel backings remain neutral; no invented dark entire tall slots.','Cross-plinth main walls and unsplit portal coping/facade remain neutral.','Unknown left rear and horizontal roofs neutral.','Three labels not a verified four-filament slicer project.']},indent=2)+'\n');q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q);print(np.unique(a,return_counts=True))
