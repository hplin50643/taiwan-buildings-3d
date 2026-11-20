"""Blender --background --python rebuild_blue_return.py -- --baseline DIR --out DIR.
SHA-locked original geometry; only two original material indices 0 to 1.
"""
from pathlib import Path
import bpy,sys,argparse,json,hashlib,zipfile,xml.etree.ElementTree as E
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.baseline=a.baseline.resolve();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=True)
IDS=[3825,3827]
EXPECTED={'model.stl': '228c0f4b8868f2a34c09f879d9beb6049528e1b4eaf59bbae3cda8ab226d3891', 'mesh.json': 'a93af1fe0c6f56a9f6c2aca9ec92eb3eda0539aa8b8052271e351db6faf89d67', 'model.3mf': '02b573f5f65f60038b26382e770e4bf4f41a8dcd22f168de65f6e186bee7c325', 'scene.blend': 'aa36fe8e048825f53fd547bbeb05789f1301d29de8034ef78e76ac5e21e5998c'}
for name,sha in EXPECTED.items():assert hashlib.sha256((a.baseline/name).read_bytes()).hexdigest()==sha,name
raw=(a.baseline/'model.stl').read_bytes();t=np.frombuffer(raw,dtype=[('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')],offset=84)['v'];assert len(t)==4760
m=json.loads((a.baseline/'mesh.json').read_text());v=np.array(m['vertices']);f=np.array(m['faces']);old=np.array(m['face_materials']);assert np.array_equal(v[f],t);assert np.all(old[IDS]==0);new=old.copy();new[IDS]=1;m['face_materials']=new.tolist();(a.out/'mesh.json').write_text(json.dumps(m,separators=(',',':')))
bpy.ops.wm.open_mainfile(filepath=str(a.baseline/'scene.blend'));o=bpy.data.objects['NTPU colored bay entry facade cut'];mesh=o.data
assert np.array_equal(np.array([x.co[:]for x in mesh.vertices])[np.array([x.vertices[:]for x in mesh.polygons])],t);assert [q.material_index for q in mesh.polygons]==old.tolist()
for i in IDS:mesh.polygons[i].material_index=1
if mesh.attributes.get('material_index'):assert [q.value for q in mesh.attributes['material_index'].data]==new.tolist()
changes={}
for key,value in {'source_color_mesh_sha256':hashlib.sha256((a.out/'mesh.json').read_bytes()).hexdigest(),'side_color_scope':'Only original faces3825/3827 0to1; entire x79 eight-face connected blue side-frame family, six original blue faces retained; photo-supported continuity inference, modeled depth not measured; other4758faces unchanged.'}.items():changes[key]={'before':o.get(key),'after':value};o[key]=value
retention=[]
for mat in bpy.data.materials:
 if mat.users==0 and not mat.use_fake_user:mat.use_fake_user=True;retention.append(mat.name)
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(a.out/'scene.blend'),compress=False)
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
with zipfile.ZipFile(a.baseline/'model.3mf')as q:payload={n:q.read(n)for n in q.namelist()}
r=E.fromstring(payload['3D/3dmodel.model']);ts=r.findall('.//m:triangle',ns);vv=np.array([[float(x.attrib[k])for k in 'xyz']for x in r.findall('.//m:vertex',ns)]);ff=np.array([[int(x.attrib[k])for k in ['v1','v2','v3']]for x in ts]);assert np.array_equal(vv.astype(np.float32)[ff],t);assert [int(x.attrib['p1'])for x in ts]==old.tolist()
for i in IDS:
 for key in ['p1','p2','p3']:
  if key in ts[i].attrib:assert ts[i].attrib[key]=='0';ts[i].set(key,'1')
# Existing explicit baseline object default retained without change.
obj=r.find('.//m:object',ns);default={k:obj.get(k)for k in ['pid','pindex']}
E.register_namespace('',ns['m']);payload['3D/3dmodel.model']=E.tostring(r,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(a.out/'model.3mf','w',zipfile.ZIP_DEFLATED)as q:
 for name,b in payload.items():info=zipfile.ZipInfo(name,(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;q.writestr(info,b)
(a.out/'model.stl').write_bytes(raw)
(a.out/'blue-return-change.json').write_text(json.dumps({'changed_faces':IDS,'old_material':0,'new_material':1,'preserved_faces':4758,'counts_before':np.bincount(old).tolist(),'counts_after':np.bincount(new).tolist(),'custom_property_updates':changes,'3mf_object_default_unchanged':default,'datablock_retention':retention,'geometry_unchanged':True,'scope':'The two faces are the3.75mm2 tail of maximal x79 eight-face connected69.5mm2 frame, NOT a separate rectangular component. Existing six blue facets preserved. Photo-visible blue upper return connects to rear vertical blue border; nominal depth is not photo-measured.'},indent=2)+'\n')
print('BLUE_RETURN_COMPLETE')
