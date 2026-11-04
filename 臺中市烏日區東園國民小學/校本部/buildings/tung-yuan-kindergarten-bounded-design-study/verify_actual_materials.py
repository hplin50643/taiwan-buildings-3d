import bpy,json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;O=P/'reference-nominal';r=json.load(open(P/'BUILD-RECORD.json'))['parts'];oldsha=hashlib.sha256((O/'scene.blend').read_bytes()).hexdigest();newsha=hashlib.sha256((P/'scene.blend').read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(O/'scene.blend'));old={};oldslots={}
for x in r:
 o=bpy.data.objects[x['id']];oldslots[x['id']]=[list(m.diffuse_color)for m in o.data.materials];old[x['id']]=[list(o.data.materials[f.material_index].diffuse_color)for f in o.data.polygons]
bpy.ops.wm.open_mainfile(filepath=str(P/'scene.blend'));rows=[];errors=[];platform=[]
for x in r:
 o=bpy.data.objects[x['id']];rgb=[list(o.data.materials[f.material_index].diffuse_color)for f in o.data.polygons];unchanged=x['sha256']==x.get('original_part_sha256');same=(rgb==old[x['id']])if unchanged else None
 if [list(m.diffuse_color)for m in o.data.materials]!=oldslots[x['id']]:errors.append(x['id']+' slot RGBA differs from original')
 if unchanged and not same:errors.append(x['id']+' original face colours differ')
 if x['id']=='PROXY_BOUNDED_2F_PLATFORM':
  for f,col in zip(o.data.polygons,rgb):
   top=all(abs(o.data.vertices[k].co.z-22.8)<2e-5 for k in f.vertices);expected=oldslots[x['id']][0 if top else 1];ok=col==expected
   platform.append({'face':f.index,'top':top,'material_name':o.data.materials[f.material_index].name,'actual_RGBA':col,'expected_role':'original platform top proxy'if top else'artificial neutral return/cut','pass':ok})
   if not ok:errors.append('platform '+str(f.index))
 if x['id'].startswith('SOURCE_NORMALIZED'):
  for f,col in zip(o.data.polygons,rgb):
   if 'F_GABLE'in x['id']:front=all(abs(o.data.vertices[k].co.y-174.91685393258427)<1e-5 for k in f.vertices)
   elif 'A_END'in x['id']:front=all(abs(o.data.vertices[k].co.y+1.5147540983606558)<1e-5 for k in f.vertices)
   else:
    sign=1 if x['id'].endswith('left')else-1;front=all(abs(76.2+sign*o.data.vertices[k].co.x-o.data.vertices[k].co.z)<1.5e-5 for k in f.vertices)
   if col!=oldslots[x['id']][0 if front else 1]:errors.append(x['id']+' face '+str(f.index)+' source/neutral mismatch')
 rows.append({'id':x['id'],'STL_unchanged':unchanged,'original_ordered_face_RGBA_exact':same,'actual_face_RGBA_sha256':hashlib.sha256(json.dumps(rgb,separators=(',',':')).encode()).hexdigest(),'material_slots':[{'name':m.name,'RGBA':list(m.diffuse_color)}for m in o.data.materials],'actual_assigned_RGBA_counts':{str(v):rgb.count(list(v))for v in list({tuple(v)for v in rgb})}})
assert oldsha==hashlib.sha256((O/'scene.blend').read_bytes()).hexdigest();assert newsha==hashlib.sha256((P/'scene.blend').read_bytes()).hexdigest()
(P/'ACTUAL-FACE-RGB-VERIFICATION-1303.json').write_text(json.dumps({'status':'PASS'if not errors else'FAIL','scene_sha256':newsha,'original_scene_sha256':oldsha,'readonly_no_save':True,'checks':rows,'platform_faces':platform,'errors':errors},indent=2)+'\n');print('material errors',errors,'unchanged',sum(x['STL_unchanged']for x in rows),'platform_faces',len(platform))
