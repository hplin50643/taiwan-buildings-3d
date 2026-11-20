"""Blender 4.3.2: start with original appearance/scene.blend; optional -- --qa-renders."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parent
d=json.loads((P/'domain.json').read_text());orig=Path(bpy.data.filepath)
assert hashlib.sha256(orig.read_bytes()).hexdigest()==d['original_appearance_blend_sha256']
s=bpy.context.scene; found=[o for o in s.objects if o.type=='MESH' and len(o.data.polygons)==7000];assert len(found)==1
o=found[0];match=[];t=d['target'];y0,y1=t['ys'];z0,z1=t['zs']
for p in o.data.polygons:
 v=[o.matrix_world@o.data.vertices[i].co for i in p.vertices]
 if all(q.x==t['x'] and y0<=q.y<=y1 and z0<=q.z<=z1 for q in v) and (v[1]-v[0]).cross(v[2]-v[0]).x>0:match.append(p.index)
assert match==d['ids']==[6993,6999]; assert len(o.data.materials)==6
assert [m.name for m in o.data.materials]==[m['id'] for m in d['unchanged_color_definitions']]
assert all(o.data.polygons[i].material_index==0 for i in match)
for i in match:o.data.polygons[i].material_index=3
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(P/'scene.blend'),compress=False,relative_remap=False)
if '--qa-renders' in sys.argv:
 # Use exactly the same model, camera and lighting per before/after diagnostic pair.
 cam=s.camera; cam.data.type='ORTHO'
 s.render.engine='BLENDER_WORKBENCH';w=s.display.shading
 w.color_type='MATERIAL';w.show_shadows=False;w.show_cavity=False;w.show_object_outline=False
 w.background_type='WORLD';s.world.color=(0.095,0.105,0.12)
 s.view_settings.view_transform='Standard';s.render.image_settings.file_format='PNG'
 s.render.film_transparent=False;s.render.use_stamp=False
 s.render.resolution_x=1100;s.render.resolution_y=800;s.render.resolution_percentage=100
 def trim(f):
  a=f.read_bytes();pre=b'\x89PNG\r\n\x1a\n';assert a[:len(pre)]==pre;j=len(pre);out=[pre]
  while j<len(a):
   n=int.from_bytes(a[j:j+4],'big');tag=a[j+4:j+8];end=j+n+12
   assert end<=len(a)
   if tag not in {b'tEXt',b'zTXt',b'iTXt',b'tIME',b'eXIf'}:out.append(a[j:end])
   j=end
  assert out[-1][4:8]==b'IEND'; f.write_bytes(b''.join(out))
 frames={}
 for phase,slot in [('before',0),('after',3)]:
  for i in match:o.data.polygons[i].material_index=slot
  for kind,pos,aim,scale in [('overview',(192,-170,133),(0,0,31),208),('eave-detail',(112,-23,106),(10.75,34,77.8),28)]:
   w.light='FLAT' if kind=='eave-detail' else 'STUDIO'
   cam.location=Vector(pos);cam.rotation_euler=(Vector(aim)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
   bpy.context.view_layer.update()
   ixs={k for i in match for k in o.data.polygons[i].vertices}
   coords=[world_to_camera_view(s,cam,o.matrix_world@o.data.vertices[k].co) for k in sorted(ixs)]
   box=[min(v.x for v in coords),max(v.x for v in coords),min(v.y for v in coords),max(v.y for v in coords)]
   assert 0<box[0]<box[1]<1 and 0<box[2]<box[3]<1,box
   if kind=='overview':
    allpts=[world_to_camera_view(s,cam,o.matrix_world@v.co) for v in o.data.vertices]
    assert all(0<v.x<1 and 0<v.y<1 for v in allpts)
   stem=f'{phase}-{kind}'
   frames[stem]={'target_projected_xy':box,'target_projected_vertices_xy':[[q.x,1-q.y] for q in coords],'camera_position':pos,'target':aim,'camera_ortho_scale':scale,'image_size':[1100,800]}
   file=P/(stem+'.png');s.render.filepath=str(file);bpy.ops.render.render(write_still=True);trim(file)
 (P/'framing-QA.json').write_text(json.dumps(frames,indent=2)+'\n')
