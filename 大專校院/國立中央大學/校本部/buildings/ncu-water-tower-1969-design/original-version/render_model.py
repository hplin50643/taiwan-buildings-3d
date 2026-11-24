from pathlib import Path
import bpy,numpy as np,json,math,hashlib,sys
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
d=np.load(R/'mesh.npz');v=d['vertices'];f=d['faces'];mi=d['materials'];pal=json.loads((R/'palette.json').read_text())
m=bpy.data.meshes.new('validated_printable_mesh');m.from_pydata(v.tolist(),[],f.tolist());m.update();o=bpy.data.objects.new('NCU 1969 design water tower',m);bpy.context.collection.objects.link(o)
o['source_mesh_sha256']=hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest();o['scale']='1:100';o['scope']='1969 original design; not current/asbuilt survey'
for name,col in pal:
 mat=bpy.data.materials.new(name);rgb=tuple(int(col[i:i+2],16)/255 for i in (1,3,5));mat.diffuse_color=(*rgb,1);mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*rgb,1);bs.inputs['Roughness'].default_value=.72;m.materials.append(mat)
for p,k in zip(m.polygons,mi):p.material_index=int(k)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=False;scene.render.resolution_x=900;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.world.color=(.7,.7,.7);scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast'
for loc,power,size in [((100,-180,400),500000,250),((-220,120,240),350000,180),((0,350,200),350000,250)]:
 bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size
 l.rotation_euler=(Vector((0,0,45))-l.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=245
views={'preview':(270,-420,240),'rear':(-270,420,240),'front':(0,-500,95.20),'back':(0,500,95.20),'west':(-500,0,95.20),'east':(500,0,95.20),'top':(0,0,600)}
from bpy_extras.object_utils import world_to_camera_view
framing=json.loads((R/"FRAMING-QA.json").read_text())["projected_vertex_bounds"] if "--details-only" in sys.argv else {}
for name,loc in views.items():
 if "--details-only" in sys.argv:continue
 cam.location=loc;target=Vector((0,0,95.20));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=100 if name=='top' else 245
 bpy.context.view_layer.update();pts=[world_to_camera_view(scene,cam,Vector(x)) for x in v];bounds=[min(p.x for p in pts),max(p.x for p in pts),min(p.y for p in pts),max(p.y for p in pts)];assert bounds[0]>.02 and bounds[1]<.98 and bounds[2]>.02 and bounds[3]<.98,(name,bounds);framing[name]=bounds
 scene.render.filepath=str(R/(name+'.png'));bpy.ops.render.render(write_still=True)

cam.location=(90,-140,230);cam.rotation_euler=(Vector((0,0,176))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=90
scene.render.filepath=str(R/'roof-detail.png');bpy.ops.render.render(write_still=True)
(R/'FRAMING-QA.json').write_text(json.dumps({'status':'PASS','mesh_sha256':o['source_mesh_sha256'],'projected_vertex_bounds':framing},indent=2))
cam.location=views['preview'];cam.rotation_euler=(Vector((0,0,95.20))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.ortho_scale=245
bpy.ops.wm.save_as_mainfile(filepath=str(R/'scene.blend'),compress=True)
