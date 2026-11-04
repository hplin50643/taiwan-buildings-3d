"""Post-2023 front color interpretation on untouched original Kangle mesh."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='4c72307153d2c4864ff303732e7ecc1d7cc187d7bd42f7e5816de5471efd5238';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==6186
pal=[('Post-2023 turquoise front frame','#67B2BF'),('Observed muted red-brown front tiles','#98695E'),('Existing front light bond grooves','#C1B19B'),('Original discrete window recess backing','#4B6069'),('Existing front lawn upward surface only','#768657'),('Observed front roof and low band gray','#687075'),('UNVERIFIED courtyard rear side roof and base','#A7ABA5')]
a=np.full(len(m.faces),6,np.int32)
for i,(t,c,n)in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.003 and hi[0]<=x1+.003 and lo[1]>=y0-.003 and hi[1]<=y1+.003 and lo[2]>=z0-.003 and hi[2]<=z1+.003
 def plane(j,v):return np.all(np.abs(t[:,j]-v)<.003)
 # Only above-base top surface of the actual original front terrain primitive.
 if inside(-44,29,-65,-25,2.799,6.41)and nz>.9 and not plane(2,2.8):a[i]=4
 # Actual exposed central front wall, not entire side or rear box.
 if plane(1,-24)and inside(-34.5,18.5,-24.01,-23.99,2.8,29.2)and ny<-.99:a[i]=1
 # Light original shallow bond recess backs; no painted texture/new cuts.
 if plane(1,-23.67)and inside(-34.3,18.3,-23.68,-23.66,7.6,29.2)and ny<-.99:a[i]=2
 # The projecting turquoise frame front and visible deep returns. Rear y=-22.7 unverified.
 if inside(-26.4,10.4,-28.5,-25.799,2.8,27.7)and nz<.2:a[i]=0
 for xx in np.linspace(-22.55,6.55,5):
  if plane(1,-25.8)and inside(xx-1.9,xx+1.9,-25.802,-25.798,6.85,24.45)and ny<-.99:a[i]=3
 # Left front only: turquoise main surround and brick projecting bay.
 if plane(1,-25)and inside(-58,-36,-25.01,-24.99,2.8,30)and ny<-.99:a[i]=0
 if plane(1,-29)and inside(-52.65,-41.35,-29.01,-28.99,2.8,28)and ny<-.99:a[i]=1
 for xx in [-50.7,-47,-43.3]:
  if plane(1,-28.4)and inside(xx-1.15,xx+1.15,-28.41,-28.39,9.3,26.3):a[i]=3
 for xx in [-55,-39]:
  for zz in [9.8,17.4,25]:
   if plane(1,-24.55)and inside(xx-.9,xx+.9,-24.56,-24.54,zz-1.3,zz+1.3):a[i]=3
 # Right lower brick front and original light groove backs.
 if plane(1,-32.5)and inside(22,68,-32.51,-32.49,2.8,18.2)and ny<-.99:a[i]=1
 if plane(1,-32.15)and inside(22,55.01,-32.16,-32.14,6.5,18.2)and ny<-.99:a[i]=2
 if inside(52,64,-34.15,-32.501,4,17.9)and nz<.2:a[i]=0
 for xx in [54.2,58,61.8]:
  for zz in [7.6,13.5]:
   if plane(1,-33.53)and inside(xx-1.35,xx+1.35,-33.54,-33.52,zz-2.1,zz+2.1):a[i]=3
 # Existing clerestory front only; no unseen side/back repetition extrapolated.
 if plane(1,2)and inside(25.5,62.5,1.99,2.01,20.9,28)and ny<-.99:a[i]=1
 for xx in np.linspace(28,60,9):
  if plane(1,2.37)and inside(xx-1.3,xx+1.3,2.36,2.38,22.55,27.05):a[i]=3
 # Roof slope with negative-Y normal and entirely front of monitor center.
 if inside(24,64,.5,17,27.7,29.7)and ny<-.1 and nz>.1 and abs(ny)>abs(nx)*2:a[i]=5
 # Small exposed front base/ledge bands visible in the two official images.
 if plane(1,-33)and inside(21.5,68.5,-33.01,-32.99,17.9,19)and ny<-.99:a[i]=5
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'geometry_policy':'6186 original triangles unchanged','limits':['Only 2023-after front entrance and front upward lawn surface supported.','Turquoise frame primitive bounds are identification only: y=-22.7 rear neutral.','Original large tile-grid cuts are geometry, not new texture or exact tiling.','Back courtyard/mound, side and broad roof unknown neutral.','Seven appearance labels are not a verified four-filament slicer project.']},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
