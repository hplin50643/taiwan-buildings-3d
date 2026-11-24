"""Blender4.3.2 surface-only patch: -- BASELINE OUTPUT. No remesh."""
import bpy,sys,json,hashlib,zipfile,shutil
from pathlib import Path
import numpy as np
import xml.etree.ElementTree as ET
B,O=map(lambda x:Path(x).resolve(),sys.argv[sys.argv.index('--')+1:]);O.mkdir(parents=True,exist_ok=True)
LOCKS={'model.stl': 'eaffa5d6b5e359c5cb9a689a9da8fdd7c02ac2a3a1a7b0b11c536f38d3592854', 'scene.blend': '87fa3d352feaa092c111d7b7537c17784c1120fd7716022d9d7facb5225f52d7', 'color-mesh.npz': '4a3ea9fc38e6831e37f5fd1eca80e637ee55d5501b695555c464f99e61dcf12b', 'appearance.3mf': 'e96289ed9c9e463048d07c30b938088dbc6baedaf5a058c3db4b4018e40e428f', 'palette.json': '085a8a7c106cc92a78c486bc632d15feec571f6daa77b4fe3dbb2920945bdb06'}
IDS=[860,861,867,868,871]
for n,h in LOCKS.items():assert hashlib.sha256((B/n).read_bytes()).hexdigest()==h
z=np.load(B/'color-mesh.npz');v=z['vertices'];f=z['faces'];mi=z['materials'].copy();assert len(f)==1216 and np.all(mi[IDS]==1);mi[IDS]=0
np.savez_compressed(O/'color-mesh.npz',vertices=v,faces=f,materials=mi)
bpy.ops.wm.open_mainfile(filepath=str(B/'scene.blend'));o=bpy.data.objects['NTUE Audiovisual partial color'];m=o.data
assert np.array_equal(np.array([tuple(x.co)for x in m.vertices]),v) and np.array_equal(np.array([tuple(x.vertices)for x in m.polygons]),f)
assert np.array_equal(np.array([x.material_index for x in m.polygons]),z['materials']) and len(m.materials)==2
retained=[]
for x in bpy.data.materials:
 if x.users==0 and not x.use_fake_user:x.use_fake_user=True;retained.append(x.name)
for i in IDS:m.polygons[i].material_index=0
o['source_mesh_sha256']=hashlib.sha256((O/'color-mesh.npz').read_bytes()).hexdigest()
bpy.ops.wm.save_as_mainfile(filepath=str(O/'scene.blend'),compress=True,check_existing=False)
for n in ['model.stl','palette.json']:shutil.copyfile(B/n,O/n)
ns={'c':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'};ET.register_namespace('',ns['c'])
with zipfile.ZipFile(B/'appearance.3mf')as q:
 entries={n:q.read(n)for n in q.namelist()}
r=ET.fromstring(entries['3D/3dmodel.model']);obj=r.find('.//c:object',ns);obj.set('pid','1');obj.set('pindex','1');tri=r.findall('.//c:triangle',ns);assert len(tri)==1216
for i in IDS:
 assert tri[i].get('p1')=='1' and all(tri[i].get(k,'1')=='1' for k in ['p2','p3'])
 for k in ['p1','p2','p3']:
  if k in tri[i].attrib:tri[i].set(k,'0')
entries['3D/3dmodel.model']=ET.tostring(r,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(O/'appearance.3mf','w',zipfile.ZIP_DEFLATED)as q:
 for n,b in entries.items():
  info=zipfile.ZipInfo(n,(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;q.writestr(info,b)
change={'fixed_ref':'8f90ae2478f00cce6832a07de537f7d333f6dbc0','locks':LOCKS,'ids':IDS,'old':1,'new':0,'unchanged_faces':1211,'counts':np.bincount(mi).tolist(),'new_materials':0,'3mf_compatibility_metadata':'object pid=1 pindex=1 added for SDK writer; all triangle p1 explicit so no appearance change','retained_orphan_fake_user':retained,'changed_metadata':['source_mesh_sha256'],'domain':'Only corner pier +X complete original 5-face connected plane, x66.6 y[-44.6,-41.4] z[3,33], existing upper rear .1x1 Boolean join notch retained','source_limit':'Official exterior photo PDF31; date unknown; visible brick family extension over approximate model thickness, not measured color or current-condition certification'}
(O/'pier-return-change.json').write_text(json.dumps(change,ensure_ascii=False,indent=2)+'\n');print(change)
