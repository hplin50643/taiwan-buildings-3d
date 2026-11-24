"""3166 original triangles; source-supported material domains only, no mesh changes."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED='ecc5c03372762acb06f7f70c9946a6285237001473274eee5839f1a1ae0bfcb1'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED
m=trimesh.load(R/'model.stl',process=True,force='mesh');assert len(m.faces)==3166 and m.is_watertight
pal=[('Approximate warm front wall','#C7BDA4'),('Approximate silver central frames','#9FA7A5'),('Existing discrete gray-green window backs','#697B78'),('Generic lower entry shade','#444C49'),('UNVERIFIED side rear roof base neutral','#A7ABA5'),('Shadowed opaque warm-gray recess inner skin','#847E71')]
t=m.triangles;c=m.triangles_center;mat=np.full(len(c),4,np.int32)
for i,(x,y,z)in enumerate(c):
 lo=t[i].min(axis=0);hi=t[i].max(axis=0);nz=m.face_normals[i,2]
 if z<=3.001:continue
 # Coherent entire front planes; outside sides do not inherit this color automatically.
 if any(abs(y-a)<.002 for a in [-35,-34,-33]):mat[i]=0
 if abs(x+15)<.002 and lo[1]>=-35.001 and hi[1]<=-12.999:mat[i]=0
 if lo[0]>=2.999 and hi[0]<=31.001 and lo[1]>=-33.001 and hi[1]<=-14.999 and lo[2]>=29.999 and hi[2]<=104.001:mat[i]=0
 if lo[0]>=28.999 and hi[0]<=31.001 and lo[1]>=-33.001 and hi[1]<=-14.999 and hi[2]<=33.001:mat[i]=0
 if lo[0]>=2.499 and hi[0]<=5.501 and lo[1]>=-32.501 and hi[1]<=-29.499 and hi[2]<=30.901:mat[i]=0
 # Central original face and mullions, never spill across the forward solid screen.
 if abs(y+27)<.002 and lo[0]>=-15.001 and hi[0]<=27.501:mat[i]=1
 for a in [-11,-6,-1,-4,3,10,17,24]:
  if lo[0]>=a-.451 and hi[0]<=a+.451 and lo[1]>=-28.451 and hi[1]<=-26.749:mat[i]=1
 if abs(y+26.2)<.002:mat[i]=2
 # Right/left slit and vertical-strip backs.
 if abs(y+33.2)<.002 and lo[0]>=29.099 and hi[0]<=53.201:mat[i]=2
 if abs(y+34.2)<.002:mat[i]=2
 # Entire tall recess opaque skin is warm shadow, not a black glass rectangle.
 if lo[0]>=-36.001 and hi[0]<=-17.999 and lo[1]>=-35.001 and hi[1]<=-24.499 and lo[2]>=56.999 and hi[2]<=88.001:mat[i]=5
 # Existing nine small backing-window panes remain individually separate.
 if abs(y+23.7)<.002 and any(abs(x-a)<2.251 for a in [-32,-26,-20]) and any(a-.001<z<a+6.801 for a in [60,70,80]):mat[i]=2
 # Entrance three original backs generic muted shade, no fabricated fittings.
 if abs(y+26.2)<.002 and any(abs(x-a)<2.501 for a in [7,14,21]) and 6.999<z<22.001:mat[i]=3
 if nz>.99 and z>30:mat[i]=4
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');assert len(np.unique(mat))==6
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int(np.sum(mat==i))}for i,(a,b)in enumerate(pal)],'geometry_policy':'3166 original triangles unchanged.','limits':'Front warm walls and existing silver central faces only; left tall recess opaque warm-gray inner skin with nine separate panes, not continuous glass. Unverified roof/rear/side neutral.','printing':'Six appearance labels are not a tested multi-filament slicer project.'},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'bounds_mm':m.bounds.tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
