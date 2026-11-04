"""Only original whole forward crown/posts and two outer vertical eave noses."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='061812d33bb8aced519a7a6344d30190401af9206341c33e0796a29857fb3a90';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==4206
t=m.triangles;n=m.face_normals;lo=t.min(1);hi=t.max(1);e=.003;a=np.full(len(t),1,np.int32)
pal=[('Observed crown front posts and eave nose concrete gray','#A8A69E'),('UNVERIFIED mixed tower walls glazing roof neutral','#B8BAB5')]
def plane(k,v):return np.max(abs(t[:,:,k]-v),axis=1)<e
D={};mask=plane(1,8.5)&(n[:,1]<-.999)&(lo[:,0]>=-55-e)&(hi[:,0]<=-33+e)&(lo[:,2]>=127-e)&(hi[:,2]<=137+e);D['whole_saddle_crown_front']=np.flatnonzero(mask).tolist();assert len(D['whole_saddle_crown_front'])==4
for x in [-50,-38]:
 mask=plane(1,11.2)&(n[:,1]<-.999)&(lo[:,0]>=x-1.3-e)&(hi[:,0]<=x+1.3+e)&(lo[:,2]>=121-e)&(hi[:,2]<=133+e)
 ids=np.flatnonzero(mask).tolist();assert len(ids)==2;D[f'front_post_x{x}']=ids
for y,z in [(-24,65),(26,80)]:
 mask=plane(0,-8)&(n[:,0]<-.999)&(lo[:,1]>=y-18.5-e)&(hi[:,1]<=y+18.5+e)&(lo[:,2]>=z+18-e)&(hi[:,2]<=z+22+e)
 ids=np.flatnonzero(mask).tolist();assert len(ids)==2;assert abs(m.area_faces[ids].sum()-148)<.01;D[f'eave_nose_y{y}']=ids
for ids in D.values():a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1)
assert all(len(set(a[c]))==1 for c in cs);assert int((a==0).sum())==12
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'coplanar_neutralized_faces':[],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'4206 original triangles unchanged','limits':['Whole crown front4, two front post fronts4, two original vertical eave noses4.','Whole connected coplanar domains uniform; no tower z-threshold.','Tower/wings mixed gray pink without geometry boundary, glazing, roof surfaces and undersides neutral.','Original thick abstract saddle preserved; cross-era photographs not2026current condition; completion1990 not capture date.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':4206,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
