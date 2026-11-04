"""1642 original triangles; two finite outer roof-edge fascia rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='426e2c3e64698c69cba3ae8221e358dc77645d6d1377e134edb196035bdc7282';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1642
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[]
for c in [-34,0,34]:
 for dx in [-11,-6.6,-2.2,2.2,6.6,11]:
  x=c+dx;fields.append((np.max(abs(t[:,:,1]+35),1)<.0001)&(lo[:,0]>=x-.8-.0001)&(hi[:,0]<=x+.8+.0001)&(lo[:,2]>=39-.0001)&(hi[:,2]<=75+.0001))
piers=[]
for x in [-47.5,-17,17,47.5]:
 piers.append((np.max(abs(t[:,:,1]+36.5),1)<.0001)&(lo[:,0]>=x-1.6-.0001)&(hi[:,0]<=x+1.6+.0001)&(lo[:,2]>=11-.0001)&(hi[:,2]<=39+.0001))
rail=np.logical_or.reduce(fields);pier=np.logical_or.reduce(piers);a[rail]=0;a[pier]=2;
p=np.arange(len(a))
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
pal=[('Observed upper louver front rectangles darkgray','#45494A'),('UNVERIFIED mixed walls glazing roof sides neutral','#B8BAB5'),('Observed lower gallery pier fronts palegray','#CECEC5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'upper_louver_fronts':int((rail&(a==0)).sum()),'lower_pier_fronts':int((pier&(a==2)).sum()),'per_louver':[int(x.sum())for x in fields],'per_pier':[int(x.sum())for x in piers],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==36 and(a==2).sum()==8 and(a==1).sum()==1598
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1642 original triangles unchanged; no cuts or newgeometry','limitations':['All vertices on complete finite front rectangles of18original louvers and4gallerypiers.','Only front surfaces; side returns backs and whole mixedwalls neutral.','Capture unknown;2023formdate and photographed109yearbanner not capturedate.','Three material labels not testedfourfilament.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':1642,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
