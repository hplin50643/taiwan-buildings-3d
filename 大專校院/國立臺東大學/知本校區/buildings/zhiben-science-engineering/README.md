# 知本理工主要教學群｜左前框正面局部灰白

## 2026-11-18 限定補色版

左前玻璃盒上梁左端的 2 個原三角，延續灰白材質。本次不增加套數、不改原始 STL 幾何，未補部位不代表實景材色。未實體試印。

[彩色 3MF](appearance.3mf) · [可編輯 Blend](scene.blend) · [原 STL](model.stl) · [本版數位查核](QA-SUMMARY.json) · [公開版清單](COLOR-RELEASE-MANIFEST.json) · [SHA256SUMS](SHA256SUMS)

| 現版模型預覽 | 現版模型預覽 | 現版模型預覽 |
| :---: | :---: | :---: |
| ![前斜視／正面](front.png)<br>前斜視／正面 | ![後斜視](rear.png)<br>後斜視 | ![頂視](top.png)<br>頂視 |
| ![前斜視](previews/color-20261118/preview.png)<br>前斜視 | ![背面](back.png)<br>背面 | ![東側](east.png)<br>東側 |
| ![西側](west.png)<br>西側 | ![入口細節](entry-detail.png)<br>入口細節 | ![框架細節](facade-detail.png)<br>框架細節 |
| ![屋面細節](roof-detail.png)<br>屋面細節 |  |  |

上級索引原代表圖保持原檔；新版彩色渲染請以上表為準。新色適用範圍及試印限制如下。下方舊版本導覽及資料只為歷史保存，舊面數、舊預覽與舊驗證不代表現版；以本章下載與公開版清單為準。

## 2026-11-18 限定更新：左端上梁完整窄側

上述原版文字原樣保留作版本記錄。本輪只將原三角 1107、1110 由中性材 1 改為既有灰白材 0；現在共 12 白面、2980 中性面，仍非全色。原 10 白面與其餘 2990 指派不動。這是同一已辨識上梁的有限材色連續推論，不是照片逐深證實，也不擴及對端或框側、底、背。

詳見 [BEAM-END-CONTINUITY.md](BEAM-END-CONTINUITY.md)、[QA-SUMMARY.json](QA-SUMMARY.json) 及 [公開版清單](COLOR-RELEASE-MANIFEST.json)。新增 SHA 鎖定重建入口 `rebuild_beam_end.py`；原色彩程式沒有覆寫或更新，單跑舊流程仍只得到原 10 白面。

## 歷史版導覽與說明

**局部補色未完成：僅左前凸玻璃盒上梁與兩側框正面10原三角灰白；玻璃屋坡混材牆未完成／非全色。** partial_color_incomplete=true、fully_colored_exterior=false。同項 zhiben-science-engineering／count_delta=0，原主要相連教學群不拆棟，不是全理工院落或2026現況測繪。

| 前斜視 | 後斜視 | 正面 |
|---|---|---|
| ![前斜視](preview.png) | ![後斜視](rear.png) | ![正面](front.png) |
| ![背面](back.png) | ![西側](west.png) | ![東側](east.png) |
| ![頂視](top.png) | ![左前凸框](entry-detail.png) | ![五完整前矩形](facade-detail.png) |
| ![中性缺天窗屋坡](roof-detail.png) | | |

## 材色範圍

枚舉原y−24.2全部三頂點共面6三角與y−24.5全部4三角，先不設x/z裁切，再共邊連通核3+2個完整矩形。上梁包含中央長面與兩側各0.25mm小外端，原柱遮擋分割所致，不能漏掉外端；兩側真框前面z15..36.5，不擴地面實填支撐。完整10面灰白、其他2982中性。原2992三角與頂點完全不改，不增分面或新框。

原三大屋坡缺照片白天窗/屋頂中斷，不整灰屋皮；玻璃凹背、梃、下方填實量體、框側頂底全部中性。主牆混白構造與黃綠板/暗窗，原無可靠界，全部中性。其他廊柱、簷棚、階、後面與底座中性。中性色不等於實景灰，資料覆蓋界不等於真正材料接縫。

## 來源與版本

親看校方正斜實景，左側凸玻璃盒灰白上梁/兩框可對原獨立前域。另綠建築合成圖上為另一理工入口，只作語義；下為師範學院，明確排除，不移色。拍攝日期未核，修改/發布日期不是capture，不宣2026現況。原列印厚化框/窄翼/窗洞近似保留，不以色審背書幾何精確。照片私人，不公開貼圖；未見CC不推商用，HEX僅名義色族。

## 檔案與 QA

原STL/build字節與2992原三角不變；immutable原包無OBJ，原builder只產STL，不聲稱保留原OBJ。原README保存ORIGINAL-MONOCHROME-README.md，舊單色previews/QA不替代新QA。appearance.3mf兩展示材與scene.blend真面材，color-mesh.npz同原幾何。精確requirements隔離build+color，核封閉正體積/完整三角、3MF材色/Blender重開、10張1200×900。重建保留不刪。未實際列印，非已驗多色切片。

## English limitations

Partial only: entire original upper-beam front plane y=-24.2,6 triangles in3 rectangles,plus two jamb fronts y=-24.5,4 triangles in2 rectangles. Both tiny beam ends beyond the jambs are included. Whole planes enumerated without x/z preclipping;all659 coplanar components uniform.10off-white triangles/2982neutral. Original2992 triangles and STL/build bytes unchanged,noimmutableOBJ,count_delta0. Missing roof skylights,glass/mullions,lower filled support mass,mixed walls and unknown rear remain neutral. Principal connected teaching facade group only,not entire college. Matching school exterior photograph is primary;alternate engineering entrance and unrelated teachers-college composite do not transfer color. Capture unknown,no2026survey or geometry-accuracy endorsement. No public source images/textures;not testprinted.
