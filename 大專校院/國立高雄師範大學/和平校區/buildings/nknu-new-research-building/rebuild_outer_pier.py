"""Blender4.3.2: --baseline DIR --out DIR. Only8 original right entrance pillar outer +X side faces material1->2.
Run after exact fixed-reference canopy6 plus white14 baseline; do not use an unrelated version.
Preserves original geometry and all other assignments. No source photograph input.
"""
from pathlib import Path
import bpy,sys,argparse,json,hashlib,zipfile,xml.etree.ElementTree as E
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.baseline=a.baseline.resolve();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=True)
IDS=[3929, 3930, 3931, 3937, 3938, 3939, 3940, 3944]
EXPECTED={'model.stl': '6eec5d4549ee730f13ae66273ea4cbb4ee4d11a942d8dc7686fb931fe534a373', 'color-mesh.npz': '742ee4c3d8ea33c094d65358cabc6f4624df91de11057b27fc509afdeb2fb2f2', 'scene.blend': '36579eaa11fe52b7091de6494fe63e7c0f346c5565d1c14f07002f1d1a382522', 'appearance.3mf': 'b4ea7bce40f1b8d8fdc6c55d5aba375109620fc5743161dbafcecebb27e41cf0'}
for name,sha in EXPECTED.items():assert hashlib.sha256((a.baseline/name).read_bytes()).hexdigest()==sha,name
raw=(a.baseline/'model.stl').read_bytes();t=np.frombuffer(raw,dtype=[('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')],offset=84)['v'];assert len(t)==8796
z=np.load(a.baseline/'color-mesh.npz');data={k:z[k].copy()for k in z.files};v=data['vertices'];f=data['faces'];old=data['materials'];assert np.array_equal(v[f],t);assert np.bincount(old).tolist()==[6,8776,14]
assert (old[IDS]==1).all();new=old.copy();new[IDS]=2;data['materials']=new;assert np.bincount(new).tolist()==[6,8768,22];np.savez_compressed(a.out/'color-mesh.npz',**data)
bpy.ops.wm.open_mainfile(filepath=str(a.baseline/'scene.blend'));o=bpy.data.objects['NKNU New Research Building partial color'];m=o.data
assert np.array_equal(np.array([x.co[:]for x in m.vertices])[np.array([x.vertices[:]for x in m.polygons])],t);assert [q.material_index for q in m.polygons]==old.tolist()
for i in IDS:m.polygons[i].material_index=2
if m.attributes.get('material_index'):assert [q.value for q in m.attributes['material_index'].data]==new.tolist()
changes={}
for key,value in {'source_mesh_sha256':hashlib.sha256((a.out/'color-mesh.npz').read_bytes()).hexdigest(),'scope':'Original6canopy and14white faces retained; eight right entrance pillar outer side faces 1 to 2 pale-family continuity inference; all8788otherfaces and geometry preserved'}.items():changes[key]={'before':o.get(key),'after':value};o[key]=value
# Preserve existing unused default material and its node tree across native saves.
retention=[]
for mat in bpy.data.materials:
 if mat.users==0 and not mat.use_fake_user:mat.use_fake_user=True;retention.append(mat.name)
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(a.out/'scene.blend'),compress=True)
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
with zipfile.ZipFile(a.baseline/'appearance.3mf')as q:payload={n:q.read(n)for n in q.namelist()}
r=E.fromstring(payload['3D/3dmodel.model']);ts=r.findall('.//m:triangle',ns);vv=np.array([[float(x.attrib[k])for k in 'xyz']for x in r.findall('.//m:vertex',ns)]);ff=np.array([[int(x.attrib[k])for k in ['v1','v2','v3']]for x in ts]);assert np.array_equal(vv.astype(np.float32)[ff],t.astype(np.float32));assert [int(x.attrib['p1'])for x in ts]==old.tolist()
for i in IDS:
 for key in ['p1','p2','p3']:
  if key in ts[i].attrib:assert ts[i].attrib[key]=='1';ts[i].set(key,'2')
# Explicit object default makes SDK native rewrite legal; every triangle has its own assignment.
obj=r.find('.//m:object',ns);old_default={k:obj.get(k)for k in ['pid','pindex']};obj.set('pid',ts[0].attrib['pid']);obj.set('pindex','1')
E.register_namespace('',ns['m']);payload['3D/3dmodel.model']=E.tostring(r,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(a.out/'appearance.3mf','w',zipfile.ZIP_DEFLATED)as q:
 for name,b in payload.items():info=zipfile.ZipInfo(name,(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;q.writestr(info,b)
(a.out/'outer-pier-change.json').write_text(json.dumps({'changed_faces':IDS,'old_material':1,'new_material':2,'preserved_faces':8788,'original_canopy6_and_white14_preserved':True,'counts':np.bincount(new).tolist(),'custom_property_updates':changes,'3mf_object_default_before':old_default,'3mf_object_default_after':{'pid':obj.get('pid'),'pindex':obj.get('pindex')},'datablock_retention':{'fake_user_enabled_only_for_original_orphans':retention},'geometry_unchanged':True,'scope':'Right entrance column outer +X whole original plane8faces,82.0400894737mm2;ground photograph visible narrow return plus same-identified-pier finish continuity inference. Modeled3.5mmdepth is nominal, not photo measurement. Original cuts and other geometry retained.'},indent=2)+'\n')
print('NKNU_OUTER_PIER_COMPLETE')
