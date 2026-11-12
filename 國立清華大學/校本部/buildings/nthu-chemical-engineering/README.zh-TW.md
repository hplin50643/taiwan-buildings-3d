# 清華化工館｜整修前舊照橫帶局部補色

**局部補色未完成：保留原 50 個前／右橫帶外表面，新增 174 個有限飾帶返側面採同構件淺色推定，共 224 面配色；其餘 2,700 面未知中性。粉牆、玻璃等未完成。整修前舊公開照片外觀近似，非2026整修後現況。** `partial_color_incomplete=true`、`fully_colored_exterior=false`。同項目`nthu-chemical-engineering`／`count_delta=0`，不新增套數、不表示整修工程完工。化工館不是化學館。

| 前斜視 | 後斜視 | 正面 |
|---|---|---|
| ![前斜視](preview.png) | ![後斜視](rear.png) | ![正面](front.png) |
| ![背面](back.png) | ![西側](west.png) | ![東側](east.png) |
| ![頂視](top.png) | ![前橫帶](entry-detail.png) | ![右橫帶](facade-detail.png) |
| ![未完成屋面](roof-detail.png) | | |

## 材色範圍

原 16 個前橫帶真正外表面（y=-29.55、兩翼 x[-56,-24]/[24,56]）及 8 個右橫帶外表面（x=56.55、y[-29,39]），共 50 原三角保留。原構件高程 z=15/26/37/48/59/70/81/87，厚 0.9。這次從原 build 的 24 個有限盒形邊界選出 275 面；僅保留整個共面連通域都在飾帶範圍內者，排除 51 個與未知大牆平面相連的候選面。新增 174 面，合計 224 面暖灰白，2,700 面保持未知中性。沒有切割三角或擴染大側牆、背牆。

官方照片支持飾帶的淺色族；同構件側返、頂面及底面色彩連續性為合理推定，並非逐面照片實證或量測色票。837 個共面連通域仍維持單一材質，未知中性不代表實景灰色。

粉色主壁包含未有幾何界的白直帶，不整牆粉色；上山牆白帽混域、入口山牆粉白框混域、全高中央spine近頂深孔無獨立界，全部中性。圓柱柱基柱帽、原簡化階梯磚白帶、窗背玻璃框簾反光亦不一色推定。未納入的飾帶混合域、後左牆、屋面主體與基座仍未知中性。前後材色範圍只資料覆蓋，不是真實材料接縫。

原2924三角、坐標尺寸、STL／OBJ／build字節保留，不新增切面或幾何。既有近似幾何不由材色審核追認，不能聲稱現況精測或全色完成。

## 來源、年代與權利

清華官方公開正面與斜側實照僅作色族參考，原照拍攝日期未確定；1993建成年份不是拍攝日。來源URL及SHA見`COLOR-SOURCE-REGISTER.json`。必保留原補充`chemical-engineering-era-clarification.zh-TW.md`：**整修前舊公開照片外觀近似，非2026整修後現況**；2026公告記施工中，不能由預定日期推完工。本次不改原版本/原幾何。

原照私存、不隨模型公開或作貼圖；未見CC不得沿repo license宣稱照片自由商用；HEX是展示近似非色票，未保證商業授權。

## 檔案、重建及 QA

`appearance.3mf`含2展示材，`scene.blend`有實際面材，`color-mesh.npz`保原三角與material index。原STL無色、原OBJ及build字節保留。原單色README另存`ORIGINAL-MONOCHROME-README.zh-TW.md`（及原包有的README），舊previews與QA是歷程不是本次新審。

依`requirements.txt`執行`python colorize_model.py`、`python export_appearance.py`、`python validate_color.py`；Blender跑`render_color.py`與`verify_color_scene.py`。原build+color全隔離重建目錄保留不刪。格式/三角multiset/封閉正體積見`COLOR-*QA.json`，重開`SCENE-QA.json`，10 張 1200×900 圖與雜湊在後續獨立審核完成後綁定目前交付 QA。先前 QA 原樣保存在 `qa/trim-return-previous/`；舊獨立色審與 FREEZE-MANIFEST 僅對應舊版本，不作本次放行依據。

**未實際列印。** 2材展示不是已驗四色切片工程；支撐/薄部強度/材料映射另驗。

## English limitations

Partial historical trim-return color study only. The original 50 observed front/right outward faces remain. A further 174 original faces inside the finite trim-member boundaries receive inferred pale color continuity, for 224 colored faces and 2,700 unknown-neutral faces. Fifty-one candidate faces were rejected because their connected coplanar domains extend into unverified broad walls. No triangular material seams, new cuts or geometry were introduced. All mixed pink walls, glazing, columns, stairs and roof mass remain neutral. Original 2,924 triangles and STL/OBJ/build bytes are unchanged. This is a pre-renovation public-photo approximation, not the renovated 2026 condition or evidence of completed construction. Source capture dates are unknown. Reference photos remain private; no texture redistribution. Not physically test-printed; two display materials are not a validated multicolor slicing job.

## 本次飾帶返側核對

參見 `TRIM-RETURN-SOURCE-QA.json`、`appearance-materials.json` 與 `COLOR-ASSIGNMENT-QA.json`。歷史 `INDEPENDENT-COLOR-VISUAL-QA.json`、原 FREEZE-MANIFEST 與前次 QA 保留原文及雜湊，不能當作本次獨立審核結果。
