"""Render the three existing publication angles from the exact saved CKS native scene."""
from pathlib import Path
from mathutils import Vector
import bpy,json,sys
name,out=sys.argv[sys.argv.index('--')+1:]
scene=bpy.context.scene;cam=scene.camera;model=scene.objects['Printable building']
assert scene.cycles.samples==24 and not scene.cycles.use_denoising and scene.render.engine=='CYCLES'
assert not bpy.data.libraries and not bpy.data.texts and not any(i.source=='FILE' for i in bpy.data.images)
assert all(o.hide_render for o in scene.objects if o.type in ('FONT','CURVE'))
assert set(o.name for o in scene.objects if o.type=='MESH')=={'Printable building','Studio floor (not part of model)'}
assert tuple(cam.location)==(0.,-250.,95.) and cam.data.type=='ORTHO'
assert cam.data.ortho_scale==247.5
center=sum((model.matrix_world@Vector(c) for c in model.bound_box),Vector())/8
aim=Vector((center.x,center.y,model.dimensions.z*.42))
views={'front':(135,-230,133),'rear':(-150,210,160),'elevation':(0,-250,95)}
cam.location=views[name];cam.rotation_euler=(aim-cam.location).to_track_quat('-Z','Y').to_euler()
assert [scene.render.resolution_x,scene.render.resolution_y]==[1200,1000]
scene.cycles.device='CPU';scene.render.use_stamp=False
scene.render.filepath=out
print('CURRENT_VIEW',json.dumps({'location':list(cam.location),'target':list(aim),'scale':cam.data.ortho_scale,'rotation':list(cam.rotation_euler)}))
bpy.ops.render.render(write_still=True)
if name=='front':
 mat=[q.material_index for q in model.data.polygons]
 Path(out+'.geometry.json').write_text(json.dumps({'vertices':[[*(model.matrix_world@v.co)] for v in model.data.vertices],'faces':[[*p.vertices] for p in model.data.polygons],'materials':mat},separators=(',',':')))
