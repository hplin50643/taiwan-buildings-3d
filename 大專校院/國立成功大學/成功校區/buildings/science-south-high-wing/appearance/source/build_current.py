from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify;assert len(old.PALETTE)==2
old.PALETTE.append(('frame_front_graywhite_background_approximation','#C4C6BD'))
TARGET=[1214, 1215, 1216, 1218, 1219, 1220, 1221, 1222, 1223, 1224, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1234, 1235, 1236, 1237, 1238, 1239, 1240, 1242, 1244, 1245, 1247, 1248, 1249, 1250, 1251, 1252, 1253, 1254, 1255, 1256, 1258, 1259, 1260, 1261, 1262, 1263, 1264, 1265, 1266, 1267, 1268]
def classify(tri):
 colors,why=original_classify(tri);assert len(tri)==5324 and np.bincount(colors).tolist()==[4004,1320]
 assert (colors[TARGET]==0).all();colors[TARGET]=2;why[TARGET]='bounded_third_frame_front_graywhite_background'
 assert np.bincount(colors).tolist()==[3956,1320,48];return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='Only lowest-row third frame complete front ring48faces to new2 #C4C6BD/.88. Original two shaders and green coarse louvres unchanged. Architect image2 front grey-white family is distinguishable; grouped closed green leaves within selected frame, open corridor in adjacent right frame. Do not paint deep backing, sides, underside or other frames. Original26mm wide coarse box and five strips not per-box survey. No calibrated color or material certification. Six current images have no EXIF capture dates; page2013start/2018completion and upload path2024/footer2026 are not shutter dates. Historical QA/manufacturing limits preserved.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
