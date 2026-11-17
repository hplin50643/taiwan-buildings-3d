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
 groups=[('roof_slab_left_fascia_continuity',2,bound(-68.5,68.5,-43.5,41.5,58.3,60.8)&vertical&plane(0,-68.5)),('roof_slab_right_fascia_continuity',2,bound(-68.5,68.5,-43.5,41.5,58.3,60.8)&vertical&plane(0,68.5)),('roof_slab_rear_fascia_inferred',2,bound(-68.5,68.5,-43.5,41.5,58.3,60.8)&vertical&plane(1,41.5)),('folded_right_fascia_outer_continuity',2,bound(64.4,67.6,-43,43,38,58.5)&vertical&plane(0,67.6))]
 records=[]
 for name,k,m in groups:
  m=m&(c==0);ids=np.flatnonzero(m);c[m]=k;w[m]=name;records.append({'component':name,'material':k,'face_ids':ids.tolist(),'count':len(ids)})
 assert np.array_equal(c[before!=0],before[before!=0]);assert all(g['count'] for g in records)
 (A/'qa-continuous-walls').mkdir(exist_ok=True)
 (A/'qa-continuous-walls/selection.json').write_text(json.dumps({'method':'Whole original vertical triangles on the original roof slab side/rear vertical fascia and outer folded fascia plane. Existing nonzero assignments preserved. No roof or underside recolored. No new photo evidence; same-component material inference only.','groups':records,'changed_faces':int(np.sum(c!=before))},indent=2)+'\n')
 return c,w

def main():
 old.classify=classify;old.main()
 p=A/'palette.json';d=json.loads(p.read_text());d['scope']='Roof-slab side/rear vertical fascia and right folded fascia outer plane use original pale-gray facade family. Original source photograph supports right fold pale appearance; unseen back/left fascia is material continuity inference. Glazing, frames, slab top/soffit, folded underside, staircase, rear service wall and base preserved.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
