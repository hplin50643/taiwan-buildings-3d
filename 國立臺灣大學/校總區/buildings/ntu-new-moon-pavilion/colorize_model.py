"""Actual original public ramp/landing/stair planes only; no wall cuts or geometry edits."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='1472feffd228eb1a85d964b8f6871afe766b5ce007132d55b12db1661dae319c';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==516
t=m.triangles;n=m.face_normals;lo=t.min(1);hi=t.max(1);e=.003;a=np.full(len(t),1,np.int32)
pal=[('Observed ramp landing and steps muted pale gray stone','#B7B9B2'),('UNVERIFIED hybrid main walls glazing rail canopy roof neutral','#B8BAB5')]
def plane(k,v):return np.max(abs(t[:,:,k]-v),axis=1)<e
def box(x0,x1,y0,y1,z0,z1):return(lo[:,0]>=x0-e)&(hi[:,0]<=x1+e)&(lo[:,1]>=y0-e)&(hi[:,1]<=y1+e)&(lo[:,2]>=z0-e)&(hi[:,2]<=z1+e)
height=2.8+(t[:,:,0]+60)*5/108
ramp=box(-60,48,-43,-33,2.8,7.8)&(((np.max(abs(t[:,:,2]-height),axis=1)<e)&(n[:,2]>.99))|(plane(1,-43)&(n[:,1]<-.999)&(np.max(t[:,:,2]-height,axis=1)<e)))
landing=box(42,54,-43.5,-30.5,3,8)&((plane(2,8)&(n[:,2]>.999))|(plane(1,-43.5)&(n[:,1]<-.999)))
stairs=np.zeros(len(t),bool)
for j in range(5):
 y=-44+1.4*j;top=3.5+.7*j
 stairs|=box(-54,-28,y-.85,y+.85,2.8,top)&((plane(2,top)&(n[:,2]>.999))|(plane(1,y-.85)&(n[:,1]<-.999)))
a[ramp|landing|stairs]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999
cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);neutralized=[]
for c in cs:
 if len(set(a[c]))>1:neutralized+=c[a[c]!=1].tolist();a[c]=1
D={k:np.flatnonzero(mask&(a==0)).tolist()for k,mask in [('ramp_true_slope_and_front',ramp),('landing_top_front',landing),('entry_treads_and_front_risers',stairs)]};assert all(len(x)>0 for x in D.values())
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'coplanar_neutralized_faces':sorted(neutralized),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'516 original triangles unchanged','limits':['Actual ramp upperplane equation and frontside profile only; not arbitrary bbox.','Landing and step original top/front faces only.','All connected coplanar domains uniform.','Entire mixed wall, opaque rail substitution, glazing and canopy remain neutral.','Pre/post renovation common form, not a single-day complete current appearance.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':516,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],{k:len(v)for k,v in D.items()},'neutralized',len(neutralized),'components',len(cs))
