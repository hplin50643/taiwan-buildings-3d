"""Blender4.3.2: -b -P this.py -- BASELINE OUTPUT. SHA-locked exact original2face material patch."""
from pathlib import Path
import bpy,sys,json,hashlib,zipfile,re,shutil
import numpy as np
B,O=map(lambda x:Path(x).resolve(),sys.argv[sys.argv.index('--')+1:]);O.mkdir(parents=True,exist_ok=True)
IDS=[672,677]
LOCKS={'palette.json': '47c49e3206b092ff98877910ee393e81d5a34a4534cc54efb871244a7215521b', 'nuuq1-appearance.3mf': '718b948951b8cc675ca59eaeff4c9c2dfe9d2b209cf2e8401221110a9bf2b747', 'model.stl': '4728cfad77601086a6b032a7d6da06535ba29e2134a37e0c9f3d322f3d0bac46', 'scene.blend': 'c14a4a6197893b260c50ec3c0d036fa07db3d453ca491776655f45ee71665f0b', 'face-materials.json': '0685ce1b7f5d2a6f10dc49b4f45a9e59efa0e9487f43d8d1b736f9c5750057a2'}
for n,h in LOCKS.items():assert hashlib.sha256((B/n).read_bytes()).hexdigest()==h,n
raw=(B/'model.stl').read_bytes();t=np.frombuffer(raw,dtype=[('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')],offset=84)['v'];fm=json.loads((B/'face-materials.json').read_text());old=np.array(fm['face_material_indices']);assert len(old)==4300 and (old[IDS]==0).all();new=old.copy();new[IDS]=2
bpy.ops.wm.open_mainfile(filepath=str(B/'scene.blend'));o=bpy.data.objects['NUU Q1 Arts Teaching Center appearance'];me=o.data;v=np.array([tuple(p.co)for p in me.vertices]);f=np.array([tuple(p.vertices)for p in me.polygons]);assert np.array_equal(v[f],t)and [p.material_index for p in me.polygons]==old.tolist() and len(me.materials)==8
for i in IDS:me.polygons[i].material_index=2
np.savez_compressed(O/'surface-colors.npz',vertices=v,faces=f,materials=new)
props={'side_color_scope':'Q1 uppermost right inner tower reveal only faces672/677 neutral0 to existing coolgray2; other4298 unchanged, including previous18top-inner-return faces. Original1.1mm depth and transverse bars are coarse geometry proxies, not measured depth or physical material joints. Exclude other4right bands, left/outer sides, glass and metal. Historical2025 selfreported photos, not2026 condition.','source_surface_colors_sha256':hashlib.sha256((O/'surface-colors.npz').read_bytes()).hexdigest()}
changes={}
for k,value in props.items():changes[k]={'before':o.get(k),'after':value};o[k]=value
orphan=[]
for m in bpy.data.materials:
 if m.users==0 and not m.use_fake_user:m.use_fake_user=True;orphan.append(m.name)
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(O/'scene.blend'),check_existing=False)
fm['face_material_indices']=new.tolist()
for i in IDS:fm['face_reasons'][i]='Q1_highest_right_inner_reveal_same_gray_family_complete_original_band_only'
(O/'face-materials.json').write_text(json.dumps(fm,indent=2)+'\n')
# Preserve entire original XML bytes and vertex strings except explicit targetmaterial attributes.
with zipfile.ZipFile(B/'nuuq1-appearance.3mf')as z:entries=[(i,z.read(i.filename))for i in z.infolist()]
changed=0
for j,(info,b) in enumerate(entries):
 if info.filename!='3D/3dmodel.model':continue
 matches=list(re.finditer(rb'<(?:\w+:)?triangle\b[^>]*/>',b));assert len(matches)==4300
 for idx in reversed(IDS):
  match=matches[idx];part=match.group()
  for key in [b'p1',b'p2',b'p3']:
   pattern=rb'\b'+key+rb'="0"';assert re.search(pattern,part);part=re.sub(pattern,key+b'="2"',part);changed+=1
  b=b[:match.start()]+part+b[match.end():]
 entries[j]=(info,b)
assert changed==6
with zipfile.ZipFile(O/'nuuq1-appearance.3mf','w')as z:
 for info,b in entries:z.writestr(info,b)
for n in ['model.stl','palette.json']:shutil.copyfile(B/n,O/n)
report={'fixed_ref':'8f90ae2478f00cce6832a07de537f7d333f6dbc0','locks':LOCKS,'faces':IDS,'old':0,'new':2,'unchanged_faces':4298,'counts':np.bincount(new,minlength=8).tolist(),'xml_modified_attributes':6,'xml_preserved_other_bytes_and_existing_object_fallback':True,'new_NPZ_exchange_from_saved_scene':True,'original8slots_and_node_values_preserved':True,'orphan_fake_user_false_to_true':orphan,'custom_properties':changes,'scope':'Complete original2face uppermost right inner reveal rectangle x1.5 normal-X; same-gray-family nominal extension, excluding all other reveal bands/glazing.'}
(O/'top-reveal-change.json').write_text(json.dumps(report,indent=2)+'\n');print('Q1_TOP_REVEAL_PATCH_COMPLETE')
