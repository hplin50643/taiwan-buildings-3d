from pathlib import Path
import hashlib,json,numpy as np,struct,zipfile,xml.etree.ElementTree as E
A=Path(__file__).resolve().parents[1];R=A.parent
b=(R/'model.stl').read_bytes();assert hashlib.sha256(b).hexdigest()=='d34b42ed9d423aae22e582488c4c17c94775d21cde894f4a03a4a905c20f11bb'
t=np.array([struct.unpack_from('<9f',b,96+50*i) for i in range(7252)]).reshape(-1,3,3)
import importlib.util
sp=importlib.util.spec_from_file_location('prior',A/'source/build_appearance.py');prior=importlib.util.module_from_spec(sp);sp.loader.exec_module(prior)
old={'face_material_indices':prior.classify(t)[0].tolist()};new=json.loads((A/'face-materials.json').read_text());o=np.array(old['face_material_indices']);n=np.array(new['face_material_indices']);changed=np.where(o!=n)[0].tolist();assert changed==[740,742,743,746,748,1682,1684,1685,1701,1704] and (o[changed]==0).all() and(n[changed]==2).all()
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
with zipfile.ZipFile(A/'auditorium-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
vs=np.array([[float(v.get(k)) for k in 'xyz'] for v in r.findall('.//m:vertex',ns)]);fs=r.findall('.//m:triangle',ns);tri=vs[[[int(f.get(k)) for k in ['v1','v2','v3']] for f in fs]];assert np.array_equal(t,tri)
assert [int(f.get('p1')) for f in fs]==n.tolist()
report={'passed':True,'source_sha256':hashlib.sha256(b).hexdigest(),'exact_triangle_coordinates_and_order_preserved':True,'triangle_count':len(t),'changed_faces':changed,'material_counts':np.bincount(n).tolist(),'all_other_7242_face_materials_preserved':True,'interpretation':'10 twin-tower cornice lateral faces use existing front stone by continuity inference; not independently photo-verified','geometry_modified':False,'physical_print_test':False}
(A/'qa/continuous-cornice-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
