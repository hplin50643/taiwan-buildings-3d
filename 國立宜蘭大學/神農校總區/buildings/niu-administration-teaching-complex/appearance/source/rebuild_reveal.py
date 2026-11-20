EXPECTED={'palette.json': '1f438227ec777661adf9168dbb218f7167ddafcfec25362ed2ef8987d9761189', 'model.stl': 'd8f9925c97d2076d1aa4eec343b0fbf9aa6bb24ccfc9c32b52974394d5df2bdd', 'niu-administration-teaching-complex-appearance.3mf': '873cd8655e914a09842ba25d6455aa50c5302a57e03a832cc87e2cd73b346562', 'scene.blend': 'ceb2baf3e669eedb0c6f5fbdff45cdaa2c9aa1545a3a8ec0ca31b60ce7c93eaa', 'face-materials.json': 'fd366a0b03ad7151d0bdee44e7880101da96bee3e33dc857284273206369e490'}
from pathlib import Path
import bpy,sys,json,hashlib,zipfile,xml.etree.ElementTree as E,struct,numpy as np
REF='8f90ae2478f00cce6832a07de537f7d333f6dbc0'
args=sys.argv[sys.argv.index('--')+1:];B=Path(args[0]).resolve();O=Path(args[1]).resolve();O.mkdir(parents=True,exist_ok=True)
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name,sha in EXPECTED.items():assert H(B/name)==sha,name
raw=(B/'model.stl').read_bytes();n=struct.unpack_from('<I',raw,80)[0];assert n==6654 and len(raw)==84+n*50
t=np.frombuffer(raw,dtype=[('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')],offset=84)['v'].astype(float)
fmat=json.loads((B/'face-materials.json').read_text());old=np.array(fmat['face_material_indices']);assert np.bincount(old).tolist()==[6345,54,255];ids=[3979,3982];assert (old[ids]==0).all();new=old.copy();new[ids]=2
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'};fn='niu-administration-teaching-complex-appearance.3mf'
with zipfile.ZipFile(B/fn) as z:
 entries=[(i,z.read(i.filename))for i in z.infolist()]
root=E.fromstring(dict((i.filename,b)for i,b in entries)['3D/3dmodel.model']);v=np.array([[float(e.get(k))for k in 'xyz']for e in root.findall('m:resources/m:object/m:mesh/m:vertices/m:vertex',ns)]);ts=root.findall('m:resources/m:object/m:mesh/m:triangles/m:triangle',ns);f=np.array([[int(e.get(k))for k in ['v1','v2','v3']]for e in ts]);assert np.array_equal(v[f],t);assert np.array_equal([int(e.get('p1'))for e in ts],old)
for i in ids:
 for k in ['p1','p2','p3']:assert ts[i].get(k)=='0';ts[i].set(k,'2')
E.register_namespace('',ns['m']);xml=E.tostring(root,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(O/fn,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for info,data in entries:z.writestr(info,xml if info.filename=='3D/3dmodel.model'else data)
fmat['face_material_indices']=new.tolist()
for i in ids:fmat['face_reasons'][i]='complete_upper_leftmost_front_window_top_reveal_same_stone_family'
(O/'face-materials.json').write_text(json.dumps(fmat,indent=2)+'\n');(O/'palette.json').write_bytes((B/'palette.json').read_bytes())
bpy.ops.wm.open_mainfile(filepath=str(B/'scene.blend'));bpy.context.preferences.filepaths.save_version=0;o=bpy.data.objects['NIU Administration Teaching Complex limited appearance'];sv=np.array([list(x.co)for x in o.data.vertices]);sf=np.array([list(x.vertices)for x in o.data.polygons]);sm=np.array([x.material_index for x in o.data.polygons]);assert np.array_equal(sv[sf],t)and np.array_equal(sm,old)
orphans=[]
for m in bpy.data.materials:
 if m.users==0 and not m.use_fake_user:m.use_fake_user=True;orphans.append(m.name)
for i in ids:o.data.polygons[i].material_index=2
o.data.update();bpy.ops.wm.save_as_mainfile(filepath=str(O/'scene.blend'),compress=False)
r={'status':'TWO_FACES_ONLY','fixed_ref':REF,'source_STL_sha256':EXPECTED['model.stl'],'faces':ids,'old':0,'new':2,'counts_before':np.bincount(old).tolist(),'counts_after':np.bincount(new).tolist(),'other6652_unchanged':True,'geometry_and_native_face_order_exact':True,'palette_unchanged':True,'object_properties_unchanged':True,'orphan_materials_fake_user_enabled':orphans,'source_scope':'Same original modeled top reveal stone-family inference, uncalibrated unknown capture date; no geometry or pane modifications; no current-condition or printing claim.'}
(O/'reveal-change.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
