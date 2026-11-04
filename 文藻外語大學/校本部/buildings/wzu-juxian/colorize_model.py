"""6182 original faces; narrow-screen lattice and complete front bands only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;expected='afbf6e7d00ccedddb3769974f57d7424a81b8e7dab13c1ed8315e3d7570cbfc5';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==6182
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.full(len(t),2,np.int32)
def span(ax,l,h):return (lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
def box(x0,x1,y0,y1,z0,z1):return span(0,x0,x1)&span(1,y0,y1)&span(2,z0,z1)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
red=np.zeros(len(t),bool);gray=red.copy();rows=[]
for xa,xb,h in [(-67,-44,73),(-44,-19,80),(-19,7,88),(7,67,95)]:
 x=(xa+xb)/2;w=xb-xa
 for z in [h-52,h-34,h-16]:
  band=plane(1,-20.9)&box(xa,xb,-20.9,-20.9,z-3,z-1.3)&(m.face_normals[:,1]<-.99);gray|=band
  if w>40:continue
  # Whole lattice front and reveals within the single actual aperture; backing y=-17.8 expressly excluded.
  ap=box(x-(w-7)/2,x+(w-7)/2,-21.5,-17.8,z,z+10)
  member=np.zeros(len(t),bool)
  for xx in range(int(xa+5),int(xb-4),4):member|=box(xx-.5,xx+.5,-21.5,-17.5,z,z+10)
  for zz in [z+3,z+7]:member|=box(x-(w-7)/2,x+(w-7)/2,-21.5,-17.5,zz,zz+1.1)
  # Coplanar union front can span several joined bars: its full front face is still entirely within this one brick aperture.
  sel=ap&(member|plane(1,-21.5))&~plane(1,-17.8)
  red|=sel;rows.append(int(sel.sum()))
assert min(rows)>0 and gray.sum()>0 and not np.any(red&gray)
a[red]=0;a[gray]=1
# Preserve complete connected coplanar domains: mixed-domain border reveals stay wholly neutral.
parent=np.arange(len(a))
def root(i):
 while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
 return i
for i,j in m.face_adjacency:
 if np.dot(m.face_normals[i],m.face_normals[j])>.999999:parent[root(i)]=root(j)
groups={}
for i in range(len(a)):groups.setdefault(root(i),[]).append(i)
removed=[]
for ids in groups.values():
 if len(set(a[ids]))>1:removed.extend(i for i in ids if a[i]!=2);a[ids]=2
red=a==0;gray=a==1
pal=[('Observed first-three narrow screen lattice terracotta','#A66550'),('Observed independent front band gray','#BABDB6'),('UNVERIFIED broad right grid mixed walls roof rear neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'6182 original triangles unchanged; no new or split faces','domains':{'narrow_lattice_initial_row_candidates':rows,'neutralized_border_reveal_faces':len(removed),'red_lattice_total':int(red.sum()),'front_band_gray':int(gray.sum()),'broad_right_lattice':'entirely neutral: joined coplanar grid crosses source gray separator'},'limitations':['Right60wide lattice conservative neutral whole-domain, not red triangular fragments beside gray separator.','All solid placeholder backings, mixed main walls and five thick roof wedges neutral.','Photo dates unknown;2023 form and2025 PDF edition not capture dates.','Material labels not a verified multi-filament slicing job.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':6182,'original_STL_sha256':expected,'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()},indent=2));print(np.unique(a,return_counts=True));print(rows)
