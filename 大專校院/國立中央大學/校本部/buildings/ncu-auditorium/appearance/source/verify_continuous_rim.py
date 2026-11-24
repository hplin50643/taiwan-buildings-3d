from pathlib import Path
import hashlib,json,numpy as np,struct,zipfile,xml.etree.ElementTree as E
A=Path(__file__).resolve().parents[1];R=A.parent
b=(R/'model.stl').read_bytes();assert hashlib.sha256(b).hexdigest()=='50964d7b2b33cb1489a01b8b3198e272d1a1a03c2d537dd9c7fb4030053e9d4b'
t=np.array([struct.unpack_from('<9f',b,96+50*i) for i in range(9614)]).reshape(-1,3,3)
import importlib.util
sp=importlib.util.spec_from_file_location('prior',A/'source/build_current.py');prior=importlib.util.module_from_spec(sp);sp.loader.exec_module(prior)
old={'face_material_indices':prior.classify(t)[0].tolist()};new=json.loads((A/'face-materials.json').read_text());o=np.array(old['face_material_indices']);n=np.array(new['face_material_indices']);changed=np.where(o!=n)[0].tolist();assert len(changed)==58 and (o[changed]==0).all() and(n[changed]==4).all()
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
with zipfile.ZipFile(A/'ncu-auditorium-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
vs=np.array([[float(v.get(k)) for k in 'xyz'] for v in r.findall('.//m:vertex',ns)]);fs=r.findall('.//m:triangle',ns);tri=vs[[[int(f.get(k)) for k in ['v1','v2','v3']] for f in fs]];assert np.array_equal(t,tri)
assert [int(f.get('p1')) for f in fs]==n.tolist()
report={'passed':True,'source_sha256':hashlib.sha256(b).hexdigest(),'exact_triangle_coordinates_and_order_preserved':True,'triangle_count':len(t),'changed_faces':changed,'material_counts':np.bincount(n).tolist(),'all_other_9556_face_materials_preserved':True,'interpretation':'58 positive-y outer upper rim faces use same negative-y rim gray-white by continuity inference; not independent photographic evidence','geometry_modified':False,'physical_print_test':False}
(A/'qa/continuous-rim-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
