# 長榮大學校門十字架鐘塔 — 限域外觀配色

| 模型預覽 | 模型預覽 | 模型預覽 |
| :---: | :---: | :---: |
| 正斜視<br>![正斜視](previews/front.png) | 後斜視（背向寬面同材質推論）<br>![後斜視](previews/rear.png) | 寬面立面<br>![寬面立面](previews/elevation.png) |
| 窄側<br>![窄側](previews/side.png) | 頂面<br>![頂面](previews/top.png) |  |

## 本次鐘塔門柱背向寬面同材質延續

僅將兩片塔板背向的 126 個完整原中性三角，延用正向寬面既有淡磚紅代理色。原 126 個已色面與其理由、兩槽色盤材料完全保留；完成後 252 面淡磚紅、248 面中性。全部 500 原三角／216 點、STL bytes、面序與幾何不變，不切面、不加厚。

逐片以原塔板 x 定值面、y=−12…12 mm、z=5…150 mm 與負 x 法向核對全部三頂點，扣除原十字開孔、小洞及內部橫連桿接觸區。實際面積約 6,744.980026 mm²，解析面積 6,744.98 mm²。窄側邊、灰帽、孔壁、橫連桿及底座全保持原中性；不把整座塔塗紅。

官方文字與空照支持既有紅褐塔板及淺色邊緣。本次背向寬面明示為同一塔板的同材質推論，不是獨立背面照片確證，亦不是量測色值或 2026 現況。原模型仍屬簡化近似造型，非測繪、施工圖或實體試印。參考圖片僅供私人審核，不加入公開包。

新版 QA 在 `qa-continuous-walls/`，歷史 QA 保留。新版重建 `python appearance/source/build_continuous_walls.py`；交換驗證使用 `verify_continuous_exchange.py`；Blender 背景執行 `render_continuous_walls.py` 與 `verify_continuous_scene.py`。來源 ZIP 含原 STL、建模腳本與有限域，不含照片。根預覽與歷史說明可能仍反映原版中性造型；本節及 appearance 新預覽記錄此次補色範圍。原製造限制完整保留。

## 前版說明與保留限制

本層為既有地標構造物的附加材質，不是新建築套數，不是慎行鐘或長榮堂。原 STL bytes、500 三角座標與面序完全不變；沒有移點、切面或新增幾何。

依官方航拍和官方文字「淺磚紅色」，僅對兩片塔朝 +X 的寬大立面著色：x=-5.2／8.8 mm，y[-12,12]、z[5,150]。所有三頂點都須位於有限平面範圍內；分別 68／58 面，合計 126 面、6744.980026 mm²。#AD7868 是低飽和視覺代理，未經儀器測色、不是官方色號。其餘 374 面維持 #AAA79F 中性代理，包括反面、窄側、灰頂、孔壁、橫繫及底座；中性不代表實景顏色判定。

原雙塔孔形、連繫、尺寸與比例為近似；不補斑駁、細紋、鐘具或小孔細部，不以配色假裝完整復原。本次僅呈現官方歷史照片可支持的範圍，不聲稱 2026 現況。未做實體列印或重算原歷史製造 QA。

## 檔案與重建
- [彩色 3MF](cjcu-gate-cross-tower-appearance.3mf)、[Blender 原生場景](scene.blend)。
- [色票](palette.json)、[原三角材質對照](face-materials.json)。
- 五圖：[正斜視](previews/front.png)、[後斜視](previews/rear.png)、[寬面立面](previews/elevation.png)、[窄側](previews/side.png)、[頂面](previews/top.png)。
- [來源](SOURCES.md)、[許可](LICENSE-NOTICE.md)。


原 model.stl 與 appearance 同父層。Python（numpy 2.3.5、lib3mf 2.5.0）依序執行 source/build_appearance.py、source/verify_exchange.py、source/verify_material_boundaries.py；Blender 4.3.2 執行 source/render_appearance.py、source/verify_scene.py。重建另於乾淨目錄進行，核對 3MF、maps、五 PNG bytes；Blend 核語義，不宣稱二進位確定性。驗證含 strict lib3mf 真材質修改存讀與 Blender 真材質／頂點修改存讀及重開渲染。
