"""1988 original faces; front rail members/fascias, true front roof slope and stair faces only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;expected='d32018bb842d024c9add566535e7da54ec13e6468aa3ed0c17de1d9496771d33';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1988
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.full(len(t),2,np.int32)
def span(ax,l,h):return (lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
def box(x0,x1,y0,y1,z0,z1):return span(0,x0,x1)&span(1,y0,y1)&span(2,z0,z1)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
rails=np.zeros(len(t),bool);fascia=rails.copy();stairs=rails.copy()
for z in [7,28,49]:
 rails|=box(-66.5,66.5,-23,-21,z+2.1,z+7.6)
 fascia|=plane(1,-24)&box(-66.5,66.5,-24,-24,z,z+2.3)&(m.face_normals[:,1]<-.99)
for i in range(6):
 y=-35+1.7*i;z=3.7+.75*i;b=box(-46.5,-21.5,y-1,y+1,2.8,z)
 stairs|=b&((plane(2,z)&(m.face_normals[:,2]>.99))|(plane(1,y-1)&(m.face_normals[:,1]<-.99)))
roof=(np.max(abs(t[:,:,2]-(70.5+(t[:,:,1]+23.5)*4.8/25.705)),axis=1)<.003)&span(0,-71,71)&span(1,-23.5,2.205)&span(2,70.5,75.3)&(m.face_normals[:,2]>.9)&(m.face_normals[:,1]<-.1)
a[rails|fascia|stairs]=0;a[roof]=1
parent=np.arange(len(a))
def root(i):
 while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
 return i
for i,j in m.face_adjacency:
 if np.dot(m.face_normals[i],m.face_normals[j])>.999999:parent[root(i)]=root(j)
g={}
for i in range(len(a)):g.setdefault(root(i),[]).append(i)
removed=[]
for ids in g.values():
 if len(set(a[ids]))>1:removed.extend(i for i in ids if a[i]!=2);a[ids]=2
assert roof.sum()==44 and int((a==0).sum())>0
pal=[('Observed front rail slab fascia and stair stone gray','#C4C0B2'),('Observed pure FRONT upper roof slope muted green','#788572'),('UNVERIFIED piers mixed colored panels walls rear equipment neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1988 original triangles unchanged; no new or split faces','domains':{'rail_candidate_faces':int(rails.sum()),'rail_actual_gray_faces':int((rails&(a==0)).sum()),'fascia_actual_gray_faces':int((fascia&(a==0)).sum()),'stairs_actual_gray_faces':int((stairs&(a==0)).sum()),'front_upper_roof_green_faces':int((roof&(a==1)).sum()),'mixed_coplanar_candidate_withdrawals':len(removed)},'limitations':['Pure front roof upper plane only; ridge/side/back/underside neutral.','Walls have unseparated different-version color panels; piers fullheight mixed base and windows neutral.','Photo dates unknown;2023 form and2025 PDF edition not capture dates.','Three material labels not a verified multi-filament slicing job.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':1988,'original_STL_sha256':expected,'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()},indent=2));print(np.unique(a,return_counts=True));print('domains',[(n,int((s&(a!=2)).sum()))for n,s in [('rail',rails),('fascia',fascia),('stairs',stairs),('roof',roof)]],len(removed))
