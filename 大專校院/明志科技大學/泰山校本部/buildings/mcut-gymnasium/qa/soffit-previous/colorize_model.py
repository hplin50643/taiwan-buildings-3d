"""5992 original triangles; two complete upper balcony slab front rectangles only."""
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
pal=[('MCUT Gymnasium upper balcony slab fronts silver white','#D3D5D1'),('MCUT Gymnasium unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'two_upper_slab_front_whole_components':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==4
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'5992 original triangles unchanged; no cuts or newgeometry','limitations':['4 original triangles on two complete upper balcony slab-front rectangles silver white.','Whole y=-52 plane8 triangles in4 complete rectangles; only upper2 slab components selected.','Lower shades, railing proxy y=-51.8, glazing, logo and tower stay neutral.','Slab top underside returns, curved roof and unknown rear remain neutral.','Photograph capture dates unknown; page2023 update not capture or2026 condition.','Original main gym only, no adjacent blocks or tested filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':5992,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
