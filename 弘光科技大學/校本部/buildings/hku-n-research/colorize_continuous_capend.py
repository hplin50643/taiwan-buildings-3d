from pathlib import Path
import json,numpy as np,hashlib,struct
R=Path(__file__).resolve().parent;Q=R/'qa-continuous-walls';Q.mkdir(exist_ok=True)
r=json.load(open(R/'capend-continuity-domains.json'));base=R/'capend-baseline-color-mesh.npz';assert hashlib.sha256(base.read_bytes()).hexdigest()==r['source_color_mesh_sha256'];assert hashlib.sha256((R/'palette.json').read_bytes()).hexdigest()==r['source_palette_sha256']
d=np.load(base);v=d['vertices'];f=d['faces'];before=d['materials'];raw=(R/'model.stl').read_bytes();assert hashlib.sha256(raw).hexdigest()==r['source_stl_sha256'];tri=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(7070)]).reshape(-1,3,3);assert np.array_equal(v[f],tri);assert np.bincount(before).tolist()==[14,7056]
a=before.copy();cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm=cross/np.linalg.norm(cross,axis=1)[:,None];selected=[]
for g in r['groups']:
 lo,hi=np.array(g['bounds']);m=(abs(tri[:,:,g['axis']]-g['value'])<.00002).all(1)&(tri>=lo-.00002).all((1,2))&(tri<=hi+.00002).all((1,2))&(norm[:,g['axis']]*g['normal_sign']>.99999);ids=np.flatnonzero(m).tolist();assert ids==g['ids']==g['complete_coplanar_component'];assert len(ids)==2;assert g['rectangle_corner_completeness'];assert abs(float(np.linalg.norm(cross[m],axis=1).sum()/2)-g['analytic_area_mm2'])<.0002;assert all(before[ids]==1);a[ids]=0;selected+=ids
assert sorted(selected)==r['face_ids'];assert np.bincount(a).tolist()==[16,7054];assert np.array_equal(a[before!=1],before[before!=1]);np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a)
(Q/'selection.json').write_text(json.dumps(dict(changed_faces=2,face_ids=sorted(selected),existing_colored_faces_preserved=14,counts=[16,7054],original_triangle_geometry_and_order_exact=True,finite_complete_rectangles=1),indent=2)+'\n')
print('PASS2finitecapend;7070originaltriangles;14priorgrayfacespreserved')
