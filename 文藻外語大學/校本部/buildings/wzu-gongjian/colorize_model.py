"""Original full-face material assignment only. No final geometry edits."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from shapely.geometry import Polygon,LineString
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='240fd8e4f8c04f5be804fc3492849de4fcbe6fd911200fc432443fb6e7329ffa';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==4976
t=m.triangles;lo=t.min(1);hi=t.max(1);n=m.face_normals;a=np.full(len(t),2,np.int32);e=.003
pal=[('Observed independent octagonal rings and front right rails warm gray','#BEB9AA'),('Observed entry front right true hip slopes muted green','#445B4A'),('UNVERIFIED mixed shell glazing lip and rear neutral','#B8BAB5')]
def bound(x0,x1,y0,y1,z0,z1):return(lo[:,0]>=x0-e)&(hi[:,0]<=x1+e)&(lo[:,1]>=y0-e)&(hi[:,1]<=y1+e)&(lo[:,2]>=z0-e)&(hi[:,2]<=z1+e)
def plane(k,v):return np.max(abs(t[:,:,k]-v),axis=1)<e
relief=[]
for xx in [9,21,38,50]:
 for z in [37,60]:
  outer=[(xx-5,z+1),(xx-4,z),(xx+4,z),(xx+5,z+1),(xx+5,z+5),(xx+4,z+6),(xx-4,z+6),(xx-5,z+5)]
  inner=[(xx-3.8,z+1.5),(xx-3.2,z+1.1),(xx+3.2,z+1.1),(xx+3.8,z+1.5),(xx+3.8,z+4.5),(xx+3.2,z+4.9),(xx-3.2,z+4.9),(xx-3.8,z+4.5)]
  ring=Polygon(outer,[inner]);mask=bound(xx-5,xx+5,-26.7,-25,z,z+6)
  for i in np.flatnonzero(mask):
   pts=t[i][:,[0,2]];poly=Polygon(pts)
   # Same original ring member only; no backing inside the octagonal hollow.
   shape=poly if poly.area>1e-7 else LineString(pts)
   if ring.buffer(.002).covers(shape):relief.append(int(i))
a[relief]=0
rails=[]
# All vertices above source terrace rail bottom; no low eave lip or roof deck.
for mask in [bound(-63.05,63.05,-29.05,-26.95,94.4,101),bound(61.15,63.05,-29.05,45.15,94.4,101)]:rails.extend(np.flatnonzero(mask).tolist())
rails=sorted(i for i in set(rails) if not (abs(n[i,2]-1)<.001 and np.max(abs(t[i,:,2]-94.6))<.003));a[rails]=0
# Genuine upper hip planes from exact original scale_top .72/.03.
z=t[:,:,2];front=(np.max(abs(z-(21+(t[:,:,1]+41)*4.8/9.7)),axis=1)<e);right=(np.max(abs(z-(21+(27-t[:,:,0])*4.8/8.12)),axis=1)<e)
hip=bound(-31,27,-41,-21,21,25.8)&(n[:,2]>0)&(front|right);a[hip]=1
assert len(relief)>0 and len(rails)>0 and hip.sum()>0
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':{'right_octagonal_rings':sorted(set(relief)),'front_right_rails':rails,'entry_front_right_hip':np.flatnonzero(hip).tolist()},'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'4976 original triangles unchanged','limits':['Only right independent ring members, no hollow backing or fullheight mixedwall.','Only above94.4 front/right rails; roofdeck and mixedlip neutral.','Green only actual upward analytic front/right entry hip planes.','Undated differing window frames allneutral; no invented preferred date.','Three material labels not a verified four-filament slicing job.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':4976,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print({k:len(v)for k,v in q['domain_face_indices'].items()},q['palette'])
