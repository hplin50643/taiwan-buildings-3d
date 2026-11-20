# 北大體育館藍框右側尾端 2 原面補色

原4760三角面中，僅3825、3827由淡混凝土展示材0改為既有藍框材1 `#51A9C9`。其餘4758面、幾何、頂點、面序、7材RGBA/shader/roughness全部保留。新版面數 `[3257,142,42,36,467,590,226]`。

## 完整框域與有限來源推論
全原網格在x79平面做共享原邊連通，最大框域是3805、3807、3811、3813、3821、3823、3825、3827共8面，模型面積69.5mm²。前6面原本已藍。後2面因舊面心 `y<1.01` 門檻而漏色；本次補齊3.75mm²尾段，消除同框上的三角對角材界。**兩改面不是獨立矩形或完整單件自然面**，它們是完整8面側框的一部分。名義座標x79、y2..5、z45..47。側窗玻璃、銀框、灰主牆／簷、任意展示背切面均不擴色。

初步曾因後段深度與牆頂交界不足而HOLD；再親看校方原幅局部，清楚看見右側玻璃上方藍框一直連至後端藍窄豎框，與灰牆／灰簷分界可辨。經交叉來源與原面域審查後，採**同一已辨識藍框的有限材族連續推論**，不是逐像素配準後段深度，不追認原模型比例為測繪，亦不代表原側窗玻璃及窗櫺均精確。這是原有幾何內的有限色域修正，不改Boolean、框深、牆高或展示裁切。

來源（只提供連結／內容識別，不附原照片）：
- 校方原照：https://cms-carrier.ntpu.edu.tw/uploads/_bbe39a1633.png
  SHA256 `fe075bb25f936bc272dbc9c157b2c604ee28285958f5cbe1d56597d9b49f948d`。
- 建築師作品攝影：https://www.twarchitect.org.tw/web2015/wp-content/uploads/2019/08/201909a5-2.jpg
  SHA256 `f475d991317a4afc2fbb1ccf12ba6828c789ad990047ad2a0f7ea2141833daa5`。

官方2025-12-15是發布日期，不是拍攝日期；2019文章脈絡亦不自動證明精確拍攝日。不宣稱2026現況、實測色票或材料組成。

## 自足精確重建
固定基準repo `hplin50643/taiwan-buildings-3d`，commit `8f90ae2478f00cce6832a07de537f7d333f6dbc0`，相對路徑 `國立臺北大學/三峽校區/buildings/ntpu-gym-colored-bay-entry-facade-segment`。

包內 `rebuild-baseline/` 保存原STL、mesh.json、model.3mf與scene.blend，四檔SHA256由wrapper鎖定：

```sh
blender -b -t 1 --python-exit-code 1 -P rebuild_blue_return.py -- --baseline rebuild-baseline --out rebuilt
```

Blender4.3.2／NumPy。原build_model.py是歷史幾何／材質入口，不覆寫；單獨重跑舊程式會恢復兩尾端舊色。新版wrapper直接使用SHA鎖定原四檔，只補指定兩面。原README字節前綴完整保留，舊QA及雜湊為舊版紀錄；新版見MANIFEST.json。

`render_blue_return.py` 從新場景讀取並重渲原5張1200×1200、Cycles48視角front/rear/elevation/top/right_oblique，保留原構圖、材質、燈光、世界、相機規則，不將渲染暫態保存回scene。PNG無損清除文字／日期／私有路徑metadata。rear仍為任意展示背切面，不是假稱真實後立面。

## 驗證界線
完整原場景RNA僅8差異：兩面在polygons/loop_triangles/material attribute共6處指派，加物件side_color_scope及source_color_mesh_sha256兩新屬性。original_STL_sha256與limitations原值保留。全部7原材與節點、物件transform、相機、燈光、世界皆不變；沒有孤立材遺失或額外fake_user變更。

3MF完整XML只兩面p1/p2/p3共6屬性0→1，pid2、原object fallback與所有座標字串、其餘XML/ZIP內容不變。clean重建STL/meshJSON/3MF/changeJSON逐byte一致，Blend完整RNA語義一致（非宣稱容器byte相同）。Strict SDK零警告、私人改材保存重讀、Blender私人頂點與面材編輯保存重開通過，公開檔未被私實驗改動。

本次沒有GUI切片或實體試印。保留原0.75mm藍窗窗櫺局部侵蝕消失、支撐與尺度限制，不因補色將製造風險宣稱解除。7展示材不是已驗多色列印耗材配置。原照片、裁圖與私人編修檔不在公開包。
