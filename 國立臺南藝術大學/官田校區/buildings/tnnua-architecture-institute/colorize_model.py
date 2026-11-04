"""Four whole original skylight beam underside rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='3f0c9a49c6e52921560417ba128f359260fa83346c351fcfe41fa7f8e16ceb88';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2350
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
for x in [-15,-5,5,15]:
 hit=(abs(t[:,:,2]-46.5).max(1)<e)&(t[:,:,0].min(1)>=x-.75-e)&(t[:,:,0].max(1)<=x+.75+e)&(t[:,:,1].min(1)>=-22-e)&(t[:,:,1].max(1)<=16+e)
 ids=np.flatnonzero(hit);assert len(ids)==2;assert abs(m.area_faces[ids].sum()-57)<.001;D[str(x)]=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[8,2342]
pal=[('Observed four skylight beam undersides nominal gray metal','#777D7E'),('UNVERIFIED roofs walls columns bridge proxies neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2350 original triangles unchanged','limits':['Only four whole original skylight beam bottom rectangles z46.5, xcenter+-0.75, y-22..16; all vertices tested, 57mm2 each.','Roof top and broad underside, beam sides/end/top, fullheight columns and bases neutral.','Photo orange open truss bridge does not map original solid parapet: neutral.','All walls window backs louvers stairs unknownneutral; photo dates unknown, no current-condition claim.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':2350,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
