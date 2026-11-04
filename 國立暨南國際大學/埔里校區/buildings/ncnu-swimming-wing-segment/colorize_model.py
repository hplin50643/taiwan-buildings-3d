"""6356 original triangles; complete left curved roof end thickness face only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='df1860f84ae473ff3abb8beb9f4224332f041360d3447682d2a64649099b5cd3';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==6356
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
ys=np.linspace(-40,40,33);zs=61.2+8.5*(1-(ys/40)**2)
whole=np.max(abs(t[:,:,0]+67),axis=1)<1e-5
upper=np.interp(t[:,:,1],ys,zs);lower=upper-1.9
finite=whole&np.all((t[:,:,1]>=-40-1e-5)&(t[:,:,1]<=40+1e-5)&(t[:,:,2]>=lower-1e-5)&(t[:,:,2]<=upper+1e-5),axis=1)
assert whole.sum()==64 and np.array_equal(whole,finite)
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
pal=[('NCNU Swimming Wing Segment left curved roof end light gray','#CBCBC5'),('NCNU Swimming Wing Segment unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'complete_left_curved_roof_end':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==64
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'6356 original triangles unchanged; no cuts or newgeometry','limitations':['64 complete original left curved roof-end triangles light gray.','Existing two depth-preview materials are not actual surface-color certification; history retained.','All other6292 triangles unknown neutral including former dark recess cues, long front fascia, roof skins, monitor, mixed balcony and screen walls.','Rectangular-window wing segment only, not full swimming hall or sports center.','Official EXIF2012-07-03 metadata not independently verified capture;architect URL2024/08 not capture;not2026.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':6356,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
