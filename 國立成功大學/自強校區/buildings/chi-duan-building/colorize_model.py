"""Color-only assignment to original 1810 triangles; no geometry changes."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED='22f1971723e00c6a7c314d9a32b1cdb15fc52046829ea8bb3aa6b873dedba64f'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED
m=trimesh.load(R/'model.stl',process=True,force='mesh');assert len(m.faces)==1810 and m.is_watertight
pal=[('Observed warm rear wall','#CECFC5'),('Observed silver vertical frame','#A4AFB3'),('Observed dark columns and shade shelves','#434E57'),('Existing discrete window backs approximate reflection','#557C95'),('Observed blue entry canopy','#263D77'),('Observed pale simplified rear fins','#C8CFCD'),('UNVERIFIED roof top frame sides base neutral','#A7ABA5')]
t=m.triangles;c=m.triangles_center;mat=np.full(len(c),6,np.int32)
for i,(x,y,z) in enumerate(c):
 lo=t[i].min(axis=0);hi=t[i].max(axis=0)
 if z<=3.001:continue
 # Broad front backing stays neutral: no invented continuous curtain wall.
 # Whole original front perimeter verticals, excluding unverified top transverse member.
 if lo[2]>=16.999 and hi[2]<=107.001 and lo[1]>=-44.001 and hi[1]<=-23.999 and (lo[0]>=55.499 or hi[0]<=-55.499):mat[i]=1
 for a in [-50,0,50]:
  if lo[0]>=a-1.751 and hi[0]<=a+1.751 and lo[1]>=-37.001 and hi[1]<=-32.999 and hi[2]<=107.001:mat[i]=2
 for a in [44,67,89]:
  if lo[0]>=-55.501 and hi[0]<=55.501 and lo[1]>=-40.001 and hi[1]<=-27.999 and lo[2]>=a-.001 and hi[2]<=a+1.501:mat[i]=2
 if abs(y+27.9)<.002 and any(abs(x-a)<7.501 for a in [-45,-27,-9,9,27,45]) and any(a-.001<z<a+15.001 for a in [23,45,68,90]):mat[i]=3
 if lo[0]>=-11.001 and hi[0]<=55.001 and lo[1]>=-48.001 and hi[1]<=-31.999 and lo[2]>=20.999 and hi[2]<=23.501:mat[i]=4
 # Rear face supported by two official photographs. No arbitrary band across large triangles.
 if abs(y-45)<.002 and z<107.899:mat[i]=0
 if abs(y-44.1)<.002 and any(abs(x-a)<1.901 for a in [-42,-23]) and any(a-.001<z<a+11.001 for a in [10,31,52,73,94]):mat[i]=3
 if abs(y-44.1)<.002 and abs(x+4)<8.501 and any(a-.001<z<a+15.001 for a in [10,31,52,73,94]):mat[i]=3
 # Only existing face domains fully within the wider window strip; no new split lines.
 if abs(y-45)<.002 and lo[0]>=-12.501 and hi[0]<=4.501 and hi[2]<=107.899:mat[i]=1
 for a in range(10,55,3):
  if lo[0]>=a-.601 and hi[0]<=a+.601 and lo[1]>=44.799 and hi[1]<=46.801 and lo[2]>=17.999 and hi[2]<=100.001:mat[i]=5
 if abs(y-44.55)<.002 and abs(x-20)<6.501 and any(a-.001<z<a+12.001 for a in [24,45,66,87]):mat[i]=2
 # Entire upper transverse frame, horizontal main roof and plain side walls stay neutral.
 if z>=107.899 or (lo[2]>=106.999 and lo[1]>=-44.001 and hi[1]<=-23.999):mat[i]=6
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');assert len(np.unique(mat))==7
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int(np.sum(mat==i))}for i,(a,b)in enumerate(pal)],'geometry_policy':'1810 original triangles unchanged.','limits':'Only existing discrete panes colored; no continuous glazing, added fins or gray band boundaries. Top transverse frame, roofs, connecting sides and obscured base neutral.','printing':'Seven appearance labels are not a tested multi-filament slicer project.'},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'bounds_mm':m.bounds.tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
