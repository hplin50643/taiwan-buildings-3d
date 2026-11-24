# 臺大社會社工館｜局部結構面參考補灰

## 2026-11-18 限定補色版

三道原水平帶底面的 6 個原三角，沿用低飽和灰。本次不增加套數、不改原始 STL 幾何，未補部位不代表實景材色。未實體試印。

[彩色 3MF](model-colored.3mf) · [可編輯 Blend](scene.blend) · [原 STL](model.stl) · [本版 3MF 相容性查核](3MF-COMPATIBILITY-QA.json) · [原建模與場景查核（歷史）](independent-verification.json) · [公開版清單](COLOR-RELEASE-MANIFEST.json) · [SHA256SUMS](SHA256SUMS)

| 現版模型預覽 | 現版模型預覽 | 現版模型預覽 |
| :---: | :---: | :---: |
| ![前斜視／正面](previews/front.png)<br>前斜視／正面 | ![後斜視](previews/rear.png)<br>後斜視 | ![立面](previews/elevation.png)<br>立面 |
| ![頂視](previews/top.png)<br>頂視 | ![左側](previews/left.png)<br>左側 | ![右側](previews/right.png)<br>右側 |
| ![水平帶底面細節](previews/band-undersides-detail.png)<br>水平帶底面細節 |  |  |

3MF 交付版僅補一個物件預設材質索引，嚴格 SDK 可讀取並在私有副本改色存回重開；原逐面色值、網格、Blender 與預覽不變。[公開相容化程式](source/normalize_3mf_compat.py)可重做此格式步驟。舊查核僅為建模檔案歷史，本版嚴格互通以新版相容性查核為準。

上級索引原代表圖保持原檔；新版彩色渲染請以上表為準。新色適用範圍及試印限制如下。下方舊版本導覽及資料只為歷史保存，舊面數、舊預覽與舊驗證不代表現版；以本章下載與公開版清單為準。

工作區中斷後由固定GitHub基底 `8f90ae2478f00cce6832a07de537f7d333f6dbc0` 重新取得並查證製作，不是舊完成包位元恢復。

只處理中央三條既有水平帶的完整下表面（6三角面，合計182.400043 mm²），沿用既有灰色 #B6B8B0，灰色面由208增至214；既有其他局部灰色保持，其餘未完成區不擴色。x=-19..19、y=-29.6..-28、z=24/38/52，均為模型毫米不是實測尺寸。補色採已存在的灰色材質，不新增材質。底面來源支持屬同一構件連續性推論，不宣稱六面均由照片逐面直接證實。

原STL／OBJ位元不變，1574頂點／3244三角面。牆、玻璃、混合山牆、平台、柱腳、其他窗框與未知面均不改；未完成整棟外觀。原場景隱藏mesh告示與FONT標示保留但不渲染，不以刪除物件達到無字預覽。

模型為外觀近似，不是施工或測繪資料；攝影日期與現況未確立，色值不是材料量測。公開候選僅模型、預覽及來源URL/限制，私人照片或PDF不隨包公開。

`scene.blend`可編輯；`model-colored.3mf`是逐面外觀交換，不代表已拆分多料實體。`model.stl`／`model.obj`為原幾何；`face-colors.json`、`domain.json`、`palette.json`記錄材料面域。六張全景及一張低仰角水平帶底面detail在previews。低仰角圖僅為補充檢視，不改正式scene的原相機；灰與中性灰相近，不以預覽亮度當成量測色。完整重建腳本和基底保存在私人備份。

未做GUI切片、實體試印、支撐或組裝驗證。原建構程式不自動產生本次補色。

## 新版檢核限制
獨立驗證確認4個原材質、Camera、world、燈光、hidden backdrop、FONT curves及節點與可讀持久設定保留。僅6面及其背後索引由1改0、輸出路徑改動。Blender 4.3.2讀取UV Sculpt懸空工具指標會崩潰，因此該子域排除；執行期依賴圖及session欄位也排除，不宣稱全檔位元一致。

## 歷史版導覽與說明

**局部補色未完成：僅中央三道獨立水平帶與左外格網局部補灰；磚牆、山牆與窗背未完成，入口基座及未知面仍中性。** `partial_color_incomplete=true`、`fully_colored_exterior=false`。同項目 `ntu-sociology-social-work`／`count_delta=0`，不新增套數。

| 前斜視 | 後斜視 | 正面 |
|---|---|---|
| ![前斜視](preview.png) | ![後斜視](rear.png) | ![正面](front.png) |
| ![背面](back.png) | ![西側](west.png) | ![東側](east.png) |
| ![頂視](top.png) | ![前橫帶](entry-detail.png) | ![左格網](facade-detail.png) |
| ![未完成山牆](roof-detail.png) | | |

## 材色範圍

中央三道原凸水平帶正向面y=-29.6，共6三角；照片可證左側格網向外x=-69的202三角，合208面為低飽和暖淺灰石材近似。其餘3036面未知中性，**不是實景灰色證明**。

依原幾何的真正外平面與各原box組合之投影聯集重新判讀，不盲抄來源face index。776個共面連通域全部材色一致，不centroid切色、不生成任何新邊界。橫帶及格網側返不自動推定同色。

中央山牆灰面和下方磚牆在原y=-28融合成共面，完整中性，不按z64取上部三角。入口門廊跨灰石上段與深色基底，原無物材界，整件中性。窗背／門格／圓窗背混框、簾、玻璃及實板，不能全黑或白。主牆灰框／腰帶／基座未有分面，不能全磚紅；屋頂、背面、基座與遮蔽面中性。

原3244三角、坐標、尺寸、STL、OBJ及build字節均不變，沒有新增窗框或修補幾何。既有原模型省略未核背面，不鏡射正門；補色不追認原幾何或稱完整現況。

## 來源與權利

臺大官方2010影像路徑下三張[6010](https://homepage.ntu.edu.tw/~cpo/2010photo/E/E9/IMG_6010.JPG)、[6011](https://homepage.ntu.edu.tw/~cpo/2010photo/E/E9/IMG_6011.JPG)、[6012](https://homepage.ntu.edu.tw/~cpo/2010photo/E/E9/IMG_6012.JPG)建築外照。2010路徑只是來源時期背景，拍攝日未獨立確認，不稱當今完整實測。精確hash及GO2225/獨審2224-v1見`COLOR-SOURCE-REGISTER.json`。

未確認CC授權，照片私存、不公開或作貼圖；原圖權利不被repo license取代，不保證商用。展示色不是精確色票。植物、人像、招牌不建模。

## 檔案與重建

`appearance.3mf`含2展示材，`scene.blend`實際面材／相機，`color-mesh.npz`原三角及material index。原STL自身無色、原OBJ未補材且兩者字節保留。

依`requirements.txt`執行`python colorize_model.py`、`python export_appearance.py`、`python validate_color.py`；Blender執行`render_color.py`及`verify_color_scene.py`。完整原build+color隔離重建保留、不自動刪。原件私存；兩個`ORIGINAL-MONOCHROME-README*`、舊`previews/`、舊QA／SHA清單是單色歷程，不是本次補色QA。

## QA與列印限制

原STL／三角multiset、封閉正體積、3MF索引及隔離重建見`COLOR-*QA.json`；重開見`SCENE-QA.json`；10張1200×900圖及三欄/hash見`DELIVERY-QA.json`。人工視看另交父終審。

**未實際列印。** 2展示材非驗證過四色列印工程，切片、材料映射、支撐及薄部強度另驗，不保證直接多料成功。
