# 國體綜合科技弧廊片段｜下薄板外緣局部淺灰

**局部補色未完成：只下薄板外垂直緣128原面淺灰；字帶柱與主牆未完成／非2026現況。** partial_color_incomplete=true、fully_colored_exterior=false。同項ntsu-science-portico-section／count_delta=0，桃園校區；只凹角門廊與裁切主翼，不是整棟綜合科技大樓。

| 前斜視 | 後斜視 | 正面 |
|---|---|---|
| ![前斜視](preview.png) | ![後斜視](rear.png) | ![正面](front.png) |
| ![背面](back.png) | ![西側](west.png) | ![東側](east.png) |
| ![頂視](top.png) | ![門廊薄板](entry-detail.png) | ![完整外緣](facade-detail.png) |
| ![中性上欄板與薄板](roof-detail.png) | | |

## 材色範圍

由原arc_strip獨立重建ro88.5、cy49、±42度65點64個chord。每chord所有三頂點須落完整無限垂直plane，再核切向0至原chord長與原z17.6..19.8有限界，容差0.0001mm。每個無限plane等於有限域，恰2共邊原面，共128淺灰、4958中性；不用面心或normal閾值漏碎面。所有1349原共面連通域一致，原5086三角不變。

只有下薄slab外垂直緣取名義淺灰；上層有字parapet與開口全部中性，圓柱貼紙/告示/異材腳未分界故整柱中性。薄板頂、暗底、內邊與端蓋不沿用前緣色。主翼磚牆混淺帶/底座/遮蔽區，玻璃窗背、地面、階、人工側後截面與未知面中性。中性不代表實景灰，資料範圍不是材料接縫。

## 來源與版本限制

親看舊官網斜照與官方PDF外觀照片，僅支持連續下薄緣淺灰色族，不稱精確飾面尺寸或測色。原舊外觀與2021外牆、2024空調改造脈絡保留，以上來源/計畫年份不是拍攝日期，不認證2026現況。凹角兩翼與弧門廊是原公開照片近似片段，側後人工截斷不是完整實測牆；補色不追認幾何、無室內或新翼。來源私人，不公開照片或貼圖，不推未見CC為商用許可。

## 檔案與 QA

原STL/build與5086三角字節/座標保留；immutable21件沒有OBJ，原builder只輸出STL。原README存ORIGINAL-MONOCHROME-README.md，舊單色previews與QA為歷程。appearance.3mf兩展示材、scene.blend真面材、color-mesh.npz同原三角。精確requirements隔離build+color、閉合正體積、3MF面材座標/Blender重開/10張1200×900檢核，重建保留不刪，未實際列印或證多色切片。

## English limitations

Partial only:128 original lower-slab outer vertical fascia triangles palegray;4958neutral. Recompute64 original chords from radius88.5,cy49,span±42degrees. All three vertices must lie on each infinite plane and finite tangent/z17.6..19.8 bounds;infinite plane equals finite pair for every facet. All1349coplanar components uniform,original5086triangles unchanged,noOBJ,count_delta0. Lettered upper parapet,columns with notices/mixedfeet,slabtop/underside/inneredge/endcaps,wingwalls,glazing and cutrear neutral. Cropped concave-corner portico section,not entire complex. Retain original older appearance and2021wall/2024AC context;unknown capture,no2026current survey. No source photos/textures public,no geometry recertification,not testprinted.
