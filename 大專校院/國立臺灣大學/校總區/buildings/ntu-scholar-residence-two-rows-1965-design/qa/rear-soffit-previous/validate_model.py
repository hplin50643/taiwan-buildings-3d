from pathlib import Path
import numpy as np,trimesh,json,hashlib,zipfile,xml.etree.ElementTree as E
R=Path(__file__).resolve().parent;d=np.load(R/'mesh.npz');t=trimesh.Trimesh(d['vertices'],d['faces'],process=False);s=trimesh.load(R/'model.stl',force='mesh',process=True)
with zipfile.ZipFile(R/'model.3mf') as z:e=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
v=np.array([[float(a.attrib[k]) for k in ['x','y','z']] for a in e.findall('.//m:vertex',ns)]);f=np.array([[int(a.attrib[k]) for k in ['v1','v2','v3']] for a in e.findall('.//m:triangle',ns)])
checks={'npz_watertight':bool(t.is_watertight),'npz_two_independent_display_components':len(t.split())==2,'zero_area_free':bool((t.area_faces>0).all()),'STL_watertight':bool(s.is_watertight),'STL_two_independent_display_components':len(s.split())==2,'STL_bounds_match':bool(np.allclose(t.bounds,s.bounds,atol=1e-4)),'3MF_mm':e.attrib['unit']=='millimeter','3MF_vertices_match':bool(np.allclose(v,d['vertices'],atol=1e-7)),'3MF_faces_exact':bool(np.array_equal(f,d['faces']))}
checks['3MF_material_indices_exact']=bool(np.array_equal(np.array([int(a.attrib['p1']) for a in e.findall('.//m:triangle',ns)]),d['materials']))
checks['3MF_object_identity']=e.find('.//m:object',ns).attrib['name']=='NTU type-B scholar residences two historical rows'
checks['STL_face_count']=len(s.faces)==len(t.faces)
checks['positive_volume']=bool(all(c.volume>0 for c in t.split()) and all(c.volume>0 for c in s.split()))
checks['finite_vertices']=bool(np.isfinite(t.vertices).all())
checks['winding_consistent']=bool(t.is_winding_consistent and s.is_winding_consistent)
q={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'FORMAT-QA.json').write_text(json.dumps(q,indent=2));print(q);assert all(checks.values())
