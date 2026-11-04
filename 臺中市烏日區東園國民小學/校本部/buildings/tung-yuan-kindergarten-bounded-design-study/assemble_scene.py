import bpy,bmesh,json,struct,hashlib,math
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent;O=P/'reference-nominal';bpy.ops.wm.open_mainfile(filepath=str(O/'scene.blend'));rows=json.loads((P/'BUILD-RECORD.json').read_text())['parts']
for r in rows:
 o=bpy.data.objects[r['id']];materials=list(o.data.materials);old=o.data;old_material_indices=[f.material_index for f in old.polygons];b=(P/r['file']).read_bytes();vs=[];fs=[];index={}
 for i in range(struct.unpack_from('<I',b,80)[0]):
  t=struct.unpack_from('<12fH',b,84+i*50)[3:12];f=[]
  for k in [0,3,6]:
   v=tuple(t[k:k+3])
   if v not in index:index[v]=len(vs);vs.append(v)
   f.append(index[v])
  fs.append(f)
 me=bpy.data.meshes.new(r['id']+'_FINITE_RELIEF');me.from_pydata(vs,[],fs);me.update();o.data=me
 for m in materials:me.materials.append(m)
 for f in me.polygons:
  if r['sha256']==r.get('original_part_sha256'):
   f.material_index=old_material_indices[f.index];continue
  front=True
  if r['id']=='SOURCE_NORMALIZED_F_GABLE':front=all(abs(vs[k][1]-174.91685393258427)<1e-5 for k in f.vertices)
  elif r['id']=='SOURCE_NORMALIZED_A_END':front=all(abs(vs[k][1]+1.5147540983606558)<1e-5 for k in f.vertices)
  elif 'SOURCE_NORMALIZED_ROOF_'in r['id']:
   sign=1 if r['id'].endswith('left')else-1;front=all(abs(76.2+sign*vs[k][0]-vs[k][2])<1.5e-5 for k in f.vertices)
  elif r['id']=='PROXY_BOUNDED_2F_PLATFORM':front=all(abs(vs[k][2]-22.8)<2e-5 for k in f.vertices)
  elif 'plane_axis'in r:
   axis='XYZ'.index(r['plane_axis']);front=all(abs(vs[k][axis]-r['plane_mm'])<2e-5 for k in f.vertices)
  f.material_index=0 if front else min(1,len(materials)-1)
 r.update(sha256=hashlib.sha256(b).hexdigest(),triangles=len(fs),bbox=[[min(v[k]for v in vs)for k in range(3)],[max(v[k]for v in vs)for k in range(3)]])
(P/'BUILD-RECORD.json').write_text(json.dumps({'status':'RELIEVED_PARTS_AWAITING_ASSEMBLY_QA_NO_PHYSICAL_FIT_CERTIFICATE','parts':rows},indent=2)+'\n')
sc=bpy.context.scene;cam=sc.camera
for name,loc,tar,scale in [('court-oblique',(270,-190,210),(0,90,35),265),('rear-oblique',(-270,300,210),(0,90,35),265),('top',(0,90,500),(0,90,35),250),('entry-end',(130,430,150),(0,100,35),250)]:
 cam.location=loc;cam.rotation_euler=(Vector(tar)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;sc.render.filepath=str(P/(name+'.png'));bpy.ops.render.render(write_still=True)
sc.render.filepath='//court-oblique.png';bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(P/'scene.blend'))
