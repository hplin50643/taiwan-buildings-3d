from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify;assert len(old.PALETTE)==9
TARGET=[455, 458, 460, 462, 465, 467]
def classify(tri):
 colors,why=original_classify(tri);assert len(tri)==6918 and np.bincount(colors).tolist()==[3146, 601, 1034, 264, 2, 380, 132, 1264, 95]
 assert (colors[TARGET]==0).all();colors[TARGET]=2;why[TARGET]='bounded_E1_lower_three_front_risers_gray_background'
 assert np.bincount(colors).tolist()==[3140, 601, 1040, 264, 2, 380, 132, 1264, 95];return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='Only E1 lowest three front riser complete domains6 original neutral faces to existing cool_gray_infill index2 #A0A8A5/.78. Existing gray tread surfaces remain unchanged. Original9 shaders/all other6912 assignments retained. Exclude side skirts/base/upper14 steps/platforms/E2/E3 and railings. Two fresh official source photos inspected as complete1600 downsample, source0 originalpixel600x500 staircase crop and nativefront original1200 viewed. Both photos show the front E1 staircase; source0 is primary, source1 similar view supporting its gray family, not independent survey. Gray fronts distinguish warmcream skirt; rail shadows/white wear not treated as separately calibrated materials. Original stairs(-14,3,-57,-32,3,15.7,17) is17 coarse levels17 width. Real middle landing/thin nosings/railings/joints not modeled, not surveyed actual step count or per-riser registration. First riser starts base z3; original overlap.08 hidden by next box. Keep geometry and all missing details unchanged. New fullplane-normal/sharededgeBFS from geometric interior seed, forward triangle containment and reverse support union. Nonzero float32 differences explicitly retained, not zero. EXIF self-reports2025:03:02 15:10:48 and2025:03:10 13:44:30. OffsetTime/OffsetTimeDigitized+08:00; OffsetTimeOriginal absent. Not independently verified capture dates/timezone or2026 condition. 33 current original blobs/sole app21/ZIP6 allsame/noOBJ/no rootSHA/6918faces3453vertices/native4CPU48. Original existing nine-material scope, historyQA/current README retained. No public private-source image/path/hash.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
