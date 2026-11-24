"""Original1928 faces only; actual front rails/fascias and bounded stair faces."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='d2137a4bfd1e7b09874c6c1d54d40ee3b7dcf72ad49ed16c3c3d1a5faa6f056a';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1928
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
def box(x0,x1,y0,y1,z0,z1):return span(0,x0,x1)&span(1,y0,y1)&span(2,z0,z1)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
rails=np.zeros(len(a),bool);fascia=rails.copy();stairs=rails.copy();parapet=rails.copy()
for z in [3,24,45]:
 rails|=box(-57,67,-24,-22,z+2,z+7.3)
 fascia|=plane(1,-25)&box(-57,67,-25,-25,z,z+2.2)&(m.face_normals[:,1]<-.99)
for i in range(5):
 y=-36+2.2*i;z=3.25+.5*i
 stairs|=box(23,49,y-1.25,y+1.25,2.8,z)&((plane(2,z)&(m.face_normals[:,2]>.99))|(plane(1,y-1.25)&(m.face_normals[:,1]<-.99)))
for y0,z0,y1,z1 in [(-28,3,9,23.8),(9,24,-28,44.8),(-28,45,9,65.7)]:
 baseline=z0+(t[:,:,1]-y0)*(z1-z0)/(y1-y0);delta=t[:,:,2]-baseline
 parapet|=plane(0,-66)&span(1,-28,9)&(delta.min(1)>=2-.003)&(delta.max(1)<=6+.003)&(m.face_normals[:,0]<-.99)
a[rails|fascia|stairs|parapet]=0
p=np.arange(len(a))
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
pal=[('Observed front railing fascia and bounded stair gray','#C4C0B2'),('UNVERIFIED roof mixed walls piers windows rear neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={n:int((s&(a==0)).sum())for n,s in [('front_rails',rails),('front_fascia',fascia),('entry_stair',stairs),('left_outer_parapets',parapet)]};domains['whole_coplanar_withdrawals']=len(removed)
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'partial_color_incomplete':True,'fully_colored_exterior':False,'domains':domains,'geometry_policy':'1928 original triangles unchanged, no split or added face','limitations':['All roof planes neutral; green roofedge not whole roof evidence.','Mixed red/blue version panels and fullheight piers/windowbacks neutral.','Outer stair parapets only exact x-66 original sloped profiles; no added openings.','2023 form and2025 edition not photo capture dates.','Two labels not verified multi-filament slicing.']},indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':1928,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
