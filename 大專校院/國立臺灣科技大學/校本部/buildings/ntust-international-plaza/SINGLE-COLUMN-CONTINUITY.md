# 台科國際大樓單一廊柱 −X 側面有限補色

只最高開放廊層 z66、中間柱中心 x−6 的 −X 側 x−7.7，原六面 **2547、2548、2549、2556、2557、2558**（零起算）由 2→1，沿用既有名義暖灰 #CDC9BD，不新增調色。

6488 原三角不變；8 黃／162 暖灰／6318 未驗中性。其他 6482 面、原 156 柱前暖灰面及 8 黃遮陽面保持。完整共面共享邊域面積 26.085013046264066 mm²，原 y18.9..22.5、z66..74.1 的交接缺口保留，不補造矩形或增加頂點。+X、其餘 29 柱、橫梁、上下皮、欄杆、暗廊、玻璃及背面不延伸。

## 來源與推論限制
台科總務處[官照2](https://general-r.ntust.edu.tw/var/file/54/1054/img/1340/110707229.jpg)及[官照3](https://general-r.ntust.edu.tw/var/file/54/1054/img/1340/127044848.jpg)。官照3最高開廊中柱的照片左側窄返，與已確認正面淡磚族連續；欄杆與暗廊在後可分離。這是**單一同柱材料連續的有限推論**，不是完整 3.6mm 原模型深度、逐磚接縫或上下交界的逐像素測量。柱排列／層高／側深仍是原展示近似，不因補色追認測繪。2012 EXIF 沒有時區、不是 2026 現況，名義 HEX 非校準色票。中性不是實景灰色；證據界線不是不同材料接縫。

官照不隨公開包附送、不作貼圖。私有 −X 前斜角前後細節是模型比較，不是來源照片同視角。

## 保留與驗證
原 STL bytes、NPZ 全幾何／其餘 arrays／dtype 保留。直接開原 Blend，只改六面 material_index（含同步 attribute），以及 source_mesh_sha256、scope 兩屬性。原材 RGBA/shader/roughness、transform、camera/world、隱藏 caption/backdrop 與其他資料不變；此 baseline 無孤立材，不新增 fake_user。完整 RNA 恰 20 差（18 面材表示＋2 屬性）；serializer 排除 runtime/depsgraph/UI 選取等，深度上限18，不聲稱 Blend 二進位相同。

3MF 全樹僅六 p1 與 object fallback pid=1/pindex=2 更新，其他 ZIP 成員及原座標字串保留。clean rebuild 核 NPZ/3MF/changeJSON bytes、Blend 全 RNA 語義。strict SDK 無警告，私有調色保存重讀，以及 Blender 私有一頂點／一面材質編修保存重開通過；不代表 GUI 切片或實際列印測試。

## 可重現
Baseline固定 commit `8f90ae2478f00cce6832a07de537f7d333f6dbc0`，repo `hplin50643/taiwan-buildings-3d`，相對目錄 `國立臺灣科技大學/校本部/buildings/ntust-international-plaza`。rebuild-baseline 附四檔，wrapper 逐檔 SHA256 鎖定：

```
blender -b --python rebuild_column_side.py -- --baseline rebuild-baseline --out rebuilt
```

原 colorize_model.py/render_color.py 未改，單獨執行仍回原 8／156／6324 版；新 wrapper 必須在精確 baseline 上追加六面，不重新推測材界。

預覽 `blender -b --python render_column_side.py`，由新 scene 載入，不重建材質／覆寫 scene；沿固定 ref 原 renderer 十視角與 framing 算式、1200×900、Cycles48。七全景與三原本刻意裁切細節，不把細節當全模型構圖。
