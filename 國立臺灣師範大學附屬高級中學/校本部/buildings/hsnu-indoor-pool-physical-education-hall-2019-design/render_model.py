from pathlib import Path
import bpy,numpy as np,json,math,hashlib,sys
from mathutils import Vector
R=Path(__file__).resolve().parent
ONLY_VIEW=next((x.split('=',1)[1] for x in sys.argv if x.startswith('--only-view=')),None)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
d=np.load(R/'mesh.npz');v=d['vertices'];f=d['faces'];mi=d['materials'];pal=json.loads((R/'palette.json').read_text())
m=bpy.data.meshes.new('validated_printable_mesh');m.from_pydata(v.tolist(),[],f.tolist());m.update();o=bpy.data.objects.new('HSNU pool2019 historical design exterior',m);bpy.context.collection.objects.link(o)
o['source_mesh_sha256']=hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest();o['scale']='1:250';o['scope']='HSNU pool2019 design; not2022asbuilt/current survey'
for name,col in pal:
 mat=bpy.data.materials.new(name);rgb=tuple(int(col[i:i+2],16)/255 for i in (1,3,5));mat.diffuse_color=(*rgb,1);mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*rgb,1);bs.inputs['Roughness'].default_value=.72;m.materials.append(mat)
for p,k in zip(m.polygons,mi):p.material_index=int(k)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=False;scene.render.resolution_x=1200;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.world.color=(.7,.7,.7);scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast'
for loc,power,size in [((100,-180,400),500000,250),((-220,120,240),350000,180),((0,350,200),350000,250),((300,-80,220),250000,180)]:
 bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size
 l.rotation_euler=(Vector((0,0,45))-l.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=370
views={'preview':(-320,-420,280),'rear':(320,420,240),'front':(-550,0,40),'back':(550,0,40),'west':(0,-550,40),'east':(0,550,40),'top':(0,0,550)}
# In-render notice is part of the scene, NOT architectural/print geometry.
bpy.ops.object.text_add();caption=bpy.context.object;caption.name='HISTORICAL_SCHEME_NOTICE_NOT_PRINT_GEOMETRY';caption.parent=cam
fontpath=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
if fontpath.exists():
 caption.data.font=bpy.data.fonts.load(str(fontpath));caption.data.body='師大附中體育教學館暨室內溫水游泳池\n2019設計圖示；非竣工圖／非現況\n外屏頂圖量±0.15m；未試印'
else:caption.data.body='HSNU POOL / 2019 DESIGN INTERPRETATION\nScreen outline +/-0.15m; not as-built\nNot current survey; unprinted'
caption.data.align_x='LEFT';caption.data.space_line=1.0
cm=bpy.data.materials.new('caption emission');cm.use_nodes=True;cm.node_tree.nodes.clear();em=cm.node_tree.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(.95,.95,.95,1);out=cm.node_tree.nodes.new('ShaderNodeOutputMaterial');cm.node_tree.links.new(em.outputs[0],out.inputs['Surface']);caption.data.materials.append(cm)
if hasattr(caption,'visible_shadow'):caption.visible_shadow=False
def update_caption():
 sc=cam.data.ortho_scale;caption.location=(-.45*sc,-.30*sc,-10);caption.rotation_euler=(0,0,0);caption.data.size=.026*sc
from bpy_extras.object_utils import world_to_camera_view
framing={}
for name,loc in views.items():
 if ONLY_VIEW and name!=ONLY_VIEW:continue
 cam.location=loc;target=Vector((0,0,40));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=280 if name in ['west','east'] else 380
 bpy.context.view_layer.update()
 for _ in range(20):
  pts=[world_to_camera_view(scene,cam,Vector(x)) for x in v];bounds=[min(p.x for p in pts),max(p.x for p in pts),min(p.y for p in pts),max(p.y for p in pts)]
  if bounds[0]>.03 and bounds[1]<.97 and bounds[2]>.14 and bounds[3]<.97:break
  cam.data.ortho_scale*=1.08;bpy.context.view_layer.update()
 assert bounds[0]>.03 and bounds[1]<.97 and bounds[2]>.14 and bounds[3]<.97,(name,bounds)
 update_caption();framing[name]=bounds;scene.render.filepath=str(R/(name+'.png'));bpy.ops.render.render(write_still=True)
if framing:
 prior=R/'FRAMING-QA.json'
 if ONLY_VIEW and prior.exists():
  old=json.loads(prior.read_text())
  if old.get('mesh_sha256')==o['source_mesh_sha256']:framing={**old['projected_vertex_bounds'],**framing}
 prior.write_text(json.dumps({'status':'PASS','mesh_sha256':o['source_mesh_sha256'],'projected_vertex_bounds':framing},indent=2))

# Two deliberately cropped detail views, not full-model framing claims.
for name,loc,target,ortho in [('entry-detail',(-300,180,100),(-135,52,20),120),('court-detail',(260,-280,200),(65,-5,37),210),('roof-detail',(-230,160,240),(-100,35,52),160)]:
 if ONLY_VIEW and name!=ONLY_VIEW:continue
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=ortho;update_caption();scene.render.filepath=str(R/(name+'.png'));bpy.ops.render.render(write_still=True)
cam.location=views['preview'];cam.rotation_euler=(Vector((0,0,40))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=420
update_caption()
bpy.ops.wm.save_as_mainfile(filepath=str(R/'scene.blend'),compress=True)
