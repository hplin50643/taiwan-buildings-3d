"""5992 original triangles; two original balcony fronts plus bounded exposed undersides."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='a1811eb3ebc0fa47f8f2a0db1386fbb280d186fd9d8b1da614a2c40c6ef1b36e';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==5992
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,1]+52),1)<1e-5
fields=[];allfields=[]
for lo,hi,left in [(35,36.6,-63),(53,54.6,-63),(71,72.8,-64),(85,86.8,-64)]:
 finite=whole&(t[:,:,0].min(1)>=left-1e-5)&(t[:,:,0].max(1)<=41+1e-5)&(t[:,:,2].min(1)>=lo-1e-5)&(t[:,:,2].max(1)<=hi+1e-5)
 assert finite.sum()==2
 allfields.append(finite)
 if lo in [71,85]:fields.append(finite)
assert whole.sum()==8 and np.array_equal(whole,np.logical_or.reduce(allfields))
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
original=a.copy();assert (original==0).sum()==4
candidate=np.zeros(len(t),bool);by={}
for z in [71,85]:
 sel=(abs(t[:,:,2]-z).max(1)<.0001)&(m.face_normals[:,2]<-.99999)&(t[:,:,0].min(1)>=-64.0001)&(t[:,:,0].max(1)<=44.0001)&(t[:,:,1].min(1)>=-52.0001)&(t[:,:,1].max(1)<=-33.9999)
 assert sel.sum()==(4 if z==71 else 83)
 assert all(not sel[ids].any() or sel[ids].all() for ids in g.values())
 by[str(z)]=np.flatnonzero(sel).tolist();candidate|=sel
assert candidate.sum()==87 and np.all(original[candidate]==1)
a[candidate]=0;assert np.bincount(a).tolist()==[91,5901]
assert all(len(set(a[ids]))==1 for ids in g.values())
pal=[('MCUT Gymnasium upper balcony fronts and bounded soffits silver white','#D3D5D1'),('MCUT Gymnasium unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'two_upper_slab_front_whole_components':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==91
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'new_underside_face_indices':by,'original_colored_faces':4,'added_colored_faces':87,'colored_faces':91,'neutral_faces':5901,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'5992 original triangles unchanged; no cuts or newgeometry','limitations':['4 original front faces retained;87 original exposed underside faces added,91 silver-white total.','Whole y=-52 plane8 triangles in4 complete rectangles; only upper2 slab components selected.','Lower shades, railing proxy y=-51.8, glazing, logo and tower stay neutral.','Slab tops and side returns, curved roof and unknown rear remain neutral. Soffit seams and small light fixtures omitted in original geometry; uniform-family mapping not per-vertex measured colors.','Photograph capture dates unknown; page2023 update not capture or2026 condition.','Original main gym only, no adjacent blocks or tested filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':5992,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
