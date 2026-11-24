"""Whole original front metal grid members only; no reflective window coloring."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='2ead81bd64af6fda7e0bf1607f1ea49eca8ec707ff3b825e8d541a9692ca60d8';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==6380
t=m.triangles;n=m.face_normals;lo=t.min(1);hi=t.max(1);e=.003;a=np.full(len(t),1,np.int32)
pal=[('Observed whole tower metal horizontal front members dark gray green','#40544D'),('UNVERIFIED reflective glazing main walls roof rear neutral','#B8BAB5')]
def plane(k,v):return np.max(abs(t[:,:,k]-v),axis=1)<e
D={}
for z in range(18,115,6):
 mask=plane(1,-30.05)&(n[:,1]<-.999)&(lo[:,0]>=47.8-e)&(hi[:,0]<=66.2+e)&(lo[:,2]>=z-e)&(hi[:,2]<=z+1+e)
 ids=np.flatnonzero(mask).tolist();assert len(ids)==2
 pts=t[ids].reshape(-1,3);assert np.allclose(pts.min(0),[47.8,-30.05,z],atol=e) and np.allclose(pts.max(0),[66.2,-30.05,z+1],atol=e)
 assert abs(m.area_faces[ids].sum()-18.4)<.01
 D['whole_band_z'+str(z)]=ids;a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999
cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1)
assert all(len(set(a[c]))==1 for c in cs);assert sum(len(x)for x in D.values())==34
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'whole_rectangle_count':17,'coplanar_neutralized_faces':[],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'6380 original triangles unchanged','limits':['17 complete original rectangular metal fronts z18..114 every6; each area18.4.','Original bottom6/12 and top120 members neutral; all reveals neutral.','Whole connected coplanar domains uniform.','Reflective glass and visible stair rails do not establish one blue/green surface.','Main wall, underlying tower plane, broad residual strips, side/rear/roof neutral.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':6380,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
