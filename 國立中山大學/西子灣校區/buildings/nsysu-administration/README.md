# 國立中山大學 行政大樓

## 模型預覽

| 新彩色正斜視 | 新彩色來源角度 | 新彩色立面 |
| :---: | :---: | :---: |
| ![正斜視](appearance/front.png) | ![來源角度](appearance/source-angle.png) | ![立面](appearance/elevation.png) |
| 新彩色背向 | 新彩色上視 | 彩色下載 |
| ![背向](appearance/rear.png) | ![上視](appearance/top.png) | [彩色3MF](appearance.3mf) · [彩色Blender](appearance.blend) |


### 側背原面材料續色（原圖保留）

保留全部原彩面，補色920個原中性三角面：上盒沿用既有正面磚色主材代理延伸完整側背，既有側背窗背／凹面與簷板側邊補同族材料。上盒細白框帶未有原面界，仍按原正面近似省略。下部背面顯著淺柱與磚牆混材無面界、人工連棟截面及未知屋頂保中性；不新增窗或飾物。


原全部預覽及代表選圖、geometry／尺寸／STL／scene不變；詳[來源與限制](APPEARANCE.md)。

[新版左側](appearance/left.png) · [新版右側](appearance/right.png) · [原版同相機正斜視](appearance-review-v2/original-front.png) · [原版同相機背向](appearance-review-v2/original-rear.png)。

[返回西子灣校區](../../README.md) · [返回全校圖鑑](../../../README.md)


[下載 STL](model.stl) · [可編輯 Blender](scene.blend) · [參數重建](build_model.py) · [幾何驗證](validation.json) · [全部來源](sources.json)

## 範圍與外觀
行政大樓主棟；相接的理學院、社會科學院與東西綜合大樓不在此件，不把整個院落群棟當作本棟完成。

尺寸（含底座）：150 × 132 × 93 mm，最長150mm，各館獨立縮放，不能拼成同比例校園。尺寸是模型尺寸，非現地測繪。

- 前部深柱廊、四支主圓柱、較細分格與水平梁
- 中央弧形陽台保留中空上緣及板下空間
- 上部寬出挑盒體、連續窗帶和中央扁弧凹口
- 官方1F–3F圖的背面中央深退縮；3F至RF中央井口及兩側樓梯頭位置

## 未知與簡化
- 原建模階段未取得完整背照；本版已親看2024-06-18背面及官方後門近照，但只補原面材料，後側窗孔及側面仍是原低細節近似，不表示與照片或現況逐窗一致。
- 屋頂中央井口由3F以上貫通，背面下層依官方平面保留退縮；各層高度、高層出挑深度及樓梯頭高度以目視比例估算，未還原內部房間。
- 主樓與東西相鄰低層群棟連接處截斷；柱身為列印加粗。

[正立面](appearance/elevation.png) · [俯視／屋頂](appearance/top.png)。官方舊相簿未提供拍攝年代；本版新增Commons照片標示2024-06-18，與查閱日分開記錄。不同來源不能視為同一時間現況。


## 列印與數位檢查
單位為毫米，底座朝下。可先用0.4mm噴嘴、0.2mm層高試切片，依材料和機器調整。主柱直徑4.1mm，次框1.35mm，陽台邊1.6mm，屋頂緣1.5mm；柱廊跨距、上層出挑、弧形陽台板與中央井口均需檢查支撐及移除路徑。

原始STL水密、每邊兩面、頂點link單環、原法向／繞序、正體積、單一連通表面、150mm、獨立重建SHA一致及儲存Blend幾何一致均通過。465個0.2mm逐層輪廓有效閉合（固定z起點0.071mm，無Polygon修補）；0.8mm參考寬度形態opening以1mm間距抽樣，最大面積損失0.0590%，超過1%層數為0。[逐層資料](valid-sections.json) · [薄特徵篩檢](thin-feature-check.json)。

數位幾何檢查不等於全面最小壁厚量測、Cura/Prusa實際工具路徑或實體試印；未做實體試印，不保證免支撐或任何機器均可印。

## 重建與驗證
Python 3.12安裝requirements.txt，執行python build_model.py。Blender 4.3.2+執行blender -b -t 2 -P render_preview.py，會匯入實際STL並儲存可編輯網格場景與四視圖。python validate_model.py、python check_valid_sections.py、python thin_canonical_v2.py各自必須成功，validate_model.py會獨立暫存重建並驗證SHA和Blend。SHA256SUMS提供逐檔完整性。

## 公開證據
- [官方校園景觀實拍相簿](https://www.nsysu.edu.tw/p/405-1000-15781,c1505.php?Lang=zh-tw)
- [官方各樓層安全平面圖目錄](https://rpa121.nsysu.edu.tw/p/405-1296-286323,c18978.php)
- [行政大樓1（官方實拍）](https://www.nsysu.edu.tw/static/file/0/1000/pictures/561/m/mczh-tw1920x1200_large98795_450676533548.jpg)
- [行政大樓3（官方實拍）](https://www.nsysu.edu.tw/static/file/0/1000/pictures/561/m/mczh-tw1920x1200_large98797_917106733548.jpg)
- [行政大樓4（官方實拍）](https://www.nsysu.edu.tw/static/file/0/1000/pictures/561/m/mczh-tw1920x1200_large98847_108720033549.jpg)
- [行政大樓5（官方實拍）](https://www.nsysu.edu.tw/static/file/0/1000/pictures/561/m/mczh-tw1920x1200_large98848_806833833549.jpg)
- [教學行政區--行政大樓 PDF](https://rpa121.nsysu.edu.tw/static/file/296/1296/attach/76/pta_174542_9100967_04268.pdf)

只自建幾何，未擷取第三方mesh。原照片和PDF不隨本包散布，預覽只含實際STL渲染。


## 本版材料驗證

[逐點逐面／材料驗證](appearance-review-v2/model-verification.json) · [完整原面與中性原因](appearance-review-v2/boundary-continuity-audit.json) · [來源判讀](appearance-review-v2/source-register.json) · [九張真渲染審閱](appearance-review-v2/color-continuity-review.json) · [乾淨重建](appearance-review-v2/clean-rebuild-equality.json)。

原appearance-review保留為前版歷史，不作本版材料與圖片綁定；現版由appearance-review-v2及appearance-freeze.json綁定。原幾何QA與未試印限制未變，校級校驗碼待授權發布時合併。
