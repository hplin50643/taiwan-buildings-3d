"""1992 original triangles; complete lower narrow-end eave rectangle only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='6c2f92c2e76795c606b83098578dcf8b98df25cf9324a99fa4813ac46c4ded33';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1992
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,0]-69.5),1)<1e-5
finite=whole&(t[:,:,1].min(1)>=-18.5-1e-5)&(t[:,:,1].max(1)<=40.5+1e-5)&(t[:,:,2].min(1)>=87.5-1e-5)&(t[:,:,2].max(1)<=89.8+1e-5)
assert whole.sum()==4 and finite.sum()==2
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
pal=[('Meiho SC lower end eave pale gray','#DEDDD3'),('Meiho SC unverified walls canopy neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'lower_end_eave_whole_component':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==2
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1992 original triangles unchanged; no cuts or newgeometry','limitations':['2 complete original lower narrow-end eave triangles pale gray.','Whole x69.5 plane has two disconnected rectangle components: lower2 approved, upper2 neutral.','All3vertex finite original lower rectangle y-18.5..40.5,z87.5..89.8; no artificial cut.','Upper canopy, mixed yellow walls, columns, window backings, roofs and other faces neutral.','Official SC map photo is small; nominal color family only, capture unknown not2026.','Actual south campus; immutable repository campus classification retained.','Two labels not verified filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':1992,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
