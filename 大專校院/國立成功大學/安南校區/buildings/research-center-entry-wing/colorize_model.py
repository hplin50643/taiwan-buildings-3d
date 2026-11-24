"""1384 original triangles; right upperframe front and entrycap frontfascia only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='fea1a92c55b182504134d309d882270267286093a782220c9a8f8170ce19bbe2';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1384
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
roofbox=plane(1,-20.5)&span(0,49.5,66.5)&span(2,24,53)&(m.face_normals[:,1]<-.99)
fascia=plane(1,-39)&span(0,-20,8)&span(2,24.6,26.7)&(m.face_normals[:,1]<-.99)
a[roofbox]=0;a[fascia]=0;p=np.arange(len(a))
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
pal=[('Observed rightupper frame and entrycap front muted stonegray','#C4C0B2'),('UNVERIFIED windowbacks main walls side roof neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');domains={'rightupper_framefront_gray':int((roofbox&(a==0)).sum()),'entrycap_frontfascia_gray':int((fascia&(a==0)).sum()),'whole_coplanar_withdrawals':len(removed)}
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1384 original triangles unchanged; no cuts or addedgeometry','limitations':['Right projecting upperframe front only; recessback/sides unknown.','All other main/entry walls neutral; no added signage.','Entrycap front vertical only; roof/underside neutral.','Architect view4 daytime exterior; image capturedate unknown.','Two material labels not tested filament slicing.']},indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':1384,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
