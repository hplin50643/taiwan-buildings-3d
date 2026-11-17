# 尚志教育研究館：東入口六材質外觀版

| 模型預覽 | 模型預覽 | 模型預覽 |
| :---: | :---: | :---: |
| 東入口側<br>![東入口](previews/front.png) | 西側：本次未確認材質<br>![西側](previews/rear.png) | ![東立面](previews/elevation.png) |
| ![頂視](previews/top.png) |  |  |

## 本次東門廊額枋與小簷兩側淺石色延伸（推估）

僅將同一東門廊原額枋及水平薄簷的左右短側，共 4 個完整矩形／8 個原三角，延續已發布正面淺石色材 1。原 4,677 著色面與所有未變更理由保留，包含先前 6 個山牆凹槽回邊 25914／25915／25934／25942／25967／25970；其餘 32,098 面不變。原 32,106 面／16,031 點、六色表、STL 位元、座標及面序不變。現中性 27,421、淺石 2,786、前石牆 931、階灰 296、開口代理 210、底座 462。

在生成器局部座標，額枋取 y=±7.9、x=9.85…19.15、z=16.4…18.35；薄簷取 y=±8.15、x=9.7…19.3、z=18.35…18.95。局部座標由 STL 的 xy÷(150/68)、(z−2.4)÷(150/68) 還原，不能把這些值直接當模型毫米。兩額枋側每片約 88.243404 mm²，兩薄簷側每片約 28.027682 mm²；均核完整原矩形、三頂點有限域與朝外法向，不裁三角。不含頂底、簷底、斜山牆頂、圓體、圓頂、時鐘，也不鏡像到西門廊。

本輪親看由大同大學公共關係中心提供、經 Wikimedia Commons 授權來源的東面照片，其柱、山牆與額枋淺石色可作代理；短側縱深仍是同構件有界延伸推論，不宣稱整段側深都獲照片確證。**原額枋和薄簷是粗略實體輪廓，實景細雕、簷齒與古典線腳未建**；不靠塗色補造或修改幾何。拍攝日期未獨立確認，不代表 2026 現況，未實體試印。照片留私人研究，不嵌入或隨公開包散布；保留原來源及權利註記。

新版 QA 在 `qa-continuous-walls/`，歷史 QA 與根 `SHA256SUMS` 原樣保留；根舊清單的 README 雜湊屬歷史版本，現行完整校驗以 `PUBLIC-MODEL-SHA256SUMS` 為準。外觀重建 `python appearance/source/build_continuous_walls.py`；交換驗證 `python appearance/source/verify_continuous_exchange.py`；渲染 `blender -b --python appearance/source/render_continuous_walls.py`；場景驗證 `blender -b --python appearance/source/verify_continuous_scene.py`。ZIP 含原 STL、原建模程式與局部選取域，不含照片，不宣稱重算歷史製造驗證。

## 前版說明與保留限制

在原 **32,106 三角面／16,031 頂點**上直接配色，座標、面序、幾何和原 STL 位元不變；沒有細分、加建或新增模型包。原模型仍是跨來源有界近似，不是測量 BIM。


[表面色 3MF](ttu-appearance.3mf) · [可編輯 Blender 場景](scene.blend) · [色表](palette.json) · [逐面分類與理由](face-materials.json) · [原 STL](../model.stl)

## 照片依據與使用邊界

