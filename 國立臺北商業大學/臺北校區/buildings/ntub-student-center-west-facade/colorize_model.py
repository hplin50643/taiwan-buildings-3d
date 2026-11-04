"""3558 original triangles; two complete canopy fascia front rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='754ab50813fe86bbe2c2cf8d2b4906e6777d67ce8c1dbcbce93f11739839f5f2';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3558
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,1]+15.8),1)<1e-5
fields=[]
for l,h in [(-36.5,-13.5),(13.5,36.5)]:
 finite=whole&(t[:,:,0].min(1)>=l-1e-5)&(t[:,:,0].max(1)<=h+1e-5)&(t[:,:,2].min(1)>=23.3-1e-5)&(t[:,:,2].max(1)<=26.5+1e-5)
 assert finite.sum()==2
 fields.append(finite)
assert whole.sum()==4 and np.array_equal(whole,np.logical_or.reduce(fields))
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
pal=[('NTUB Student Center West Facade two canopy fascia fronts muted red brown','#8A5148'),('NTUB Student Center West Facade unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'two_canopy_front_whole_components':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==4
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3558 original triangles unchanged; no cuts or newgeometry','limitations':['4 original triangles forming two complete canopy front rectangles, nominal red brown.','Whole y=-15.8 plane equals two finite rectangles; no fragment clipping.','Gold-lettered centre sign, painted stairs, columns,49 fins, windows and mixed walls remain neutral.','Canopy top underside returns, cornice and rear section cut remain neutral.','EXIF2023-09-02 without timezone or clock verification, not2026 appearance.','West elevation section only, not full building; no tested filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':3558,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
