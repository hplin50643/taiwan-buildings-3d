from pathlib import Path
import numpy as np,trimesh,json,hashlib,zipfile,xml.etree.ElementTree as E
R=Path(__file__).resolve().parent;d=np.load(R/'mesh.npz');v=d['vertices'];f=d['faces'];t=trimesh.Trimesh(v,f,process=False)
assert np.isfinite(v).all();assert t.is_watertight and t.is_winding_consistent;assert (t.area_faces>0).all();assert len(t.split(only_watertight=False))==1
s=trimesh.load(R/'model.stl',process=True);assert s.is_watertight and s.is_winding_consistent;assert len(s.faces)==len(f);assert np.allclose(s.bounds,t.bounds,atol=.00003)
with zipfile.ZipFile(R/'model.3mf') as z:
 assert z.testzip() is None;e=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'};o=e.find('.//m:object',ns);assert o.attrib['name']=='TMU activity center undated original design reconstruction';assert e.attrib['unit']=='millimeter'
v3=np.array([[float(a.attrib[k]) for k in ['x','y','z']] for a in e.findall('.//m:vertex',ns)]);f3=np.array([[int(a.attrib[k]) for k in ['v1','v2','v3']] for a in e.findall('.//m:triangle',ns)]);assert np.allclose(v3,v,atol=1e-8) and np.array_equal(f3,f)
r={'status':'PASS','mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest(),'triangles':len(f),'components':1,'mesh_watertight':True,'stl_float32_roundtrip':True,'stl_watertight':True,'3mf_identity_unit_mesh':True,'zero_area_faces':0,'min_triangle_area_mm2':float(t.area_faces.min()),'manufacturing':'No physical print test; zeroarea and connectivity are not a guarantee of all printer settings.'};(R/'FORMAT-QA.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
