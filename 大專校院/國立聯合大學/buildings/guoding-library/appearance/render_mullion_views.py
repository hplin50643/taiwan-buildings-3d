"""Render unchanged original cameras from saved corrected scene, never reconstruct/save scene."""
from pathlib import Path
import bpy,sys,json,struct,hashlib
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(sys.argv[-1]).resolve();P=R/'previews';P.mkdir(exist_ok=True);bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'));s=bpy.context.scene;c=s.camera;o=bpy.data.objects['NUU Guoding Library appearance']
views={'front':((180,-240,155),(0,0,28),230),'rear':((-180,240,155),(0,0,28),230),'elevation':((0,-290,31),(0,0,29),190),'top':((0,0,350),(0,0,0),180)};records=[]
for name,(loc,target,scale) in views.items():
 c.location=loc;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=scale;bpy.context.view_layer.update();q=[world_to_camera_view(s,c,o.matrix_world@v.co)for v in o.data.vertices];assert all(.035<v.x<.965 and .035<v.y<.965 and v.z>0 for v in q)
 p=P/(name+'.png');s.render.filepath=str(p);bpy.ops.render.render(write_still=True);b=p.read_bytes();out=b[:8];at=8
 while at<len(b):
  n=struct.unpack('>I',b[at:at+4])[0];kind=b[at+4:at+8]
  if kind not in [b'tEXt',b'zTXt',b'iTXt',b'eXIf']:out+=b[at:at+n+12]
  at+=n+12
 p.write_bytes(out);records.append({'name':name,'loc':loc,'target':target,'scale':scale,'resolution':[s.render.resolution_x,s.render.resolution_y],'samples':s.cycles.samples,'all_vertices_in_frame':True,'sha256':hashlib.sha256(out).hexdigest()})
(R/'render-view-receipts.json').write_text(json.dumps(records,indent=2)+'\n')
