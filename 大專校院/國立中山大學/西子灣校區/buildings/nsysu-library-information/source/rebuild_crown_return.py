EXPECTED={'palette.json': '459d223edf366b9567b6dae0de11d51aa454bacd25d4741c1c1f17c7cf2cc5b5', 'color-mesh.npz': '0a61097133c46478259ff09e00a630b0e5ac2560a09e848e2b86c51adf556583', 'appearance-materials.json': '0c73d6157ed2f154fe74281b2e954bf0627d2cb8916f86a0ec2489e13a1bb5e9', 'README.md': 'bda9c8d300195fae09295ec59ff20f9885b5303d896078bfc3c6b734abe6fded', 'model.stl': '4fde918dd4060a88e5ed64b03e6a233e8e34d176306fd21f16cbd171e14acb35', 'appearance.3mf': 'b6861060d6878aabe7d7ebf650babd4520739708a9dd5039487bb7db3ae37986', 'scene.blend': '47c1585d808ee274fffe51886c72b4f01d5516b5615204bf21118ab1aa3a61e4'}
from pathlib import Path
import bpy,sys,numpy as np,json,hashlib,zipfile,xml.etree.ElementTree as E,struct
REF='8f90ae2478f00cce6832a07de537f7d333f6dbc0';IDS=[35934,35935,35936,35965]
a=sys.argv[sys.argv.index('--')+1:];B=Path(a[0]).resolve();O=Path(a[1]).resolve();assert B!=O and B not in O.parents and O not in B.parents;O.mkdir(parents=True,exist_ok=True);H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,h in EXPECTED.items():assert H(B/n)==h,n
raw=(B/'model.stl').read_bytes();assert struct.unpack_from('<I',raw,80)[0]==38898 and len(raw)==84+38898*50
t=np.frombuffer(raw,dtype=[('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')],offset=84)['v'];d=np.load(B/'color-mesh.npz');v=d['vertices'];f=d['faces'];old=d['materials'];assert np.array_equal(v[f],t) and np.bincount(old).tolist()==[507,38391] and(old[IDS]==1).all();new=old.copy();new[IDS]=0
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
with zipfile.ZipFile(B/'appearance.3mf')as z:entries=[(i,z.read(i.filename))for i in z.infolist()]
x=E.fromstring(dict((i.filename,b)for i,b in entries)['3D/3dmodel.model']);vs=x.findall('.//m:vertex',ns);ts=x.findall('.//m:triangle',ns);xv=np.array([[float(e.get(k))for k in 'xyz']for e in vs]);xf=np.array([[int(e.get(k))for k in ['v1','v2','v3']]for e in ts]);assert np.array_equal(xf,f) and np.array_equal(xv.astype(np.float32),v.astype(np.float32)) and np.max(abs(xv-v))<5.1e-9;assert np.array_equal([int(e.get('p1'))for e in ts],old)
for i in IDS:
 assert ts[i].get('p1')=='1' and ts[i].get('p2')is None and ts[i].get('p3')is None;ts[i].set('p1','0')
obj=x.find('.//m:object',ns);assert 'pid'not in obj.attrib and 'pindex'not in obj.attrib;obj.set('pid','1');obj.set('pindex','1')
E.register_namespace('',ns['m']);xml=E.tostring(x,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(O/'appearance.3mf','w')as z:
 for i,b in entries:z.writestr(i,xml if i.filename=='3D/3dmodel.model'else b)
np.savez_compressed(O/'color-mesh.npz',vertices=v,faces=f,materials=new);(O/'palette.json').write_bytes((B/'palette.json').read_bytes())
q=json.loads((B/'appearance-materials.json').read_text());q['domain_face_indices']['south_crown_left_outer_return']=IDS
for i,e in enumerate(q['palette']):e['faces']=int((new==i).sum())
q['limits'].append('Four original left crown return faces use same nominal brick family; six-edge original column-contact notch retained, not photo-resolved detail. All other triangles unchanged.');(O/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n')
bpy.ops.wm.open_mainfile(filepath=str(B/'scene.blend'));bpy.context.preferences.filepaths.save_version=0;o=bpy.data.objects['NSYSU Library Information v2 partial color'];sv=np.array([list(a.co)for a in o.data.vertices]);sf=np.array([list(a.vertices)for a in o.data.polygons]);sm=np.array([a.material_index for a in o.data.polygons]);assert np.array_equal(sv[sf],t)and np.array_equal(sm,old)
orphans=[]
for m in bpy.data.materials:
 if m.users==0 and not m.use_fake_user:m.use_fake_user=True;orphans.append(m.name)
for i in IDS:o.data.polygons[i].material_index=0
o.data.update();o['source_mesh_sha256']=H(O/'color-mesh.npz');o['scope']='Original507crown/columnfaces retained;4whole leftcrownreturnfaces samebrickfamily inferred;38387neutral;originalgeometry unchanged;notasbuilt/current'
bpy.ops.wm.save_as_mainfile(filepath=str(O/'scene.blend'),compress=True)
report={'status':'FOUR_ORIGINAL_FACES_ONLY','fixed_ref':REF,'ids':IDS,'from':1,'to':0,'counts_before':[507,38391],'counts_after':[511,38387],'other38894_unchanged':True,'geometry_and_order_exact':True,'XML_original_decimal_strings_preserved':True,'XML_changes':'four p1 values; added object pid1/pindex1 fallback for SDK editability; all triangles explicit p1, inherited p2/p3 unchanged','orphan_material_fake_user_enabled':orphans,'object_property_changes':['source_mesh_sha256','scope'],'no_other_scene_changes_allowed':True,'scope':'Nominal samebrickfamily;originalsixedgecolumncontactnotch retained,notphotomeasured;noothercrown/columns/underside/backwing/geometry changed'}
(O/'crown-return-change.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
