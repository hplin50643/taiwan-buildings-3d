"""Blender4.3.2: --baseline DIR --out DIR. Only6 original negativeX columnside faces material2->1.
Run after exact fixed-reference8yellow156gray baseline; do not use an unrelated version.
Preserves original geometry and all other assignments. No source photograph input.
"""
from pathlib import Path
import bpy,sys,argparse,json,hashlib,zipfile,xml.etree.ElementTree as E
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.baseline=a.baseline.resolve();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=True)
IDS=[2547, 2548, 2549, 2556, 2557, 2558]
EXPECTED={'model.stl': '4cb5bfdbde4b9d544e6944dc1e6a9b72bafb310e6df4bace43f63c6ae0037d42', 'color-mesh.npz': '2b3658f38a3627e977244f4778233e45f2fd5e7a9c8319be475b5a772eaaf617', 'scene.blend': '6ea4f2d2ca7dddcba760f55658917ea07c1d8d2b77deacb20de57f59ed7297be', 'appearance.3mf': 'a7d9ab94d706a86f615807e026d8f65df26f971121386463ac3bf898edb5947f'}
for name,sha in EXPECTED.items():assert hashlib.sha256((a.baseline/name).read_bytes()).hexdigest()==sha,name
raw=(a.baseline/'model.stl').read_bytes();t=np.frombuffer(raw,dtype=[('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')],offset=84)['v'];assert len(t)==6488
z=np.load(a.baseline/'color-mesh.npz');data={k:z[k].copy()for k in z.files};v=data['vertices'];f=data['faces'];old=data['materials'];assert np.array_equal(v[f],t);assert np.bincount(old).tolist()==[8,156,6324]
assert (old[IDS]==2).all();new=old.copy();new[IDS]=1;data['materials']=new;assert np.bincount(new).tolist()==[8,162,6318];np.savez_compressed(a.out/'color-mesh.npz',**data)
bpy.ops.wm.open_mainfile(filepath=str(a.baseline/'scene.blend'));o=bpy.data.objects['NTUST International Plaza partial color'];m=o.data
assert np.array_equal(np.array([x.co[:]for x in m.vertices])[np.array([x.vertices[:]for x in m.polygons])],t);assert [q.material_index for q in m.polygons]==old.tolist()
for i in IDS:m.polygons[i].material_index=1
if m.attributes.get('material_index'):assert [q.value for q in m.attributes['material_index'].data]==new.tolist()
changes={}
for key,value in {'source_mesh_sha256':hashlib.sha256((a.out/'color-mesh.npz').read_bytes()).hexdigest(),'scope':'Original8yellow/156gray retained;6negativeX sidefaces on one topgallery middlecolumn nominal palegray same-finish inference;6318neutral;originalgeometryunchanged'}.items():changes[key]={'before':o.get(key),'after':value};o[key]=value
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
  if key in ts[i].attrib:assert ts[i].attrib[key]=='2';ts[i].set(key,'1')
# Explicit object default makes SDK native rewrite legal; every triangle has its own assignment.
obj=r.find('.//m:object',ns);old_default={k:obj.get(k)for k in ['pid','pindex']};obj.set('pid',ts[0].attrib['pid']);obj.set('pindex','2')
E.register_namespace('',ns['m']);payload['3D/3dmodel.model']=E.tostring(r,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(a.out/'appearance.3mf','w',zipfile.ZIP_DEFLATED)as q:
 for name,b in payload.items():info=zipfile.ZipInfo(name,(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;q.writestr(info,b)
(a.out/'column-side-change.json').write_text(json.dumps({'changed_faces':IDS,'old_material':2,'new_material':1,'preserved_faces':6482,'original_gray_faces_preserved':156,'original_yellow_faces_preserved':8,'neutral_remaining':6318,'custom_property_updates':changes,'3mf_object_default_before':old_default,'3mf_object_default_after':{'pid':obj.get('pid'),'pindex':obj.get('pindex')},'datablock_retention':{'fake_user_enabled_only_for_original_orphans':retention},'geometry_unchanged':True,'scope':'One topgallery middlecolumn negativeX full original side, pale finish continuity inference, not photo-measured full3.6mmdepth;2012source not2026condition.'},indent=2)+'\n')
print('PLAZA_SINGLE_COLUMN_COMPLETE')
