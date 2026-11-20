# 生活機能館單支鋼撐背半面材色連續推論（2026-11-18）

僅右前叉撐向 x=33 的一支，起點 (42,-20,37) 至 (33,-20,48.4166666667)，原 16 邊柱 facet 8..15 的完整存留面，延續既有淺灰塗層族。此背半並非照片直接逐面證實；依官方建築獎 PDF 印刷頁 42 的同一鋼管可見前側塗層作有限材料連續推論。2013 文件資訊不等同攝影時間，更非 2026 現況。

來源：https://ws.moi.gov.tw/001/Upload/OldFile/moi_note_file/tcc_file_286.pdf 。原照片/PDF 不隨公開包附送。

指定原面（零起算）：1630, 1631, 1632, 1633, 1634, 1635, 1637, 1638, 1639, 1658, 1659, 1660, 1661, 1662, 1663, 1664, 1665, 1666, 1667, 1668, 1669, 1671, 1672。23 面 1→0，面積 37.55677440675305 mm²。原 46 淺灰面全部保留，總 1952 面變為 69 淺灰、1883 中性，其他 1929 指派不變。中性不是對真實灰色的認定。原 16 邊粗化、端部及交接近似不追認為實測；柱、collar、端蓋、另一支、屋網及其他未知面不變。

## 重建
固定 baseline：hplin50643/taiwan-buildings-3d commit `8f90ae2478f00cce6832a07de537f7d333f6dbc0`，相對目錄 `國立臺南藝術大學/官田校區/buildings/tnnua-campus-life-hall`。所需四檔已附於 rebuild-baseline，wrapper 逐檔 SHA256 鎖定。Blender 4.3.2：

```
blender -b --python rebuild_branch_back.py -- --baseline rebuild-baseline --out rebuilt
```

原 colorize_model.py/render_color.py 保留歷史用途，未覆寫，單獨執行舊流程會回到原 46 面版本。新 wrapper 在精確 baseline 上改指定面，不重新分類。

## 保留與驗證
STL 原 bytes、NPZ vertices/faces/其他 arrays/dtypes 保留。Blend 從原 scene 開啟，只改 23 面 material_index（含同步 attribute）與 source_mesh_sha256/scope 兩屬性；原材 RGBA、shader、roughness、transform、camera/world、隱藏 caption/backdrop 全保留。此 baseline 無孤立材需增 fake_user。隱藏舊 caption 仍描述舊前半範圍，屬保留歷史資料，不是本輪變更清單。

3MF 全樹只改 23 個 p1 與 object fallback pid/pindex；原座標字串精度、其他 ZIP 成員不動。完整 RNA 共 71 差；原/新/clean rebuild 語義核對，strict SDK 無警告與私有改材往返，Blender 私有頂點＋材質編修保存重開通過。未以此聲稱 GUI 切片或實際列印已驗證。RNA 排除 runtime/depsgraph/互動選取等不穩定狀態，深度上限 18，非二進位 Blend 完全相等聲明。

原十視角以原 camera 投影、1200×900、Cycles 48 samples 重渲，七全景及三原本刻意裁切細節；預覽不覆寫保存的原生 scene。來源資料與前後私有比對不公開。

預覽重建：`blender -b --python render_branch_back.py`，由新保存 scene 讀取，使用已核固定 ref 原 renderer 的十視角與 framing 算式；不重新建立材質或覆寫 scene。單視角可加 `-- --only-view=preview`。
