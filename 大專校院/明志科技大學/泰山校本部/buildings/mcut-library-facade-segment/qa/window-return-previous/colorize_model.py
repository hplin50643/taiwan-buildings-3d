"""4662 original triangles; three complete upper square window front rings only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='4f7d9eabeeb9d4626bc679405bb4996604a119a516417b56370d0079b7358aae';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==4662
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,1]+10.5),1)<1e-5
fields=[]
for cx in [-27,-5,17]:
 finite=whole&(t[:,:,0].min(1)>=cx-5.5-1e-5)&(t[:,:,0].max(1)<=cx+5.5+1e-5)&(t[:,:,2].min(1)>=113-1e-5)&(t[:,:,2].max(1)<=122+1e-5)
 assert finite.sum()==8
 fields.append(finite)
assert whole.sum()==40
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
pal=[('MCUT Library Facade Segment upper square window front rings medium gray','#878985'),('MCUT Library Facade Segment unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'three_upper_window_ring_whole_components':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==24
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'4662 original triangles unchanged; no cuts or newgeometry','limitations':['24 original triangles on three complete upper window front rings medium gray, not black.','Whole y=-10.5 plane40 triangles;24 ring triangles and16 unrelated balcony-end triangles neutral.','Window glass inner frames and reveals remain neutral; no shadow black treatment.','Mixed brick yellow walls, gold-lettered tower, balcony proxies, roof and rear neutral.','Source1 EXIF2011-07-24 metadata only; source0 captureunknown; not2026 condition.','Artificial68mm deep facade section only, not full library footprint; no tested filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':4662,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
