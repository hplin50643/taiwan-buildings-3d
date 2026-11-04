"""Two complete original outer high-frame and adjoining end-panel planes."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='6efc4133d359b70fab35aaeec47dd77bf6dffe53e48b93e6aa7183facbd16879';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==27290
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
for name,y,count in [('short_outer',-34.75,23),('long_outer',34.75,31)]:
 ids=np.flatnonzero(np.abs(t[:,:,1]-y).max(1)<e)
 assert len(ids)==count
 D[name]=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[54,27236]
pal=[('NCUT Yanghao Dormitory observed complete outer upper frames offwhite','#D6D8D0'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'27290 original triangles unchanged','limits':['1240 broad frame candidates remain withdrawn. Only54 outer-plane faces are recommended, with top/bottom/interior faces excluded.', 'No partial z clipping, no glass recoloring, no red canopy extrapolation.', 'Whole outer rooftop domain whiteness is supported by opposing completed photographs but remains approximate photographic color family, not calibrated paint.', 'No geometry changes or original source-photo redistribution.', 'Original exported Y reflection already applied; do not reflect again.', 'Prior three-class preview is not a monochrome baseline; explicitly replaced with54 approved offwhite and27236unknown neutral.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':27290,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
