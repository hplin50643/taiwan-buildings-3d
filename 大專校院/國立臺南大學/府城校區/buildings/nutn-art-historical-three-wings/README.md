# 國立臺南大學｜2024年8月部分拆除前歷史美術館三翼

## 模型預覽

| 歷史中庭總覽 | 正立面 | 背側中性面 |
| :---: | :---: | :---: |
| ![](previews/front.png) | ![](previews/courtyard_elevation.png) | ![](previews/rear.webp) |
| 翼端 | 平面頂視 | 中央梯塔 |
| ![](previews/left_end.webp) | ![](previews/top.png) | ![](previews/stair_detail.webp) |

**這是北棟與中棟於2024年8月拆除前的歷史外觀近似模型，不是2026現況，也不是現存南棟單獨模型。** 官方現行系網註記北棟與中棟已拆除、南棟仍使用；同站保留的舊照片與平面用於本件歷史重建。

## 範圍與依據
- 官方1F/2F平面：U形三翼、中庭開口；3F僅右側L形。無北向箭頭，模型座標不是地理方位。
- 兩張官方中庭照片：白色走廊、淺杏色帶與中央曲面樓梯屏牆。曲面塔對應中央朝庭院凸出的梯間，非翼端獨立塔。
- 外側立面缺照片，採中性封閉，不表示現實無窗。屋頂設備、金字美術館題字、樹木、雕塑與室內未建。
- 平面為配置示意，無尺寸標註；絕對尺寸、層高、柱距、窗列/窗型、梯塔半徑均為近似。不能由本模型取得實測尺寸。
- 官方現頁面積893.2/357.82/1842.95㎡為各棟總面積，不是單層面積；本模型未以面積表反推精確尺度。

翼端、背側中性面與中央梯塔三張展示圖改用 1200 × 900 無損 WebP，與原 PNG 的 RGBA 像素逐一相同。正面代表圖、正立面、頂視、模型、場景和既有 QA 不變。用 Blender 4.3.2 與 Pillow 13.0.0（libwebp 1.6.0）執行 `python export_display_webp.py` 可重新輸出這三張 WebP，不覆寫交付場景或其他視角；工具會先核對渲染像素的 SHA-256。需要原始 PNG 位元時，請下載固定版本的 [原翼端 PNG](https://github.com/hplin50643/taiwan-buildings-3d/blob/870b9b96c4638755150001d7f323a74340406521/%E5%9C%8B%E7%AB%8B%E8%87%BA%E5%8D%97%E5%A4%A7%E5%AD%B8/%E5%BA%9C%E5%9F%8E%E6%A0%A1%E5%8D%80/buildings/nutn-art-historical-three-wings/previews/left_end.png) · [原背側中性面 PNG](https://github.com/hplin50643/taiwan-buildings-3d/blob/870b9b96c4638755150001d7f323a74340406521/%E5%9C%8B%E7%AB%8B%E8%87%BA%E5%8D%97%E5%A4%A7%E5%AD%B8/%E5%BA%9C%E5%9F%8E%E6%A0%A1%E5%8D%80/buildings/nutn-art-historical-three-wings/previews/rear.png) · [原中央梯塔 PNG](https://github.com/hplin50643/taiwan-buildings-3d/blob/870b9b96c4638755150001d7f323a74340406521/%E5%9C%8B%E7%AB%8B%E8%87%BA%E5%8D%97%E5%A4%A7%E5%AD%B8/%E5%BA%9C%E5%9F%8E%E6%A0%A1%E5%8D%80/buildings/nutn-art-historical-three-wings/previews/stair_detail.png)。Blender 重渲染的時間與路徑欄位可能不同。

[原發布逐檔清單](https://github.com/hplin50643/taiwan-buildings-3d/blob/870b9b96c4638755150001d7f323a74340406521/%E5%9C%8B%E7%AB%8B%E8%87%BA%E5%8D%97%E5%A4%A7%E5%AD%B8/%E5%BA%9C%E5%9F%8E%E6%A0%A1%E5%8D%80/buildings/nutn-art-historical-three-wings/manifest.json)保留於原提交；本目錄的校驗表與清單對應目前展示檔。

## 檔案
[STL](model.stl) · [多色3MF](model.3mf) · [Blender](scene.blend) · [建模程式](build_model.py) · [來源](SOURCES.md) · [幾何QA](QA.json)


## 重建
Python 3，numpy、trimesh、manifold3d；Blender 4.3含numpy。於本目錄執行：python build_model.py、python validate_model.py；以Blender背景模式執行 render_model.py，--out指定本目錄。原創部件保存於construction-parts.json，Blender隱藏集合為前布林可編輯件，不是逐件列印包。無來源照片、外連材質或腳本嵌入BLEND。

## 列印與可信度限制
- 統一網格封閉/連通與格式核對僅為幾何完整性，**未實體試印**，不保證直接可印或免支撐。
- 顯示尺度約221.7×103.8×38.7mm；走廊懸板約0.72mm、細框/色帶約0.075–0.15mm，宜放大/加粗，依噴嘴、材料、支撐與切片檢查。
- 3MF為標準基礎材質色，不含特定切片機的噴頭配置；色表7項、實際表面6色。
- 本件不是現況調查、精確測繪、室內動線或建築法規/無障礙認證。
