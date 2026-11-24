"""Color-only original 21884 triangles; full-vertex domains and coherent plane fallback."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED='e3c99e1ac086fd37cb1db00633400f25867b2692a8ae9ce3bafa034e1daec642'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED
m=trimesh.load(R/'model.stl',process=True,force='mesh');assert len(m.faces)==21884 and m.is_watertight
pal=[('Approximate warm ochre lower wall','#B78B5D'),('Gray existing stone trim','#95998F'),('Light gray existing projecting grid','#BBC0B7'),('Subdued discrete recess shade','#52615F'),('UNVERIFIED mixed recessed wall rear roof neutral','#A7ABA5')]
t=m.triangles;c=m.triangles_center;mat=np.full(len(c),4,np.int32)
for i,(x,y,z)in enumerate(c):
 lo=t[i].min(axis=0);hi=t[i].max(axis=0);nz=m.face_normals[i,2]
 if z<=3.001:continue
 # Complete lower frontal planes; no drawn pediment edge where no matching topology.
 if np.all(abs(t[i,:,1]+65)<.002) and hi[2]<=56.701:mat[i]=0
 # Existing side plane has coherent boundary z33, first horizontal grid bottom.
 # z31 would cut two original triangles on each side; use existing edge, not subdivision.
 if np.all(abs(t[i,:,0]-np.sign(x)*39)<.002) and hi[2]<=33.001:mat[i]=0
 # Source-supported lower arch backs; shadow rather than literal glazing.
 if any(abs(y-a)<.002 for a in [-63.35,-63.5]) and hi[2]<=41.201:mat[i]=3
 if abs(abs(x)-37.5)<.002 and hi[2]<=22.001:mat[i]=3
 # Existing front relief ring, cornices and dentils only; no fresh outlines.
 if lo[1]>=-66.501 and hi[1]<=-65.001 and hi[2]<=56.701:mat[i]=1
 # Original front grid members: entire existing boxes.
 if lo[1]>=-50.851 and hi[1]<=-47.149 and lo[2]>=30.999:
  if any(lo[0]>=a-.501 and hi[0]<=a+.501 for a in [-38.5+j*5.5 for j in range(15)]) or any(lo[2]>=a-.001 and hi[2]<=a+1.301 for a in [33,47,61,75,89,103,107]):mat[i]=2
 # Existing side grids: broad horizontal members and narrow verticals.
 if lo[2]>=30.999 and ((lo[0]>=37.149 and hi[0]<=40.851)or(lo[0]>=-40.851 and hi[0]<=-37.149)):
  if any(lo[1]>=a-.501 and hi[1]<=a+.501 for a in [-47+j*5.5 for j in range(22)]) or any(lo[2]>=a-.001 and hi[2]<=a+1.301 for a in [33,47,61,75,89,103,107]):mat[i]=2
 # Existing middle-of-window crossbars (only whole original box face regions).
 if any(lo[2]>=a+5-.001 and hi[2]<=a+5.901 for a in [37,51,65,79,93]):
  if lo[1]>=-48.701 and hi[1]<=-46.899:mat[i]=2
  if (lo[0]>=37.787 and hi[0]<=39.589)or(lo[0]>=-39.589 and hi[0]<=-37.787):mat[i]=2
 if abs(y+46.65)<.002 and z>36.999:mat[i]=3
 if abs(abs(x)-37.65)<.002 and z>36.999:mat[i]=3
 # Existing medallion recessed backs remain shade, not new paint symbols.
 if abs(y+63.7)<.002 and any(abs(x-a)<r+.002 and abs(z-b)<r+.002 for a,b,r in [(0,49.5,1.6),(-21,36,1.8),(21,36,1.8)]):mat[i]=3
 # Photograph does not verify rear and horizontal roof planes.
 if abs(y-68)<.002 or (nz>.99 and z>55):mat[i]=4
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');assert len(np.unique(mat))==5
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int(np.sum(mat==i))}for i,(a,b)in enumerate(pal)],'geometry_policy':'21884 original triangles unchanged.','limits':'Lower side ochre ends at original z33 edge, not a measured paint line. Mixed upper recessed wall fully neutral. Existing projecting grid only gray; discrete backs shaded; rear and horizontal roofs neutral.','printing':'Five appearance labels are not a tested multi-filament slicer project.'},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'bounds_mm':m.bounds.tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
