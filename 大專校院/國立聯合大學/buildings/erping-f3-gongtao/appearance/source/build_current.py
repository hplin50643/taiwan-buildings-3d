from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify;assert len(old.PALETTE)==8
old.PALETTE.append(('entrance_riser_gray_background','#9DA29B'))
TARGET=[6760, 6764, 6777, 6785, 6802, 6808]
def classify(tri):
 colors,why=original_classify(tri);assert len(tri)==7840 and np.bincount(colors).tolist()==[3174, 1463, 665, 1401, 94, 287, 46, 710]
 assert (colors[TARGET]==0).all();colors[TARGET]=8;why[TARGET]='bounded_F3_upper_three_entrance_risers_gray_background'
 assert np.bincount(colors).tolist()==[3168, 1463, 665, 1401, 94, 287, 46, 710, 6];return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='僅F3原入口短階i2–4上三前立完整域6面→新8 entrance_riser_gray_background #9DA29B/.88，原8shader與所有踏/側面/其他面不改，不稱真最低三級。 source1主證及source0正面輔證，兩3072×2048當次GET200保留，親看各完整1600縮覽、source1原像素470×230階局部及nativefront1200；灰短階與下方褐長階/紅鋪地分離，不借鄰館。 原add(0,-17+i*1.3,7+i*.65,16,2,.85)五階為粗代理，真級數/鼻緣/接縫/顆粒未建，顏色只灰背景族非校準測色或石種鑑定，不把陰影烘成深材。 只i2–4前向平面，完整BFS與每三角/反覆蓋核；原平台7.8吞i0大部，圓環切頂8.05干擾i1，均排除且不修復。選三立底8.5/9.15/9.8，頂9.15/9.8/10.45，原浮點非零外逸/反缺保留。 不染入口上平台/門/牌匾/踏面/側裙、前方褐長階/圓廣場、屋頂PV或側後；已配8材維持，照片不證PV頂不能猜深藍。 兩EXIF自報日期時間依fresh-metadata原欄；Originaloffset缺失不借OffsetTime/Digitized+08，不當2026現況。 本段為已核定後現行六面材質範圍，原幾何/材質/歷史QA與README保持。';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
