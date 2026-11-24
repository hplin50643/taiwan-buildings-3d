"""3962 original triangles; front bands/cap and entry steps preserved; four complete upperright return faces added."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='a3d5cc659830a56537d7b602bdd32f140c2581dbc703c0b9b1758efeafb0d47a';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3962
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
bands=np.zeros(len(a),bool);steps=bands.copy()
for z in [35,42,83]:bands|=plane(1,-15.5)&span(0,-69,69)&span(2,z,z+1.8)&(m.face_normals[:,1]<-.99)
cap=plane(1,-17.5)&span(0,-72,72)&span(2,90,92)&(m.face_normals[:,1]<-.99)
for i in range(16):
 y=-53+1.65*i;z=3+1.1*(i+1)
 steps|=span(0,-20,8)&span(1,y-.95,y+.95)&span(2,3,z)&((plane(2,z)&(m.face_normals[:,2]>.99))|(plane(1,y-.95)&(m.face_normals[:,1]<-.99)))
a[bands|cap|steps]=0;p=np.arange(len(a))
def root(i):
 while p[i]!=i:p[i]=p[p[i]];i=p[i]
 return i
for i,j in m.face_adjacency:
 if np.dot(m.face_normals[i],m.face_normals[j])>.999999:p[root(i)]=root(j)
g={}
for i in range(len(a)):g.setdefault(root(i),[]).append(i)
removed=[]
for ids in g.values():
 if len(set(a[ids]))>1:removed.extend(i for i in ids if a[i]==0);a[ids]=1
pal=[('Observed front bands capfascia and entry tread riser stone gray','#C4C0B2'),('UNVERIFIED mixed brickstone wall windowbacks sides roof neutral','#B8BAB5')]
original=a.copy();added=np.zeros(len(a),bool)
added|=plane(0,72)&span(1,-17.5,39.5)&span(2,90,92)&(m.face_normals[:,0]>.99)
added|=plane(0,70)&span(1,-14.5,36.5)&span(2,83,84.8)&(m.face_normals[:,0]>.99)
assert np.flatnonzero(added).tolist()==[2662,2666,3946,3952] and np.all(original[added]==1)
assert all(not added[c].any() or added[c].all() for c in g.values())
a[added]=0
assert (original==0).sum()==94 and (a==0).sum()==98 and np.array_equal(a[~added],original[~added])
assert all(len(set(a[c]))==1 for c in g.values())
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');domains={n:int((mask&(a==0)).sum())for n,mask in [('front_bands',bands),('cap_fascia',cap),('entry_treads_risers',steps)]};domains['whole_coplanar_withdrawals']=len(removed);domains['right_upper_returns']=int(added.sum())
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3962 original triangles unchanged; no cuts or addedgeometry','limitations':['Original front bands/cap/steps plus4 rightupper cap/belt faces; otherreturns and rooftops neutral.','Whole mixed brickstone walls/windowbacks/annexe/cheeks/landing neutral.','2010photo path not precise capture evidence.','Two material labels not tested filament slicing.']},indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':3962,'original_colored':94,'new_faces':4,'new_face_indices':np.flatnonzero(added).tolist(),'colored':98,'neutral':3864,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
