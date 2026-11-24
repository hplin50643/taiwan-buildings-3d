"""Extend same outer upper rim to positive-y side; no wall/panel inference."""
from pathlib import Path
import importlib.util,json,numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('current',S/'build_current.py');cur=importlib.util.module_from_spec(sp);sp.loader.exec_module(cur);prior=cur.old.classify

def classify(t):
 c,w=prior(t);lo=t.min(1);hi=t.max(1);n=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);n/=np.linalg.norm(n,axis=1)[:,None]
 mask=np.zeros(len(t),bool)
 for j in range(144):
  a=2*np.pi*(j+.5)/144
  residual=(t[:,:,0]/61.5)*np.cos(a)+(t[:,:,1]/41.5)*np.sin(a)-np.cos(np.pi/144)
  out=np.array([np.cos(a)/61.5,np.sin(a)/41.5,0]);out/=np.linalg.norm(out)
  mask|=np.all(abs(residual)<2e-7,axis=1)&(n@out>.999999)
 mask&=(lo[:,1]>=-.00001)&(hi[:,0]<=-20.49999)&(lo[:,2]>=82.99999)&(hi[:,2]<=84.80001)&(c==0)
 assert mask.sum()==58
 c[mask]=4;w[mask]='inferred_same_outer_upper_rim_positive_y_continuity_not_independent_photo'
 return c,w
cur.old.classify=classify
if __name__=='__main__':
 cur.old.main();p=A/'palette.json';j=json.loads(p.read_text());j['scope']='Original front foyer and58 negative-y upper rim faces plus same outer upper rim positive-y facets by continuity inference. Roof top, inner/bottom/end faces and all full-height/mixed-panel walls unchanged. Not independent positive-y photographic evidence.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
