"""Validate color-only same-item update without modifying/deleting source geometry."""
from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as E,tempfile,shutil,subprocess,sys
import numpy as np,trimesh
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected='4b7f69e59b76e32cee16be3402f990cd72c9a429df253c8553f070549359b5dd'
s=trimesh.load(R/'model.stl',force='mesh',process=True);d=np.load(R/'color-mesh.npz');t=trimesh.Trimesh(d['vertices'],d['faces'],process=False)
def canonical(tri):
 return sorted(tuple(k for v in sorted(map(tuple,np.round(q,6)))for k in v)for q in tri)
with zipfile.ZipFile(R/'appearance.3mf') as z:e=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
v=np.array([[float(x.attrib[k])for k in ['x','y','z']]for x in e.findall('.//m:vertex',ns)]);f=np.array([[int(x.attrib[k])for k in ['v1','v2','v3']]for x in e.findall('.//m:triangle',ns)]);ma=np.array([int(x.attrib['p1'])for x in e.findall('.//m:triangle',ns)])
checks={'original_STL_bytes_unchanged':H(R/'model.stl')==expected,'18548_triangles_preserved':len(t.faces)==len(s.faces)==18548,'triangle_coordinates_unchanged':canonical(s.triangles)==canonical(t.triangles),'watertight':bool(t.is_watertight),'single_positive_volume':len(t.split())==1 and t.volume>0,'finite_and_nondegenerate':bool(np.isfinite(t.vertices).all() and (t.area_faces>0).all()),'two_materials_actually_assigned':len(np.unique(d['materials']))==2,'3MF_mm':e.attrib.get('unit')=='millimeter','3MF_vertices_same':bool(np.allclose(v,d['vertices'],atol=1e-7)),'3MF_faces_same':bool(np.array_equal(f,d['faces'])),'3MF_material_assignment_exact':bool(np.array_equal(ma,d['materials']))}
checks['3MF_object_identity']=e.find('.//m:object',ns).attrib.get('name')=='NKNU Pool Stand 1985 Design partial color'
# Retained isolated original build + color program reproduction, never TemporaryDirectory cleanup.
before={n:H(R/n)for n in ['build_model.py','colorize_model.py','model.stl','color-mesh.npz','appearance-materials.json']}
tmp=Path(tempfile.mkdtemp(prefix='nknu-pool-stand-1985-design-color-isolated-'))
for n in ['build_model.py','colorize_model.py']:shutil.copy2(R/n,tmp/n)
subprocess.run([sys.executable,str(tmp/'build_model.py')],check=True,capture_output=True)
subprocess.run([sys.executable,str(tmp/'colorize_model.py')],check=True,capture_output=True)
checks['isolated_original_STL_hash']=H(tmp/'model.stl')==expected
checks['isolated_color_mesh_hash']=H(tmp/'color-mesh.npz')==H(R/'color-mesh.npz')
checks['isolated_palette_assignment_hash']=H(tmp/'appearance-materials.json')==H(R/'appearance-materials.json')
checks['inputs_unchanged_during_QA']=before=={n:H(R/n)for n in before}
(R.parent/'PRIVATE-COLOR-REBUILD-LOCATION.json').write_text(json.dumps({'retained_directory':str(tmp)},indent=2))
checks={k:bool(v) for k,v in checks.items()}
q={'status':'PASS'if all(checks.values())else'FAIL','checks':checks,'color_mesh_sha256':H(R/'color-mesh.npz'),'original_STL_sha256':expected,'bounds_mm':t.bounds.tolist(),'retained_rebuild':'Isolated rebuild retained privately; no automatic file deletion.','limitations':['Color model uses original unrefined geometry; no new facade accuracy claim.','Two base-material labels are not a tested four-filament slicer project.','STL format itself does not contain color.']}
(R/'COLOR-FORMAT-GEOMETRY-QA.json').write_text(json.dumps(q,indent=2)+'\n');print(q);assert all(checks.values())
