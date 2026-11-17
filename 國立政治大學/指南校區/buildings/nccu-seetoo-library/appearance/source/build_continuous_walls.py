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
 for x in [-5,60]:
  sides=plane(0,x-.75)|plane(0,x+.75)
  tips=plane(1,49)&((hi[:,2]<=50.504)|(lo[:,2]>=52.096))
  groups.append(('upper_straight_row_end_fin_'+str(x)+'_inferred',1,bound(x-.75,x+.75,44,49,39,63)&(sides|tips)))
 panel=bound(0,6.7,-51,-41.2,39,63)&vertical
 frontline=-51+4*t[:,:,0]/6.7
 inside=np.all((t[:,:,1]>=frontline-.004)&(t[:,:,1]<=frontline+5.8+.004),axis=1)
 rear=np.all(abs(t[:,:,1]-(frontline+5.8))<.004,axis=1)
 groups.append(('central_upper_canted_panel_side_returns_inferred',2,panel&inside&(plane(0,0)|plane(0,6.7)|rear)))
 records=[]
 for name,k,m in groups:
  m=m&(c==0);ids=np.flatnonzero(m);c[m]=k;w[m]=name;records.append({'component':name,'material':k,'face_ids':ids.tolist(),'count':len(ids)})
 assert np.array_equal(c[before!=0],before[before!=0]);assert all(g['count'] for g in records)
 (A/'qa-continuous-walls').mkdir(exist_ok=True)
 (A/'qa-continuous-walls/selection.json').write_text(json.dumps({'method':'Whole original vertical triangles on the same straight-row end fins and central canted panel side returns. Existing nonzero assignments preserved. No roof or underside recolored. No new photo evidence; same-component material inference only.','groups':records,'changed_faces':int(np.sum(c!=before))},indent=2)+'\n')
 return c,w

def main():
 old.classify=classify;old.main()
 p=A/'palette.json';d=json.loads(p.read_text());d['scope']='Two end fins of the existing upper straight lake-facing row use its brown family; side returns of the already colored central upper entrance canted panel use its existing warm gray. Same-component material continuity inference only. Horizontal beams, lower/diagonal/other fins, roofs, adjacent panels and all original colored faces preserved.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
