"""Partial stone/shadow interpretation. Roof tiles and polychromy UNFINISHED."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='bd32a0940033919d25496b511fc16fbbed9083e10f81ae0f266c16651aa3c8d1';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==51852
pal=[('Observed front stone family','#93968F'),('Genuine existing aperture shadow; not door paint','#454945'),('UNFINISHED roof polychromy and unknown geometry','#B8BAB6')];a=np.full(len(m.faces),2,np.int32)
for i,(t,n)in enumerate(zip(m.triangles,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.003 and hi[0]<=x1+.003 and lo[1]>=y0-.003 and hi[1]<=y1+.003 and lo[2]>=z0-.003 and hi[2]<=z1+.003
 def plane(j,v):return np.all(np.abs(t[:,j]-v)<.003)
 # Original polygonal front apron only, not entire landscape or base.
 if inside(-44,44,-71,-48,3.001,8.801) and (nz>.9 or ny<-.3):a[i]=0
 for x in [-27,-10,10,27]:
  if inside(x-1.15,x+1.15,-53.15,-50.85,6,26) and nz<.2:a[i]=0
 if inside(-29.5,29.5,-53.25,-50.75,24.5,26.5) and (ny<-.99 or nz<-.9):a[i]=0
 for x in [-10,10]:
  if inside(x-.8,x+.8,-53.25,-51.95,9,25) and nz<.2:a[i]=0
 if inside(-7.5,7.5,-53.4,-52.6,22.95,25.25) and (ny<-.99 or nz<-.9):a[i]=0
 for x,w in [(-19,12),(0,13),(19,12)]:
  if plane(1,-48.35) and inside(x-w/2,x+w/2,-48.36,-48.34,8.05,22.55) and ny<-.99:a[i]=1
 for x in [-45,45]:
  if inside(x-2.85,x+2.85,-52.2,-51.501,10.5,19.5) and nz<.2:a[i]=0
  for z in [12.5,15,17.5]:
   if plane(1,-51.45) and inside(x-1.9,x+1.9,-51.46,-51.44,z-.375,z+.375) and ny<-.99:a[i]=1
 for x in [-39,39]:
  if plane(1,-49.7) and inside(x-5,x+5,-49.71,-49.69,6,18) and ny<-.99:a[i]=1
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'geometry_policy':'51852 original triangles unchanged','partial_color_incomplete':True,'limits':['Partial stone and actual recess shadows only.','Roof tiles and detailed polychromy UNFINISHED: conflicting photos not resolved.','No red infill invented on fused original wall; no new face boundaries.','Unknown side/back/courtyard and roof neutral.','Not a verified four-filament slicer project.']},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'partial_color_incomplete':True,'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
