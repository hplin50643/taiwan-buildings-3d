"""Blender 4.3.2: open the checksum-bound appearance/scene.blend first."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parent
d=json.loads((P/'domain.json').read_text());orig=Path(bpy.data.filepath)
assert hashlib.sha256(orig.read_bytes()).hexdigest()==d['original_appearance_blend_sha256']
s=bpy.context.scene;m=[o for o in s.objects if o.type=='MESH' and len(o.data.polygons)==8560];assert len(m)==1
o=m[0];ids=[]
for p in o.data.polygons:
 v=[o.matrix_world@o.data.vertices[i].co for i in p.vertices]
 if all(q.y==19 for q in v) and (v[1]-v[0]).cross(v[2]-v[0]).y>0:ids.append(p.index)
assert ids==d['ids']==[1420,1468]
assert len(o.data.materials)==3 and [x.name for x in o.data.materials]==[x['id']for x in d['unchanged_color_definitions']]
assert all(o.data.polygons[i].material_index==0 for i in ids)
def srgb_byte_to_linear(n):
 return n/12.92 if n<=0.04045 else ((n+0.055)/1.055)**2.4
a=d['new_material'];assert bpy.data.materials.get(a['id']) is None
m=bpy.data.materials.new(a['id']);m.use_nodes=True
c=tuple(srgb_byte_to_linear(int(a['srgb'][i:i+2],16)/255)for i in (1,3,5))+(1.0,)
m.diffuse_color=c
bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=c;bs.inputs['Roughness'].default_value=.85
o.data.materials.append(m)
for i in ids:o.data.polygons[i].material_index=3
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(P/'scene.blend'),compress=False,relative_remap=False)
if '--qa-renders' in sys.argv:
 # Diagnostic rerender settings are never saved to the model scene.
 cam=s.camera;cam.data.type='ORTHO'
 s.render.engine='BLENDER_WORKBENCH';w=s.display.shading
 w.light='FLAT';w.color_type='MATERIAL';w.show_shadows=False;w.show_cavity=False;w.show_object_outline=False
 w.background_type='WORLD';s.world.color=(0.095,0.105,0.12)
 s.view_settings.view_transform='Standard';s.render.image_settings.file_format='PNG'
 s.render.film_transparent=False;s.render.use_stamp=False
 s.render.resolution_x=1180;s.render.resolution_y=224;s.render.resolution_percentage=100
 def trim(f):
  a=f.read_bytes();pre=b'\x89PNG\r\n\x1a\n';assert a[:len(pre)]==pre;j=len(pre);out=[pre]
  while j<len(a):
   n=int.from_bytes(a[j:j+4],'big');tag=a[j+4:j+8];end=j+n+12
   assert end<=len(a)
   if tag not in {b'tEXt',b'zTXt',b'iTXt',b'tIME',b'eXIf'}:out.append(a[j:end])
   j=end
  assert out[-1][4:8]==b'IEND'; f.write_bytes(b''.join(out))
 pos=(30,219,86);aim=(0,19,45.5);scale=151
 cam.location=Vector(pos);cam.rotation_euler=(Vector(aim)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
 bpy.context.view_layer.update();ixs={k for i in ids for k in o.data.polygons[i].vertices}
 coords=[world_to_camera_view(s,cam,o.matrix_world@o.data.vertices[k].co) for k in sorted(ixs)]
 assert all(0<v.x<1 and 0<v.y<1 for v in coords)
 fr={'target_projected_vertices_xy':[[q.x,1-q.y] for q in coords],'camera_position':pos,'target':aim,'camera_ortho_scale':scale,'image_size':[1180,224]}
 frames={}
 for phase,slot in [('before',0),('after',3)]:
  for i in ids:o.data.polygons[i].material_index=slot
  stem=f'{phase}-pool-fascia'
  frames[stem]=fr
  file=P/(stem+'.png');s.render.filepath=str(file);bpy.ops.render.render(write_still=True);trim(file)
 (P/'framing-QA.json').write_text(json.dumps(frames,indent=2)+'\n')
