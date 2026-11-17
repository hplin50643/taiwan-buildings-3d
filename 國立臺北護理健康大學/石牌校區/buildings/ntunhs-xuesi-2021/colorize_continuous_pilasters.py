from pathlib import Path
import json,numpy as np,hashlib,struct
R=Path(__file__).resolve().parent;Q=R/'qa-continuous-pilasters';Q.mkdir(exist_ok=True)
r=json.load(open(R/'pilaster-continuity-domains.json'));base=R/'pilaster-baseline-color-mesh.npz';assert hashlib.sha256(base.read_bytes()).hexdigest()==r['baseline']['color-mesh.npz'];assert hashlib.sha256((R/'palette.json').read_bytes()).hexdigest()==r['baseline']['palette.json']
d=np.load(base);v=d['vertices'];f=d['faces'];before=d['materials'];raw=(R/'model.stl').read_bytes();assert hashlib.sha256(raw).hexdigest()==r['baseline']['model.stl'];tri=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(18170)]).reshape(-1,3,3);assert np.array_equal(v[f],tri);assert np.bincount(before).tolist()==[18,18136,16]
a=before.copy();cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm=cross/np.linalg.norm(cross,axis=1)[:,None];selected=[]
for g in r['domains']:
 m=(abs(tri[:,:,0]-g['x_plane'])<.0001).all(1)&(tri[:,:,1]>=-33.8-.0001).all(1)&(tri[:,:,1]<=-32.4+.0001).all(1)&(tri[:,:,2]>=11.5-.0001).all(1)&(tri[:,:,2]<=78.3+.0001).all(1)&(norm[:,0]*g['sign']>.99999);ids=np.flatnonzero(m).tolist();assert ids==g['face_ids'];assert g['whole_global_coplanar_component'];assert abs(float(np.linalg.norm(cross[m],axis=1).sum()/2)-g['analytic_area_mm2'])<.0003;assert all(before[ids]==1);a[ids]=2;selected+=ids
assert sorted(selected)==sorted(r['selected_face_ids']);assert np.bincount(a).tolist()==[18,17600,552];assert np.array_equal(a[before!=1],before[before!=1]);np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a)
(Q/'selection.json').write_text(json.dumps(dict(changed_faces=536,face_ids=sorted(selected),existing_colored_faces_preserved=34,counts=[18,17600,552],original_triangle_geometry_and_order_exact=True,finite_complete_notched_domains=14),indent=2)+'\n')
print('PASS536 finite pilaster side faces;18170 original triangles;34 prior colored faces preserved')
