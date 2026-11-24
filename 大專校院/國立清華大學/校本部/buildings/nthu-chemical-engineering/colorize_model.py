"""Original front/right trim with bounded inferred returns; no segmentation or geometry changes."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='41e8564cf83b71f554aa716cfd5ae1992bbc522e7443b0ba5a81aaa0102e952a';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2924
t=m.triangles;n=m.face_normals;lo=t.min(1);hi=t.max(1);e=.003;a=np.full(len(t),1,np.int32)
pal=[('Pre-renovation pale trim; bounded return continuity inferred','#D3D0C5'),('UNVERIFIED mixed pink walls glazing stairs roof neutral','#B8BAB5')]
def plane(k,v):return np.max(abs(t[:,:,k]-v),axis=1)<e
D={}
for z in [15,26,37,48,59,70,81,87]:
 for x0,x1 in [(-56,-24),(24,56)]:
  mask=plane(1,-29.55)&(n[:,1]<-.999)&(lo[:,0]>=x0-e)&(hi[:,0]<=x1+e)&(lo[:,2]>=z-e)&(hi[:,2]<=z+.9+e)
  ids=np.flatnonzero(mask).tolist();assert len(ids)>=2
  assert abs(m.area_faces[ids].sum()-32*.9)<.01
  D[f'front_x{x0}_z{z}']=ids;a[ids]=0
 mask=plane(0,56.55)&(n[:,0]>.999)&(lo[:,1]>=-29-e)&(hi[:,1]<=39+e)&(lo[:,2]>=z-e)&(hi[:,2]<=z+.9+e)
 ids=np.flatnonzero(mask).tolist();assert len(ids)==2;assert abs(m.area_faces[ids].sum()-68*.9)<.01
 D[f'right_z{z}']=ids;a[ids]=0
# Retain the original 50 observed outward faces before considering return faces.
original=a.copy();assert int((original==0).sum())==50
candidate=np.zeros(len(t),bool);boxes=[];eps=3e-5
for z in [15,26,37,48,59,70,81,87]:
 for label,cx,cy,w,depth in [('front_left',-40,-29,32,1.1),('front_right',40,-29,32,1.1),('right',56,5,1.1,68)]:
  low=np.array([cx-w/2,cy-depth/2,z]);high=np.array([cx+w/2,cy+depth/2,z+.9])
  inside=np.all((t>=low-eps)&(t<=high+eps),axis=(1,2));surface=np.zeros(len(t),bool)
  for axis in range(3):
   surface|=(np.max(abs(t[:,:,axis]-low[axis]),axis=1)<eps)|(np.max(abs(t[:,:,axis]-high[axis]),axis=1)<eps)
  mask=inside&surface;candidate|=mask;boxes.append({'member':label,'z':z,'bounds':[low.tolist(),high.tolist()],'candidate_faces':np.flatnonzero(mask).tolist()})
assert candidate.sum()==275 and np.all(candidate[original==0])
trial=original.copy();trial[candidate]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999
cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1)
# Never extend a partial band mask across a shared broad wall/roof plane.
# Reject new selections unless the whole connected coplanar domain is selected.
rejected=[]
for ids in cs:
 if np.all(trial[ids]==0):a[ids]=0
 elif np.any(candidate[ids]):rejected.extend(int(i) for i in ids if candidate[i] and original[i]!=0)
added=np.flatnonzero((a==0)&(original!=0));assert len(added)==174 and (a==0).sum()==224
assert np.all(a[original==0]==0);assert len(set(rejected))==51
assert all(len(set(a[ids]))==1 for ids in cs)
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'original_domain_face_indices':D,'candidate_members':boxes,'new_return_face_indices':added.tolist(),'excluded_candidate_faces':sorted(set(rejected)),'coplanar_components':len(cs),'original_color_faces':50,'new_color_faces':174,'colored_faces':224,'neutral_faces':2700,'partial_color_incomplete':True,'fully_colored_exterior':False,'count_delta':0,'geometry_policy':'2924 original triangles unchanged; no cuts or added geometry.','limits':['Original 50 observed outward trim faces retained.','174 bounded return faces use inferred nominal same-member color continuity, not direct observation of each surface.','51 candidate faces touching mixed broad coplanar domains remain neutral. No expansion across blank side/rear walls.','Mixed pink walls, gable caps, center spine, columns, all glazing, stairs and roof mass remain neutral.','Pre-renovation historical photo approximation, not the renovated 2026 condition; no completion inference.']}
(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':2924,'original_color_faces':50,'new_color_faces':174,'colored_faces':224,'neutral_faces':2700,'newly_selected_faces':added.tolist(),'all_coplanar_domains_uniform':True,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2)+'\n');print('PASS',len(added),'added;',len(set(rejected)),'excluded')
