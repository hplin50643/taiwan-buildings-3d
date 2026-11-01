"""Generate substitute-font old school name outlines using Blender and installed Noto Sans CJK Bold.
Glyphs are not tracings of the original lettering. Local X right, Y up, Z depth.
"""
from pathlib import Path
import bpy,bmesh,numpy as np,json,hashlib
R=Path(__file__).resolve().parent
fontpath='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc';font=bpy.data.fonts.load(fontpath)
result={}
for i,ch in enumerate('國立交通大學'):
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 c=bpy.data.curves.new('letter','FONT');c.body=ch;c.font=font;c.size=1;c.extrude=.06;c.resolution_u=8
 o=bpy.data.objects.new('substitute_'+ch,c);bpy.context.collection.objects.link(o);bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH')
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 v=np.array([x.co[:] for x in o.data.vertices]);f=np.array([p.vertices[:] for p in o.data.polygons]);v[:,:2]-=v[:,:2].min(0);v[:,:2]*=1.00/(v[:,1].max());v[:,0]-=v[:,0].max()/2
 result[f'v{i}']=v;result[f'f{i}']=f
np.savez_compressed(R/'letter_meshes.npz',**result)
(R/'LETTERING-NOTE.json').write_text(json.dumps({'text':'國立交通大學','placement':'Right-to-left name along lower curved wall; font substitution, not source glyph tracing','font':'Noto Sans CJK Bold','font_source_path':fontpath,'height_m':1.00,'extrusion_m':.12,'source':'A1 3尺3寸 interpreted approximately as1.00m; stated2寸3分 approximately0.07m depth thickened to0.12m for display/printing','original_crest_omitted':True},ensure_ascii=False,indent=2))
