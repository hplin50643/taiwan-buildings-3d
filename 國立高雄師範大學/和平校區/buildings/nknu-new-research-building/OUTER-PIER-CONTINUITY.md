# 高師新研究大樓：右入口柱外側 8 面有限補色

本件沿既有雨庇頂 6 灰面與柱 14 暖白面，僅將原 **3929、3930、3931、3937、3938、3939、3940、3944** 由未知中性 1 改為既有名義暖白 2 `#D7D5CC`。8796 原三角面、面序、頂點、尺寸與 STL 不變，其餘 8788 面保持。面數為 `[6,8768,22]`；三材名稱、HEX、RGBA、shader 與 roughness 不改。歷史色名 frontfaces 不代表現在只含前面。未知中性不是實物灰色證明，整棟分色仍未完成。

## 來源與推論界線
官方地面斜照可辨右入口獨立柱的正面與外向窄回面；典禮近照辨同一柱淺色洗石表觀族，但其直接內向側是既有已補範圍，不能當作新增外側逐面直視照片。這次採**外側透視可見＋同一柱的有限材族連續推論**。既有模型 3.5 mm 方柱深度、全高與階梯／雨庇 Boolean 裁切形狀不是照片量測或重新測繪。

新域為 +X、x=22.25、名義 y[−65.55,−62.05]，實際 z[3.9,28] mm，原 8 面一完整最大共面連通域，面積 82.04008947 mm²（模型數值，不是實體面積）。不切面，不補紋理、分縫、小燈或材界。左側實景較深回牆、右柱背／頂底、混材雨庇 fascia／底面、窗背、欄杆代理實板及整棟側後均不擴色。保留原近似工程與未試印限制。

公開來源連結與內容識別：
- https://c.nknu.edu.tw/affair/fckeditor/ckfinder/userfiles/dbhp/images/04%20%281%29.jpg
  SHA256 `a7d1fe9af28509e112be79a626657a1bb37a944f331d4ba1d9442c54c2c4190c`。
- https://www.nknush.kh.edu.tw/wp-content/uploads/sites/129/2026/01/%E9%AB%98%E5%B8%AB%E5%A4%A7%E7%A0%94%E7%A9%B6%E5%A4%A7%E6%A8%93.jpg
  SHA256 `959d06924274cb30f31e066c62c87291eacd1e657ffe495fee9c7734cbf5b040`。

地面照網址 2026/01 是附件路徑，不證明 2026 新拍；典禮頁 2020 脈絡亦非精確拍攝日認證。不宣稱2026現況、校準色票或材料規格。原圖、PDF、私人模型比較及編修實驗均不在公開包，不推定第三方圖像可再散布。

## 精確重建
固定基準 repo `hplin50643/taiwan-buildings-3d`，commit `8f90ae2478f00cce6832a07de537f7d333f6dbc0`，相對目錄 `國立高雄師範大學/和平校區/buildings/nknu-new-research-building`。包內 `rebuild-baseline/` 保留該版 STL、NPZ、3MF、Blend，wrapper 逐檔 SHA256 鎖定：

```sh
blender -b -t 1 --python-exit-code 1 -P rebuild_outer_pier.py -- --baseline rebuild-baseline --out rebuilt
```

Blender 4.3.2／NumPy。原 `colorize_model.py` 仍是已補右內側的歷史基準，直接重跑會退回本次外側舊色；不覆寫或冒稱舊流程已更新。新 wrapper 產出NPZ/3MF/scene/change JSON，原STL直接保留。`render_outer_pier.py` 讀新場景、原解析度及相機規則渲染 7 全景＋3 細節，不保存渲染相機變化。PNG 無損移除私有路徑／日期／時間文字 metadata，不改像素。

## 保留與驗證
完整原場景 RNA 僅 27 差異：8 面在 polygons／loop_triangles／material attribute 共24指派，物件 scope/source_mesh_sha256 兩項，以及既有孤立 Material.use_fake_user False→True 一項。後者避免 Blender 儲存清除原孤立材及 node tree；不是新增 shader，原材其他參數皆不變。可見／隱藏物件、文字底板、相機、燈光、世界、幾何、transform 及全部原材 inventory 保留。

3MF 原完整樹僅 8 p1＋物件 fallback pid/pindex 兩屬性變動；fallback=既有中性1，每面明確材指派不變。原座標字串、全部其餘XML與ZIP內容保留。Clean 重跑NPZ/3MF/change JSON逐byte一致、Blend完整RNA語義一致，不聲稱容器byte決定性。strict SDK零警告、私人改材保存重讀、Blender私人頂點＋面材編輯保存重開通過，公開檔未受私實驗修改。有限 ray 內點檢查確認私近景 +X 目標面未被遮擋，非逐像素或來源視角配準。

未實體試印或 GUI 切片驗證；3 展示材不是已驗三色／四色耗材工程。原尺寸、粗幾何、薄部、支撐限制不因補色自動重新合格。README原字節完整前綴保留，舊QA/雜湊屬歷史版本；新版以 `MANIFEST.json` 為準。
