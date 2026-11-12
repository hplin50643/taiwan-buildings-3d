"""Validate unchanged geometry and declared full-facet tile-material extension.
Run with numpy and trimesh installed. --rebuild also rebuilds from untouched source
in a retained isolated directory, never deleting source or the existing build.
"""
from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as E,io,sys,tempfile,shutil,subprocess
import numpy as np,trimesh
R=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
STL_SHA='711cc5fe4d900955600e1fc5fea5930b3b1db1b7e12fc4cc3b35730c18d47206'
OLD_COLOR_SHA='66876da02c40bd7458c05e0e600d385dab3864bbebd6eba9635db66d90e78375'
d=np.load(R/'color-mesh.npz');c=np.load(R/'continuity-map.npz');pal=json.loads((R/'palette.json').read_text())
s=trimesh.load(R/'model.stl',force='mesh',process=True);t=trimesh.Trimesh(d['vertices'],d['faces'],process=False)
b=io.BytesIO();np.savez_compressed(b,vertices=d['vertices'],faces=d['faces'],materials=c['original_materials'])
changed=d['materials']!=c['original_materials']
checks={
 'original_STL_bytes_unchanged':H(R/'model.stl')==STL_SHA,
 'original_color_archive_reconstructs_exactly':hashlib.sha256(b.getvalue()).hexdigest()==OLD_COLOR_SHA,
 'original_vertex_coordinates_and_order':np.array_equal(s.vertices,d['vertices']),
 'original_faces_and_order':np.array_equal(s.faces,d['faces']),
 '29236_triangles_14620_vertices':len(t.faces)==29236 and len(t.vertices)==14620,
 'original_colored_faces_preserved':np.array_equal(d['materials'][c['original_materials']!=4],c['original_materials'][c['original_materials']!=4]),
 'only_neutral_to_existing_tile':np.all(c['original_materials'][changed]==4)and np.all(d['materials'][changed]==0),
 '13366_whole_faces_changed':int(changed.sum())==13366,
 'changed_faces_upward_slope':np.all(t.face_normals[changed,2]>.01),
 'no_new_horizontal_wall_caps_colored':np.all(t.face_normals[changed,2]<.999999),
 'excluded_horizontal_faces_stay_original_neutral':np.all(d['materials'][c['excluded_horizontal_face_ids']]==4)and np.all(c['original_materials'][c['excluded_horizontal_face_ids']]==4),
 'excluded_near_horizontal_faces_stay_original_neutral':np.all(d['materials'][c['excluded_near_horizontal_face_ids']]==4)and np.all(c['original_materials'][c['excluded_near_horizontal_face_ids']]==4),
 'material_map_exact':np.array_equal(c['materials'],d['materials']),
 'map_is_blank_on_unchanged':np.all(c['domain'][~changed]==''),
 'no_new_palette_colors':pal==[['Source-bounded front orange tile family','#AC6948'],['Observed front gray stone family','#93948C'],['Existing front eave dark underside','#4D4841'],['Original genuine aperture shadows','#424743'],['UNVERIFIED ornaments roof backs walls and base','#B8BAB6']],
 'watertight':t.is_watertight,
 'single_positive_volume':len(t.split())==1 and t.volume>0,
 'finite_nondegenerate':np.isfinite(t.vertices).all()and(t.area_faces>0).all(),
 'dimensions_preserved':np.array_equal(t.bounds,s.bounds),
}
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
with zipfile.ZipFile(R/'appearance.3mf')as z:e=E.fromstring(z.read('3D/3dmodel.model'));checks['3MF_archive_valid']=z.testzip()is None
v=np.array([[float(x.attrib[k])for k in ['x','y','z']]for x in e.findall('.//m:vertex',ns)]);f=np.array([[int(x.attrib[k])for k in ['v1','v2','v3']]for x in e.findall('.//m:triangle',ns)]);ma=np.array([int(x.attrib['p1'])for x in e.findall('.//m:triangle',ns)])
checks.update({'3MF_mm':e.attrib.get('unit')=='millimeter','3MF_vertices_same':np.allclose(v,d['vertices'],atol=1e-7,rtol=0),'3MF_faces_same':np.array_equal(f,d['faces']),'3MF_material_assignment_exact':np.array_equal(ma,d['materials']),'3MF_same_palette_names_RGBA':[(x.attrib['name'],x.attrib['displaycolor'])for x in e.findall('.//m:base',ns)]==[(n,col+'FF')for n,col in pal],'3MF_identity_transform':all('transform'not in x.attrib for x in e.findall('.//m:item',ns))})
rebuild_status='not_requested'
if '--rebuild'in sys.argv:
 tmp=Path(tempfile.mkdtemp(prefix='longshan-continuity-clean-'))
 for n in ['build_model.py','colorize_model.py','export_appearance.py']:shutil.copy2(R/n,tmp/n)
 for n in ['build_model.py','colorize_model.py','export_appearance.py']:subprocess.run([sys.executable,str(tmp/n)],check=True,capture_output=True)
 for n in ['model.stl','color-mesh.npz','palette.json','continuity-map.npz','appearance-materials.json']:checks['clean_rebuild_'+n]=H(tmp/n)==H(R/n)
 with zipfile.ZipFile(tmp/'appearance.3mf')as a,zipfile.ZipFile(R/'appearance.3mf')as b:checks['clean_rebuild_3MF_contents']=set(a.namelist())==set(b.namelist())and all(a.read(n)==b.read(n)for n in a.namelist())
 rebuild_status='performed_and_retained'
 (R.parent/'PRIVATE-REBUILD-LOCATION.json').write_text(json.dumps({'directory':str(tmp)},indent=2))
checks={k:bool(v)for k,v in checks.items()}
q={'status':'PASS'if all(checks.values())else'FAIL','checks':checks,'color_mesh_sha256':H(R/'color-mesh.npz'),'original_STL_sha256':STL_SHA,'bounds_mm':t.bounds.tolist(),'volume_mm3':t.volume,'changed_face_count':int(changed.sum()),'rebuild':rebuild_status,'limitations':['No fabricated polychrome ornament, wall, aperture or geometry.','Approximate tile continuity, not measured present-day full exterior.','No physical print or slicer test.']}
(R/'COLOR-FORMAT-GEOMETRY-QA.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2));assert all(checks.values())
