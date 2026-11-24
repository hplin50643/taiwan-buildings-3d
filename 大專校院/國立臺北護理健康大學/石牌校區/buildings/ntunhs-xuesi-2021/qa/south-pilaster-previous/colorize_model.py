"""18170 original triangles; complete north four-row outer frame front only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='2de888add0b76df4136756192cd94ee9be8d5a50f91a17756464f95897bcb883';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==18170
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,1]-33.65),axis=1)<1e-5
inside=np.zeros(t.shape[:2],bool)
for cx,z,w,h in [(-67,34,1.8,30.4),(28.5,34,1.8,30.4),(-19.2,34,97,1.5),(-19.2,63.3,97,1.5)]:
 inside|=(t[:,:,0]>=cx-w/2-1e-5)&(t[:,:,0]<=cx+w/2+1e-5)&(t[:,:,2]>=z-1e-5)&(t[:,:,2]<=z+h+1e-5)
finite=whole&inside.all(axis=1)
assert whole.sum()==18 and np.array_equal(whole,finite)
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
pal=[('NTUNHS Xuesi 2021 north outer frame medium gray','#747675'),('NTUNHS Xuesi 2021 unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'complete_north_four_row_outer_frame':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==18
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'18170 original triangles unchanged; no cuts or newgeometry','limitations':['18 complete original north four-row outer frame front triangles medium gray;18152 neutral.','Original four readability/depth/frame presentation materials and all original evidence retained;not monochrome discovery.','22 ground columns with890 cross-layer corner-loss samples,max2.0436738percent retained as finite exception,not890columns or global minimum thickness.','No new printability endorsement or physical slicer/print certification.','Project49.9m unallocated to this building;2022mirror-suspect aerial not used for orientation.2021publication context not individual capture or2026 condition.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':18170,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
