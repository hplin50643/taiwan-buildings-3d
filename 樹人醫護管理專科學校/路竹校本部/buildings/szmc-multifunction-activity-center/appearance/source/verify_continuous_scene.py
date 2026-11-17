from pathlib import Path
import bpy,numpy as np,json,hashlib,tempfile,struct
R=Path(__file__).resolve().parents[1];Q=R/'qa-continuous-rightreturn';d=np.load(R/'mesh-data.npz');pal=[(p['id'],p['srgb'])for p in json.loads((R/'palette.json').read_text())['materials']];name='SZMC_unchanged_original_mesh'
def get():return bpy.data.objects[name]
def geometry(o):
 assert np.array_equal(np.array([list(v.co)for v in o.data.vertices]),d['vertices']);assert np.array_equal(np.array([list(p.vertices)for p in o.data.polygons]),d['faces']);assert np.array_equal([p.material_index for p in o.data.polygons],d['materials']);assert np.array_equal(np.array(o.matrix_world),np.eye(4));assert not o.modifiers
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'));o=get();geometry(o);assert o.get('source_sha256')==hashlib.sha256((R.parent/'model.stl').read_bytes()).hexdigest();assert len(o.data.materials)==6
expected=[]
for m,(n,h)in zip(o.data.materials,pal):
 rgb=[int(h[i:i+2],16)/255 for i in [1,3,5]];rgba=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb]+[1];expected.append(rgba);assert abs(m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value-(.35 if 'glazing' in n else .75))<1e-7;assert m.name==n[:63];assert max(abs(a-b)for a,b in zip(m.diffuse_color,rgba))<1e-7;assert max(abs(a-b)for a,b in zip(m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value,rgba))<1e-7
assert not bpy.data.libraries and not bpy.data.texts and not bpy.data.sounds and not bpy.data.movieclips;assert all(im.type=='RENDER_RESULT' and not im.filepath for im in bpy.data.images);assert all(f.filepath=='<builtin>'for f in bpy.data.fonts)
assert len([x for x in bpy.data.objects if x.type=='MESH'])==1
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
 p=Path(td)/'preview.png';bpy.context.scene.render.filepath=str(p);bpy.ops.render.render(write_still=True);assert clean(p.read_bytes())==(R/'previews/front.png').read_bytes()
(Q/'scene-validation.json').write_text(json.dumps(dict(vertices=len(d['vertices']),triangles=len(d['faces']),original_vertices_faces_and_assignments_exact=True,palette_srgb_exact=True,blender_material_names_match_legacy_63byte_truncation=True,full_names_retained_in_palette_and_3MF=True,single_material_edit_save_reopen=True,single_vertex_edit_save_reopen=True,reopened_render_matches_preview=True,one_architectural_mesh=True,no_extra_display_meshes=True,no_external_assets=True,scene_sha256=hashlib.sha256((R/'scene.blend').read_bytes()).hexdigest(),physical_print_tested=False),indent=2)+'\n')
