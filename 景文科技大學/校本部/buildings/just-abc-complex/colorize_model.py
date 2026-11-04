"""2798 original triangles; complete curved and straight front canopy fascia only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='d6041d23be6781602e968776afe8971ca1caff32e93c845ea3d74a686d546c3a';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2798
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[]
for k in range(45,75):
 a0=np.array([17*np.cos(2*np.pi*k/80),-25+17*np.sin(2*np.pi*k/80)])
 b0=np.array([17*np.cos(2*np.pi*(k+1)/80),-25+17*np.sin(2*np.pi*(k+1)/80)])
 u=(b0-a0)/np.linalg.norm(b0-a0);n=np.array([-u[1],u[0]]);d=t[:,:,:2]-a0
 whole=np.max(abs(d@n),1)<1e-5
 finite=whole&np.all((d@u>=-1e-5)&(d@u<=np.linalg.norm(b0-a0)+1e-5),1)&np.all((t[:,:,2]>=16-1e-5)&(t[:,:,2]<=18.4+1e-5)&(t[:,:,1]<=-32.5+1e-5),1)
 assert finite.sum()==2 and np.array_equal(whole,finite)
 fields.append(finite)
whole=np.max(abs(t[:,:,1]+32.5),1)<1e-5
finite=whole&np.all((abs(t[:,:,0])<=24+1e-5)&(t[:,:,2]>=16-1e-5)&(t[:,:,2]<=18.4+1e-5),1)
assert whole.sum()==4 and np.array_equal(whole,finite)
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
pal=[('JUST ABC Complex front canopy fascia pale warm tan','#C5B5A4'),('JUST ABC Complex unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'complete_canopy_fascia_components':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==64
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2798 original triangles unchanged; no cuts or newgeometry','limitations':['64 complete original canopy front fascia triangles pale muted warm tan.','30 finite80gon curved facets retain60 original triangles plus two straight rectangles4.','Canopy green top lacks pale perimeter boundary; top underside side and rear neutral.','Banner columns, mixed pediment, windows, A/C walls and all unlisted faces neutral.','ABC connected complex is one group/count0, not three buildings.','Capture dates unverified; not2026 survey or tested filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':2798,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
