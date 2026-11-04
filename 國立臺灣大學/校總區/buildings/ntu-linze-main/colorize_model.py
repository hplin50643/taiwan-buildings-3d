"""2010 pre-renovation source color families on unchanged original triangles."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='a3f4ad6ddb02a5a0c65f2abb1f939102f3144b4d80e47d002ce8e303fd208f1b'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==4150
pal=[('2010 photographed front and left brick','#AD7B69'),('Observed concrete and existing mullions','#A7AAA3'),('Existing window recess shadow','#414B4D'),('Observed raised canopy edge gray','#727C7A'),('UNVERIFIED right rear horizontal roof','#A9ACA6')]
a=np.full(len(m.faces),4,dtype=np.int32)
for i,(t,c,n) in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 x,y,z=c; nx,ny,nz=n;lo=t.min(0);hi=t.max(0)
 if hi[2]<=3.001:continue
 front=abs(y+19)<.003 and ny<-.99;left=abs(x+68)<.003 and nx<-.99
 if front or left:
  if hi[2]<=35.801 or (lo[2]>=63.799 and hi[2]<=70.001):a[i]=1
  if (lo[2]>=35.799 and hi[2]<=62.001) or (lo[2]>=71.799 and hi[2]<=100.001):a[i]=0
 # Existing projected concrete bands, limited to photographed front and left.
 for zz in [27,34,62,70,100]:
  if lo[2]>=zz-.001 and hi[2]<=zz+1.801 and ((lo[1]>=-21.001 and hi[1]<=-17.999 and hi[0]<=69.001 and lo[0]>=-69.001) or (lo[0]>=-70.001 and hi[0]<=-66.999 and lo[1]>=-20.001 and hi[1]<=34.001)):
   a[i]=1
 # Front discrete openings and their original tiny horizontal mullions.
 for zz in [37,51,74,88]:
  for center in [-57,-38,-19,0,19,38,57]:
   for dx in [-5,0,5]:
    xx=center+dx
    if lo[0]>=xx-1.701 and hi[0]<=xx+1.701 and lo[1]>=-19.001 and hi[1]<=-17.499 and lo[2]>=zz-.001 and hi[2]<=zz+9.501:
     a[i]=2 if ny<-.99 and y>-18 else 0
    if lo[0]>=xx-1.501 and hi[0]<=xx+1.501 and lo[1]>=-19.201 and hi[1]<=-17.199 and lo[2]>=zz+6.799 and hi[2]<=zz+7.701:a[i]=1
  for yy in [-13,-6,22,29]:
   if lo[0]>=-68.001 and hi[0]<=-66.499 and lo[1]>=yy-2.001 and hi[1]<=yy+2.001 and lo[2]>=zz-.001 and hi[2]<=zz+9.501:a[i]=2 if nx<-.99 else 0
 # Lower ribbons: gray returns and dark backs.
 for zz in [29,64]:
  for xx in [-56,-38,-19,0,19,38,56]:
   if lo[0]>=xx-7.501 and hi[0]<=xx+7.501 and lo[1]>=-19.001 and hi[1]<=-17.499 and lo[2]>=zz-.001 and hi[2]<=zz+3.601:a[i]=2 if ny<-.99 else 1
  if lo[0]>=-68.001 and hi[0]<=-66.499 and lo[1]>=-16.001 and hi[1]<=30.001 and lo[2]>=zz-.001 and hi[2]<=zz+3.601:a[i]=2 if nx<-.99 else 1
 for xx in [-52,-36,36,52]:
  if lo[0]>=xx-6.001 and hi[0]<=xx+6.001 and lo[1]>=-19.001 and hi[1]<=-17.499 and lo[2]>=4.999 and hi[2]<=24.001:a[i]=2 if ny<-.99 else 1
  if lo[0]>=xx-.551 and hi[0]<=xx+.551 and lo[1]>=-19.601 and hi[1]<=-17.599 and lo[2]>=4.999 and hi[2]<=24.001:a[i]=1
 # Existing entrance concrete, not fabricated glazing.
 if lo[0]>=-17.001 and hi[0]<=17.001 and lo[1]>=-29.001 and hi[1]<=-10.999 and lo[2]>=2.999 and hi[2]<=27.001:a[i]=1
 if hi[1]<-29 and hi[2]<8:a[i]=1
 # Visible canopy vertical edge only; entire horizontal top remains unknown.
 if lo[2]>=106.999 and hi[2]<=109.001 and ((abs(y+23)<.003 and ny<-.99) or (abs(x+72)<.003 and nx<-.99)):a[i]=3
 if lo[2]>=101.499 and hi[2]<=107.501 and (hi[1]<=-16.899 or hi[0]<=-63.899):a[i]=1
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'geometry_policy':'4150 original triangles unchanged','limits':['2010 source images before 2017–2018 facade renovation, not current appearance.','Right, rear and horizontal roof unverified neutral.','Five material labels not a tested four-filament print.']},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
