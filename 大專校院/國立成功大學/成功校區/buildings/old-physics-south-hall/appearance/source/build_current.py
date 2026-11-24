"""Current bounded front hip slope, original classifier retained."""
from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify;assert len(old.PALETTE)==8
old.PALETTE.append(('front_roof_graybrown_background_approximation','#79776D'))
def classify(tri):
 colors,why=original_classify(tri);assert len(tri)==2436 and np.bincount(colors).tolist()==[544, 439, 4, 1160, 224, 10, 33, 22]
 assert (colors[[943,953]]==0).all();colors[[943,953]]=8;why[[943,953]]='bounded_front_hip_graybrown_background'
 assert np.bincount(colors).tolist()==[542, 439, 4, 1160, 224, 10, 33, 22, 2];return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='Only largest front hip slope two faces to new8 #79776D/.88; original eight shaders unchanged. Source0 gray-brown tile family with tree occlusion and cropped ends permits bounded same-slope background approximation, not every point directly seen. Source1 entrance is not roof evidence. Exclude thin front strip, side/rear hips, eaves/underside, walls and canopy. Coarse roof pitch/depth and missing tile rows retained; not measured color/tile species/current2026 condition. EXIF self-reported2023-11-12 without explicit offset; upload2023-11-13 distinct. Historical QA/manufacturing limits unchanged.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
