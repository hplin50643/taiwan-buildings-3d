"""2560 original triangles; complete finite front half curved ribbon facets only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='24dd885b3cf13ca73a5903d9e57195ebc3bd9b3a2819315da19f83c5a3a6d65d';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2560
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
rx=np.radians(3);ry=np.radians(-12)
RX=np.array([[1,0,0],[0,np.cos(rx),-np.sin(rx)],[0,np.sin(rx),np.cos(rx)]])
RY=np.array([[np.cos(ry),0,np.sin(ry)],[0,1,0],[-np.sin(ry),0,np.cos(ry)]])
scale=np.ptp(t[:,:,0])/110
local=(t/scale-np.array([0,0,43]))@(RY@RX)
fields=[]
for k in range(48,96):
 a0=2*np.pi*k/96;a1=2*np.pi*(k+1)/96
 p0=np.array([38*np.cos(a0),-2+25*np.sin(a0)]);p1=np.array([38*np.cos(a1),-2+25*np.sin(a1)])
 delta=p1-p0;length=np.linalg.norm(delta);tan=delta/length;n=np.array([-tan[1],tan[0]])
 vec=local[:,:,:2]-p0;dist=vec@n;along=vec@tan
 whole=np.max(abs(dist),1)<1e-5
 finite=whole&(along.min(1)>=-1e-5)&(along.max(1)<=length+1e-5)&(local[:,:,2].min(1)>=-1e-5)&(local[:,:,2].max(1)<=19+1e-5)
 assert np.array_equal(whole,finite)
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
pal=[('HKU Gate front ribbon exterior pale gray','#DEDDD3'),('HKU Gate unverified tower booth rear neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'front_half_ribbon_finite_facets':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==98
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2560 original triangles unchanged; no cuts or newgeometry','limitations':['98 original front half ribbon exterior triangles pale gray.','Inverse original scale and Ry(-12)@Rx(3), finite ellipse96 chord facets48..95, all3vertices.','Each entire infinite plane equals finite chord domain; facet94 retains4 original Boolean fragments.','Tower emblem and glazing, ribbon rear half, inner top and underside remain neutral.','Original approximate tower/ribbon and supports unchanged; separate sign wall excluded.','Capture date unverified, source filename not proof; not2026condition.','Two labels not verified filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':2560,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
