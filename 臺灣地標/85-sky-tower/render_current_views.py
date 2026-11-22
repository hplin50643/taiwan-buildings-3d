"""Render the three existing publication angles from the exact saved Sky Tower native scene."""
from pathlib import Path
from mathutils import Vector
import bpy,json,sys
name,out=sys.argv[sys.argv.index('--')+1:]
scene=bpy.context.scene;cam=scene.camera;model=scene.objects['Printable_STL_mm']
assert scene.render.engine=='BLENDER_WORKBENCH'
assert not bpy.data.libraries and not bpy.data.texts and not any(i.source=='FILE' for i in bpy.data.images)
assert all(o.hide_render for o in scene.objects if o.type in ('FONT','CURVE'))
assert set(o.name for o in scene.objects if o.type=='MESH')=={'Printable_STL_mm','Studio floor, not printable'}
assert cam.data.type=='ORTHO'
assert cam.data.ortho_scale==185.0
center=sum((model.matrix_world@Vector(c) for c in model.bound_box),Vector())/8
aim=Vector((0,0,72))
views={'front':(160,-350,170),'rear':(-190,330,185),'elevation':(0,-350,95)}
cam.location=views[name];cam.rotation_euler=(aim-cam.location).to_track_quat('-Z','Y').to_euler()
assert [scene.render.resolution_x,scene.render.resolution_y]==[900,1050]
scene.cycles.device='CPU';scene.render.use_stamp=False
scene.render.filepath=out
print('CURRENT_VIEW',json.dumps({'location':list(cam.location),'target':list(aim),'scale':cam.data.ortho_scale,'rotation':list(cam.rotation_euler)}))
bpy.ops.render.render(write_still=True)
if name=='front':
 mat=[q.material_index for q in model.data.polygons]
 Path(out+'.geometry.json').write_text(json.dumps({'vertices':[[*(model.matrix_world@v.co)] for v in model.data.vertices],'faces':[[*p.vertices] for p in model.data.polygons],'materials':mat},separators=(',',':')))
