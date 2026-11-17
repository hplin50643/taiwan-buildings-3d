"""Complete original upper portal side triangles; same-component material inference."""
import build_appearance as old
import numpy as np,json
A=old.A
base_classify=old.classify

def classify(t):
 c,w=base_classify(t);before=c.copy();lo=t.min(1);hi=t.max(1)
 normal=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);vertical=np.abs(normal[:,2])<1e-7
 def bound(x1,x2,y1,y2,z1,z2):return (lo[:,0]>=x1-.004)&(hi[:,0]<=x2+.004)&(lo[:,1]>=y1-.004)&(hi[:,1]<=y2+.004)&(lo[:,2]>=z1-.004)&(hi[:,2]<=z2+.004)
 def plane(ax,val):return np.all(abs(t[:,:,ax]-val)<.004,axis=1)
 groups=[]
 for x in [-11,11]:groups.append(('upper_portal_upright_'+str(x)+'_sides_inferred',2,bound(x-1,x+1,-4.5,-1.5,13.3,26.5)&vertical&(plane(0,x-1)|plane(0,x+1))))
 groups.append(('upper_portal_lintel_ends_inferred',2,bound(-13.5,13.5,-4.8,-1.8,26.5,28)&vertical&(plane(0,-13.5)|plane(0,13.5))))
 records=[]
 for name,k,m in groups:
  m=m&(c==0);ids=np.flatnonzero(m);c[m]=k;w[m]=name;records.append({'component':name,'material':k,'face_ids':ids.tolist(),'count':len(ids)})
 assert np.array_equal(c[before!=0],before[before!=0]);assert all(g['count'] for g in records)
 (A/'qa-continuous-walls').mkdir(exist_ok=True)
 (A/'qa-continuous-walls/selection.json').write_text(json.dumps({'method':'Original complete side triangles bounded to the upper two portal uprights and lintel ends. Does not select window returns or subdivide faces. Same-component inference, not new photo evidence.','groups':records,'changed_faces':int(np.sum(c!=before))},indent=2)+'\n')
 return c,w

def main():
 old.classify=classify;old.main()
 p=A/'palette.json';d=json.loads(p.read_text());d['scope']='Original roof slopes and portal front assignments preserved. Upper portal upright sides and lintel ends inferred with the existing gray material only; window returns, other wall fields, roofs, base, lower piers and all geometry unchanged.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
