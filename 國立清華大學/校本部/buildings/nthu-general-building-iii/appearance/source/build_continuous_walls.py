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
 groups=[('main_wing_left_outer_wall_inferred',1,bound(-63,63,-38.5,4.5,3,105)&vertical&plane(0,-63)),('main_wing_rear_wall_inferred',1,bound(-63,23,-38.5,4.5,3,105)&vertical&plane(1,4.5)),('return_inner_wall_inferred',1,bound(23,63,4.5,62.5,3,105)&vertical&plane(0,23)),('combined_right_outer_wall_inferred',1,bound(-63,63,-38.5,62.5,3,105)&vertical&plane(0,63)),('return_end_wall_inferred',1,bound(23,63,4.5,62.5,3,105)&vertical&plane(1,62.5))]
 records=[]
 for name,k,m in groups:
  m=m&(c==0);ids=np.flatnonzero(m);c[m]=k;w[m]=name;records.append({'component':name,'material':k,'face_ids':ids.tolist(),'count':len(ids)})
 assert np.array_equal(c[before!=0],before[before!=0]);assert all(g['count'] for g in records)
 (A/'qa-continuous-walls').mkdir(exist_ok=True)
 (A/'qa-continuous-walls/selection.json').write_text(json.dumps({'method':'Whole original vertical triangles on the side/rear exterior planes of the original L-shaped building volumes. Existing nonzero assignments preserved. No roof or underside recolored. No new photo evidence; same-component material inference only.','groups':records,'changed_faces':int(np.sum(c!=before))},indent=2)+'\n')
 return c,w

def main():
 old.classify=classify;old.main()
 p=A/'palette.json';d=json.loads(p.read_text());d['scope']='Only exact side/rear vertical exterior wall planes of the L-shaped original volumes use the existing ivory front structure color. Same-component material inference, not additional side/rear photograph proof. Mixed recessed window backs, original frames, roofs, base, entrance, steps, all existing color and geometry unchanged.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
