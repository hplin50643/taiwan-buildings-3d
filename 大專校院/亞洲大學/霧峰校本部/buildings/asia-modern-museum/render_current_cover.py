"""Inspect the saved camera and render a controlled reduced-resolution comparison; never save the scene."""
import bpy, json, sys
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:]
scene=bpy.context.scene; c=scene.camera
assert c and not bpy.data.libraries
assert not any(i.source=='FILE' and i.filepath and not i.packed_file for i in bpy.data.images)
for o in scene.objects:
 if 'NOTICE' in o.name:assert o.hide_render
scene.render.resolution_x=1200;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.render.use_stamp=False;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
if scene.render.engine=='CYCLES':
 scene.cycles.samples=48;scene.cycles.seed=0;scene.cycles.use_denoising=False
scene.render.filepath=args[0]
print('CONTROLLED_SAVED_VIEW',json.dumps(dict(camera=list(c.location),rotation=list(c.rotation_euler),scale=c.data.ortho_scale,engine=scene.render.engine,frame=scene.frame_current)))
bpy.ops.render.render(write_still=True)
