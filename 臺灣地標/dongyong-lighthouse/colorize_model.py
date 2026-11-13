"""Original lighthouse facets only; cliff and mixed lantern glazing remain neutral."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib,math
R=Path(__file__).resolve().parent;EXPECTED_STL='f7bc48b52757cdfde579736c1ba7ad93bf72f9cb8fcb7ddf06eb47411e49771f';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==11696
pal=[('Observed white tower and original rails','#D5D9D3'),('Observed black dome and simplified finial','#303637'),('Existing exposed walking stone','#A5937C'),('Pale neutral mixed upper lantern','#B4C4C0'),('Original shallow aperture shadows','#414C4B'),('UNVERIFIED abstract cliff and display base','#A7ABA5')]
a=np.full(len(m.faces),5,np.int32)
for i,(t,c,n)in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 lo=t.min(0);hi=t.max(0);x,y,z=c;nx,ny,nz=n;rad=np.linalg.norm(t[:,:2]-[-32,-15],axis=1)
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.003 and hi[0]<=x1+.003 and lo[1]>=y0-.003 and hi[1]<=y1+.003 and lo[2]>=z0-.003 and hi[2]<=z1+.003
 def plane(j,v):return np.all(np.abs(t[:,j]-v)<.003)
 if hi[2]<=3.001:continue
 # Fused cylindrical tower continuation: no abstract terrain below it is paint-mapped.
 if rad.max()<=14.601 and lo[2]>=10.799 and hi[2]<=59.001:a[i]=0
 if rad.max()<=17.801 and lo[2]>=55.49 and hi[2]<=76.31:a[i]=0
 # Original low perimeter white parapet, not its floor or all nearby terrain.
 if lo[2]>=11.99 and hi[2]<=16.01 and rad.min()>=20.19 and rad.max()<=21.51:a[i]=0
 if inside(-22,-10.999,-21.51,-8.49,11.6,32.71):a[i]=0
 # Upper lantern is mixed opaque white screens/pale glass; entire drum cannot be called blue glazing.
 if rad.max()<=11.001 and lo[2]>=75.999 and hi[2]<=91.501:a[i]=3
 for k in range(12):
  cx=-32+10.55*math.cos(k*math.pi/6);cy=-15+10.55*math.sin(k*math.pi/6)
  if lo[2]>=75.999 and hi[2]<=91.701 and np.linalg.norm(t[:,:2]-[cx,cy],axis=1).max()<=.531:a[i]=0
 for zz in [76.4,83,90.8]:
  if rad.max()<=10.901 and lo[2]>=zz-.001 and hi[2]<=zz+.651:a[i]=0
 if lo[2]>=90.999 and hi[2]<=92.201 and rad.max()<=11.601:a[i]=0
 if lo[2]>=91.999 and rad.max()<=11.701:a[i]=1
 # Exposed existing annular gallery floor; no rust or fictitious masonry texture.
 if plane(2,62.5)and rad.min()>=10.79 and rad.max()<=17.71:a[i]=2
 if np.max(np.abs(rad-17.7))<.003 and lo[2]>=60.999 and hi[2]<=62.501 and abs(nz)<.01:a[i]=2
 # Straight original stair sidewall faces identified by their planes, not hillside bbox.
 for sy in [-1,1]:
  for yy in [-15+sy*5.5-.65,-15+sy*5.5+.65]:
   if plane(1,yy)and inside(-9.1,54.1,-21.2,-8.8,2.7,40.01):a[i]=0
 for j in range(18):
  top=12+23*(j+1)/18;xx=-9+63*(j+.5)/18
  if inside(xx-1.81,xx+1.81,-20,-10,2.7,top+.002)and plane(2,top):a[i]=2
  if inside(xx-1.82,xx+1.82,-21.15,-8.85,top+4.999,top+5.001):a[i]=0
  # Complete riser face on a known original step plane.
  if inside(xx-1.80,xx+1.80,-20,-10,2.7,top)and(abs(nx)>.999):a[i]=0
 if inside(52.5,63.5,-21.5,-8.5,2.7,34.3):
  if plane(2,34.3):a[i]=2
  elif abs(nx)>.999 or abs(ny)>.999:a[i]=0
 if inside(63.25,64.75,-22,-8,34.25,41.75):a[i]=0
 # Existing vestibule/window recesses only, no optics or interior apparatus.
 if inside(-13.6,-12.4,-17.65,-12.35,17.35,27.85)and nx>.99:a[i]=4
 for ang,zz in [(0,29),(180,43),(90,34)]:
  # The shallow boxes rotate around original tower center; inner backs lie 12.4 from center.
  th=math.radians(ang);u=(t[:,0]+32)*math.cos(th)+(t[:,1]+15)*math.sin(th);v=-(t[:,0]+32)*math.sin(th)+(t[:,1]+15)*math.cos(th)
  if np.max(np.abs(u))<=1.601 and np.all(np.abs(v+12.4)<.003)and lo[2]>=zz-3.151 and hi[2]<=zz+3.151:a[i]=4
# Original complete vestibule outer front fascia only; no coverage expansion.
old=a.copy();t=m.triangles;hit=(abs(t[:,:,0]+11)<.0001).all(1)&(t[:,:,1]>=-21.5001).all(1)&(t[:,:,1]<=-8.4999).all(1)&(t[:,:,2]>=31.2999).all(1)&(t[:,:,2]<=32.7001).all(1)
new=np.flatnonzero(hit);assert new.tolist()==[982,987] and (old[new]==0).all()
ad=m.face_adjacency;groups=trimesh.graph.connected_components(ad[(m.face_normals[ad[:,0]]*m.face_normals[ad[:,1]]).sum(1)>.999999],nodes=np.arange(len(m.faces)),min_len=1)
assert any(set(c)==set(new) for c in groups)
a[new]=2;assert np.array_equal(a[~hit],old[~hit]);assert np.bincount(a).tolist()==[8402,1720,593,404,8,569]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'geometry_policy':'11696 original triangles unchanged','limits':['Same cylindrical white structure continuity, not every hidden face independently observed.','Upper drum mixed pale material, not twelve invented blue glazing sectors.','Coarse cliff and display base neutral; no sea/vegetation map.','Six appearance labels, not a verified four-filament print.']},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
