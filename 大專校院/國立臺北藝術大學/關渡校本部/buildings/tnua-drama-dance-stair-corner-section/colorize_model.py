"""3196 original triangles; complete tower cap front and right rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='2553c19571f53b70a8fd1c82736caa54002bd5dcc9cc03e2584bc714c09918d5';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3196
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[]
for ax,value,other,l,h in [(1,-23.5,0,15.5,44.5),(0,44.5,1,-23.5,9.5)]:
 whole=np.max(abs(t[:,:,ax]-value),1)<1e-5
 finite=whole&(t[:,:,other].min(1)>=l-1e-5)&(t[:,:,other].max(1)<=h+1e-5)&(t[:,:,2].min(1)>=147.1-1e-5)&(t[:,:,2].max(1)<=150+1e-5)
 assert whole.sum()==2 and np.array_equal(whole,finite)
 fields.append(finite)
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
old=a.copy();hit=(abs(t[:,:,0]-46.5)<1e-4).all(1)&((t[:,:,1]>=-16.2001)&(t[:,:,1]<=-7.7999)&(t[:,:,2]>=115.4999)&(t[:,:,2]<=118.3001)).all(1)
new=np.flatnonzero(hit);assert new.tolist()==[1905,1909] and (old[new]==1).all()
gs=[c for c in g.values() if hit[c].any()];assert len(gs)==1 and set(gs[0])==set(new)
a[new]=0;assert np.array_equal(a[~hit],old[~hit]);assert np.bincount(a).tolist()==[6,3190];assert all(len(set(a[c]))==1 for c in g.values())
pal=[('TNUA Drama Dance Stair Corner Section tower cap front right light stone','#C5C3B8'),('TNUA Drama Dance Stair Corner Section unverified corner walls glazing neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'front_right_cap_whole_components':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'new_upper_sill_faces':2,'new_upper_sill_domains':1,'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==6
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3196 original triangles unchanged; no cuts or newgeometry','limitations':['4 original capfront/right faces retained;2new upperwindow sill outward vertical faces same nominal lightstone gray.','Both whole infinite planes equal finite all3vertex rectangles; original top150mm retained.','Full-height tower wall, landings, glazing proxies, mixed brick base, roofs and other faces neutral.','Outer stair and glazing corner section only, not complete teaching building, courtyard or sculpture.','2016 article and filename are not proven photo capture; not2026 condition.','Original3196 faces and approximate geometry retained; not tested filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':3196,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
