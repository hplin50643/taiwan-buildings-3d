"""3248 original triangles; two finite outer roof-edge fascia rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='0dee5572aad7ff5d8b7fa56d4463d71dbb8585d3b029c131b554e0533194fc41';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3248
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[]
for cx in [-63,-51,-39,-27,-15,-3,9,21,33,45,57,66]:
 q=t[:,:,:2]-[cx,30]
 for j in range(12):
  theta=2*np.pi*(j+.5)/24;n=np.array([np.cos(theta),np.sin(theta)]);v=np.array([-n[1],n[0]])
  fields.append((np.max(abs(q@n-1.1*np.cos(np.pi/24)),1)<1e-5)&(np.max(abs(q@v),1)<=1.1*np.sin(np.pi/24)+1e-5)&(t[:,:,2].min(1)>=3-1e-5)&(t[:,:,2].max(1)<=18.6+1e-5))
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
pal=[('Observed south column outward facets mediumgray','#858983'),('UNVERIFIED mixedbrickwalls entryframes glazing roofplanes neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'south_column_outward_facets':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==288
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3248 original triangles unchanged; no cuts or newgeometry','limitations':['All vertices on finite original24gon chord planes and tangent bounds;full originalheight3..18.6.','12 columns times12 outward facets times2 original triangles=288.','No normal or centroid shortcuts;horizontal roofs side returns neutral.','Mixedbasewalls longobscuredelevations windows bands neutral.','Captureunknown;2023documentdate notcamera date.','Two labels not testedfourfilament.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':3248,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
