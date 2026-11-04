"""17682 original triangles; two complete24gon support front halves only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='0c326c24f88f5572c7ca74f373e5ab9ded637749224de6a8ac8f2a18da6b4da5';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==17682
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[]
for cx in [-52.,-16.]:
 for k in range(12,24):
  a0=np.array([cx+1.4*np.cos(k*np.pi/12),-32+1.4*np.sin(k*np.pi/12)])
  b0=np.array([cx+1.4*np.cos((k+1)*np.pi/12),-32+1.4*np.sin((k+1)*np.pi/12)])
  tangent=(b0-a0)/np.linalg.norm(b0-a0);normal=np.array([tangent[1],-tangent[0]])
  delta=t[:,:,:2]-a0;along=delta@tangent
  whole=np.max(abs(delta@normal),1)<1e-5
  finite=whole&(along.min(1)>=-1e-5)&(along.max(1)<=np.linalg.norm(b0-a0)+1e-5)&(t[:,:,2].min(1)>=3-1e-5)&(t[:,:,2].max(1)<=25+1e-5)
  assert np.array_equal(whole,finite)
  fields.append(finite)
assert sum(x.sum()for x in fields)==52
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
pal=[('NTUA Library Entrance Section two support column front halves silver gray','#AEB3B5'),('NTUA Library Entrance Section unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'two_support_front_half_finite_facets':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==52
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'17682 original triangles unchanged; no cuts or newgeometry','limitations':['52 original triangles on24 finite24gon front facets of two entrance supports, nominal silver gray.','All3vertices chord plane tangent and z bounds, including4piece Boolean facets, without normal filtering.','Rear column halves, solid globe proxy, glass backings and opaque canopy remain neutral.','Original sphere is not the photographed open steel grid and must not be blanket silver.','EXIF2010-07-25 without verified timezone/clock; night image supports position only.','Entrance adjacent section only, not full library; no tested filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':17682,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
