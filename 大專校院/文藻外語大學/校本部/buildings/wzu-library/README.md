# 圖書館大樓｜文藻外語大學

## 模型預覽


| 模型預覽 | 模型預覽 | 模型預覽 |
| :---: | :---: | :---: |
| ![實際STL正面](appearance/previews/front.png) | ![實際STL背面](appearance/previews/rear.png) |  |

## 本次屋簷左右與後緣米白延伸（推估）

將原屋簷兩側與兩段後緣共 4 個完整矩形／8 個原中性三角，延續原前緣米白材 3。原 5,236 著色面及逐面角色理由完全保留，其餘 6,890 面不變。原 6,898 面／3,379 點、原 first-seen 頂點順序、STL 位元、座標、面序及八色身份不變；現在中性 1,654、磚 348、青綠窗 184、淺石 3,351、灰梃 1,112、暗下窗 58、暗牌背 2、底座 189。新增逐面 `face_reasons` 方便審核，原角色計數仍保留對照。

範圍限 z=100…102 mm 的左右 x=±70.5、後 y=39 原外側面，四組面積 140、140、227、7.5 mm²。**後右段只能 x=66.75…70.5，不能誤取 x=65 起**：原服務塔窗洞切割 x=63.25…66.75 已切入屋簷，該缺口保持，不補幾何、不染其內回面。服務塔、屋頂、陰暗簷底、前磚牆與窗皆不改。

本輪親看校方圖書館正面照片，既有前屋簷米白可作同構件族的代理色；左右後緣是有界延伸推論，不宣稱背面每點有照片或真實材料接縫／色值量測，也不把前磚色套到整片側後牆。原照片與形體資料的時間限制照留，不作 2026 現況或實印保證；原屋頂與窗洞交接簡化不藉配色修正。照片只作私人研究，不入公開包。

新版 QA 在 `appearance/qa-continuous-walls/`，歷史 QA 與根 `SHA256SUMS` 原樣保留；根舊清單的 README 與外觀產物雜湊屬歷史版本，現行完整校驗以 `PUBLIC-MODEL-SHA256SUMS` 為準。原分類器是單面函式、外讀 palette，故保留其封裝與頂點序而非改套其他模型分類器。外觀重建 `python appearance/source/build_continuous_walls.py`；交換驗證 `python appearance/source/verify_continuous_exchange.py`；渲染 `blender -b --python appearance/source/render_continuous_walls.py`；場景驗證 `blender -b --python appearance/source/verify_continuous_scene.py`。新增 ZIP 含原 STL、建模程式、八色色表及選取域，不含照片；不重算歷史製造檢核。

## 前版說明與保留限制

校本部／公開外觀近似模型。每棟独立縮放，最長尺寸含底板150mm；並非各館同一比例。實際尺寸：150.00 × 91.00 × 115.10 mm。


## 最新配色與下載

[八材質通用 3MF](appearance/wzu-appearance.3mf) · [彩色 Blender scene](appearance/scene.blend) · [四視圖、來源及配色界線](appearance/README.md)。正面實照支持紅磚橫帶、青綠玻璃與米白柱檐；未確認側後／屋面中性，原 STL 與歷史 QA 不變，未經 FFF／實體試印。

## 外觀與範圍
八層主體、上段四道連續帶窗、中央招牌框、下段兩層柱廊及退縮陽台、屋頂大出簷、側後服務塔與十字架。

後面窗序及樓梯間深度近似；未納入前庭地下採光罩。

主要依據[校方建築物介紹](https://c005.wzu.edu.tw/category/132558)及[2025-03-12公開PDF第19頁外觀照片](https://c004.wzu.edu.tw/datas/upload/files/Documents/111_1075_%E6%A0%A1%E5%9C%92%E7%81%BD%E5%AE%B3%E9%98%B2%E6%95%91%E8%A8%88%E7%95%AB%E6%9B%B8_1140312.pdf#page=19)。現況表填於2023-12；兩來源照片拍攝日期未註明，不把文件日期當拍攝日期，不宣稱2026完全現況。來源照片、PDF及私用對照不隨模型公開。[完整來源及近似限制](sources.json)。

## 檔案
- [STL](model.stl)／[Blender](scene.blend)／[Python重建](build_model.py)
- [原始STL拓撲、法向、重建SHA及Blend一致性](validation.json)
- [0.2mm輪廓閉合與逐輪廓/合成多邊形有效性](contour-validity-check.json)
- [0.8mm XY薄特徵篩查](thin-feature-check.json)

## 數位檢查與列印限制
單一連接表面殼、正體積、所有邊恰有兩面、vertex-link單循環、無獨立內腔、原始法向一致；Python重建SHA相同，Blend與STL三角形一致。0.2mm實際STL斷面通過閉合及有效性assert，未用buffer修補無效多邊形。

屋頂十字架1.8mm方柱及橫桿角點造成8個薄篩警示層；0.8mm開運算未抹除任何獨立柱，非懸浮細柱。

這些均為數位幾何檢查，未經實際列印或真正列印切片器驗證。建議底板朝下、0.4mm噴嘴、0.2mm層高作為切片起點；簷口、雨遮、格柵及挑空需在切片器檢視支撐、橋接與可拆性；不得據此保證免支撐。

## 重建
Python 3.12，安裝requirements.txt，執行build_model.py；Blender以背景模式執行render_preview.py，產生實際STL預覽與scene.blend。接著依序執行validate_model.py、check_contour_validity.py、check_thin_features.py，退出碼均須為0且validation.json所有checks為true。

STL SHA-256：46fd8857dab8dadca6bc429ef697d4dbfe4a797c0b541347d331480a664c0a3c

[校區圖鑑](../../README.md)／[學校](../../../README.md)

## 歷史單色記錄

原 scene.blend、render_preview.py 與三張單色圖完整保留：正面（歷史檔案留存，不作本頁預覽）、背面（歷史檔案留存，不作本頁預覽）、立面（歷史檔案留存，不作本頁預覽）。它們是原模型重建及製造檢查的歷史證據，最新配色展示與交換檔位於 appearance/。原 8 層薄篩警示仍保留，沒有被本次外觀檢查取代。