本次閱讀 [UVA Darden 的尚志館報導](https://news.darden.virginia.edu/articles/darden-executive-program-alumnus-rotunda-taipei)，並實際查看其**頁首大同大學東入口照片**。該照片由 Darden CDN 取得，文章圖說署名 Tatung University Public Relations Center，經 Wikimedia Commons、CC BY-SA 3.0（[圖說所引原紀錄](https://commons.wikimedia.org/w/index.php?curid=30412510)）。不是直接從 Commons 下載，也不把文章其他美國 UVA 建物照片當成大同實景。

文章發表日為 2026-07-01；**原照片拍攝日未在本次確認**，不能將發表日當成拍攝日或聲稱 2026 同步現況。照片尺寸 URL 參數不等於伺服器實際輸出；實際核對檔為 1920 × 1275 像素，來源 URL 與 SHA256 記於 [來源 QA](qa/source-review.json)。參考原圖不隨本包公開散布。

- 原腳本局部 +X 為東入口。六根柱、簡化柱頭、東面三角山牆與額枋取淺石色，入口石牆和東低翼正面取灰色，正面階梯取較深灰，原窗／門凹口背面取深色代理。
- 東低翼正面與外欄沿連續構造作有限配色外推；照片兩端裁切及遮擋使逐段材質不能全部獨立確認。未把同款顏色鏡射到西門廊、院內或未知後方。
- **圓頂、頂環、上部未知屋面與西側保持中性**。本張低視角照片不足以支持圓頂色，不借 UVA 原館圓頂推測。
- 窗背深色只是原封實凹面代理，不是新增透明玻璃、幕簾或內部空間。照片的石縫、雕刻、文字、時鐘指針與數字不重製或捏造；原圓形鐘面凹位保持空白淺色。
- 原階數、柱頭與欄杆簡化未修正。廣告旗、植栽、盆栽和街景不加入。展示底板不是實際地坪。

六材質是未知中性色、淺石柱／山牆、東面灰石牆、灰階梯、深色開口代理、展示底板。色值未校正，光影和污漬沒有被當成精確建材分界；沒有宣稱原色測定。

[原來源](../sources.json) · [原模型、年代及尺度限制](../README.md)。其他舊幾何來源本次未全部重讀，不拿它們冒充此次顏色覆核。

## 可重建與編輯

安裝 [依賴](source/requirements.txt)，使用 Blender 4.3.2。由本資料夾上層提供原 model.stl：

1. `python appearance/source/build_appearance.py`
2. `python appearance/source/verify_exchange.py`
3. `blender -b -t 4 --python-exit-code 1 -P appearance/source/render_appearance.py`
4. `blender -b -t 4 --python-exit-code 1 -P appearance/source/verify_scene.py`

[獨立重建 ZIP](rebuild-source.zip)包含原 STL、四支程式與依賴說明，不含第三方照片；不取代原參數幾何腳本。[SHA256 清單](SHA256SUMS)

[交換／拓撲 QA](qa/exchange-validation.json)逐面核對原座標與順序、完整材質指派、正體積、有向水密邊、頂點 link 單環及單連通，零退化與重複面。lib3mf 嚴格讀取零警告，實際改一色、存檔再讀回，其他顏色與面指派不變；SDK 六位小數存檔量化誤差另列。

[Blender 存讀／編輯 QA](qa/scene-validation.json) · [渲染記錄](qa/render-manifest.json) · [獨立重建核對](qa/rebuild-validation.json)

## 製造與歷史 QA 限制

含底板約 127.94 × 150 × 59.75 mm；舊 STL、建模程式、原場景及歷史 QA 均保留。歷史層檢、薄特徵與射線報告未在本次重跑，不由材質 QA 取代。出檐、門廊與細柱仍需按材料、支撐及拆除風險自行評估。

3MF 是一個網格的顯示色，不是六個封閉色塊、切片工程、噴頭映射或 G-code；未測切片 GUI、多材料工具路徑或實體列印，沒有保證免支撐可印。舊 README 的候選／未發布文字是原幾何工作歷程，本次外觀交付與核驗另列於此，不改寫歷史 QA。


## 2026-11-14 有限外觀修正｜模型交付版

來源：https://news.darden.virginia.edu/articles/darden-executive-program-alumnus-rotunda-taipei
文章主圖標示大同大學公關中心供圖（經 Wikimedia Commons），不是直接大同站照片。文章日期2026-07-01不是拍攝日期，不宣稱現況。

只原東三角inset三條返回完整6面由0沿既有pale1 #C9CBC6/.78。三角周圍窄灰石表觀可辨，僅有限同框家族近似，不認證石種、測色或實際各層同材。原單層三角框與0.16設計深度皆粗代理；未建多層斜簷、齒飾、板縫與細裝飾，不把陰影當異材。完整原STL面序、其他32100面及六材不變；不塗整屋坡、深底棚、穹頂、西入口或中庭。

模型、材質、原生視角圖與必要重建程式沿用完成候選，未改幾何或新切材界，不代表全館精確復色、現況或實體試印通過。原來源年代、工程與列印限制仍適用，舊說明與審核僅屬各自版本，本段更新上述局部範圍。

本次只公開模型、必要重建輸入／腳本、預覽與說明；完整來源、比較及研究審核不隨本批交付。根目錄PUBLIC-MODEL-SHA256SUMS僅校驗所列當前產品，舊表不驗證新版。重建ZIP只含必要重建檔與本說明；歷史來源及QA連結指儲存庫既有文件，非ZIP內的新增審核附件。

現版共有 6 個顯示材質（含未知中性色）；以上保留段落的材質數與舊 QA 結果屬歷史版本，現版以當前 palette.json／face-materials.json 為準，不代表封閉分色實體或列印認證。
