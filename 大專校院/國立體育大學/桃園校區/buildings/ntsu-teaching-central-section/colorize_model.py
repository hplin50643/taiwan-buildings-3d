"""1734 original triangles; one complete central fin front rectangle only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='1e0b7b5bc0b55fb9e89d1561b3ed813517ae4663095fb2e7b74c5a9e5784f173';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1734
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,1]+14),1)<1e-5
finite=whole&(t[:,:,0].min(1)>=-1.5-1e-5)&(t[:,:,0].max(1)<=3.5+1e-5)&(t[:,:,2].min(1)>=2.8-1e-5)&(t[:,:,2].max(1)<=117.8+1e-5)
assert np.array_equal(whole,finite)
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
pal=[('Observed complete central fin front nominal green','#6F9E84'),('UNVERIFIED mixedwalls windows lettering neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'one_complete_central_fin_front':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==2
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1734 original triangles unchanged; no cuts or newgeometry','limitations':['One complete centralfin frontrectangle2triangles,nominalgreen.','All3vertices originalfiniteplane; entire infiniteplane equalsfinite rectangle.','NaturalBoolean survivingz28.6..116,not artificialmaterialcut.','Horizontal sills differfromphoto extent;entireplane neutral.','Central facadegroup plus narrow wingstrips,notwholebuilding.','Captureunknown;2024AC notnewgeometry or2026proof.','Two labels not verifiedfilament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':1734,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
