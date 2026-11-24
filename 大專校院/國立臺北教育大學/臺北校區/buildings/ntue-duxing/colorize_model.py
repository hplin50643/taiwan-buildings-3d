"""Whole original outer left entry-frame return, all surviving Boolean fragments."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='8f9f2dd522f47de6caadd109b304f9abe71ada41a577919fbbcf14d800cc3e4a';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2534
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
for name,ax,p,bounds,count in [('outer_left_return',0,24,[(1,-63,-51),(2,3,40)],14)]:
 hit=abs(t[:,:,ax]-p).max(1)<e
 for k,lo,hi in bounds:hit &= (t[:,:,k].min(1)>=lo-e)&(t[:,:,k].max(1)<=hi+e)
 ids=np.flatnonzero(hit);assert len(ids)==count;D[name]=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[14,2520]
pal=[('Observed entrance outer left return nominal medium gray','#818683'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2534 original triangles unchanged','limits':['Only complete surviving original entry outer left return x24 y-63..-51 z3..40.','Main facade, unknown walls, window mixed backs, pale entrance soffits and roofs neutral.','Photo capture date unknown;2023form date not capture.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':2534,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
