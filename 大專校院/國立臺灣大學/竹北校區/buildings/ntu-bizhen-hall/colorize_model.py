"""Existing clock-end stone planes and cap fascias, exported z already scaled .75."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='0f56c56c8d50798f67ea5fe1ac746030b14b979e62a0b4c0e094040c8b5d00de';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3576
t=m.triangles;n=m.face_normals;lo=t.min(1);hi=t.max(1);e=.003;a=np.full(len(t),1,np.int32)
pal=[('Observed clock-end outer stone and cap fascias muted warm gray','#B2B3AB'),('UNVERIFIED long walls windows clock roof rear neutral','#B8BAB5')]
def plane(k,v):return np.max(abs(t[:,:,k]-v),axis=1)<e
wall=plane(0,-70)&(n[:,0]<-.999)
front=plane(1,-25.5)&(n[:,1]<-.999)&(lo[:,2]>=63-e)&(hi[:,2]<=64.5+e)
back=plane(1,25.5)&(n[:,1]>.999)&(lo[:,2]>=63-e)&(hi[:,2]<=64.5+e)
a[wall|front|back]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999
cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);neutralized=[]
for c in cs:
 if len(set(a[c]))>1:neutralized+=c[a[c]!=1].tolist();a[c]=1
D={k:np.flatnonzero(v&(a==0)).tolist()for k,v in [('clock_end_outer_stone',wall),('front_cap_fascia',front),('reverse_cap_fascia',back)]};assert [len(v)for v in D.values()]==[78,2,2]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'coplanar_neutralized_faces':sorted(neutralized),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3576 original triangles unchanged','z_transform':'Original build applies .75 before export; all domain tests use actual exported coordinates.','limits':['Whole actual x-70 outer stone planes, no slot back or clock cylinder.','Both long cap fascias y+/-25.5 only, exported z63..64.5; not roof top.','Whole connected coplanar domains uniform.','Long walls, glazing, frame reflections, clock and opposite end neutral.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':3576,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],{k:len(v)for k,v in D.items()},'neutralized',len(neutralized),'components',len(cs))
