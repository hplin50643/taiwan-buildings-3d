import bpy,bmesh,json,math,struct,hashlib
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent;O=P/'reference-nominal';bpy.ops.wm.open_mainfile(filepath=str(O/'scene.blend'))
G={'SOURCE_NORMALIZED_A_END':(Vector((0,1,0)),1.5147540983606558),'SOURCE_NORMALIZED_F_GABLE':(Vector((0,-1,0)),174.91685393258427)}
R={f'SOURCE_NORMALIZED_ROOF_{side}':(Vector((sgn/math.sqrt(2),0,-1/math.sqrt(2))),76.2/math.sqrt(2))for side,sgn in [('left',1),('right',-1)]}
log=[]
for name,(n,c)in {**G,**R}.items():
 o=bpy.data.objects[name];bm=bmesh.new();bm.from_mesh(o.data)
 for other,(nn,cc)in (R if name in G else G).items():
  normal=n-.98*nn;const=c-.98*cc
  bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=-const*normal/normal.length_squared,plane_no=normal,clear_outer=True,clear_inner=False)
  bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-5);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));
 if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
 bm.to_mesh(o.data);bm.free();o.data.update()
 data=bytearray(b'ANALYTIC SOURCE PRESERVING BACK MITERS ONLY'.ljust(80,b' '));data+=struct.pack('<I',len(o.data.polygons))
 for f in o.data.polygons:
  v=[o.data.vertices[i].co for i in f.vertices];data+=struct.pack('<12fH',*f.normal,*v[0],*v[1],*v[2],0)
 p=P/'parts'/(name+'.stl');p.write_bytes(data);log.append({'id':name,'sha256':hashlib.sha256(data).hexdigest(),'triangles':len(o.data.polygons),'bounds':[[min(v.co[k]for v in o.data.vertices)for k in range(3)],[max(v.co[k]for v in o.data.vertices)for k in range(3)]]})
(P/'ANALYTIC-SOURCE-MITER-RECORD.json').write_text(json.dumps(log,indent=2)+'\n')
