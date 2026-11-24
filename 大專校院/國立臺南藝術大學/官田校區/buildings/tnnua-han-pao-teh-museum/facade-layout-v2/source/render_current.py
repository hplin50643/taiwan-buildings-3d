import bpy, sys
from mathutils import Vector
from pathlib import Path
out=Path(sys.argv[sys.argv.index('--')+1])
s=bpy.context.scene;c=s.camera
s.cycles.samples=24;s.cycles.use_denoising=False;s.render.resolution_x=1008;s.render.resolution_y=720
s.render.image_settings.file_format='PNG';s.render.use_stamp=False
views={'front':((195,-240,170),(0,0,42),270),'stairs':((-195,-240,170),(0,0,42),270),'rear':((-195,230,165),(0,0,42),270),'top':((0,0,350),(0,0,0),230)}
for n,(loc,target,scale) in views.items():
 c.location=loc;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=scale
 s.render.filepath=str(out/(n+'.png'));bpy.ops.render.render(write_still=True)
c.data.type='ORTHO'
s.render.engine='BLENDER_WORKBENCH'; w=s.display.shading
w.light='FLAT'; w.color_type='MATERIAL'; w.show_shadows=False; w.show_cavity=False; w.show_object_outline=False
w.background_type='WORLD'; s.world.color=(.095,.105,.12)
s.view_settings.view_transform='Standard'; s.render.film_transparent=False
s.render.resolution_x=1000;s.render.resolution_y=790;s.render.resolution_percentage=100
c.location=(-139,-48,95); c.rotation_euler=(Vector((-44,-33,61.3))-c.location).to_track_quat('-Z','Y').to_euler(); c.data.ortho_scale=35
s.render.filepath=str(out/'stair-door.png'); bpy.ops.render.render(write_still=True)
