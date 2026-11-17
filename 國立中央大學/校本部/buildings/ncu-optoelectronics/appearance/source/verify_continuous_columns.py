from pathlib import Path
import hashlib,json,numpy as np,struct,zipfile,xml.etree.ElementTree as E
A=Path(__file__).resolve().parents[1];R=A.parent
b=(R/'model.stl').read_bytes();assert hashlib.sha256(b).hexdigest()=='f8b49387d3e9237da92bb6c3b8d7ed89f931f412ddae9494de118acf6694c287'
t=np.array([struct.unpack_from('<9f',b,96+50*i) for i in range(4138)]).reshape(-1,3,3)
import importlib.util
sp=importlib.util.spec_from_file_location('prior',A/'source/build_current.py');prior=importlib.util.module_from_spec(sp);sp.loader.exec_module(prior)
old={'face_material_indices':prior.classify(t)[0].tolist()};new=json.loads((A/'face-materials.json').read_text());o=np.array(old['face_material_indices']);n=np.array(new['face_material_indices']);changed=np.where(o!=n)[0].tolist();assert len(changed)==18 and (o[changed]==0).all() and(n[changed]==3).all()
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
with zipfile.ZipFile(A/'ncu-optoelectronics-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
vs=np.array([[float(v.get(k)) for k in 'xyz'] for v in r.findall('.//m:vertex',ns)]);fs=r.findall('.//m:triangle',ns);tri=vs[[[int(f.get(k)) for k in ['v1','v2','v3']] for f in fs]];assert np.array_equal(t,tri)
assert [int(f.get('p1')) for f in fs]==n.tolist()
report={'passed':True,'source_sha256':hashlib.sha256(b).hexdigest(),'exact_triangle_coordinates_and_order_preserved':True,'triangle_count':len(t),'changed_faces':changed,'material_counts':np.bincount(n).tolist(),'all_other_4120_face_materials_preserved':True,'interpretation':'18 side/rear faces of same3 central columns use existing front pale gray by material-continuity inference; not verified rear-photo color','geometry_modified':False,'physical_print_test':False}
(A/'qa/continuous-columns-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
