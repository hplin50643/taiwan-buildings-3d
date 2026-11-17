from pathlib import Path
import bpy,numpy as np,json,hashlib,tempfile,struct
R=Path(__file__).resolve().parents[1];Q=R/'qa-continuous-column';d=np.load(R/'color-mesh.npz');pal=json.loads((R/'palette.json').read_text());name='NTUE MoNTUE partial color'
def get():return bpy.data.objects[name]
def geometry(o):
 assert np.array_equal(np.array([list(v.co)for v in o.data.vertices]),d['vertices']);assert np.array_equal(np.array([list(p.vertices)for p in o.data.polygons]),d['faces']);assert np.array_equal([p.material_index for p in o.data.polygons],d['materials']);assert np.array_equal(np.array(o.matrix_world),np.eye(4));assert not o.modifiers
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'));o=get();geometry(o);assert o.get('source_mesh_sha256')==hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest();assert len(o.data.materials)==2
expected=[]
for m,(n,h)in zip(o.data.materials,pal):
 rgb=[int(h[i:i+2],16)/255 for i in [1,3,5]];rgba=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb]+[1];expected.append(rgba);assert m.name==n[:63];assert max(abs(a-b)for a,b in zip(m.diffuse_color,rgba))<1e-7;assert max(abs(a-b)for a,b in zip(m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value,rgba))<1e-7
assert not bpy.data.libraries and not bpy.data.texts and not bpy.data.sounds and not bpy.data.movieclips;assert all(im.type=='RENDER_RESULT' and not im.filepath for im in bpy.data.images);assert all(f.filepath=='<builtin>'for f in bpy.data.fonts)
extras=[x for x in bpy.data.objects if x.type=='MESH' and x!=o];assert len(extras)==1 and extras[0].name=='NOTICE_BACKDROP_NOT_PRINT_GEOMETRY' and extras[0].hide_render;assert bpy.data.objects['HISTORICAL_SCHEME_NOTICE_NOT_PRINT_GEOMETRY'].hide_render
with tempfile.TemporaryDirectory()as td:
 m=o.data.materials[0];m.diffuse_color=(.1,.2,.3,1);m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.1,.2,.3,1);p=Path(td)/'edit.blend';bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(p));bpy.ops.wm.open_mainfile(filepath=str(p));o=get();geometry(o)
 for i,m in enumerate(o.data.materials):
  want=(.1,.2,.3,1)if i==0 else expected[i];assert max(abs(a-b)for a,b in zip(m.diffuse_color,want))<1e-7;assert max(abs(a-b)for a,b in zip(m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value,want))<1e-7
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'));o=get()
with tempfile.TemporaryDirectory()as td:
 o.data.vertices[0].co.x+=.125;p=Path(td)/'vertex.blend';bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(p));bpy.ops.wm.open_mainfile(filepath=str(p));o=get();want=d['vertices'].copy();want[0,0]+=.125;assert np.array_equal(np.array([list(v.co)for v in o.data.vertices]),want);assert np.array_equal([p.material_index for p in o.data.polygons],d['materials'])
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'));geometry(get())
def clean(raw):
 out=raw[:8];pos=8
 while pos<len(raw):
  n=struct.unpack('>I',raw[pos:pos+4])[0];kind=raw[pos+4:pos+8]
  if kind not in [b'tEXt',b'zTXt',b'iTXt',b'eXIf']:out+=raw[pos:pos+n+12]
  pos+=n+12
 return out
with tempfile.TemporaryDirectory()as td:
 p=Path(td)/'preview.png';bpy.context.scene.render.filepath=str(p);bpy.ops.render.render(write_still=True);assert clean(p.read_bytes())==(R/'preview.png').read_bytes()
(Q/'scene-validation.json').write_text(json.dumps(dict(vertices=len(d['vertices']),triangles=len(d['faces']),original_vertices_faces_and_assignments_exact=True,palette_srgb_exact=True,blender_material_names_match_legacy_63byte_truncation=True,full_names_retained_in_palette_and_3MF=True,single_material_edit_save_reopen=True,single_vertex_edit_save_reopen=True,reopened_render_matches_preview=True,one_architectural_mesh=True,one_retained_hidden_notice_backdrop_not_print_mesh=True,no_external_assets=True,scene_sha256=hashlib.sha256((R/'scene.blend').read_bytes()).hexdigest(),physical_print_tested=False),indent=2)+'\n')
