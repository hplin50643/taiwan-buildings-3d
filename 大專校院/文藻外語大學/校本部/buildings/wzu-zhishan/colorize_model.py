"""Existing whole coplanar connected panes only; no cuts/new geometry."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='d7419f9bfbc65e746413bd49cb8fdd9f807c06ce6cff21bc265ddbe61f3f84f4';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==8394
t=m.triangles;lo=t.min(1);hi=t.max(1);n=m.face_normals;a=np.full(len(t),2,np.int32);e=.003
pal=[('Source-supported fully closed front crown panes muted cyan green','#659A96'),('Existing roof cross pale neutral metal','#CCD0CB'),('UNVERIFIED mixed wall curved glazing roof and rear neutral','#B8BAB5')]
# Build whole front coplanar connected components BEFORE any height/zone filtering.
mask=(np.max(abs(t[:,:,1]+18.5),axis=1)<e)&(n[:,1]<-.999);ad=m.face_adjacency;ad=ad[mask[ad].all(1)];cs=trimesh.graph.connected_components(ad,nodes=np.flatnonzero(mask),min_len=1)
components=[];panes=[]
for comp in cs:
 p=t[comp];l=p.min((0,1));h=p.max((0,1));eligible=False;domain=None
 for xa,xb in [(-29.55,-25.45),(-24.55,-20.45),(-19.55,-15.45),(15.45,19.55),(20.45,24.55),(25.45,29.55)]:
  for za,zb in [(128.9,132),(132.9,136),(136.9,140)]:
   if np.allclose(l,[xa,-18.5,za],atol=e) and np.allclose(h,[xb,-18.5,zb],atol=e) and abs(m.area_faces[comp].sum()-(xb-xa)*(zb-za))<.001:
    # Rectangle closure: boundary vertices only on its four existing groove borders.
    edges=m.faces[comp][:,[[0,1],[1,2],[2,0]]].reshape(-1,2);edges=np.sort(edges,axis=1);ed,cnt=np.unique(edges,axis=0,return_counts=True);boundary=ed[cnt==1];v=m.vertices[np.unique(boundary)]
    onedge=np.minimum.reduce([abs(v[:,0]-xa),abs(v[:,0]-xb),abs(v[:,2]-za),abs(v[:,2]-zb)])<e
    assert onedge.all();assert len(boundary)==4;eligible=True;domain=[xa,xb,za,zb]
 if eligible:a[comp]=0;panes.extend(comp.tolist())
 components.append({'faces':comp.tolist(),'bounds':[l.tolist(),h.tolist()],'area':float(m.area_faces[comp].sum()),'selected':eligible,'rectangular_domain':domain})
# Cross identity from two original boxes, axis-planar exposed faces only.
upright=(lo[:,0]>=-.75-e)&(hi[:,0]<=.75+e)&(lo[:,1]>=5.25-e)&(hi[:,1]<=6.75+e)&(lo[:,2]>=143.8-e)&(hi[:,2]<=150+e)
bar=(lo[:,0]>=-2.8-e)&(hi[:,0]<=2.8+e)&(lo[:,1]>=5.25-e)&(hi[:,1]<=6.75+e)&(lo[:,2]>=147.5-e)&(hi[:,2]<=149+e)
cross=(upright|bar)&(np.max(abs(n),axis=1)>.9999);a[cross]=1
assert len(panes)==24 and sum(x['selected']for x in components)==12;assert cross.sum()>0
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':{'closed_front_panes':sorted(panes),'cross':np.flatnonzero(cross).tolist()},'whole_front_coplanar_components':components,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'8394 original triangles unchanged','limits':['Only12 whole closed original rectangular crown components, not z-selected upperwall triangles.','All curvedbay/rings/motif/mainwalls neutral.','Cross only true existing exposed boxes, not roof planes.','Three material labels not verified four-filament job.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':8394,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'selected components',sum(x['selected']for x in components))
