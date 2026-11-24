"""1720 original triangles; complete outer curved canopy vertical fascia only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='a36f266bf25424ea993f3a9d0d92eaf4b17055bd604f6c046828a6f3df59634f';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1720
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[]
for k in range(64):
 a0=np.array([48+83*np.cos(np.radians(254+k*.5)),67+83*np.sin(np.radians(254+k*.5))])
 b0=np.array([48+83*np.cos(np.radians(254+(k+1)*.5)),67+83*np.sin(np.radians(254+(k+1)*.5))])
 u=(b0-a0)/np.linalg.norm(b0-a0);n=np.array([-u[1],u[0]]);d=t[:,:,:2]-a0
 whole=np.max(abs(d@n),1)<1e-5
 finite=whole&np.all((d@u>=-1e-5)&(d@u<=np.linalg.norm(b0-a0)+1e-5)&(t[:,:,2]>=19-1e-5)&(t[:,:,2]<=21.7+1e-5),1)
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
pal=[('NFU Main Gate outer curved canopy pale blue-green','#A4BCBA'),('NFU Main Gate unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'finite_outer_canopy_chord_components':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==128
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1720 original triangles unchanged; no cuts or newgeometry','limitations':['128 complete original outer canopy fascia triangles pale muted blue-green.','64 original finite chord facets radius83 centered48,67 angles254..286 z19..21.7; whole planes equal finite domains.','Canopy top inner ends and underside neutral; no transparency invented.','Yellow sign walls contain letters without boundaries; all walls glazing base and rear neutral.','PDF2025-06-27 is publication not capture; no tiger sculpture or adjacent tower added.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':1720,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
