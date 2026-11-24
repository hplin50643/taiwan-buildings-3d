"""Blender4.3.2: --baseline DIR --out DIR. Only original1107/1110 material1->0.
Run after exact fixed-reference10frontface baseline; do not use an unrelated version.
Preserves original geometry and all other assignments. No source photograph input.
"""
from pathlib import Path
import bpy,sys,argparse,json,hashlib,zipfile,xml.etree.ElementTree as E
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.baseline=a.baseline.resolve();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=True)
IDS=[1107,1110]
EXPECTED={'color-mesh.npz': '7d66f900856b9d2590dafae7ddd32f16086649119254d87a06ecfcbf0fde4df1', 'model.stl': 'a14fa14bae7f2462d442f7f226862135b32781f7f6f032724ff31bb256a8c7cf', 'appearance.3mf': '0a56f6d6c6b56c3177deb0daa623f39fd41796e017d3502d71e78beaef8f19d6', 'scene.blend': '9f8e2a4738b1d71b26448b941f22a061a2666abc9562dc7fe8f0d5ffe4d7385d'}
for name,sha in EXPECTED.items():assert hashlib.sha256((a.baseline/name).read_bytes()).hexdigest()==sha,name
raw=(a.baseline/'model.stl').read_bytes();t=np.frombuffer(raw,dtype=[('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')],offset=84)['v'];assert len(t)==2992
z=np.load(a.baseline/'color-mesh.npz');data={k:z[k].copy()for k in z.files};v=data['vertices'];f=data['faces'];old=data['materials'];assert np.array_equal(v[f],t);assert np.bincount(old).tolist()==[10,2982]
mask=(abs(t[:,:,0]+65)<.0001).all(1);assert np.flatnonzero(mask).tolist()==IDS
for axis,lo,hi in [(1,-24.2,-22.2),(2,35.2,36.5)]:assert (t[mask,:,axis]>=lo-.0001).all() and (t[mask,:,axis]<=hi+.0001).all()
cr=np.cross(t[mask,1].astype(float)-t[mask,0],t[mask,2].astype(float)-t[mask,0]);assert (cr[:,0]<0).all();assert abs(np.linalg.norm(cr,axis=1).sum()/2-2.6)<.0002
assert old[IDS].tolist()==[1,1];new=old.copy();new[IDS]=0;data['materials']=new;assert np.bincount(new).tolist()==[12,2980];np.savez_compressed(a.out/'color-mesh.npz',**data)
bpy.ops.wm.open_mainfile(filepath=str(a.baseline/'scene.blend'));o=bpy.data.objects['Zhiben Science Engineering partial color'];m=o.data
assert np.array_equal(np.array([x.co[:]for x in m.vertices])[np.array([x.vertices[:]for x in m.polygons])],t);assert [q.material_index for q in m.polygons]==old.tolist()
for i in IDS:m.polygons[i].material_index=0
if m.attributes.get('material_index'):assert [q.value for q in m.attributes['material_index'].data]==new.tolist()
changes={}
for key,value in {'source_mesh_sha256':hashlib.sha256((a.out/'color-mesh.npz').read_bytes()).hexdigest(),'scope':'Original10framefrontfaces retained;2complete leftbeamendfaces nominaloffwhite inferredsamematerial;2980otherfacesneutral;originalgeometryunchanged'}.items():changes[key]={'before':o.get(key),'after':value};o[key]=value
# Preserve existing unused default material and its node tree across native saves.
assert all(m.users>0 for m in bpy.data.materials) # No orphan material in this baseline; no retention flag is changed.
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(a.out/'scene.blend'),compress=True)
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
with zipfile.ZipFile(a.baseline/'appearance.3mf')as q:payload={n:q.read(n)for n in q.namelist()}
r=E.fromstring(payload['3D/3dmodel.model']);ts=r.findall('.//m:triangle',ns);vv=np.array([[float(x.attrib[k])for k in 'xyz']for x in r.findall('.//m:vertex',ns)]);ff=np.array([[int(x.attrib[k])for k in ['v1','v2','v3']]for x in ts]);assert np.array_equal(vv.astype(np.float32)[ff],t.astype(np.float32));assert [int(x.attrib['p1'])for x in ts]==old.tolist()
for i in IDS:
 for key in ['p1','p2','p3']:
  if key in ts[i].attrib:assert ts[i].attrib[key]=='1';ts[i].set(key,'0')
# Explicit object default makes SDK native rewrite legal; every triangle has its own assignment.
obj=r.find('.//m:object',ns);old_default={k:obj.get(k)for k in ['pid','pindex']};obj.set('pid',ts[0].attrib['pid']);obj.set('pindex','1')
E.register_namespace('',ns['m']);payload['3D/3dmodel.model']=E.tostring(r,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(a.out/'appearance.3mf','w',zipfile.ZIP_DEFLATED)as q:
 for name,b in payload.items():info=zipfile.ZipInfo(name,(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;q.writestr(info,b)
(a.out/'beam-end-change.json').write_text(json.dumps({'changed_faces':IDS,'old_material':1,'new_material':0,'preserved_faces':2990,'original_white_faces_preserved':10,'neutral_remaining':2980,'custom_property_updates':changes,'3mf_object_default_before':old_default,'3mf_object_default_after':{'pid':obj.get('pid'),'pindex':obj.get('pindex')},'datablock_retention':'All original materials in use; no fake-user flags changed','geometry_unchanged':True,'scope':'Nominal same-beam material family on one whole left terminal rectangle, not photo-measured hidden depth or geometry certification.'},indent=2)+'\n')
print('TWO_FACE_REBUILD_COMPLETE')
