"""Same central parapet vertical-face stone continuity; inferred, not new evidence."""
from pathlib import Path
import importlib.util,json,numpy as np
S=Path(__file__).resolve().parent;A=S.parent
s=importlib.util.spec_from_file_location('original',S/'build_appearance.py');old=importlib.util.module_from_spec(s);s.loader.exec_module(old);prior=old.classify
ADDED=[5065,5066,5073,5075,5076,5077,5079,5080,5081,5082,5089,5091,5093,5095,5096,5097,5098,5100,5101,5103,5104,5107,5108,5109,5110,5112,5113,5115,5117,5118,5120,5121,5123,5125,5128,5129,5130,5131,5132,5133,5135]
def classify(t):
 c,w=prior(t);lo=t.min(1);hi=t.max(1);n=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);n/=np.linalg.norm(n,axis=1)[:,None]
 mask=(lo[:,0]>=-22.0002)&(hi[:,0]<=22.0002)&(lo[:,1]>=-23.5002)&(hi[:,1]<=-6.4998)&(lo[:,2]>=83.9998)&(hi[:,2]<=91.8002)&(abs(n[:,2])<.001)&(c==0)
 assert np.where(mask)[0].tolist()==ADDED
 c[mask]=2;w[mask]='inferred_same_central_crest_vertical_side_and_back_stone_continuity_not_photo_verified'
 return c,w
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['scope']='Existing front appearance plus41 same central crest vertical side/rear faces by inferred stone continuity. Top horizontal surfaces, low roof gable, cropped building ends/rear and all other indices unchanged. Not independently photo-verified side/rear material.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
