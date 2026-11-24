import bpy,json,math,struct
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent.parent
bpy.ops.wm.open_mainfile(filepath=str(D/'appearance.blend'))
scene=bpy.context.scene;obj=next(o for o in scene.objects if o.type=='MESH')
views={'front':((-235,-205,165),(-5,0,37.4)),'rear':((235,205,160),(-5,0,37.4)),'elevation':((-300,0,37.4),(-5,0,37.4)),'source-angle':((-230,-140,110),(-5,0,37.4)),'left':((-40,-300,120),(-5,0,37.4)),'right':((-40,300,120),(-5,0,37.4)),'top':((0,0,350),(-5,0,0))}
meta=json.loads((D/'appearance-materials.json').read_text())
for name,(pos,target) in [(n,views[n.removeprefix('original-')]) for n in ['original-front','original-rear']]:
 if name.startswith('original-'):
  for p,i in zip(obj.data.polygons,meta['original_face_material_indices']):p.material_index=i
  out=D/'appearance-review-v2';out.mkdir(exist_ok=True)
 else:out=D/'appearance'
 c=scene.camera;c.location=pos;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();inv=c.rotation_euler.to_matrix().transposed();projected=[inv@(obj.matrix_world@Vector(corner)-c.location) for corner in obj.bound_box]
 width=max(v.x for v in projected)-min(v.x for v in projected);height=max(v.y for v in projected)-min(v.y for v in projected);c.data.ortho_scale=max(width,height*scene.render.resolution_x/scene.render.resolution_y)*1.18
 scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
 data=(out/(name+'.png')).read_bytes();cleaned=data[:8];off=8
 while off<len(data):
  length=struct.unpack_from('>I',data,off)[0];typ=data[off+4:off+8]
  if typ not in (b'tEXt',b'zTXt',b'iTXt'):cleaned+=data[off:off+length+12]
  off+=length+12
 (out/(name+'.png')).write_bytes(cleaned)
 print('FINISHED',name,flush=True)
