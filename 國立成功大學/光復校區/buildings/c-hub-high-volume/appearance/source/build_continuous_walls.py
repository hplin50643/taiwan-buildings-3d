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
 groups=[]
 for j,eq in enumerate([[-0.9976378994757635, 0.06235236871723522, -0.02882366466874232, -43.5630694745253], [-0.9987344843937248, 0.0188440468753533, -0.04662972850189395, -42.339255444390844], [0.06047540526443885, 0.9978441868632411, -0.0254892938572074, -25.325751258878416], [0.07667898065672123, 0.996826748537376, -0.021372115614721757, -25.16540550077859], [-0.056501578906166715, 0.998194560675612, -0.020376226803125487, -26.74149120342935], [-0.03699619287293694, 0.9988972075692976, -0.028907618773744873, -26.44243819545193]]):
  eq=np.array(eq);m=np.all(abs(t@eq[:3]+eq[3])<.005,axis=1)&(lo[:,2]>=2.999)&(hi[:,2]<=150.001)
  groups.append(("original_loft_left_rear_facet_"+str(j)+"_concrete_inferred",1,m))
 records=[]
 for name,k,m in groups:
  m=m&(c==0);ids=np.flatnonzero(m);c[m]=k;w[m]=name;records.append({'component':name,'material':k,'face_ids':ids.tolist(),'count':len(ids)})
 assert np.array_equal(c[before!=0],before[before!=0]);assert all(g['count'] for g in records)
 (A/'qa-continuous-walls').mkdir(exist_ok=True)
 (A/'qa-continuous-walls/selection.json').write_text(json.dumps({'method':'Whole original slightly inclined shell triangles on the six original convex-loft boundary planes forming the left/rear concrete shell. Existing nonzero assignments preserved. No roof or underside recolored. No new photo evidence; same-component material inference only.','groups':records,'changed_faces':int(np.sum(c!=before))},indent=2)+'\n')
 return c,w

def main():
 old.classify=classify;old.main()
 p=A/'palette.json';d=json.loads(p.read_text());d['scope']='Only original left/rear convex-loft shell facets extend existing exposed-concrete color by same-component inference; no new left/rear photo evidence. Exact whole-triangle coplanarity checked against original generator hulls. Window backs and reveals, roof, base, all existing colors and geometry preserved.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
