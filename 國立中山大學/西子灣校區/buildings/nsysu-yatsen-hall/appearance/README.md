# 國立中山大學逸仙館：來源限域磚紅外觀代理

[彩色3MF](nsysu-yatsen-hall-appearance.3mf) · [可編輯Blend](scene.blend) · [面材質對照](face-materials.json) · [色盤](palette.json) · [來源](SOURCES.md) · [重建原始碼包](rebuild-source.zip)

| 模型預覽 | 模型預覽 | 模型預覽 |
| :---: | :---: | :---: |
| 正面<br>![正面](previews/front.png) | 背面<br>![背面](previews/rear.png) |  |

[正立面](previews/elevation.png) · [側面](previews/side.png) · [俯視](previews/top.png)

| 模型預覽 | 模型預覽 | 模型預覽 |
| :---: | :---: | :---: |
| 正立面<br>![正立面](previews/elevation.png) | 側面<br>![側面](previews/side.png) | 俯視<br>![俯視](previews/top.png) |

## 範圍與限制
官方未標年的完整實拍2、3支持正面上部磚牆51面與門廊前磚欄板2面，合計53個原完整三角採低飽和磚紅 #AE6C58；其餘3057面保持中性 #AAA79F。此為模型既有**磚牆主平面粗外觀代理**，不是細外皮精密還原。窄灰壓頂、字樣、磚縫及污漬未建，沒有切面造色條；屋頂水平面仍為中性。弧洞內表面、側背、白梁柱、玻璃陰影、底座均不擴染；側牆灰裙基界面不清，整片不選。

照片不標日期，2020整建新聞不能證明照片屬整建後，亦不代表2026現況。顏色為未校準視覺proxy，不推定確切建材成分。非相鄰體育館，不另計同棟逸仙美術館。原幾何粗近似與未知後立面/屋頂限制均保留。

原STL 3110三角、1533頂點、150 × 145 × 78.5 mm；STL bytes、每三角座標/繞序/面序不變，無切面、重拓撲、外加幾何。53面總面積約3980.3316 mm²。完整三頂點平面與範圍檢查見 [邊界QA](qa/material-boundaries.json)。不承諾最小壁厚、免支撐或實體可印；此包未做實際切片/試印，歷史列印QA未重算。

## 重建
Python安裝 source/requirements.txt，同層上級放原model.stl。執行 python source/build_appearance.py、python source/verify_material_boundaries.py、python source/verify_exchange.py；Blender 4.3.2 執行 blender -b -t 2 -P source/render_appearance.py，再 blender -b -t 2 -P source/verify_scene.py。交換strict零warning並真edit-save-reopen；Blend可編輯材質。乾淨第二目錄3MF/maps/palette/五PNG逐bytes一致，Blend以語義一致驗證，不宣稱二進位一致。

[交換QA](qa/exchange-validation.json) · [Blend QA](qa/scene-validation.json) · [獨立重建QA](qa/rebuild-validation.json) · [校驗碼](SHA256SUMS) · [權利說明](LICENSE-NOTICE.md)


## 2026-11-13 有限外觀修正｜模型交付版
# 逸仙館門廊前梁淺色背景增補

官方相簿：https://www.nsysu.edu.tw/p/405-1000-15781,c1505.php?Lang=zh-tw
官原幅2：https://www.nsysu.edu.tw/static/file/0/1000/pictures/561/m/mczh-tw1920x1200_large98820_749570333548.jpg
官原幅3：https://www.nsysu.edu.tw/static/file/0/1000/pictures/561/m/mczh-tw1920x1200_large98855_929364033549.jpg

僅原y−67門廊主梁及同平面7格梁端聯集完整30面，0→新2 #D8D8D1/.88淺白背景近似。兩官低角原幅支持前緣淺白，與上方磚欄板及後深凹分開。非識別塗料/建材或校準色；不全底棚、頂/露台、側返、柱、磚欄板、窗或弧洞內。

原7格梁數量/梁寬厚/端點均粗代理，無逐點測繪，細接縫/燈具未建，不以陰影判異材。原3110面及原2材、其餘3080indices（含53舊磚面）保持。兩照未標年，2020整建新聞不證照片年代或2026現況。原工程限制與未知背頂保留，非新製造QA/切片或試印。
模型與原生視角圖沿用完成候選的原bytes；不改幾何、不增加分界、不稱全棟精確配色或實體試印通過。公開預覽只含模型，不含新增圖片文字。原來源年代、工程及列印限制仍適用。先前敘述與審核屬其原版本，本段僅更新上述局部範圍。
本次只交付模型、必要重建輸入/腳本、預覽與此說明；完整研究與獨立審核紀錄另行保留，不在本批公開。PUBLIC-MODEL-SHA256SUMS只核本次所列公開產品，舊校驗與QA不代表本次新版。
