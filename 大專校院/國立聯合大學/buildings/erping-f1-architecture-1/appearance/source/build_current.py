from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify;assert len(old.PALETTE)==7
TARGET=[1408, 1409]
def classify(tri):
 colors,why=original_classify(tri);assert len(tri)==1524 and np.bincount(colors).tolist()==[817, 314, 281, 32, 2, 70, 8]
 assert (colors[TARGET]==0).all();colors[TARGET]=2;why[TARGET]='bounded_F1_central_canopy_front_pale_background'
 assert np.bincount(colors).tolist()==[815, 314, 283, 32, 2, 70, 8];return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='僅原中央入口棚前垂直完整矩形域兩面1408/1409，0→既有pale_frame_sign_fascia2 #C3C7C4/.78，不延左右側/頂/底或門框。 當次source1斜照主證與source0正照輔證，兩3072×2048保留、親看完整1600縮覽及source1原像素440×430局部、nativefront1200。右端鄰招牌局部遮擋僅同一前帶有限延續，不稱每點全實見。 真棚為內凹頂盤/邊牆，原為實板；只前帶淺灰背景近似，黑內盤、風化條紋、薄金屬與排水細節未建不修復、不把陰影烘入材質。原16寬2高8.5露深與棚位置比例非測繪。 原add(8,-18,19,16,9,2)在y−22.5形成完整x0..16/z19..21矩形，其他host/doorcut/shop/annex不交此平面。完整BFS與每三角包含/反覆蓋實核，不裁面。 真中央入口為斜坡而原有三階，保持原錯近似不授灰階；前庭長階有局部插階/轉折原未建，不套本棚證據。 兩EXIF Original自報2025-02-28 10:26:40與10:25:39，Originaloffset缺失；OffsetTime/Digitized+08不能代填，非2026現況。 範圍僅F1，排左F2及右後H1，既有七材原shader、geometry/STL/面序、歷史QA與README表格保持；不新增商標或文字。 現可讀21prefix精確排除、歷史全索引缺不稱全庫已核；私源不公開，不改凍包/index、不發布。';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
