# 高師新研究大樓｜入口雨庇頂與柱前局部灰白

**混材簷面、欄代實板、窗背與其他未證面未完成分色。** `partial_color_incomplete=true`、`fully_colored_exterior=false`。只12個入口有據原面，不是全色現況。

| 總覽 | 背側 | 正面 |
|---|---|---|
|![總覽](preview.png)|![背側](rear.png)|![正面](front.png)|
|![背面](back.png)|![西側](west.png)|![東側](east.png)|
|![頂面](top.png)|![兩柱前](entry-detail.png)|![雨庇真頂](facade-detail.png)|
|![中性屋部](roof-detail.png)|||

## 材色範圍
同 `nknu-new-research-building` 原項目，same-item、count_delta=0。**原8796三角面、STL、OBJ與build_model.py字節不變**；無切面／新增幾何。
- 獨立入口雨庇真頂 z30.2、x−20..34／y−66..−48，6原面中灰，並非整盒灰色。
- 兩柱真正前表面 y−65.55、中心x−15.5／20.5，原臺階／雨庇Boolean已剪界，6原面暖白。
- 其餘8784面中性：雨庇前fascia混深上緣與淺下皮、柱側／雨庇底、主體混牆、代欄杆的原實板、窗背與粗框、屋頂設備、側後、中庭及階。
- 全共面連通域同材，0候選撤色。不把實欄板塗黑冒充透空欄杆，不畫三角楔假材界。色／中性界是證據與原拓撲範圍，不是真實材接縫。
- 此為新研究大樓，非已拆舊館；補色不重新背書原照片近似幾何、窗框或樓層精度。

## 來源／日期與權利
官方完工高視角與地面外觀兩照片。2020文章／完成歷史、2026附件網址均不是獨立拍攝日期證明，不稱2026現況精測。
原照私有保存，不公開／貼圖；未確認CC／再散布授權，不保證商用。HEX只是近似灰白材色族，非校準色票。
最終來源GO是來源範圍放行，不是發布核准，也不免除幾何／共面／視覺QA。

## 格式與列印
[原STL](model.stl) · [原OBJ](model.obj) · [材色3MF](appearance.3mf) · [Blender](scene.blend)
150×147mm原展示底座，照片近似非精測比例。STL無色，3MF與Blender真逐面材質。三材質標籤不是驗證三色／四色耗材切片；**未實際列印**，無切片路徑。

## 重建與 QA
原 `build_model.py` → `colorize_model.py` → `export_appearance.py` → `validate_color.py`；Blender `render_color.py` 與 `verify_color_scene.py`。
原字節／三角multiset、閉合正體積、3MF面材、完整隔離原build＋color重建、scene重開、十圖1200×900及圖文hash皆核，程序不取代來源人工判讀。
原README與單色previews/render/validation保留歷程，不冒稱新QA，沒有刪除原件。
