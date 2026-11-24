"""Render from the latest immutable colored Blender file; never save the scene."""
import bpy,json,sys,struct
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
name,out,*extra=sys.argv[sys.argv.index('--')+1:]
s=bpy.context.scene;cam=s.camera
views={'front':((-195,-260,145),(0,0,18),230),
       'left':((-230,-160,120),(0,0,18),230),
       'right':((230,-160,120),(0,0,18),230),
       'rear':((195,260,145),(0,0,18),230),
       'top':((0,0,350),(0,0,0),230)}
assert set(o.type for o in s.objects)=={'MESH','CAMERA','LIGHT'}
assert not bpy.data.libraries and not bpy.data.texts and not bpy.data.movieclips and not any(i.source=='FILE' for i in bpy.data.images)
assert s.render.engine=='CYCLES' and s.cycles.device=='CPU' and s.cycles.samples==32 and s.cycles.seed==0 and not s.cycles.use_denoising
assert tuple(cam.location)==(-195.0,-260.0,145.0)
loc,target,scale=views[name];cam.location=loc
cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
s.render.resolution_x=1200;s.render.resolution_y=1200;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.use_stamp=False
bpy.context.view_layer.update()
mesh=next(o for o in s.objects if o.type=='MESH')
q=[world_to_camera_view(s,cam,mesh.matrix_world@v.co) for v in mesh.data.vertices]
assert all(.035<p.x<.965 and .035<p.y<.965 and p.z>0 for p in q)
qbox=[world_to_camera_view(s,cam,mesh.matrix_world@Vector(c)) for c in mesh.bound_box]
bounds=lambda points:[min(p.x for p in points),min(p.y for p in points),max(p.x for p in points),max(p.y for p in points)]
print('CURRENT_VIEW',json.dumps(dict(location=loc,target=target,scale=cam.data.ortho_scale,resolution=[s.render.resolution_x,s.render.resolution_y],vertices_bounds=bounds(q),bbox_bounds=bounds(qbox),rotation=list(cam.rotation_euler))))
s.render.filepath=out;bpy.ops.render.render(write_still=True)
if name=='front':
 material=[f.material_index for f in mesh.data.polygons]
 assert material.count(0)==6245 and material.count(1)==23
 Path(out+'.native.json').write_text(json.dumps({'triangles':[[*f.vertices] for f in mesh.data.polygons],'vertices':[[*v.co] for v in mesh.data.vertices],'material_indices':material},separators=(',',':')))
