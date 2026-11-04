"""2198 original triangles; front and rightfold whole roof fascia planes only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='369cd63ba611be6fe51cca721c0b1b8cb198c8cee8a5ef451eed584d6c47a6d4';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2198
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole1=np.max(abs(t[:,:,1]+19),1)<1e-5
whole2=np.max(abs(16*(t[:,:,0]-27)-27*(t[:,:,1]+19))/np.hypot(16,27),1)<1e-5
zok=(t[:,:,2].min(1)>=82-1e-5)&(t[:,:,2].max(1)<=84.8+1e-5)
f1=whole1&zok&(t[:,:,0].min(1)>=-67-1e-5)&(t[:,:,0].max(1)<=27+1e-5)
f2=whole2&zok&(t[:,:,0].min(1)>=27-1e-5)&(t[:,:,0].max(1)<=54+1e-5)&(t[:,:,1].min(1)>=-19-1e-5)&(t[:,:,1].max(1)<=-3+1e-5)
assert np.array_equal(whole1,f1) and np.array_equal(whole2,f2)
fields=[f1,f2]
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
pal=[('HKU P front roof fascia pale gray','#DEDDD3'),('HKU P unverified tower walls roof neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'front_and_rightfold_roof_fascia':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==4
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2198 original triangles unchanged; no cuts or newgeometry','limitations':['Two whole front and chamfer fascia planes four original triangles pale warm gray.','All three vertices finite original polygon edges; each entire infinite plane equals its finite domain.','Tower union naturally shortens chamfer to x52.5, not material clipping.','Lettered brick tower, roof tops and soffits, mixed walls and glazing remain neutral.','P single original group, no glass pyramid or extra floors added.','Completion2009 not capture date; no2026 claim.','Two labels not verified filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':2198,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
