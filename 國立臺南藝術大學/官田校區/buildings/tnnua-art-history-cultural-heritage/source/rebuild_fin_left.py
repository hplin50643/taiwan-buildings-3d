EXPECTED={'palette.json': '9a745c98c51cfb66b5ca191c5695bd5d1e33702d0ada4282d770a77f91d0ce15', 'color-mesh.npz': 'ed46f1c248a0fb4576c2af486e899604e0c381297c9bb8f5d1bcf75e539dc2dd', 'appearance-materials.json': 'd08c272fd10db1363d4e664f94ff94dc2b98aeb3202b61806db7584ea0cc4131', 'README.md': '5f618d877c79e591c0d042d2c939452447b10b5ffb63451c767567eb96237ac1', 'model.stl': '5013da67e9ac5fdccd6a8b742bf63e59251cfa85dc9015956babe2e8c2d1d8a0', 'appearance.3mf': 'ce61383b030582a2bcb22fc1dc8bf899f3d3558723e468edc2d290e9e092a00d', 'scene.blend': '9c41b8a95fd960c511ddb7712c5175c2395c303ba81a184c641fa7ffeef8b2bc'}
from pathlib import Path
import bpy,sys,numpy as np,json,hashlib,zipfile,xml.etree.ElementTree as E,struct
REF='8f90ae2478f00cce6832a07de537f7d333f6dbc0';IDS=[564,568,570,571]
a=sys.argv[sys.argv.index('--')+1:];B=Path(a[0]).resolve();O=Path(a[1]).resolve();assert B!=O and B not in O.parents and O not in B.parents;O.mkdir(parents=True,exist_ok=True);H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,h in EXPECTED.items():assert H(B/n)==h,n
raw=(B/'model.stl').read_bytes();assert struct.unpack_from('<I',raw,80)[0]==2498 and len(raw)==84+2498*50
t=np.frombuffer(raw,dtype=[('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')],offset=84)['v'];d=np.load(B/'color-mesh.npz');v=d['vertices'];f=d['faces'];old=d['materials'];assert np.array_equal(v[f],t) and np.bincount(old).tolist()==[156,22,2320] and(old[IDS]==2).all();new=old.copy();new[IDS]=1
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
with zipfile.ZipFile(B/'appearance.3mf')as z:entries=[(i,z.read(i.filename))for i in z.infolist()]
x=E.fromstring(dict((i.filename,b)for i,b in entries)['3D/3dmodel.model']);vs=x.findall('.//m:vertex',ns);ts=x.findall('.//m:triangle',ns);xv=np.array([[float(e.get(k))for k in 'xyz']for e in vs]);xf=np.array([[int(e.get(k))for k in ['v1','v2','v3']]for e in ts]);assert np.array_equal(xf,f) and np.array_equal(xv.astype(np.float32),v.astype(np.float32)) and np.max(abs(xv-v))<5.1e-9;assert np.array_equal([int(e.get('p1'))for e in ts],old)
for i in IDS:
 assert ts[i].get('p1')=='2' and ts[i].get('p2')is None and ts[i].get('p3')is None;ts[i].set('p1','1')
obj=x.find('.//m:object',ns);assert 'pid'not in obj.attrib and 'pindex'not in obj.attrib;obj.set('pid','1');obj.set('pindex','2')
E.register_namespace('',ns['m']);xml=E.tostring(x,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(O/'appearance.3mf','w')as z:
 for i,b in entries:z.writestr(i,xml if i.filename=='3D/3dmodel.model'else b)
np.savez_compressed(O/'color-mesh.npz',vertices=v,faces=f,materials=new);(O/'palette.json').write_bytes((B/'palette.json').read_bytes())
q=json.loads((B/'appearance-materials.json').read_text());q['domain_face_indices']['single_central_fin_negative_x_return']=IDS
for i,e in enumerate(q['palette']):e['faces']=int((new==i).sum())
q['limits'].append('Four original centralfin negativeX side faces use existingoffwhitefamily; originalLprofile/upper0.5mmbackextension retained, notphotomeasured. OppositepositiveX/otherfins/walls unchanged.');(O/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n')
bpy.ops.wm.open_mainfile(filepath=str(B/'scene.blend'));bpy.context.preferences.filepaths.save_version=0;o=bpy.data.objects['TNNUA Art History Cultural Heritage partial color'];sv=np.array([list(a.co)for a in o.data.vertices]);sf=np.array([list(a.vertices)for a in o.data.polygons]);sm=np.array([a.material_index for a in o.data.polygons]);assert np.array_equal(sv[sf],t)and np.array_equal(sm,old)
orphans=[]
for m in bpy.data.materials:
 if m.users==0 and not m.use_fake_user:m.use_fake_user=True;orphans.append(m.name)
for i in IDS:o.data.polygons[i].material_index=1
o.data.update();o['source_mesh_sha256']=H(O/'color-mesh.npz');o['scope']='Original156brickred and22offwhite fronts retained;4whole negativeX centralfinside faces existingoffwhitefamily inferred;2316neutral;originalgeometry unchanged;notasbuilt/current'
bpy.ops.wm.save_as_mainfile(filepath=str(O/'scene.blend'),compress=True)
report={'status':'FOUR_ORIGINAL_FACES_ONLY','fixed_ref':REF,'ids':IDS,'from':2,'to':1,'counts_before':[156,22,2320],'counts_after':[156,26,2316],'other2494_unchanged':True,'geometry_and_order_exact':True,'XML_original_decimal_strings_preserved':True,'XML_changes':'four p1 values; added object pid1/pindex2 fallback for SDK editability; all triangles explicit p1, inherited p2/p3 unchanged','orphan_material_fake_user_enabled':orphans,'object_property_changes':['source_mesh_sha256','scope'],'no_other_scene_changes_allowed':True,'scope':'Nominal samefinwhitefamily;originalLprofile retained,notphotomeasured;positiveXside andotherfins/brick/box/walls/geometry unchanged'}
(O/'fin-left-change.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
