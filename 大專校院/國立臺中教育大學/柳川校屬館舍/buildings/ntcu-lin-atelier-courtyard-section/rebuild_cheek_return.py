"""Blender4.3.2 surface-only patch: -- BASELINE OUTPUT. No remesh."""
import bpy,sys,json,hashlib,zipfile,shutil
from pathlib import Path
import numpy as np
import xml.etree.ElementTree as ET
B,O=map(lambda x:Path(x).resolve(),sys.argv[sys.argv.index('--')+1:]);O.mkdir(parents=True,exist_ok=True)
LOCKS={'model.stl': '4f46d9cf812ce60da69dae3c9727c2d7911ca0b263ba4c0f7291558543031349', 'scene.blend': 'a00f650b4dba1cd9b1e9f19424f53c7af84a714ec2d58c4d1b7e333e7665e577', 'color-mesh.npz': '98fe8ab00db0e89d779ee8463c7c4724bc43a699858c1c5761df9a5e901bcd37', 'appearance.3mf': '503bdc79b3d5b3e8c7a8055d07f17db9130507516fb25d14baba9c5237648afe', 'palette.json': 'db7215199ecce848608e658afe7e0a2c405b355609fb6633ecbffea5dfa16e06'}
IDS=[2615, 2616, 2617, 2618, 2619, 2620, 2621, 2622, 2623, 2628, 2629, 2630, 2631, 2632, 2636, 2637, 2638, 2639, 2640, 2646, 2652, 2653, 2658, 2659, 2662, 2663]
for n,h in LOCKS.items():assert hashlib.sha256((B/n).read_bytes()).hexdigest()==h
raw=(B/'model.stl').read_bytes();rawtri=np.frombuffer(raw,offset=84,dtype=[('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')])['v']
z=np.load(B/'color-mesh.npz');v=z['vertices'];f=z['faces'];mi=z['materials'].copy();assert len(f)==5250 and np.all(mi[IDS]==1);assert np.array_equal(v[f],rawtri) and len(v)==2527;mi[IDS]=0
np.savez_compressed(O/'color-mesh.npz',vertices=v,faces=f,materials=mi)
bpy.ops.wm.open_mainfile(filepath=str(B/'scene.blend'));o=bpy.data.objects['NTCU Lin Atelier Courtyard Section partial color'];m=o.data
assert np.array_equal(np.array([tuple(x.co)for x in m.vertices]),v) and np.array_equal(np.array([tuple(x.vertices)for x in m.polygons]),f)
assert np.array_equal(np.array([x.material_index for x in m.polygons]),z['materials']) and len(m.materials)==2
retained=[]
for x in bpy.data.materials:
 if x.users==0 and not x.use_fake_user:x.use_fake_user=True;retained.append(x.name)
for i in IDS:m.polygons[i].material_index=0
o['side_color_scope']='Only left window door-facing outer jamb -X cheek26 original faces material1 to existingbrown0; existing48 frontfaces retained. Other5224faces unchanged. Original stepped weatherboard intersections retained; nominal brown family and approximate depth, not calibrated timber or current survey.'
o['source_mesh_sha256']=hashlib.sha256((O/'color-mesh.npz').read_bytes()).hexdigest()
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(O/'scene.blend'),compress=True,check_existing=False)
for n in ['model.stl','palette.json']:shutil.copyfile(B/n,O/n)
ns={'c':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'};ET.register_namespace('',ns['c'])
with zipfile.ZipFile(B/'appearance.3mf')as q:
 entries={n:q.read(n)for n in q.namelist()}
r=ET.fromstring(entries['3D/3dmodel.model']);obj=r.find('.//c:object',ns);obj.set('pid','1');obj.set('pindex','1');tri=r.findall('.//c:triangle',ns);assert len(tri)==5250
xmlv=np.array([[float(x.attrib[k])for k in ['x','y','z']]for x in r.findall('.//c:vertex',ns)]);xmlf=np.array([[int(x.attrib[k])for k in ['v1','v2','v3']]for x in tri]);xmlmat=np.array([int(x.attrib['p1'])for x in tri]);assert np.array_equal(xmlf,f)and np.allclose(xmlv,v,rtol=0,atol=5.1e-9)and np.array_equal(xmlmat,z['materials'])
for i in IDS:
 assert tri[i].get('p1')=='1' and all(tri[i].get(k,'1')=='1' for k in ['p2','p3'])
 for k in ['p1','p2','p3']:
  if k in tri[i].attrib:tri[i].set(k,'0')
entries['3D/3dmodel.model']=ET.tostring(r,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(O/'appearance.3mf','w',zipfile.ZIP_DEFLATED)as q:
 for n,b in entries.items():
  info=zipfile.ZipInfo(n,(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;q.writestr(info,b)
change={'fixed_ref':'8f90ae2478f00cce6832a07de537f7d333f6dbc0','locks':LOCKS,'ids':IDS,'old':1,'new':0,'unchanged_faces':5224,'counts':np.bincount(mi).tolist(),'new_materials':0,'3mf_compatibility_metadata':'object pid=1 pindex=1 added for SDK writer; all triangle p1 explicit so no appearance change','retained_orphan_fake_user':retained,'changed_metadata':['source_mesh_sha256','side_color_scope'],'domain':'Only door-facing left window -X complete original26face connected plane x-15.6 y[-9.3,-6.875] z[17.8,44.2], original weatherboard-intersection stepped boundary retained','source_limit':'Official courtyard VR original photo; capture unknown, post2015restoration context, not2025entrance or2026condition; finite brown frame family continuation, not measured depth/wood species/calibrated color'}
(O/'cheek-return-change.json').write_text(json.dumps(change,ensure_ascii=True,indent=2)+'\n');print(change)
