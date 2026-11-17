"""Same-component color inference; original geometry and existing colored faces retained."""
import build_appearance as old
import numpy as np,json,hashlib
A=old.A
base_classify=old.classify

def classify(t):
 c,w=base_classify(t);before=c.copy();lo=t.min(1);hi=t.max(1)
 normal=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);vertical=np.abs(normal[:,2])<1e-7
 def bound(x1,x2,y1,y2):return (lo[:,0]>=x1-.004)&(hi[:,0]<=x2+.004)&(lo[:,1]>=y1-.004)&(hi[:,1]<=y2+.004)&(lo[:,2]>=16-.004)&(hi[:,2]<=39+.004)
 def plane(ax,val):return np.all(abs(t[:,:,ax]-val)<.004,axis=1)
 groups=[('left_metal_box_side_rear_inferred',1,bound(-65,-31,-26,26)&vertical&(plane(0,-31)|plane(1,26))),('right_metal_box_side_rear_inferred',1,bound(40,68,-20,28)&vertical&(plane(0,40)|plane(1,28)|((lo[:,0]>=67.675-.004)))),('central_concrete_box_side_rear_inferred',2,bound(-25.5,33.5,-28,24)&vertical&(plane(0,-25.5)|plane(1,24)))]
 records=[]
 for name,k,m in groups:
  m=m&(c==0);ids=np.flatnonzero(m);c[m]=k;w[m]=name;records.append({'component':name,'material':k,'face_ids':ids.tolist(),'count':len(ids)})
 assert np.array_equal(c[before!=0],before[before!=0]);assert all(g['count'] for g in records)
 (A/'qa-continuous-walls').mkdir(exist_ok=True)
 (A/'qa-continuous-walls/selection.json').write_text(json.dumps({'method':'Whole original vertical triangles bounded within each original upper gallery box. Existing nonzero assignments preserved. No roof or underside recolored. No new photo evidence; same-component material inference only.','groups':records,'changed_faces':int(np.sum(c!=before))},indent=2)+'\n')
 return c,w

def main():
 old.classify=classify;old.main()
 p=A/'palette.json';d=json.loads(p.read_text());d['scope']='Upper gallery box vertical side/rear walls extended using each box existing front material: silver-gray metal on left/right boxes; warm concrete on central box. Same-component inference, not verified rear-photo evidence. Original colored faces, roof, underside, ground-level walls and geometry preserved.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
