"""Original primitive-surface matching; no geometric modification or invented painted boundaries."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib,math
R=Path(__file__).resolve().parent;EXPECTED_STL='6e1c338abc56367db05ceb285e223071e96eb950f847d7895347387233de68b7';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
mesh=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(mesh.faces)==133722
# Original helper definitions only. The original final geometry build is never executed here.
G={'__file__':str(R/'build_model.py')};exec((R/'build_model.py').read_text().split('\nparts=[',1)[0],G)
M=G['m'];loft=G['loft'];tube=G['tube']
pal=[('Visible tower body golden ochre','#DDB15B'),('Broad front tile slopes muted terracotta','#C98A43'),('Supported short rails teeth and dragon horns off-white','#DCDDD1'),('Existing schematic tiger stripe tubes','#343735'),('True front arch recess shadow','#414443'),('UNVERIFIED animals mixed face/body fine trim rear neutral','#B6B8B2')]
a=np.full(len(mesh.faces),5,np.int32);verts=mesh.vertices;tri=mesh.triangles;norm=mesh.face_normals;face_lo=tri.min(1);face_hi=tri.max(1);domain_counts={}
def tm(man):
 q=man.to_mesh64();return trimesh.Trimesh(np.asarray(q.vert_properties)[:,:3],np.asarray(q.tri_verts),process=False)
def assign_surface(ref,mat,label,selector=None):
 if selector is not None:ref=trimesh.Trimesh(ref.vertices,ref.faces[selector(ref)],process=False)
 if not len(ref.faces):return
 b=ref.bounds;mask=((verts>=b[0]-.025)&(verts<=b[1]+.025)).all(1);ids=np.flatnonzero(mask);good=np.zeros(len(verts),bool)
 for k in range(0,len(ids),1000):
  ii=ids[k:k+1000];_,dist,_=trimesh.proximity.closest_point(ref,verts[ii]);good[ii]=dist<.012
 cand=np.flatnonzero(good[mesh.faces].all(1));accepted=[]
 for k in range(0,len(cand),1000):
  ii=cand[k:k+1000];_,dist,fi=trimesh.proximity.closest_point(ref,mesh.triangles_center[ii]);ok=(dist<.012)&((norm[ii]*ref.face_normals[fi]).sum(1)>.96);accepted.extend(ii[ok])
 a[accepted]=mat;domain_counts[label]=len(accepted)
for cx in [-36,36]:
 for level in range(7):
  z=6.6+12.8*level;r=13.8-.35*level;re=22.2-.45*level
  ref=tm(M.Manifold.cylinder(13.8,r,r-.35,12).rotate((0,0,15)).translate((cx,22,z-.2)))
  assign_surface(ref,0,f'body_{cx}_{level}',lambda t:(abs(t.face_normals[:,2])<.1)&(t.face_normals[:,1]<-.25))
  # Complete five original twelve-sided front roof sectors. Do not select tiny facet normals.
  rv=[]
  for rad,zz,lift in [(re*.88,z+11.5,.5),(r*.90,z+14.3,0)]:
   for ii in range(72):
    sector=ii//6;tt=(ii%6)/6;aa=math.pi/12+sector*math.pi/6;bb=aa+math.pi/6
    rv.append([cx+rad*((1-tt)*math.cos(aa)+tt*math.cos(bb)),22+rad*((1-tt)*math.sin(aa)+tt*math.sin(bb)),zz+lift*abs(2*tt-1)**3])
  rf=[]
  for ii in range(72):
   if ii//6 not in [6,7,8,9,10]:continue
   jj=(ii+1)%72;rf.extend([[ii,jj,72+jj],[ii,72+jj,72+ii]])
  ref=trimesh.Trimesh(rv,rf,process=False)
  assign_surface(ref,1,f'roof_broad_{cx}_{level}')
  rr=r+2.4
  ref=tm(M.Manifold.cylinder(1.15,rr,rr,12).rotate((0,0,15)).translate((cx,22,z+2.3)))
  assign_surface(ref,2,f'low_rail_{cx}_{level}',lambda t:(abs(t.face_normals[:,2])<.01)&(t.face_normals[:,1]<-.25))
  # Exact cutter-back planes on the five visible front/oblique sides, not exterior wall fields.
  radius=r*math.cos(math.pi/12)-.15
  for f in [0,1,2,10,11]:
   ang=math.radians(f*30);n=np.array([math.sin(ang),-math.cos(ang),0]);u=np.array([math.cos(ang),math.sin(ang),0]);rel=tri-np.array([cx,22,0]);depth=rel@n;across=rel@u
   good=(abs(depth-(radius-1.2)).max(1)<.003)&(abs(across).max(1)<=1.903)&(face_lo[:,2]>=z+3.1-.003)&(face_hi[:,2]<=z+9.1+.003)
   a[good]=4;domain_counts[f'arch_back_{cx}_{level}_{f}']=int(good.sum())
# No trunk color: original ellipsoids have no reliable boundary separating colored flanks from white belly.
# No face/nose/eye/ear/fins coloration, even if approximate primitive names suggest one.
for cx in [-36,36]:
 for dx in [-7.4,7.4]:
  for z,h,r1,r2 in [(21.6,3.5,.9,1.45),(8.9,2.5,1.35,.85)]:
   assign_surface(tm(M.Manifold.cylinder(h,r1,r2,18).translate((cx+dx,-48,z))),2,f'fang_{cx}_{dx}_{z}')
for dx in [-7.5,7.5]:assign_surface(tm(M.Manifold.cylinder(10,2.6,.9,24).rotate((-17,0,0)).translate((-36+dx,-34,31))),2,f'dragon_horn_{dx}')
for y in [-24,-18,-12,-6,0,6]:
 k=math.sqrt(max(.05,1-((y+11)/24)**2));pts=[(36+14*k*math.cos(ang),y,19+12*k*math.sin(ang))for ang in np.linspace(.10,math.pi-.10,25)]
 assign_surface(tm(tube(pts,.55)),3,f'original_stripe_{y}')
np.savez_compressed(R/'color-mesh.npz',vertices=mesh.vertices,faces=mesh.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'133722 original triangles unchanged','method':'All original triangle vertices and center matched to approved original primitive surfaces within 0.012 mm, normal agreement above 0.96. No remeshing.','domain_counts':domain_counts,'limits':['2025 reopening-publication color families, not precise restoration paintwork.','Whole mixed dragon/tiger trunks and heads neutral; no arbitrary hemisphere or xyz painted borders.','Only original stripe tubes black, teeth/horns white; schematic geometry does not reproduce painted animal detail.','Broad front roof slopes orange; thin colored cornices and finials neutral.','Only short front rail bands off-white; repeated 7.4mm posts neutral.','Rear/ground/unknown fields neutral; no pond or vegetation.','Six labels are not a verified four-filament slicer project.']},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(mesh.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q,flush=True)
