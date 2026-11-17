"""Same-component color inference; original geometry and existing colored faces retained."""
import build_appearance as old
import numpy as np,json,hashlib
A=old.A
base_classify=old.classify

def classify(t):
 c,w=base_classify(t);before=c.copy();lo=t.min(1);hi=t.max(1)
 normal=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);vertical=np.abs(normal[:,2])<1e-7
 def bound(x1,x2,y1,y2,z1,z2):return (lo[:,0]>=x1-.004)&(hi[:,0]<=x2+.004)&(lo[:,1]>=y1-.004)&(hi[:,1]<=y2+.004)&(lo[:,2]>=z1-.004)&(hi[:,2]<=z2+.004)
 def plane(ax,val):return np.all(abs(t[:,:,ax]-val)<.004,axis=1)
 groups=[('high_wing_rear_tile_inferred',1,bound(-65.5,3.5,-34,48,3,77)&vertical&plane(1,48)),('high_wing_right_tile_inferred',1,bound(-65.5,3.5,-34,48,3,77)&vertical&plane(0,3.5)),('low_wing_rear_tile_inferred',1,bound(3.5,68.5,-34,20,3,42)&vertical&plane(1,20)),('low_wing_right_tile_inferred',1,bound(3.5,68.5,-34,20,3,42)&vertical&plane(0,68.5))]
 records=[]
 for name,k,m in groups:
  m=m&(c==0);ids=np.flatnonzero(m);c[m]=k;w[m]=name;records.append({'component':name,'material':k,'face_ids':ids.tolist(),'count':len(ids)})
 assert np.array_equal(c[before!=0],before[before!=0]);assert all(g['count'] for g in records)
 (A/'qa-continuous-walls').mkdir(exist_ok=True)
 (A/'qa-continuous-walls/selection.json').write_text(json.dumps({'method':'Whole original vertical triangles on the rear/right exterior planes of the two original wing volumes. Existing nonzero assignments preserved. No roof or underside recolored. No new photo evidence; same-component material inference only.','groups':records,'changed_faces':int(np.sum(c!=before))},indent=2)+'\n')
 return c,w

def main():
 old.classify=classify;old.main()
 p=A/'palette.json';d=json.loads(p.read_text());d['scope']='High and low wing rear/right exterior vertical planes extended with the original cool-offwhite tile material. Same-component inference, not new photographic evidence. Existing gray projected grid, pavilion members, window backs, passage, roofs, base and geometry preserved.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
