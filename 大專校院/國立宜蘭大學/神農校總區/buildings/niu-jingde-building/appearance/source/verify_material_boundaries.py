from pathlib import Path
import numpy as np,json,struct
from build_appearance import regions
A=Path(__file__).resolve().parents[1];raw=(A.parent/'model.stl').read_bytes();n=struct.unpack_from('<I',raw,80)[0];t=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)]).reshape(n,3,3);m=json.loads((A/'face-materials.json').read_text())['face_material_indices'];e=2e-5;out=[];ids=[]
for name,x0,x1,z0,z1 in regions():
 found=[]
 for i,v in enumerate(t):
  normal=np.cross(v[1]-v[0],v[2]-v[0])
  if normal[1]<0 and all(abs(y+61.9)<e and x0-e<=x<=x1+e and z0-e<=z<=z1+e for x,y,z in v):found.append(i)
 ids+=found;v=t[found];out.append(dict(name=name,rectangle_xz=[x0,x1,z0,z1],canonical_stl_ids=found,triangles=v.tolist(),area_mm2=float(np.linalg.norm(np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]),axis=1).sum()/2)))
assert len(ids)==len(set(ids))==230 and set(ids)=={i for i,c in enumerate(m) if c==1};grid=[7944, 7945, 7949, 7951, 7952, 7954, 7957, 7959, 7960, 7962, 7965, 7966, 7967, 7970, 7974, 7975, 7979, 7981, 7982, 7984, 7987, 7989, 7990, 7992, 7995, 7996, 7997, 8000, 8004, 8005, 8009, 8011, 8012, 8013, 8017, 8018, 8020, 8021, 8024, 8025, 8027, 8029, 8033, 8037, 8039, 8044, 8046, 8047, 8051, 8053, 8057, 8060, 8063, 8067, 8070, 8071, 8075, 8077, 8081, 8084, 8087, 8091, 8094, 8096, 8099, 8101];assert all(m[i]==2 for i in grid);assert all(c==0 for i,c in enumerate(m) if i not in ids and i not in grid)
area=sum(r['area_mm2'] for r in out);assert abs(area-1986.98958)<.001
(A/'qa-grid-continuation/material-boundaries.json').write_text(json.dumps(dict(original_faces=n,colored_faces=296,neutral_faces=n-296,new_grid_faces=grid,regions=out,glazing_area_mm2=area,glazing_support_plane_y=-61.9,grid_support_plane_x=55.7,grid_scope="Only original lowest east lattice front; all vertices finite original3vertical+3horizontal bar union; not backing or returns",all_three_vertices_finite_plane_checked=True,no_subdivision=True,no_centroid_selection=True,epsilon_mm=e),indent=2)+'\n')
