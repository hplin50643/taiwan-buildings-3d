# 臺大萬才主體｜前帶與入口階梯局部材色

**磚灰混牆、窗背與未知面未完成分色。** `partial_color_incomplete=true`、`fully_colored_exterior=false`。僅主體前帶、頂前緣與入口階局部補灰，不是整館全色完成。

| 總覽 | 背側 | 正面 |
|---|---|---|
|![總覽](preview.png)|![背側](rear.png)|![正面](front.png)|
|![背面](back.png)|![西側](west.png)|![東側](east.png)|
|![頂面](top.png)|![入口階梯](entry-detail.png)|![前帶](facade-detail.png)|
|![頂前緣](roof-detail.png)|||

## 材色範圍
同 `ntu-wancai-main` 原項目，same-item、count_delta=0。**3962原三角面及原STL／OBJ／build_model.py位元組不變**，無新切面、加構件、修形。兩份原README另存原單色歷程。
- 三條獨立前水平帶6面、最上帽前fascia2面、真階踏面及前立面86面，總94面近似石灰色。
- 初候選90階面中4面因與未放行面連續共平面，整域撤中性。不是為滿色沿三角邊切色；不稱全部梯／頰牆／曲平台已校色。
- 其餘3868面中性，包含上磚／下灰但無材界的整主牆、短端、窗背玻璃反光細框、低附屋窗、右突出窗背、屋水平面、帶側返、未知側後／地台。不能以z高切紅磚、不能整窗塗黑。
- 色／中性界是原拓撲與證據範圍，並非真實材接縫。保留原粗欄省略與階數，補色不為原近似幾何重新背書；不新增文字、人物或周邊連接建築。

## 來源／日期與權利
三張校方公開影像IMG6031／6032／6044，2010網址資料夾只作年代脈絡，**不能當精確拍攝日或2026現況精測**。只外觀材色，不涉及內部。
照片私人保存，不公開／貼圖；未確認CC或再散布授權，不保證商用，HEX為展示近似色族非校準色票。

## 格式與列印
[原STL](model.stl) · [材色3MF](appearance.3mf) · [Blender](scene.blend) · [原說明](ORIGINAL-MONOCHROME-README.md)
150×120mm獨立近似展示底座，非精測縮尺。STL本身不含色，3MF與Blender真逐面材質；兩材標籤非已驗證兩色／四色耗材切片。**未實際列印**，無切片路徑，原薄件／挑台風險未因補色解除。

## 重建與 QA
原 `build_model.py` → `colorize_model.py` → `export_appearance.py` → `validate_color.py`；Blender執行 `render_color.py` 與 `verify_color_scene.py`。
原bytes／三角multiset、閉合正體積、3MF頂點與材號、完整隔離原build＋color重建、scene重開、十圖1200×900與圖文hash均核。整連通共面同材另核，不以程式代替人工來源審核。
原單色previews/render/validation全保留為歷程，不當新材色QA；未刪檔。
