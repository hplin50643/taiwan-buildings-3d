"""19686 original triangles. Explicit full-vertex domains and normals, no new geometry."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED='7299fbbef4a0f9f8a15eb84b2e5560f4b26dcdb39e791e1486a52ef33df2cc9c'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED
m=trimesh.load(R/'model.stl',process=True,force='mesh');assert len(m.faces)==19686 and m.is_watertight
pal=[('Approximate verified front brick','#A85143'),('Approximate existing pale stone relief','#CAC9BC'),('Generic dark recess shade','#3F4946'),('Bounded observed front low roof gray-green','#829C87'),('High central tower cap dark gray','#505955'),('UNVERIFIED sides rear courts roof neutral','#A7ABA5')]
t=m.triangles;c=m.triangles_center;mat=np.full(len(c),5,np.int32)
for i,(x,y,z)in enumerate(c):
 lo=t[i].min(axis=0);hi=t[i].max(axis=0);nx,ny,nz=m.face_normals[i]
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.002 and hi[0]<=x1+.002 and lo[1]>=y0-.002 and hi[1]<=y1+.002 and lo[2]>=z0-.002 and hi[2]<=z1+.002
 def box(cx,cy,cz,w,d,h):return inside(cx-w/2,cx+w/2,cy-d/2,cy+d/2,cz-h/2,cz+h/2)
 def plane_y(a):return np.all(abs(t[i,:,1]-a)<.002)
 if z<=3.001:continue
 # Verified front planes only; side/court/rear planes do not inherit red.
 if ny<-.99 and any(plane_y(a)for a in [-42.5,-43.5,-44.5]) and hi[2]<=36.201:mat[i]=0
 # Front of iconic tower shaft, with limited visible side returns (not the rear plane).
 if inside(-5.25,5.25,-40.5,-28.5,20,54.8) and abs(nz)<.01 and not plane_y(-28.5):mat[i]=0
 # Front regular relief strips, pilasters and upper rectangular details.
 if any(box(0,-42.6,a,140,.9,.65)for a in [6.5,8,17,24,27.8]):mat[i]=1
 for a in [-51,-44.5,-38,-31.5,-25,-18.5,18.5,25,31.5,38,44.5,51]:
  if box(a,-42.65,26,3.2,.9,1.5):mat[i]=1
  if any(box(a+b,-42.9,15.8,.75,1.05,17)for b in [-2.75,2.75]):mat[i]=1
  if any(box(a,-43.05,b,5.5,1.15,.65)for b in [7.75,17.65,24.05]):mat[i]=1
 # Front corner groups: only front stone faces; rear groups remain unknown.
 for a in [-62,62]:
  if ny<-.99 and any(box(a,-34.5,b,17.7,18.7,.75)for b in [6.4,8.1,10,22.4,24.2,29.1,31.8]):mat[i]=1
  if box(a,-44,29.6,12,2,3.8):mat[i]=1
  if any(box(a+b,-43.9,17,.9,1.3,22)for b in [-6.8,6.8]):mat[i]=1
  if box(a,-34.5,33,12,13,2.6) and ny<-.01:mat[i]=1
  if inside(a-6.5,a+6.5,-41.5,-27.5,34.15,36.75) and nz>.01 and ny<=.001:mat[i]=3
 # Front escorts, independent projecting bands not painted fake stripes.
 for a in [-10.2,10.2]:
  if any(box(a,-35.9,b,7.9,18,.75)for b in [7.4,9,23.1,25,31.1,35.1]) and ny<-.01:mat[i]=1
  if box(a,-35.9,35.5,7.6,17.8,1.4) and ny<-.01:mat[i]=1
 # Shaft front ribs and upper flared stone support.
 if any(box(a,-40.7,40,.9,1,27)for a in [-4.4,4.4]):mat[i]=1
 if inside(-6.5,6.5,-41.75,-27.25,53.4,55.55):mat[i]=1
 # Existing octagonal lantern: brick vertical panels, stone ring extrusions, dark recesses.
 if inside(-7.4,7.4,-42.5,-26.5,55.35,62.9) and abs(nz)<.01:mat[i]=0
 if inside(-7.4,7.4,-42.5,-26.5,55.35,62.95) and any(lo[2]>=a-.002 and hi[2]<=a+.552 for a in [56.2,57.8,59.4,61,62.4]):mat[i]=1
 if inside(-7.4,7.4,-42.5,-26.5,56.7,61.7) and (plane_y(-39.8)or plane_y(-29.2)or np.all(abs(t[i,:,0]-5.3)<.002)or np.all(abs(t[i,:,0]+5.3)<.002)):mat[i]=2
 if inside(-7.1,7.1,-42.1,-26.9,62.9,65.1):mat[i]=4
 # Central front pediment and solid original porch/steps.
 if box(0,-44,31.7,10,2,3.4):mat[i]=1
 if inside(-9,9,-50.351,-42,3,15.7):mat[i]=1
 if inside(-11,11,-51.351,-47.799,2.85,4):mat[i]=1
 # Limited rear semicircular porch only; no extrapolation into rear wing/courts.
 if inside(-9.501,9.501,42.499,52.001,3,15.001):mat[i]=1
 # Discrete front arch backs (shadow, not all glass).
 if plane_y(-41.45) and any(abs(x-a)<2.101 for a in [-51,-44.5,-38,-31.5,-25,-18.5,18.5,25,31.5,38,44.5,51]) and any(a-.002<z<a+h+.002 for a,h in [(8.2,6.8),(18.15,5.6)]):mat[i]=2
 if plane_y(-43.05) and any(abs(x-a)<2.351 for a in [-62,62]) and any(a-.002<z<a+h+.002 for a,h in [(9,6.5),(19,5.5)]):mat[i]=2
 if plane_y(-43.5) and any(abs(x-a)<1.401 for a in [-10.2,10.2]) and any(a-.002<z<a+4.602 for a in [11,20,28]):mat[i]=2
 if plane_y(-40.05) and abs(x)<1.351 and any(a-.002<z<a+4.402 for a in [32.7,39.1,45.3,51.5]):mat[i]=2
 if plane_y(-48.2) and abs(x)<3.001 and 3.699<z<13.701:mat[i]=2
 if plane_y(50) and abs(x)<2.401 and 3.499<z<12.001:mat[i]=2
 # Front outward-facing wing low slopes only; rearward courtyard slopes neutral.
 if inside(-70.35,70.35,-42.85,-26.15,29.15,32.35) and nz>.01 and ny<-.01:mat[i]=3
 for a in [-43,-25,25,43]:
  if box(a,-34.5,32.9,2.7,2.7,2.8):mat[i]=1
  if inside(a-1.7,a+1.7,-36.2,-32.8,34.1,35.5) and nz>.01:mat[i]=3
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');assert len(np.unique(mat))==6
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int(np.sum(mat==i))}for i,(a,b)in enumerate(pal)],'geometry_policy':'19686 original triangles unchanged.','limits':'Verified front and limited rear porch only; side/rear/court surfaces neutral. Low front roof green is not applied to high tower cap, which is dark gray. Relief is original coarse geometry, no new bands, texture or symbols.','printing':'Six appearance labels are not a tested multi-filament slicer project.'},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'bounds_mm':m.bounds.tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
