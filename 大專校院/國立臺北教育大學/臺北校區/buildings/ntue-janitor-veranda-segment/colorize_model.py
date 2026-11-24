"""Original four fronts plus first post lower gable-facing side."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='5911c359bf430b39188165357ecb05ff66d2a2b016b552a73edbbc1ba6ad0410';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==912
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
for name,ax,p,bounds,count in [('post_Y_front_-57', 1, -36.6, [(0, -66, -48), (2, 10.5, 43)], 18), ('post_Y_front_-19', 1, -36.6, [(0, -28, -10), (2, 10.5, 43)], 16), ('post_Y_front_19', 1, -36.6, [(0, 10, 28), (2, 10.5, 43)], 16), ('post_Y_front_57', 1, -36.6, [(0, 48, 66), (2, 10.5, 43)], 18)]:
 hit=abs(t[:,:,ax]-p).max(1)<e
 for k,lo,hi in bounds:hit &= (t[:,:,k].min(1)>=lo-e)&(t[:,:,k].max(1)<=hi+e)
 ids=np.flatnonzero(hit);assert len(ids)==count;D[name]=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[68,844]
pal=[('Observed narrow post and Y brace front aged off-white','#CFD0C7'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
original=a.copy()
added=(abs(t[:,:,0]+58.6).max(1)<e)&(t[:,:,1].min(1)>=-36.6-e)&(t[:,:,1].max(1)<=-33.4+e)&(t[:,:,2].min(1)>=10.5-e)&(t[:,:,2].max(1)<=36.423)
assert np.flatnonzero(added).tolist()==[578,581]
assert (original[added]==1).all()
a[added]=0
assert np.array_equal(a[~added],original[~added])
assert all(len(set(a[c]))==1 for c in cs)
D['first_post_gable_facing_lower_shaft']=np.flatnonzero(added).tolist()
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'912 original triangles unchanged','limits':['All gray masonry feet, including top surfaces.', 'All side/back post and brace faces except first post lower gable-facing side; cutoff and rear unchanged.', 'Entire front beam: older dark reddish fascia and later flaking pale paint, not a uniform color claim.', 'Red-brick wall mass crossing gray base without original material boundary.', 'Roof planes: moss is not green tile material, changing weathering is not a uniform material color.', 'Glazing/window backs, door reflections and interior views, floor and site base.', 'Only visible gable and selected three-bay/four-post veranda segment, not whole historic dormitory or full column count.', 'Does not include separate toilet building or auditorium.', 'Original cutoff, uncertain lengths, tree-hidden openings and omitted rear windows remain unchanged.', '2012 and 2024 reference periods are not one date; no 2026 current or restoration-completion claim.', 'Only exterior photos used; source originals remain private, never textures or public package imagery.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':912,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
