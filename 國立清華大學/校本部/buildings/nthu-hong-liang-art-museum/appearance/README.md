# 清華宏亮美術館：六材質外觀版

沿用原 **1,278 三角面／639 頂點**，不改原 STL 位元、座標、面序或幾何；這是既有模型外觀改版，不增加模型包數。

| 模型預覽 | 模型預覽 | 模型預覽 |
| :---: | :---: | :---: |
| 正面<br>![正面](previews/front.png) | 未知後牆屋頂中性／左側來源構件<br>![背面](previews/rear.png) | ![正立面](previews/elevation.png) |
| ![頂視](previews/top.png) |  |  |

[表面色 3MF](nthuhong-appearance.3mf) · [可編輯 Blender](scene.blend) · [材質色表](palette.json) · [逐面指派與依據](face-materials.json) · [原 STL](../model.stl)

## 來源與配色邊界

親自核對清華官方[景點介紹](https://attractions.site.nthu.edu.tw/p/406-1515-301460,r8697.php?Lang=zh-tw)、[草坪正面照](https://attractions.site.nthu.edu.tw/var/file/515/1515/pictures/836/m/mczh-tw700x700_large56157_505174882110.jpg)及[左端高位照](https://attractions.site.nthu.edu.tw/var/file/515/1515/pictures/836/m/mczh-tw700x700_large56158_139048982110.jpg)。照片無 EXIF 拍攝日，不把工程完工日期或網站路徑當拍攝日期，也不宣稱 2026 即時外觀。[來源覆核與雜湊](qa/source-review.json)，原照不入公開包。

- 兩側上盒**正面**及可核對左盒端面採冷銀灰金屬，既有板縫同系統低差異，不塗成黑玻璃。中央正面淺暖混凝土，未註冊回折面保守中性。
- 下層各離散窗背與左端凹背暗灰綠玻璃，原窗梃銀灰；樹影與草地反射不烘成綠牆。兩段凹連接盒只賦來源可見前面，不把隱藏整盒全部塗黑。
- 原主支柱與細圓柱混凝土代理，圓周及短回折面為同構件有界材料延伸；左端原低磚牆紅褐，包括短頂面按同一磚構件有界延伸，不聲稱每面皆有特寫。
- 上盒屋頂、右端、後面及其他未註冊面中性。底板沒有草坪界線，不整片塗綠；不增屋頂設備、字牌、管線或室內。
- 原 STL 位元、座標、面序、原腳本／場景／歷史 QA 保持，不新增面或棟數，不宣稱實體列印成功。

[原幾何與歷史來源限制](../README.zh-TW.md)

## 重建與核驗

安裝 [依賴](source/requirements.txt)，Blender 使用 4.3.2。由本資料夾上層提供原 model.stl：

1. `python appearance/source/build_appearance.py`
2. `python appearance/source/verify_exchange.py`
3. `blender -b -t 3 --python-exit-code 1 -P appearance/source/render_appearance.py`
4. `blender -b -t 3 --python-exit-code 1 -P appearance/source/verify_scene.py`

[獨立重建 ZIP](rebuild-source.zip)含原 STL、四支程式及依賴，不含第三方照片；不取代原建模腳本。[逐檔 SHA256](SHA256SUMS)

[交換／拓撲 QA](qa/exchange-validation.json)核對原座標與面序、全部面材質、單連通、有向水密邊、頂點 link 單環、正體積與零退化／重複面；lib3mf 嚴格讀取零警告，實際編輯單材質再存讀，其他材質及面指派不變。SDK 六位小數量化誤差另列。

[Blender 存讀與編輯](qa/scene-validation.json) · [渲染記錄](qa/render-manifest.json) · [獨立重建](qa/rebuild-validation.json)

## 製造限制照舊

尺寸仍為 150 × 100 × 39 mm；原 STL、建模程式、場景及歷史 QA 保留。原層檢與薄特徵檢查本次未重跑，不能由材質 QA 代替。

3MF 是同一網格的表面色，不是各材質各自封閉的分色實體、切片專案、噴頭映射或 G-code。切片 GUI、多材料路徑與實體列印未測；柱頭、屋簷、窗框及薄邊仍須評估材料、支撐及拆除風險，沒有保證可印或免支撐。


## 2026-11-14 有限外觀修正｜模型交付版

# 宏亮美術館：中央混凝土盒右側有限背景近似

主證為官方竣工報告第二外觀圖 https://construc.site.nthu.edu.tw/var/file/167/1167/img/449174070.pdf ，中央混凝土盒轉角側前段與相鄰銀灰盒有界。另兩官圖 https://attractions.site.nthu.edu.tw/var/file/515/1515/pictures/836/m/mczh-tw700x700_large56157_505174882110.jpg 及 https://attractions.site.nthu.edu.tw/var/file/515/1515/pictures/836/m/mczh-tw700x700_large56158_139048982110.jpg 僅正面/左端輔證。報告所述2025-02-05主體完工不是快門日期，不保證2026實況未變；施工地面/鷹架不作完成景觀依據。

僅357/358/359/361/362/365六原面0→existing pale_warm_concrete2 #C4BFB1/.78；原6shader與其餘1272indices保持。完整x33.5側面由原中央盒y−28..24,z16..39扣原link及lowerhost交會，面積約914.2mm²。不是完整52×23矩形，也不裁分新增面。

全52mm深度、盒間距與link錯位皆原粗代理。照片只直接支持側前段，後段被右金屬盒遮蔽，僅同一中央盒側牆的有界背景延續，非逐點註冊/測繪或全深直接觀察；沒有補幾何或修復原錯位。不延另一側、屋頂、盒底、右金屬盒、連接玻璃或地面。原模板縫/拉桿孔未加，不認證材料產品或校準色。

模型、材質、原生視角圖與必要重建程式沿用完成候選，未改幾何或新切材界，不代表全館精確復色、現況或實體試印通過。原來源年代、工程與列印限制仍適用，舊說明與審核僅屬各自版本，本段更新上述局部範圍。

本次只公開模型、必要重建輸入／腳本、預覽與說明；完整來源、比較及研究審核不隨本批交付。根目錄PUBLIC-MODEL-SHA256SUMS僅校驗所列當前產品，舊表不驗證新版。重建ZIP只含必要重建檔；若原ZIP含README則同步本說明。歷史來源及QA連結指儲存庫既有文件，非ZIP內的新增審核附件。

現版共有 6 個顯示材質（含未知中性色）；上方舊材質總數、舊中性範圍與 QA 為歷史描述，僅由本節有限範圍更新，非分色實體或製造認證。
