"""Original Chimei triangles only; source-limited front palette, no geometry edits."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='4638f88fa1d8d6dd598d17c98d74086cc5a66923a4ddf0b519e47a74a2e2a873';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==17960
pal=[('Observed front pale stone family','#D8DAD2'),('Observed front half dome gray','#9DA9A6'),('Original front aperture shadow','#4B5755'),('UNVERIFIED side rear roof angel and plinth','#A7ABA5')]
a=np.full(len(m.faces),3,np.int32)
for i,(t,c,n)in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.003 and hi[0]<=x1+.003 and lo[1]>=y0-.003 and hi[1]<=y1+.003 and lo[2]>=z0-.003 and hi[2]<=z1+.003
 def plane(j,v):return np.all(np.abs(t[:,j]-v)<.003)
 if hi[2]<=3.5:continue
 # Front-facing original facade; side returns and broad roof remain unverified.
 if hi[1]<=-16.59 and lo[2]>=3.499 and hi[2]<=30.01 and ny<-.99:a[i]=0
 # Complete freestanding portico columns/capitals, identified original components.
 for xx in np.linspace(-9.8,9.8,6):
  if inside(xx-1.18,xx+1.18,-26.18,-23.82,4,21.8):a[i]=0
 # Original small window mullions/sill relief only, not a new color line on large faces.
 for side in [-1,1]:
  for xx in np.linspace(side*30,side*54,7):
   if inside(xx-.23,xx+.23,-17.471,-16.669,14,19.6):a[i]=0
   for zz,hh,yy,dd in [(13.65,.5,-17.18,.85),(19.4,.5,-17.15,.75)]:
    if inside(xx-1.3,xx+1.3,yy-dd/2,yy+dd/2,zz,zz+hh):a[i]=0
  # Original shallow terminal crown/finial, not the central angel.
  if inside(side*62-5.5,side*62+5.5,-19.901,-16.9,23.1,29.91) and hi[1]<=-17.59:a[i]=0
 # Only existing front aperture backs, with direct cut-plane and full-vertex bounds.
 for side in [-1,1]:
  for xx in np.linspace(side*30,side*54,7):
   if inside(xx-1.001,xx+1.001,-16.632,-16.628,5.1,19.5) and plane(1,-16.63):a[i]=2
  xx=side*22
  if inside(xx-1.601,xx+1.601,-17.657,-17.653,5,20.4) and plane(1,-17.655):a[i]=2
  xx=side*62
  if inside(xx-2.501,xx+2.501,-18.027,-18.023,5,21) and plane(1,-18.025):a[i]=2
 for xx in [-6,0,6]:
  if inside(xx-1.451,xx+1.451,-21.002,-20.998,4.2,15.6) and plane(1,-21):a[i]=2
 # Front half original dome only. Neither rear half nor simplified angel is extrapolated.
 rad=np.linalg.norm(t[:,:2]-[0,-6],axis=1)
 if rad.max()<=9.521 and lo[2]>=27.599 and hi[2]<=36.157 and hi[1]<=-5.999 and nz>0:a[i]=1
 if rad.max()<=1.741 and lo[2]>=35.629:a[i]=3
 # Original drum front, vertical only; horizontal rim is not a verified roof surface.
 if rad.max()<=9.801 and lo[2]>=22.899 and hi[2]<=28.101 and hi[1]<=-5.999 and abs(nz)<.1:a[i]=0
 if lo[2]>=36.17:a[i]=3
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'geometry_policy':'17960 original triangles unchanged','limits':['Backlit official front photo supports color families, not calibrated stone color.','Front half dome only; summit angel is unverified neutral, not gold.','Broad roofs, side/rear and display plinth neutral.','Four appearance labels are not a verified four-filament slicer project.']},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
