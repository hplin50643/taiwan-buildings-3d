"""Original whole face domains; no geometry edits or tower z cut."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='e2d5852fbacec11765fe1fcdd1574f1bdac637b41c9ed2f6e68ada603d890b5e';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==990
t=m.triangles;lo=t.min(1);hi=t.max(1);n=m.face_normals;a=np.full(len(t),2,np.int32);e=.003
pal=[('Observed whole low sail front muted warm taupe','#A49A86'),('Observed separate grid and aperture reveals muted stone gray','#AAACA5'),('UNVERIFIED mixed tower walls window backs roof and rear neutral','#B8BAB5')]
def plane(k,v):return np.max(abs(t[:,:,k]-v),axis=1)<e
def bound(x0,x1,y0,y1,z0,z1):return(lo[:,0]>=x0-e)&(hi[:,0]<=x1+e)&(lo[:,1]>=y0-e)&(hi[:,1]<=y1+e)&(lo[:,2]>=z0-e)&(hi[:,2]<=z1+e)
sail=plane(1,-38)&bound(-43,40,-38,-38,3,50.7)&(n[:,1]<-.999);a[sail]=0
grid=np.zeros(len(t),bool)
for x in [-60,-36,-12,12,36]:
 mask=bound(x-1.5,x+1.5,-23.5,-21.5,26,95)&(plane(1,-23.5)|plane(0,x-1.5)|plane(0,x+1.5)|plane(2,26)|plane(2,95));grid|=mask
for z in [51,74,94]:
 mask=bound(-62,46,-23.5,-21.5,z,z+3)&(plane(1,-23.5)|plane(0,-62)|plane(0,46)|plane(2,z)|plane(2,z+3));grid|=mask
a[grid]=1
apertures=[]
for x in [49.5,58.5]:
 for z in [100,118]:
  mask=bound(x-3,x+3,-22,-2,z,z+14)&((plane(0,x-3)&(n[:,0]>.999))|(plane(0,x+3)&(n[:,0]<-.999))|(plane(2,z)&(n[:,2]>.999))|(plane(2,z+14)&(n[:,2]<-.999)))
  assert mask.sum()==8,(x,z,mask.sum());a[mask]=1;apertures.extend(np.flatnonzero(mask).tolist())
# Enforce entire connected coplanar material domains; left beam ends merge into unknown sidewall.
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999
cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);corrected=[]
for comp in cs:
 if len(set(a[comp]))>1:
  corrected.extend(comp[a[comp]!=2].tolist());a[comp]=2
assert len(corrected)==9;grid &= a==1
assert sail.sum()>0 and grid.sum()>0
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':{'whole_sail_front':np.flatnonzero(sail).tolist(),'independent_grid':np.flatnonzero(grid).tolist(),'four_tower_hole_reveals':apertures},'coplanar_neutralized_faces':sorted(corrected),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'990 original triangles unchanged','limits':['Whole sail front plane only; seven windowbackings and reveals excluded.','Original grid box surface planes only, no mainwall sameheight tint.','Tower hole interior only; entire mixed exterior shell neutral, never z100 cut.','All window reflections/frames/curtains neutral.','Three labels not verified four-filament slicing.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':990,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],{k:len(v)for k,v in q['domain_face_indices'].items()})
