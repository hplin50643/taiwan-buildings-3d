import bpy,json,hashlib,zipfile,xml.etree.ElementTree as E
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'))
original=next(o for o in bpy.context.scene.objects if o.type=='MESH')
j={'v':[list(v.co) for v in original.data.vertices],'f':[list(p.vertices) for p in original.data.polygons],'matrix':[list(r) for r in original.matrix_world]}
bpy.ops.wm.open_mainfile(filepath=str(R/'appearance.blend'))
o=next(o for o in bpy.context.scene.objects if o.type=='MESH');d=json.load(open(R/'appearance-materials.json'));j['m']=d['wall_continuity_baseline_face_material_indices'];sel={'faces':d['wall_continuity_changed_faces'],'groups':d['wall_continuity_groups']}
v=[list(v.co) for v in o.data.vertices];f=[list(p.vertices) for p in o.data.polygons];m=[p.material_index for p in o.data.polygons]
assert v==j['v'] and f==j['f'] and [list(r) for r in o.matrix_world]==j['matrix']
changed=[i for i,(a,b) in enumerate(zip(m,j['m'])) if a!=b];assert changed==sel['faces']
assert all(j['m'][i]==0 and m[i]==1 for i in changed)
assert m==d['face_material_indices']
for idx,entry in enumerate(d['palette']):
 expected=[int(entry['srgb'][k:k+2],16)/255 for k in (1,3,5)]
 actual=list(o.data.materials[idx].diffuse_color)[:3]
 assert all(abs(a-b)<1e-6 for a,b in zip(actual,expected))
assert [a['srgb'] for a in d['palette']]==['#A7A9A5','#BA9E92','#536562','#A5AEA3','#A2A19B']
with zipfile.ZipFile(R/'appearance.3mf') as z:
 n={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'};x=E.fromstring(z.read('3D/3dmodel.model'))
 vv=[[float(a.attrib[k]) for k in ['x','y','z']] for a in x.findall('.//m:vertex',n)]
 ff=[[int(a.attrib[k]) for k in ['v1','v2','v3']] for a in x.findall('.//m:triangle',n)]
 mm=[int(a.attrib['p1']) for a in x.findall('.//m:triangle',n)]
 assert vv==v and ff==f and mm==m
 assert [e.attrib['displaycolor'] for e in x.findall('.//m:base',n)]==[e['srgb']+'FF' for e in d['palette']]
q={'passed':True,'vertices':len(v),'triangles':len(f),'changed_faces':changed,'wall_color_corrected_face_count':m.count(1),'other_material_face_count':len(f)-m.count(1),'geometry_order_transform_unchanged':True,'original_nonwall_palette_unchanged':True,'wall_palette_revision':{'previous':'#AA715C','new':'#BA9E92','reason':'Official 2010 repaint to pink and accompanying post-repaint photographs'},'unchanged_face_material_indices':len(f)-len(changed),'scene_3mf_indices_exact':True,'groups':sel['groups'],'limits':['Same-material continuity inference, not additional side/rear photographic evidence','Original geometric simplifications retained','Not physically test printed']}
(R/'appearance-continuity-verification.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q))
