from pathlib import Path
import tempfile,shutil,subprocess,sys,json,numpy as np,hashlib,struct
R=Path(__file__).resolve().parent;Q=R/'qa-continuous-walls';Q.mkdir(exist_ok=True)
baseline=R/'column-baseline-color-mesh.npz'
assert hashlib.sha256(baseline.read_bytes()).hexdigest()=='7d229ee6e7db1b2e158db787f95bd2177e7d7ea940cdd64cfbb60f839cff6ef0'
d=np.load(baseline);v=d['vertices'].copy();f=d['faces'].copy();before=d['materials'].copy();pal=json.load(open(R/'palette.json'))
raw=(R/'model.stl').read_bytes();assert hashlib.sha256(raw).hexdigest()=='ebecf2597fbc17fd0faf5a8bcd3ac13d1d9511d70a9600c5c09084ddbd26d879'
tri=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(4694)]).reshape(-1,3,3);assert np.array_equal(v[f],tri);assert np.bincount(before).tolist()==[16,4678]
report=json.load(open(R/'column-continuity-domains.json'));a=before.copy();selected=[];cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm=cross/np.linalg.norm(cross,axis=1)[:,None]
for g in report['groups']:
 off=tri[:,:,:2]-g['origin_xy'];u=np.array(g['tangent']);n=np.array(g['outward_xy']);along=off@u
 m=(abs(off@n)<1e-5).all(1)&(along>=-1e-5).all(1)&(along<=g['width']+1e-5).all(1)&(tri[:,:,2]>=3-1e-5).all(1)&(tri[:,:,2]<=31+1e-5).all(1)&(norm[:,:2]@n>.99999)
 ids=np.flatnonzero(m).tolist();assert ids==g['ids'];assert len(ids)==2;assert len(np.unique(tri[m].reshape(-1,3),axis=0))==4;assert abs(float(np.linalg.norm(cross[m],axis=1).sum()/2)-g['analytic_area'])<.0001
 assert (before[m]==1).all();a[m]=0;selected.extend(ids)
assert len(selected)==80;assert np.bincount(a).tolist()==[96,4598];assert np.array_equal(a[before==0],before[before==0]);assert np.flatnonzero(a!=before).tolist()==sorted(selected)
np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a)
assert json.load(open(R/'palette.json'))==pal
(Q/'selection.json').write_text(json.dumps(dict(changed_faces=80,face_ids=sorted(selected),existing_colored_faces_preserved=16,counts=[96,4598],original_triangle_geometry_and_order_exact=True,historical_appearance_untouched=True),indent=2)+'\n')
print('PASS original16gray preserved;80new wholecolumnskin triangles;4694geometry exact')
