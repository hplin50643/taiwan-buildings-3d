"""Blender4.3.2: -b -P this.py -- BASELINE OUTPUT. SHA-locked exact original4face material patch."""
from pathlib import Path
import bpy,sys,json,hashlib,zipfile,re,shutil
import numpy as np
B,O=map(lambda x:Path(x).resolve(),sys.argv[sys.argv.index('--')+1:]);O.mkdir(parents=True,exist_ok=True)
IDS=[5236,5242,5243,5247]
LOCKS={'model.stl': '1835376abf92fd7d961d43567fd4cf221e7478eba42176e4507cea165a7bab28', 'scene.blend': '35b0b4f7846888d15cfda62327503c8568517e4397510fa216b9e1c2c7fea0c0', 'nuulib-appearance.3mf': '057528c56758d395fe534db59b5b5930791acbdec8a30bba9580025c2d742f07', 'face-materials.json': 'ef66a8850276bae64541282f8d58050dcd8fb9f23d4c206f8bb091f1b2441260', 'palette.json': '1da8d4df506669f4f2461b74b19d55470d3bc916fc4c88605b3e1cfa6f823645'}
for n,h in LOCKS.items():assert hashlib.sha256((B/n).read_bytes()).hexdigest()==h,n
raw=(B/'model.stl').read_bytes();t=np.frombuffer(raw,dtype=[('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')],offset=84)['v'];fm=json.loads((B/'face-materials.json').read_text());old=np.array(fm['face_material_indices']);assert len(old)==16742 and (old[IDS]==1).all();new=old.copy();new[IDS]=5
bpy.ops.wm.open_mainfile(filepath=str(B/'scene.blend'));o=bpy.data.objects['NUU Guoding Library appearance'];me=o.data;v=np.array([tuple(p.co)for p in me.vertices]);f=np.array([tuple(p.vertices)for p in me.polygons]);assert np.array_equal(v[f],t)and [p.material_index for p in me.polygons]==old.tolist() and len(me.materials)==8
for i in IDS:me.polygons[i].material_index=5
np.savez_compressed(O/'surface-colors.npz',vertices=v,faces=f,materials=new)
props={'side_color_scope':'Single original entry integral mullion +X cheek four faces5236/5242/5243/5247 material1 to existing silver5; other16738 faces unchanged. Excludes coplanar canopy5233/5238. Historical2025 photo-family proxy, not precise physical post identification or .75mm depth survey.','source_surface_colors_sha256':hashlib.sha256((O/'surface-colors.npz').read_bytes()).hexdigest()}
changes={}
for k,value in props.items():changes[k]={'before':o.get(k),'after':value};o[k]=value
orphan=[]
for m in bpy.data.materials:
 if m.users==0 and not m.use_fake_user:m.use_fake_user=True;orphan.append(m.name)
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(O/'scene.blend'),check_existing=False)
fm['face_material_indices']=new.tolist()
for i in IDS:fm['face_reasons'][i]='single_integral_entry_mullion_complete_original_cheek_same_silver_family_not_canopy'
(O/'face-materials.json').write_text(json.dumps(fm,indent=2)+'\n')
# Preserve entire original XML bytes and vertex strings except explicit targetmaterial attributes.
with zipfile.ZipFile(B/'nuulib-appearance.3mf')as z:entries=[(i,z.read(i.filename))for i in z.infolist()]
changed=0
for j,(info,b) in enumerate(entries):
 if info.filename!='3D/3dmodel.model':continue
 matches=list(re.finditer(rb'<(?:\w+:)?triangle\b[^>]*/>',b));assert len(matches)==16742
 for idx in reversed(IDS):
  match=matches[idx];part=match.group()
  for key in [b'p1',b'p2',b'p3']:
   pattern=rb'\b'+key+rb'="1"';assert re.search(pattern,part);part=re.sub(pattern,key+b'="5"',part);changed+=1
  b=b[:match.start()]+part+b[match.end():]
 entries[j]=(info,b)
assert changed==12
with zipfile.ZipFile(O/'nuulib-appearance.3mf','w')as z:
 for info,b in entries:z.writestr(info,b)
for n in ['model.stl','palette.json']:shutil.copyfile(B/n,O/n)
report={'fixed_ref':'8f90ae2478f00cce6832a07de537f7d333f6dbc0','locks':LOCKS,'faces':IDS,'old':1,'new':5,'unchanged_faces':16738,'counts':np.bincount(new,minlength=8).tolist(),'xml_modified_attributes':12,'xml_preserved_other_bytes_and_existing_object_fallback':True,'new_NPZ_exchange_from_saved_scene':True,'original8slots_and_node_values_preserved':True,'orphan_fake_user_false_to_true':orphan,'custom_properties':changes,'scope':'Complete original4face rectangle along natural y=-37 frame/canopy edge, not entire6face maximal coplanar component; nominal existing silver family extension only.'}
(O/'mullion-return-change.json').write_text(json.dumps(report,indent=2)+'\n');print('MULLION_RETURN_PATCH_COMPLETE')
