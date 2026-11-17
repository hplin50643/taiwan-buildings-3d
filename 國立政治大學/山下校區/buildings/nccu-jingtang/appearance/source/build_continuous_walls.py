"""Original main curved wall external plane material continuity inference."""
import build_appearance as old
import numpy as np,json
A=old.A
base_classify=old.classify

def classify(v):
 c,w=base_classify(v);before=c.copy();eps=.0003
 actual=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);n=actual/np.linalg.norm(actual,axis=1)[:,None]
 sel=np.zeros(len(v),bool)
 for i in range(80):
  th=(i+.5)*np.pi/80;u=np.array([np.cos(th),np.sin(th)]);rel=v[:,:,:2]-[0,-28];d=rel@u;t=np.array([-np.sin(th),np.cos(th)]);s=rel@t
  m=(abs(d-65*np.cos(np.pi/160))<eps).all(1)&(abs(s)<=65*np.sin(np.pi/160)+eps).all(1)&(v[:,:,2]>=3-eps).all(1)&(v[:,:,2]<=57+eps).all(1)&(abs(n[:,2])<eps)&((n[:,:2]@u)>.99)
  sel|=m
 ends=np.zeros(len(v),bool)
 for lo,hi in [(-65,-43),(43,65)]:
  ends|=(abs(v[:,:,1]+28)<eps).all(1)&(v[:,:,0]>=lo-eps).all(1)&(v[:,:,0]<=hi+eps).all(1)&(v[:,:,2]>=3-eps).all(1)&(v[:,:,2]<=57+eps).all(1)&(abs(n[:,2])<eps)
 records=[]
 for name,m in [('main_outer_arc_wall_inferred',sel),('main_end_walls_inferred',ends)]:
  m=m&(c==0);ids=np.flatnonzero(m);c[m]=1;w[m]=name;records.append({'component':name,'material':1,'face_ids':ids.tolist(),'count':len(ids)})
 assert np.array_equal(c[before!=0],before[before!=0]);assert all(g['count'] for g in records)
 (A/'qa-continuous-walls').mkdir(exist_ok=True)
 (A/'qa-continuous-walls/selection.json').write_text(json.dumps({'method':'Every original triangle must lie on an exact main outer arc facet or bounded end wall plane. Excludes roof, crown, appendage, openings and original colored faces. Same-component inference, not newly photographed rear evidence.','groups':records,'changed_faces':int(np.sum(c!=before))},indent=2)+'\n')
 return c,w

def main():
 old.classify=classify;old.main()
 p=A/'palette.json';d=json.loads(p.read_text());d['scope']='Original white inner walls and columns retained; exact main outer arc and end wall facets inferred with existing white material. Detached-region rear appendage, roof/crown, window recesses, canopy, base and all geometry remain unchanged. This is material continuity inference, not new rear photograph evidence.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
