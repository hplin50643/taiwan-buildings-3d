"""Preserve original 900x700 front/rear/top/courtyard views; never save rendered scene."""
import bpy,sys,json
from pathlib import Path
from mathutils import Vector
R=Path(sys.argv[-1]).resolve();P=R/'previews';P.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'));s=bpy.context.scene;ob=bpy.data.objects['Printable_NDHU'];cam=s.camera
z=(min(v.co.z for v in ob.data.vertices)+max(v.co.z for v in ob.data.vertices))/2
receipts=[]
for name,loc,aim in [('front',(300,100,210),(0,0,z)),('rear',(-260,-175,200),(0,0,z)),('top',(0,0,300),(0,0,0))]:
 s.display.shading.show_shadows=name!='top';cam.location=loc;cam.rotation_euler=(Vector(aim)-cam.location).to_track_quat('-Z','Y').to_euler()
 inv=cam.rotation_euler.to_matrix().transposed();p=[inv@(ob.matrix_world@v.co-cam.location) for v in ob.data.vertices]
 w=max(v.x for v in p)-min(v.x for v in p);h=max(v.y for v in p)-min(v.y for v in p);cam.data.ortho_scale=max(w,h*s.render.resolution_x/s.render.resolution_y)*1.18
 cam.data.shift_x=(max(v.x for v in p)+min(v.x for v in p))/2/cam.data.ortho_scale;cam.data.shift_y=(max(v.y for v in p)+min(v.y for v in p))/2/cam.data.ortho_scale
 s.render.filepath=str(P/(name+'.png'));bpy.ops.render.render(write_still=True);receipts.append({'view':name,'camera':list(cam.location),'ortho':cam.data.ortho_scale,'shift':[cam.data.shift_x,cam.data.shift_y],'dimensions':[s.render.resolution_x,s.render.resolution_y]})
# Courtyard original script reopens saved scene; retain saved shadow flag, not loop's current state.
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'));s=bpy.context.scene;cam=s.camera;cam.location=(-85,80,125);cam.rotation_euler=(Vector((6,-15,15))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=115;cam.data.shift_x=cam.data.shift_y=0
s.render.resolution_x=900;s.render.resolution_y=700;s.render.filepath=str(P/'courtyard.png');bpy.ops.render.render(write_still=True)
(R/'render-view-receipts.json').write_text(json.dumps(receipts+[{'view':'courtyard','camera':[-85,80,125],'aim':[6,-15,15],'ortho':115,'dimensions':[900,700],'intentional_detail_crop':True}],indent=2)+'\n')
