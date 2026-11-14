from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify;assert len(old.PALETTE)==7
TARGET=[387, 388, 389, 393, 397]
def classify(tri):
 colors,why=original_classify(tri);assert len(tri)==3832 and np.bincount(colors).tolist()==[494, 2477, 14, 520, 2, 20, 305]
 assert (colors[TARGET]==0).all();colors[TARGET]=1;why[TARGET]='bounded_T3_upper_rear_tower_stone_background'
 assert np.bincount(colors).tolist()==[489, 2482, 14, 520, 2, 20, 305];return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='僅原高塔後向上段 y15 完整六面域，其中五中性面改既有石灰1，385原灰保持；不延前側頂、下塔、簷底、警衛室或另一門。 source0後照為直接主證，source1較遠後照輔助；source2至8前向不代替後面材料證。九圖只親看完整1600縮覽，不冒稱全原像素。 石板縫、風化非色斑逐項重建；照片近棚的淺色斜凸翼原未建，原矩形塔深寬及棚肋交會為粗代理。本案只作後塔石族背景近似，不宣稱真牆全域均質或修復缺失翼。 九張EXIF Original自報2025-03-02各時刻見metadata，Originaloffset缺失，不能借OffsetTime或Digitized +08補入；非2026現況認證。 原7材逐值保持、不新增材，不改geometry/STL/面序/歷史QA/現README；原標牌無字保持，不新增文字。 完整域以原box扣棚與x60肋解析，支承外逸及反缺非零浮點如實保留；不裁面造小安全域。 僅現可讀20 prefix排除，缺失歷史全索引未查全；已知B1–4/A2/看台同HOLD域避開。私人參考及審核不公開、不改凍包或index、不發布。';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
