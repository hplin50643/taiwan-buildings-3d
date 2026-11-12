"""Blender background verification of the actual saved color scene.
Optional --baseline=/path/to/no-text/scene.blend checks its original shader values,
mesh and object transform directly; the original scene is only opened read-only.
"""
from pathlib import Path
import bpy,numpy as np,json,hashlib,sys
R=Path(__file__).resolve().parent
B=next((Path(x.split('=',1)[1])for x in sys.argv if x.startswith('--baseline=')),None)
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():
 o=bpy.data.objects.get('Longshan Temple color');assert o and o.type=='MESH'
 s=bpy.context.scene
 return {'vertices':np.array([list(v.co)for v in o.data.vertices]),'faces':np.array([list(p.vertices)for p in o.data.polygons]),'matrix':np.array(o.matrix_world),'materials':[{'name':m.name,'diffuse':list(m.diffuse_color),'Base Color':list(m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value),'Roughness':m.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value,'Metallic':m.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value,'IOR':m.node_tree.nodes.get('Principled BSDF').inputs['IOR'].default_value}for m in o.data.materials], 'lighting': [{'name':x.name,'matrix':[list(row)for row in x.matrix_world],'type':x.data.type,'energy':x.data.energy,'color':list(x.data.color),'shape':x.data.shape,'size':x.data.size}for x in sorted(bpy.data.objects,key=lambda x:x.name)if x.type=='LIGHT'], 'world_color':list(s.world.color),'color_management':{'view_transform':s.view_settings.view_transform,'look':s.view_settings.look,'exposure':s.view_settings.exposure,'gamma':s.view_settings.gamma}}
base=None
if B:
 before=H(B);bpy.ops.wm.open_mainfile(filepath=str(B));base=snapshot();assert H(B)==before
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'));o=bpy.data.objects['Longshan Temple color'];scene=bpy.context.scene;got=snapshot();d=np.load(R/'color-mesh.npz');pal=json.loads((R/'palette.json').read_text())
checks={'vertices_exact':np.array_equal(got['vertices'],d['vertices']),'faces_exact':np.array_equal(got['faces'],d['faces']),'material_indices_exact':np.array_equal(np.array([p.material_index for p in o.data.polygons]),d['materials']),'identity_matrix':np.array_equal(got['matrix'],np.eye(4)),'palette_count':len(got['materials'])==len(pal),'text_objects_hidden':all(x.hide_render for x in bpy.data.objects if x.type=='FONT'),'text_bodies_empty':all(x.data.body=='' for x in bpy.data.objects if x.type=='FONT'),'caption_backing_hidden':bpy.data.objects['NOTICE_BACKDROP_NOT_PRINT_GEOMETRY'].hide_render,'no_render_stamp':not scene.render.use_stamp,'96_samples':scene.cycles.samples==96,'denoise_disabled':not scene.cycles.use_denoising,'cpu_single_thread':scene.cycles.device=='CPU'and scene.render.threads==1 and scene.render.threads_mode=='FIXED','portable_output':scene.render.filepath=='//preview.png','no_external_image_textures':len(bpy.data.images)==0 or all(x.source not in ('FILE','MOVIE','SEQUENCE')or x.name=='Render Result'for x in bpy.data.images),'no_external_fonts':all(x.filepath=='<builtin>'for x in bpy.data.fonts)}
for i,((name,h),s)in enumerate(zip(pal,got['materials'])):
 vals=[int(h[k:k+2],16)/255 for k in (1,3,5)];rgb=[v/12.92 if v<=.04045 else((v+.055)/1.055)**2.4 for v in vals]+[1]
 checks['material_'+str(i)+'_name_RGBA_roughness']=s['name']==name and np.allclose(s['diffuse'],rgb,rtol=0,atol=3e-8)and np.allclose(s['Base Color'],rgb,rtol=0,atol=3e-8)and abs(s['Roughness']-.72)<3e-8
if base:
 checks.update({'baseline_vertices_exact':np.array_equal(got['vertices'],base['vertices']),'baseline_topology_exact':np.array_equal(got['faces'],base['faces']),'baseline_matrix_exact':np.array_equal(got['matrix'],base['matrix']),'baseline_all_material_names_RGBA_basecolor_roughness_metallic_IOR_exact':got['materials']==base['materials'],'baseline_lighting_exact':got['lighting']==base['lighting'],'baseline_world_color_exact':got['world_color']==base['world_color'],'baseline_color_management_exact':got['color_management']==base['color_management']})
checks={k:bool(v)for k,v in checks.items()}
q={'status':'PASS'if all(checks.values())else'FAIL','checks':checks,'scene_sha256':H(R/'scene.blend'),'color_mesh_sha256':H(R/'color-mesh.npz'),'baseline_scene_sha256':H(B)if B else None,'material_values':got['materials'],'object_transform':got['matrix'].tolist(),'dimensions_mm':list(o.dimensions)}
(R/'SCENE-QA.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2));assert all(checks.values())
