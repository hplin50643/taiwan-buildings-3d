from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify;assert len(old.PALETTE)==7
old.PALETTE.append(('d1_lower_steps_gray_background_approximation','#979C94'))
TARGET=[523, 526, 533, 534, 538, 539, 551, 552, 555, 556, 557, 558]
def classify(tri):
 colors,why=original_classify(tri);assert len(tri)==4476 and np.bincount(colors).tolist()==[2051,832,225,35,92,610,631]
 assert (colors[TARGET]==0).all();colors[TARGET]=7;why[TARGET]='bounded_D1_lower_three_steps_gray_background'
 assert np.bincount(colors).tolist()==[2039,832,225,35,92,610,631,12];return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='Only D1 lowest three tread and front riser complete domains12faces to new7 #979C94/.88, original7 shaders unchanged. Source0 D1 grey background distinguished from cream skirts; source1 D2 not substitute. Original14 coarse levels and11.5 width are not surveyed actual steps. Real middle landing/thin nosings/rails/joints unmodelled; no geometry repair. Exclude upper11steps/platforms/skirts/base/D2 stairs. EXIF self-reported2025-03-02: OffsetTime/OffsetTimeDigitized+08:00, OffsetTimeOriginal absent; not independently verified capture timezone/date or2026 condition. Historical QA/manufacturing limitations preserved. Fresh continuation not recovery.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
