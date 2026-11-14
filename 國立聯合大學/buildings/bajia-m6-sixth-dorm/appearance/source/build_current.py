from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify;assert len(old.PALETTE)==5
old.PALETTE.append(('rear_parapet_light_background_approximation','#D1D3C9'))
TARGET=[6965, 6966, 6969, 6970]
def classify(tri):
 colors,why=original_classify(tri);assert len(tri)==7000 and np.bincount(colors).tolist()==[1729, 2230, 240, 2545, 256]
 assert (colors[TARGET]==0).all();colors[TARGET]=5;why[TARGET]='bounded_M6_rear_parapet_inward_light_background'
 assert np.bincount(colors).tolist()==[1725, 2230, 240, 2545, 256, 4];return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='Only complete original rear parapet inward vertical face, four neutral0 faces to new5 rear_parapet_light_background_approximation #D1D3C9/.88. Original5 shaders and other6996 assignments unchanged. Exclude topcap/backface/front brick parapet, roof paving, hip tiles, canopy, stairs and all other surfaces. Personally viewed source0/1 complete1600 downsample images, source0 originalpixel1450x270 crop and nativefront1200. Source0 directly shows white inward rear wall background on both sides; central tower hides central segment. Extending the same wall background through its hidden middle is a limited same-component inference, not full direct visibility. Source1 lower angle does not substitute roofwall evidence. Real gray narrow cap and black lower weatherproofing/weathering band differ from the light wall. Original coarse1.8 parapet with only1.6 exposed above slab lacks separate fineband boundaries. Light background approximation does not certify a uniformly white real component or repair cap/base bands. No shadow baking, calibrated color or coating-species certification. Original add(0,56.9,68.5,82,1.2,1.8), inward plane y56.3, is clipped by roofslab up to68.7 and two original hips at both ends. Complete fullplane/shared-edge BFS and original box-minus-slab/hip XZ support checked in both directions; nonzero float32 outside/missing values preserved, tolerance .001mm2. Source0 EXIF DateTimeOriginal2025:03:10 15:37:24 and source1 15:37:09 selfreported; Originaloffset absent, OffsetTime/OffsetTimeDigitized+08:00 do not supply Originaloffset. Dates/timezones not independently verified, not proof of2026 condition. Scope is current M6 U-shaped Sixth Dormitory, not M10/M11 or separate round hall. Original five material system, bounded tiled-roof inference, unconfirmed outerwalls/backside and manufacturing limitations retained. No residents/indoor/access details included.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
