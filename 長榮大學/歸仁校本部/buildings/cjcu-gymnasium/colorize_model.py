"""4694 original triangles; original eight left-column faces plus eight bounded right-column faces."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='ebecf2597fbc17fd0faf5a8bcd3ac13d1d9511d70a9600c5c09084ddbd26d879';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==4694
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[]
for k in range(14,18):
 aa=2*np.pi*k/24;bb=2*np.pi*(k+1)/24
 A=np.array([-12+1.7*np.cos(aa),-49+1.7*np.sin(aa)]);B=np.array([-12+1.7*np.cos(bb),-49+1.7*np.sin(bb)])
 e=B-A;L=np.linalg.norm(e);u=e/L;n=np.array([-u[1],u[0]])
 off=t[:,:,:2]-A;whole=np.max(abs(off@n),axis=1)<1e-5;along=off@u
 finite=whole&np.all((along>=-1e-5)&(along<=L+1e-5)&(t[:,:,2]>=3-1e-5)&(t[:,:,2]<=31+1e-5),axis=1)
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
pal=[('CJCU Gymnasium visible left column facets light gray','#CBCBC5'),('CJCU Gymnasium unverified walls windows neutral','#B8BAB5')]
original=a.copy();added=np.zeros(len(a),bool)
for k in range(14,18):
 aa=2*np.pi*k/24;bb=2*np.pi*(k+1)/24
 A=np.array([12+1.7*np.cos(aa),-49+1.7*np.sin(aa)]);B=np.array([12+1.7*np.cos(bb),-49+1.7*np.sin(bb)])
 e=B-A;L=np.linalg.norm(e);u=e/L;n=np.array([-u[1],u[0]])
 off=t[:,:,:2]-A;along=off@u
 hit=(np.max(abs(off@n),axis=1)<1e-5)&np.all((along>=-1e-5)&(along<=L+1e-5)&(t[:,:,2]>=3-1e-5)&(t[:,:,2]<=31+1e-5),axis=1)
 assert hit.sum()==2;added|=hit
assert np.flatnonzero(added).tolist()==[694,697,698,699,718,719,721,722] and np.all(original[added]==1)
assert all(not added[c].any() or added[c].all() for c in g.values())
a[added]=0
assert (original==0).sum()==8 and (a==0).sum()==16 and np.array_equal(a[~added],original[~added])
assert all(len(set(a[c]))==1 for c in g.values())
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'four_complete_left_column_facets':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'right_column_added_faces':int(added.sum()),'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==16
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'4694 original triangles unchanged; no cuts or newgeometry','limitations':['Original8 left facets plus8 right front-left facet triangles; each four complete24gon facets.','Existing1206 roof-face neutral sheet-family display is historical arbitrary preview, not verified daylight color.','All other4678 triangles neutral, including unselected column facets, roof, mixed walls/glazing/steps/soffit.','Old appearance folder and original scene/renderer preserved unchanged; this is not a monochrome discovery or new building.','Capture date unknown; URL202404 not capture or2026 condition. No textures, geometry changes or tested filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_colored':8,'new_faces':8,'new_face_indices':np.flatnonzero(added).tolist(),'colored':16,'neutral':4678,'triangles':4694,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
