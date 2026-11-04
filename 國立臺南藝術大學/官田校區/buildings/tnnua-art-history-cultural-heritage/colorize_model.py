"""Original independent brick relief, fin and box front rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='5013da67e9ac5fdccd6a8b742bf63e59251cfa85dc9015956babe2e8c2d1d8a0';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2498
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),2,np.int32);D={}
def rect(name,y,x0,x1,z0,z1,material):
 hit=(abs(t[:,:,1]-y).max(1)<e)&(t[:,:,0].min(1)>=x0-e)&(t[:,:,0].max(1)<=x1+e)&(t[:,:,2].min(1)>=z0-e)&(t[:,:,2].max(1)<=z1+e)
 ids=np.flatnonzero(hit);assert len(ids)==2,(name,len(ids));assert abs(m.area_faces[ids].sum()-(x1-x0)*(z1-z0))<.003;D[name]=ids.tolist();a[ids]=material
for z in range(24,62,3):
 for j in range(6):
  x=-60+j*4.2+(1 if z%2 else 0);rect(f'brick_{z}_{j}',-32.7,x-1.6,x+1.6,z,z+1.2,0)
for x in range(-22,25,5):rect(f'fin_{x}',-24.5,max(x-.8,-21.5),x+.8,51 if x>=18 else 45,65,1)
rect('right_box',-36.5,17,69,33,51,1)
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[156,22,2320]
pal=[('Observed coarse brick relief fronts muted brick red','#985747'),('Observed central fin and right box fronts offwhite','#D2D3CB'),('UNVERIFIED mixed walls bases proxies roof neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2498 original triangles unchanged','limits':['78coarse brickfront rectangles red,10finfronts and one rightboxfront offwhite; complete allvertices rectangles only.','Coarse relief pattern not faithful brick/perforated geometry; no new holes.','Fullheight left wall/backing/graybase/whiteframe mixed domains neutral.','All component sides/top/back, solid railproxy, windowbacks roof rear steps neutral.','Single PDFfigure29 builtphoto,2019report not capture, banner503 not accessed.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':2498,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
