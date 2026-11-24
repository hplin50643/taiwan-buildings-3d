import bpy,json,hashlib,struct
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
A=Path(__file__).resolve().parent;(A/'previews').mkdir(exist_ok=True);(A/'qa').mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(A/'scene.blend'));scene=bpy.context.scene;cam=scene.camera;camd=cam.data;vs=[v.co[:] for v in bpy.data.objects['NTPU colored bay entry facade cut'].data.vertices]
def aim(o,t):o.rotation_euler=(Vector(t)-o.location).to_track_quat('-Z','Y').to_euler()
views={'front':((-80,-230,135),(93,0,24),230),'rear':((220,190,130),(93,0,24),230),'elevation':((93,-250,26),(93,0,26),220),'top':((93,0,350),(93,0,0),220),'right_oblique':((240,-210,100),(93,0,24),230)}
records=[]
for name,(loc,target,scale) in views.items():
 cam.location=loc;aim(cam,target);camd.ortho_scale=scale;bpy.context.view_layer.update();q=[world_to_camera_view(scene,cam,Vector(v)) for v in vs];assert all(.035<p.x<.965 and .035<p.y<.965 and p.z>0 for p in q),name
 scene.render.filepath=str(A/'previews'/(name+'.png'));bpy.ops.render.render(write_still=True)
 p=A/'previews'/(name+'.png');raw=p.read_bytes();clean=raw[:8];pos=8
 while pos<len(raw):
  n=struct.unpack('>I',raw[pos:pos+4])[0];kind=raw[pos+4:pos+8]
  if kind not in [b'tEXt',b'zTXt',b'iTXt',b'eXIf',b'tIME']:clean+=raw[pos:pos+n+12]
  pos+=n+12
 p.write_bytes(clean);records.append({'path':'previews/'+name+'.png','bytes':len(clean),'sha256':hashlib.sha256(clean).hexdigest(),'camera':loc,'target':target,'ortho_scale':scale,'all_vertices_in_frame':True})
(A/'qa/render-manifest.json').write_text(json.dumps({'blender':bpy.app.version_string,'samples':scene.cycles.samples,'resolution':[scene.render.resolution_x,scene.render.resolution_y],'files':records},indent=2)+'\n')
