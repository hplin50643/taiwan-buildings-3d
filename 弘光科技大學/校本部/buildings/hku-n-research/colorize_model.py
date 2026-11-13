"""7070 original triangles; highest complete balcony front component only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='b6f7a1f79f82f2c535ba629446a1482941f4f55900b20e7c182f683804c7daec';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==7070
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,1]+7),1)<1e-5
finite=whole&(t[:,:,0].min(1)>=-62-1e-5)&(t[:,:,0].max(1)<=-14+1e-5)&(t[:,:,2].min(1)>=58-1e-5)&(t[:,:,2].max(1)<=63.2+1e-5)
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
original=a.copy()
added=(np.max(abs(t[:,:,1]-5),1)<1e-5)&(t[:,:,0].min(1)>=-67.5-1e-5)&(t[:,:,0].max(1)<=27.5+1e-5)&(t[:,:,2].min(1)>=77-1e-5)&(t[:,:,2].max(1)<=79+1e-5)
assert np.flatnonzero(added).tolist()==[6956,6959]
assert any(set(np.flatnonzero(added))==set(ids)for ids in g.values())
assert (original==0).sum()==12 and (original[added]==1).all()
a[added]=0
assert np.array_equal(a[~added],original[~added])
assert all(len(set(a[ids]))==1 for ids in g.values())
pal=[('HKU N highest balcony front pale gray','#DEDDD3'),('HKU N unverified walls lower balconies neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'highest_complete_balcony_front':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g),'highest_roof_front_added':int(added.sum())}
assert (a==0).sum()==14
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'7070 original triangles unchanged; no cuts or newgeometry','limitations':['Highest whole connected balcony front component twelve original triangles pale gray.','All three vertices finite original bounds; four whole coplanar components enumerated.','Original slab and solid rail union retained with original slot, not upper-only selection.','Three lower fronts mix real open railing and solid panel; entire original components neutral.','N research connected group only, not neighboring D.','Construction dates and URL are not capture date; not2026.','Two labels not verified filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':7070,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
