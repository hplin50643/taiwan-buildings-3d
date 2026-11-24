"""2940 original triangles; complete front and right cap rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='e907ae0be17200fc2391d9f17f942db0847b0e1ff6c6622eaec143ebee6390fe';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2940
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[]
for ax,value,other,l,h in [(1,-18.5,0,-69.5,69.5),(0,69.5,1,-18.5,28.5)]:
 whole=np.max(abs(t[:,:,ax]-value),1)<1e-5
 finite=whole&(t[:,:,other].min(1)>=l-1e-5)&(t[:,:,other].max(1)<=h+1e-5)&(t[:,:,2].min(1)>=71-1e-5)&(t[:,:,2].max(1)<=72.4+1e-5)
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
pal=[('VNU Renai RHB front right cap muted gray brown','#8F857B'),('VNU Renai RHB unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'front_right_cap_whole_components':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==4
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2940 original triangles unchanged; no cuts or newgeometry','limitations':['4 original front and right roofcap vertical triangles muted gray brown.','Each whole infinite plane equals finite rectangle all3vertices; no discarded fragments.','Lettered connected pier bands, banner wall, windows, trees and base remain neutral.','Roof top underside rear and left edge remain neutral.','Capture unknown, nominal uncalibrated family not2026 appearance.','Same original building and geometry; two labels not verified filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':2940,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
