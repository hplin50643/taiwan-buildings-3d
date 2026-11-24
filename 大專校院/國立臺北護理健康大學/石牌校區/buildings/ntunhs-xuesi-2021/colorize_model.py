"""18170 original triangles; complete north four-row outer frame front only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='2de888add0b76df4136756192cd94ee9be8d5a50f91a17756464f95897bcb883';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==18170
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,1]-33.65),axis=1)<1e-5
inside=np.zeros(t.shape[:2],bool)
for cx,z,w,h in [(-67,34,1.8,30.4),(28.5,34,1.8,30.4),(-19.2,34,97,1.5),(-19.2,63.3,97,1.5)]:
 inside|=(t[:,:,0]>=cx-w/2-1e-5)&(t[:,:,0]<=cx+w/2+1e-5)&(t[:,:,2]>=z-1e-5)&(t[:,:,2]<=z+h+1e-5)
finite=whole&inside.all(axis=1)
assert whole.sum()==18 and np.array_equal(whole,finite)
fields=[finite]
rail=np.logical_or.reduce(fields)
a[rail]=0;p=np.arange(len(a))
def root(i):
 while p[i]!=i:p[i]=p[p[i]];i=p[i]
 return i
for i,j in m.face_adjacency:
 if np.dot(m.face_normals[i],m.face_normals[j])>.999999:p[root(i)]=root(j)
g={}
for i in range(len(a)):g.setdefault(root(i),[]).append(i)
removed=[]
for ids in g.values():
 if len(set(a[ids]))>1:removed.extend(i for i in ids if a[i]!=1);a[ids]=1
pal=[('NTUNHS Xuesi 2021 north outer frame medium gray','#747675'),('NTUNHS Xuesi 2021 unverified walls windows neutral','#B8BAB5')]

old=a.copy();hit=np.zeros(len(t),bool);fronts={};n=m.face_normals
for xx in [-65.5,-50.5,-35.5,-20.5,-5.5,9.5,24.5,39.5]:
 q=(abs(t[:,:,1]+33.8).max(1)<.0001)&(t[:,:,0].min(1)>=xx-1.3-.0001)&(t[:,:,0].max(1)<=xx+1.3+.0001)&(t[:,:,2].min(1)>=11.5-.0001)&(t[:,:,2].max(1)<=78.3+.0001)&(n[:,1]<-.999999);assert q.sum()==2;fronts[str(xx)]=np.flatnonzero(q).tolist();hit|=q
assert hit.sum()==16 and np.all(old[hit]==1)
assert all(not hit[c].any()or hit[c].all()for c in g.values())
a[hit]=2;pal.append(('South pilaster fronts nominal pale family','#E0E0D9'));assert np.bincount(a).tolist()==[18,18136,16];assert all(len(set(a[c]))==1 for c in g.values())
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'south_front_domains':fronts,'new_face_indices':np.flatnonzero(hit).tolist(),'original_colored_faces':18,'added_colored_faces':16,'colored_faces':34,'neutral_faces':18136,'triangles':18170,'complete_new_domains':8,'mixed_coplanar_domains':0,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'18170original triangles and STL/build unchanged','limitations':['Original18northgray and original2palette entries unchanged; newpaleindex2 distinct from neutralindex1.','Only south projectingpilaster front,y-33.8;not horizontalband y-33.2 or returns.','Lower treehidden parts inferred continuoussamepilaster;not eachface directlyseen.','Original2021identity/22groundcolumns/890crosslayercornerexceptions remain,not globalengineering certification.','No2026condition or calibratedcolor. Sourcephotos private.']}
(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':18170,'original_STL_sha256':expected,'added_faces':16,'colored':34,'neutral':18136,'mixed_domains':0,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2)+'\n');print(q['palette'])
