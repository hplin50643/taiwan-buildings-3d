"""3742 original triangles; complete main cap front rectangle only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='2cb33cecad68ca099df60f8544b7f7386e3b045af8330d961c261d0f649a8bca';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3742
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,1]+21),1)<1e-5
finite=whole&(t[:,:,0].min(1)>=-47-1e-5)&(t[:,:,0].max(1)<=31+1e-5)&(t[:,:,2].min(1)>=132-1e-5)&(t[:,:,2].max(1)<=134.2+1e-5)
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
pal=[('VNU Wanfang V main cap front muted gray brown','#8F857B'),('VNU Wanfang V unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'main_cap_front_whole_component':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==2
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3742 original triangles unchanged; no cuts or newgeometry','limitations':['2 original main high tower cap front triangles muted gray brown.','Whole y-21 plane equals finite x-47..31,z132..134.2 all3vertices; no omitted fragments.','Right loggia cap10 connected triangles remain neutral because complete photographic termination unverified.','Gold-lettered walls, full-height piers, glazing and roofs remain neutral.','Original190x143 official photo supports nominal family only;capture unknown not2026.','Wanfang building associated hotel/reception uses do not create separate models.','Two material labels not verified filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':3742,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
