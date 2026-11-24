"""Whole original right-end wall and independent front pier, all vertices finite domains."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='eaffa5d6b5e359c5cb9a689a9da8fdd7c02ac2a3a1a7b0b11c536f38d3592854';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1216
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
for name,ax,p,bounds,count in [('right_wall',0,68,[(1,-41.5,-6.5),(2,2.8,84.8)],8),('front_pier',1,-44.6,[(0,63.4,66.6),(2,3,33)],2)]:
 hit=abs(t[:,:,ax]-p).max(1)<e
 for k,lo,hi in bounds:hit &= (t[:,:,k].min(1)>=lo-e)&(t[:,:,k].max(1)<=hi+e)
 ids=np.flatnonzero(hit);assert len(ids)==count;D[name]=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[10,1206]
pal=[('Observed right wall and independent front pier muted brick','#A47258'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1216 original triangles unchanged','limits':['Only complete original right wall x68 and independent pier front y-44.6, all vertices finite bounds.','Main facade, unknown walls, window mixed backs, pale entrance soffits and roofs neutral.','Photo capture date unknown;2023form date not capture.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':1216,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
