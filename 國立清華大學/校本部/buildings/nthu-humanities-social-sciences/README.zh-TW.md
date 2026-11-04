# 清華人社院｜冠前與斜檐鼻端局部補灰

**局部補色未完成：僅冠前、前鐘亭柱及兩斜檐鼻端灰色；塔身、主牆與其餘未知面未完成。跨年代外觀近似，非2026全貌。** `partial_color_incomplete=true`、`fully_colored_exterior=false`。同項目`nthu-humanities-social-sciences`／`count_delta=0`，不新增套數。

| 前斜視 | 後斜視 | 正面 |
|---|---|---|
| ![前斜視](preview.png) | ![後斜視](rear.png) | ![正面](front.png) |
| ![背面](back.png) | ![西側](west.png) | ![東側](east.png) |
| ![頂視](top.png) | ![真檐鼻](entry-detail.png) | ![塔冠柱](facade-detail.png) |
| ![未知屋面](roof-detail.png) | | |

## 材色範圍

原厚鞍冠真正前剖面y8.5的4面、兩前鐘亭柱y11.2各2面，以及兩斜檐x-8真正竪鼻端各2面：共12三角灰混凝土色族，4194面中性未知，**不是實景灰色證明**。逐原構件全頂點、鼻端完整矩形面積核驗；1195共面連通域均一致，不硬切z、不以大牆三角造斜色楔。

全高塔身有上灰下粉而原無材界，全塔身中性；鐘冠與柱側背未釋出不推色。兩屋檐上皮、底面、托架不把陰影當黑材；原厚鞍只是抽象雕塑近似，不改輪廓。兩翼混粉／灰／磚／遮蔽無界，主壁全中性。窗背混玻璃、空調、框、反光及植物，不一律玻璃或綠色。台階、基地、未知背面不染。

原4206三角、尺寸、STL／OBJ／build字節保留，不新增切面、雕刻或幾何。分色與中性界線僅來源覆蓋，不是真實不同材界；色審不追認既有近似幾何，也不宣全色完成。

## 來源年代與權利

四張來源為校方教學外照、校史2020展覽舊影、校友遠景、承包商外部作品照，皆已實看；各原URL/hash見`COLOR-SOURCE-REGISTER.json`。**1990落成與2020刊登不是經認證拍攝日**；照片跨年代不得拼作2026單日完整現況。不使用室內與安全資料。

原照私存、不隨模型公開、不作貼圖；未見CC，不沿repo license推定照片自由商用。材色僅概略族群非測量色票，不保證商用授權。

## 檔案、重建及 QA

`appearance.3mf`含2展示材、`scene.blend`實際面材、`color-mesh.npz`保原頂點/三角/材索引。原STL無色，原OBJ和build字節保留。原單色README另存`ORIGINAL-MONOCHROME-README.zh-TW.md`（及原包有的README），舊previews/QA是歷程非本次色審。

依`requirements.txt`執行`python colorize_model.py`、`python export_appearance.py`、`python validate_color.py`；Blender跑`render_color.py`、`verify_color_scene.py`。原build+color完整隔離重建目錄保留不刪。格式/三角multiset/封閉正體積見`COLOR-*QA.json`，重開`SCENE-QA.json`，10張1200×900與hash綁定`DELIVERY-QA.json`。父另人工終審。

**未實際列印。** 2材展示不是已驗四色切片工程；材料映射、支撐與薄部強度另驗。

## English limitations

Partial reference color only: saddle front4, front belfry post faces4 and two vertical eave noses4 triangles. Other4194 triangles remain unverified neutral. Original4206 triangles, STL/OBJ/build bytes unchanged; no new geometry and count_delta0. Existing thick saddle abstraction is not corrected or newly validated. Four references span unknown capture dates;1990completion and2020publication are not capture dates, and this is NOT a complete2026condition or fully colored reconstruction. Source photos private; no texture redistribution. Not physically test-printed.
