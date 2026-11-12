"""Original observed faces plus finite front belfry post side continuity inference."""
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
original=a.copy();assert (original==0).sum()==12
candidate=np.zeros(len(t),bool);members=[]
for x in [-50,-38]:
 low=np.array([x-1.3,11.2,121]);high=np.array([x+1.3,13.8,133]);inside=np.all((t>=low-e)&(t<=high+e),axis=(1,2));side=np.zeros(len(t),bool)
 for k in [0,1]:side|=(np.max(abs(t[:,:,k]-low[k]),axis=1)<e)|(np.max(abs(t[:,:,k]-high[k]),axis=1)<e)
 q=inside&side;candidate|=q;members.append({'x':x,'bounds':[low.tolist(),high.tolist()],'side_faces':np.flatnonzero(q).tolist()})
trial=a.copy();trial[candidate]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);excluded=[]
for ids in cs:
 if np.all(trial[ids]==0):a[ids]=0
 elif np.any(candidate[ids]):excluded.extend(int(i) for i in ids if candidate[i] and original[i]!=0)
added=np.flatnonzero((a==0)&(original!=0));assert len(added)==12 and (a==0).sum()==24 and candidate.sum()==16
assert not excluded and np.all(a[original==0]==0) and all(len(set(a[c]))==1 for c in cs)
pal[0]=('Observed crown post fronts eave noses; inferred front post returns gray','#A8A69E')
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'original_domain_face_indices':D,'front_post_members':members,'new_inferred_face_indices':added.tolist(),'original_colored_faces':12,'added_colored_faces':12,'colored_faces':24,'neutral_faces':4182,'coplanar_components':len(cs),'excluded_faces':excluded,'partial_color_incomplete':True,'fully_colored_exterior':False,'count_delta':0,'geometry_policy':'4206 original triangles and original STL/OBJ/build bytes unchanged; no cuts','limits':['Original 12 observed faces retained. Only the two original front belfry posts receive inferred continuous gray on their bounded vertical side/rear faces.','Twelve new faces are same-member continuity inference, not directly photograph verified individually.','Rear posts, post caps, saddle crown returns, roof/eave tops, undersides and brackets remain neutral; shadow is not black material.','Mixed pink/gray tower shaft, wing walls, glazing, base and all other unknown surfaces remain neutral.','Original thick sculptural saddle remains an abstraction, not newly geometry-certified.','Cross-era photographs with unknown capture dates do not establish 2026 current condition; 1990 completion and 2020 publication are not capture dates.']}
(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':4206,'color_mesh_sha256':H(R/'color-mesh.npz'),'original':12,'added':12,'colored':24,'neutral':4182,'mixed_coplanar_domains':0},indent=2)+'\n');print(q)
