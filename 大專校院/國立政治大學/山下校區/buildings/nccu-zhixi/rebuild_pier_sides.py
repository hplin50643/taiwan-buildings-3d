"""Blender4.3.2: --baseline DIR --out DIR. Only4 original lower portal pier outer side faces material1->0.
Run after exact fixed-reference corrected-front baseline; do not use an unrelated version.
Preserves original geometry and all other assignments. No source photograph input.
"""
from pathlib import Path
import bpy,sys,argparse,json,hashlib,zipfile,xml.etree.ElementTree as E
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.baseline=a.baseline.resolve();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=True)
IDS=[508, 510, 524, 526]
EXPECTED={'model.stl': '8708e06528a5e6287650b16b1ca37473c3fe9941156243aab04bb27b1024f1b8', 'color-mesh.npz': '1812d37eba590b5c2e7a39276d7ff94d44153f98e50e1315ab2bdaead5a7b222', 'scene.blend': '533a8ff5c57f1eeccfd835571fdb4e79091538e311ad009dada2d202ee521d74', 'appearance.3mf': '6fc7c7604f81b40a7010387f63f78b682cb5d337a70481b75afb4f49f58ae4ae'}
for name,sha in EXPECTED.items():assert hashlib.sha256((a.baseline/name).read_bytes()).hexdigest()==sha,name
raw=(a.baseline/'model.stl').read_bytes();t=np.frombuffer(raw,dtype=[('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')],offset=84)['v'];assert len(t)==1026
z=np.load(a.baseline/'color-mesh.npz');data={k:z[k].copy()for k in z.files};v=data['vertices'];f=data['faces'];old=data['materials'];assert np.array_equal(v[f],t);assert np.bincount(old).tolist()==[491,169,44,116,150,56]
assert (old[IDS]==1).all();new=old.copy();new[IDS]=0;data['materials']=new;assert np.bincount(new).tolist()==[495,165,44,116,150,56];np.savez_compressed(a.out/'color-mesh.npz',**data)
bpy.ops.wm.open_mainfile(filepath=str(a.baseline/'scene.blend'));o=bpy.data.objects['NCCU Zhixi preserved original geometry colored appearance'];m=o.data
assert np.array_equal(np.array([x.co[:]for x in m.vertices])[np.array([x.vertices[:]for x in m.polygons])],t);assert [q.material_index for q in m.polygons]==old.tolist()
for i in IDS:m.polygons[i].material_index=0
if m.attributes.get('material_index'):assert [q.value for q in m.attributes['material_index'].data]==new.tolist()
changes={}
for key,value in {'source_mesh_sha256':hashlib.sha256((a.out/'color-mesh.npz').read_bytes()).hexdigest(),'scope':'Original four corrected pier fronts retained; four lower outer pier sides 1 to 0 gray-family continuity inference; all1022otherfaces and geometry preserved'}.items():changes[key]={'before':o.get(key),'after':value};o[key]=value
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
  if key in ts[i].attrib:assert ts[i].attrib[key]=='1';ts[i].set(key,'0')
# Explicit object default makes SDK native rewrite legal; every triangle has its own assignment.
obj=r.find('.//m:object',ns);old_default={k:obj.get(k)for k in ['pid','pindex']};obj.set('pid',ts[0].attrib['pid']);obj.set('pindex','4')
E.register_namespace('',ns['m']);payload['3D/3dmodel.model']=E.tostring(r,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(a.out/'appearance.3mf','w',zipfile.ZIP_DEFLATED)as q:
 for name,b in payload.items():info=zipfile.ZipInfo(name,(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;q.writestr(info,b)
(a.out/'pier-side-change.json').write_text(json.dumps({'changed_faces':IDS,'old_material':1,'new_material':0,'preserved_faces':1022,'original_corrected_fronts_preserved':[507,509,523,525],'counts':np.bincount(new).tolist(),'custom_property_updates':changes,'3mf_object_default_before':old_default,'3mf_object_default_after':{'pid':obj.get('pid'),'pindex':obj.get('pindex')},'datablock_retention':{'fake_user_enabled_only_for_original_orphans':retention},'geometry_unchanged':True,'scope':'Two lower structural portal pier outer sides,36mm2 total, same gray-family continuity inference. Exact modeled depth not directly measured from PDF554. No current-condition or physical-print claim.'},indent=2)+'\n')
print('ZHIXI_PIER_SIDES_COMPLETE')
