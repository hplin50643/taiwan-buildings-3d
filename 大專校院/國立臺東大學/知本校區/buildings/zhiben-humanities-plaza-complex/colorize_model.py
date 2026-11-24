"""4742 original triangles; two finite outer roof-edge fascia rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='a2766d109052b10610b3bbcfa20b27d854ac8b18bbc5521a27bfc857ec8c80e2';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==4742
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[]
for z in [29,38]:
 fields.append((np.max(abs(t[:,:,1]+42.5),1)<1e-5)&(t[:,:,0].min(1)>=55.9-1e-5)&(t[:,:,0].max(1)<=68.1+1e-5)&(t[:,:,2].min(1)>=z-1e-5)&(t[:,:,2].max(1)<=z+1.2+1e-5))
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
pal=[('Observed upper two landing fronts warmgray','#C0BDB1'),('UNVERIFIED mixedbrickwalls entryframes glazing roofplanes neutral','#B8BAB5')]
old=a.copy();extra=np.zeros(len(a),bool)
for z in [29,38]:extra|=plane(0,55.9)&span(1,-42.5,-41)&span(2,z,z+1.2)
assert np.flatnonzero(extra).tolist()==[4390,4391,4407,4408] and np.all(a[extra]==1)
assert all(not extra[ids].any() or extra[ids].all() for ids in g.values())
a[extra]=0
assert np.array_equal(a[~extra],old[~extra]) and np.bincount(a).tolist()==[8,4734]
assert all(len(set(a[ids]))==1 for ids in g.values())
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'top_two_complete_landing_fronts':int((rail&(a==0)).sum()),'added_upper_landing_left_returns':int(extra.sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==8
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'4742 original triangles unchanged; no cuts or newgeometry','limitations':['All vertices on complete frontplane y-42.5;two fullconnected landing components.','Two whole landingfront components times2 originaltriangles=4.','No normal or centroid shortcuts;only two exposed upper landing left returns additionally assigned; all other returns and horizontal roofs neutral.','Mixedbasewalls longobscuredelevations windows bands neutral.','Captureunknown;EXIF306 modificationdates notcapture.','Two labels not testedfourfilament.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':4742,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
