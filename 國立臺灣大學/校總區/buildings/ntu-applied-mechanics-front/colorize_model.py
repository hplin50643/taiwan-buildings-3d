"""Partial original-face color: mixed masonry/portal planes stay neutral."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='d6e367ac30bb294c31a2f63968623a995955ee4aec07e2cbbce3bf502c088e57';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2904
pal=[('Supported pediment beam and stair gray','#999C97'),('Restrained existing inset glazing shadow','#4B5A60'),('Existing discrete dark window frames','#414B4F'),('UNVERIFIED mixed masonry portal columns rear roof neutral','#B6B8B2')];a=np.full(len(m.faces),3,np.int32)
for i,(t,n)in enumerate(zip(m.triangles,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.003 and hi[0]<=x1+.003 and lo[1]>=y0-.003 and hi[1]<=y1+.003 and lo[2]>=z0-.003 and hi[2]<=z1+.003
 def plane(j,v):return np.all(abs(t[:,j]-v)<.003)
 # Separate segmental profile has its own front plane; main wall NEVER threshold-painted.
 if plane(1,-14.5) and inside(-40,40,-14.51,-14.49,71,80.4):a[i]=0
 # Actual circular backing ends y=-13, no new circle ring geometry.
 if plane(1,-13) and inside(-3.1,3.1,-13.01,-12.99,71.9,78.1):a[i]=1
 # Separate colonnade beam FRONT only. Mixed columns and portal stay entirely neutral.
 for x in [-35,35]:
  if plane(1,-25.5) and inside(x-14.5,x+14.5,-25.51,-25.49,26,31):a[i]=0
 # Existing window cut backings, no saturated blue reflections replicated.
 for z in [30,44,58]:
  for x,w in [(-48,11),(-33,3),(-26,3),(-14,11),(0,11),(14,11),(26,3),(33,3),(48,11)]:
   if plane(1,-12.75) and inside(x-w/2,x+w/2,-12.76,-12.74,z,z+9):a[i]=1
   if w>5:
    if inside(x-.5,x+.5,-14.601,-12.799,z,z+9):a[i]=2
    if inside(x-w/2,x+w/2,-14.601,-12.799,z+4.5,z+5.4):a[i]=2
 for x in [-49,-36,36,49]:
  if plane(1,-12.75) and inside(x-3.5,x+3.5,-12.76,-12.74,6,23):a[i]=1
 for x in [-66,66]:
  for z in [8,24,40,56]:
   if plane(1,-13.5) and inside(x-2.5,x+2.5,-13.51,-13.49,z,z+9):a[i]=1
 # Entrance cut, overlapping upper-window cut: only actual backing plane receives shadow.
 if plane(1,-12.5) and inside(-16,16,-12.51,-12.49,5,37):a[i]=1
 for x in [-10,0,10]:
  if inside(x-.55,x+.55,-14.701,-12.699,5,37):a[i]=2
 for z in [16,27]:
  if inside(-16,16,-14.701,-12.699,z,z+1):a[i]=2
 # Existing front tread/riser surfaces; no new railings.
 if inside(-33,33,-36.85,-29.55,2.801,6.301) and (nz>.5 or ny<-.5):a[i]=0
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2904 original triangles unchanged','limits':['2010 and undated official source families, not current-condition precision.','Main wall/portal/colonnade columns mixed brick/gray without boundaries: whole plane neutral.','Only separate pediment front, front colonnade beams, existing windows and steps assigned.','Unknown end/rear/roof neutral.','Four appearance labels are not a verified four-filament slicer job.']},indent=2)+'\n');q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
