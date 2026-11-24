"""Original triangles only: separate upper faces; continuous west wall stays neutral."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='c3f378290aa76b677b0350ad97fbc96c21b20e135d30eadb24ecd56cf0d33152';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==22312
# Original base spans150mm, so its final150/maxextent transform is verified, not assumed.
scale=m.extents.max()/150.;assert abs(scale-1)<1e-6
v=m.triangles/scale;lo=v.min(1);hi=v.max(1);normal=m.face_normals
pal=[('Supported separate upper core return muted brown','#8B7764'),('Supported upper pale folded screens and return','#D1D4CF'),('Upper structural bands subdued gray','#AEB6B3'),('Discrete existing window backing restrained gray green','#485752'),('Observed simplified terrace neutral gray','#B3B5AD'),('UNVERIFIED continuous wall podium and other domains neutral','#B8BAB5')];a=np.full(len(m.faces),5,np.int32)
def box(x0,x1,y0,y1,z0,z1):return (lo[:,0]>=x0-.004)&(hi[:,0]<=x1+.004)&(lo[:,1]>=y0-.004)&(hi[:,1]<=y1+.004)&(lo[:,2]>=z0-.004)&(hi[:,2]<=z1+.004)
def plane(j,p):return np.max(abs(v[:,:,j]-p),axis=1)<.004
levels=[34+i*10.25 for i in range(10)]
# Distinct rear core plane y33.5 does not coincide with podium y37. West x-63 is never brown.
a[plane(1,33.5)&box(-63,-43,33.49,33.51,33.5,144)]=0
# Separate pale folded screens and original ribs; whole stepped geometry, not clipped triangles.
a[box(-63,-47.2,-38,-29.7,33.4,144)]=1
a[box(49,63,-38,-29.7,33.4,144)]=1
a[box(37.15,63,29.7,38.2,33.4,144)]=1
# Rear white end's own plane and long thin original ribs, no copying all x+63 wall.
a[plane(1,33.5)&box(37,63,33.49,33.51,33.5,144)]=1
for x in [39,46,53,60]:a[box(x-.6,x+.6,33.05,35.15,33.5,144)]=1
for i,z in enumerate(levels):
 # Front gallery slab/parapet physically separated from continuous rear main wall.
 x0,x1=(-26,-4) if i==8 else(-26.5,48.5)
 a[box(x0,x1,-36.2,-20,z,z+1.8)]=2
 a[box(x0,x1,-36.2,-34.6,z+1.6,z+3.6)]=2
 a[box(-27.5,37.5,28.2,36.6,z,z+1.8)]=2
 a[box(-27.5,37.5,35.05,36.55,z+1.5,z+3.4)]=2
 # Window backs only; existing mullions stay light-gray separate components.
 if i<8:
  for x in [-15,9,33]:
   a[plane(1,-24.3)&box(x-9.5,x+9.5,-24.31,-24.29,z+3,z+9.2)]=3
   for xx in [x-5.5,x,x+5.5]:a[box(xx-.55,xx+.55,-26.1,-23.9,z+3,z+9.2)]=2
   a[box(x-9.5,x+9.5,-26.1,-23.9,z+5.5,z+6.5)]=2
 for x in [-17,4,25]:a[plane(1,30.35)&box(x-8.5,x+8.5,30.34,30.36,z+3,z+8.8)]=3
 for yy,w in [(-14,8),(8,3.3),(16,3.3),(25,3.3)]:a[plane(0,-61.45)&box(-61.46,-61.44,yy-w/2,yy+w/2,z+3.3,z+9.7)]=3
 for x in [41.2,48.1,55,61.3]:a[plane(1,32)&box(x-2.4,x+2.4,31.99,32.01,z+3,z+9.4)]=3
for z in [122,131,140]:a[plane(1,31.85)&box(-60.25,-45.75,31.84,31.86,z,z+2.6)]=3
for z in [39,80,121]:a[plane(1,-29.45)&box(-57.8,-52.2,-29.46,-29.44,z,z+13.5)]=3
# Actual upper terrace and service roof horizontal surface, planting not invented.
a[plane(2,137.1)&box(-32.5,48.5,-27,33,137.09,137.11)]=4
a[plane(2,146.7)&box(-56,-38,-1.5,27.5,146.69,146.71)]=4
# All unverified podium and entire continuous end-wall plane kept neutral, including upper triangles.
a[plane(0,-63)]=5
a[hi[:,2]<33.39]=5
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'22312 original triangles unchanged','limits':['Continuous western mixed wall x-63 entirely neutral including upper surface.','Front podium and entrance remain neutral; reverse PDF does not authorize front sunshades.','Unknown capture dates and mixed lighting: approximate families only.','No letters, planting, equipment or new geometry.','Six colors are not a verified multi-filament slicer job.']},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest(),'source_coordinate_scale':scale};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
