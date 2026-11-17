from pathlib import Path
import numpy as np,json,hashlib,struct
R=Path(__file__).resolve().parent;Q=R/'qa-continuous-walls';Q.mkdir(exist_ok=True);r=json.load(open(R/'cap-continuity-domains.json'));base=R/'cap-baseline-color-mesh.npz';assert hashlib.sha256(base.read_bytes()).hexdigest()==r['baseline']['mesh_sha256'];assert hashlib.sha256((R/'palette.json').read_bytes()).hexdigest()==r['baseline']['files']['palette.json']
d=np.load(base);v=d['vertices'];f=d['faces'];before=d['materials'];raw=(R/'model.stl').read_bytes();assert hashlib.sha256(raw).hexdigest()=='e5c014bb143e5c8682be55e3bfb4022121c06a6594ad28cfcfeb12f3cddd7153';tri=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(21916)]).reshape(-1,3,3);assert np.array_equal(v[f],tri);assert np.bincount(before).tolist()==[4,21912]
a=before.copy();cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm=cross/np.linalg.norm(cross,axis=1)[:,None];selected=[]
for g in r['candidate']['groups']:
 m=(abs(tri[:,:,0]-g['value'])<.00002).all(1)&(tri[:,:,1]>=-64-.00002).all(1)&(tri[:,:,1]<=-32+.00002).all(1)&(tri[:,:,2]>=95.5-.00002).all(1)&(tri[:,:,2]<=97.6+.00002).all(1)&(norm@np.array(g['outward_normal'])>.99999)
 ids=np.flatnonzero(m).tolist();assert ids==g['faces'];assert len(ids)==2;assert len(np.unique(tri[m].reshape(-1,3),axis=0))==4;assert abs(float(np.linalg.norm(cross[m],axis=1).sum()/2)-g['analytic_area_mm2'])<.0001;assert (before[ids]==1).all();a[ids]=0;selected+=ids
assert sorted(selected)==r['candidate']['faces'];assert np.bincount(a).tolist()==[12,21904];assert np.array_equal(a[before==0],before[before==0]);np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a)
(Q/'selection.json').write_text(json.dumps(dict(changed_faces=8,face_ids=sorted(selected),existing_colored_faces_preserved=4,counts=[12,21904],original_triangle_geometry_and_order_exact=True,finite_complete_rectangles=4),indent=2)+'\n')
