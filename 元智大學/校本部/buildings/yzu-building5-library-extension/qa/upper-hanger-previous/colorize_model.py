"""19122 original triangles; complete suspended-box west lower fascia only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='6dcbb67f01518782ba634d89008483a98147878694fc912c68b53743f9999011';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==19122
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,0]+28.95),axis=1)<1e-5
finite=whole&np.all((t[:,:,1]>=-3.45-1e-5)&(t[:,:,1]<=29.4187507629+1e-5)&(t[:,:,2]>=15.9-1e-5)&(t[:,:,2]<=16.95+1e-5),axis=1)
assert whole.sum()==2 and np.array_equal(whole,finite)
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
pal=[('YZU Building 5 Library Extension suspended box lower west fascia pale gray','#DDDCD5'),('YZU Building 5 Library Extension unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'complete_suspended_box_lower_west_fascia':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==2
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'19122 original triangles unchanged; no cuts or newgeometry','limitations':['2 complete original suspended-box lower west fascia triangles pale off-white.','Original PV-aware display and2024 source evidence stay intact; neutral PV in this separate2018photo study is not denial of evidence.','All other19120 triangles neutral in this restricted variant; not replaying or newly claiming inherited PV colors.','Original HFU_Library_Bounded_Approximation object label is template residue preserved in original scene; new identity YZU.','One Building5 and2006 connected extension group,count0;not2026 condition or same-year fullcolor.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':19122,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
