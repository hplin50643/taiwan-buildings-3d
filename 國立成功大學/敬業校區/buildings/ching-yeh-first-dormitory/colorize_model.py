"""5896 original triangles; upper balcony slab frontfascias only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='c3f02fb6107bb3d9f0ab00b6661dcb2f0c6464bf38b33ebbbc05964d70fadfb3';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==5896
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
slabs=np.zeros(len(t),bool)
for zz in range(43,134,10):
 for xx in [-49,-29,29,49]:slabs|=plane(1,-49.5)&span(0,xx-9,xx+9)&span(2,zz-1.7,zz-.3)&(m.face_normals[:,1]<-.99)
a[slabs]=0;p=np.arange(len(a))
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
pal=[('Observed upper balcony slab outward fascias gray','#AAA9A2'),('UNVERIFIED walls windows balconyupstands roof neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'upper_balcony_slab_fronts':int((slabs&(a==0)).sum()),'whole_coplanar_withdrawals':len(removed)}
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'5896 original triangles unchanged; no cuts or addedgeometry','limitations':['Only ten uppertiers of four original slabfrontfascias.','Lowest three tiers vegetationobscured and neutral.','Upstands,windowbacks,mixed walls,rooftops,slabsides all neutral.','2024 albumpublication not capturedate.','Two material labels not tested filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':5896,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
