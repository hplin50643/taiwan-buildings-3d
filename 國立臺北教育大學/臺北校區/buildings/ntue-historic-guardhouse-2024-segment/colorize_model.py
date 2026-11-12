"""Original lowest clapboard plus two bounded lower-sill adjacent front pieces."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='6d40b0ae68f5739412626889d5b14d3b0df23ad6e32b15fbea243726c24feed9';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1224
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
for name,ax,p,bounds,count in [('lowest_front_board',1,-49,[(0,5.5,64.5),(2,12,12.8)],2)]:
 hit=abs(t[:,:,ax]-p).max(1)<e
 for k,lo,hi in bounds:hit &= (t[:,:,k].min(1)>=lo-e)&(t[:,:,k].max(1)<=hi+e)
 ids=np.flatnonzero(hit);assert len(ids)==count;D[name]=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[2,1222]
pal=[('Observed lowest independent clapboard faded pale green','#A7B8A2'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
original=a.copy()
added=(abs(t[:,:,1]+49).max(1)<e)&(t[:,:,0].min(1)>=5.5-e)&(t[:,:,0].max(1)<=64.5+e)&(t[:,:,2].min(1)>=16-e)&(t[:,:,2].max(1)<=16.8+e)
assert np.flatnonzero(added).tolist()==[368,371,374,377]
assert (original[added]==1).all()
a[added]=0
assert np.array_equal(a[~added],original[~added])
assert all(len(set(a[c]))==1 for c in cs)
D['lower_sill_adjacent_board_fronts']=np.flatnonzero(added).tolist()
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1224 original triangles unchanged','limits':['Main continuous timber plane crossing weathered upper wood and lower green paint', 'All higher board faces except the two lower-sill adjacent front pieces, plus all returns, back and side cutoff surfaces', 'Left window coarse original subdivisions cross upper gray pane/aged trim and lower red frame; no blanket red', 'Roof, moss/weathering, gable infill/brackets/attic vent and added sheet-metal hood', 'Large window backing with omitted fine iron bars', 'Masonry plinth/vent backs, ground/base and all remaining faces', 'Model remains explicitly a2024-visible-image-derived segment. Article publication year does not independently verify photographic shutter date; no2026 repaired/current-condition claim. Plan approval is not construction completion.', 'Only projecting timber gabled bay and setback left wing. Rear35model-mm cutoff is an intentional approximation, not measured depth; no hidden rear rooms, full site or underground foundations. No19-address boundary wall/red gate/added perimeter canopy, and not134-address active university gate security space.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':1224,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
