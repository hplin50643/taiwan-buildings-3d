# 故宮博物院北部院區正館｜原模型材色更新

| 彩色預覽 | 彩色預覽 | 彩色預覽 |
|---|---|---|
| ![前斜視](preview.png) | ![後斜視](rear.png) | ![正面](front.png) |
| ![背面](back.png) | ![左側](west.png) | ![右側](east.png) |
| ![頂視](top.png) | ![入口細部](entry-detail.png) | ![立面細部](facade-detail.png) |
| ![屋頂細部](roof-detail.png) | | |

## 材色範圍
同一既有北院正館項目補彩（count_delta 0），非南院。原 5558 三角面、頂點、STL 與 build_model.py 不變；不新增斗栱、欄杆、文字、旗、人像或室內。原照片推估的簡化幾何不因材色更新而變成精確測繪。

- 2023 官方正照與 2020 廣角實景支持正面黃褐牆、淺色既有欄板／柱／浮雕、灰石入口和階梯。使用色族，不是校準色票；來源年份不等於整館當年精確紀錄。
- 屋面僅原有完整、明確前向的斜面採保守玉綠色；向後、向內、側向未唯一對位的坡面與大水平頂面中性。原抬角可令側面三角法線帶微小前向分量，不能僅憑該分量塗綠形成斜色片。本版採主要面朝向及各原屋面中心之前半域共同限制；後緣反折小唇即使法線朝前也保持中性。沒有分割任何三角面。
- 只有原獨立屋脊框之前段可用黃褐色近似；不增照片中的細脊飾。中央雨棚既有斜實體用灰綠、凸肋灰，仍是原不透明簡化實體，不造透明玻璃、題字或內部。
- 窗／門凹口只在既有分離面作暗陰影；不以整面玻璃填補缺失開口。未知後部、側部、屋頂平台及展示座中性，非全棟滿色。
- 七種外觀材料不是四色或多耗材列印切片方案；**未實際列印**，不保證免支撐。STL 本身不存色。

## 檔案與重建
[彩色 3MF](appearance.3mf) · [彩色 Blender](scene.blend) · [保留原 STL](model.stl)

原 build_model.py 重建原幾何；colorize_model.py 對完整原面分材，export_appearance.py 產 3MF 基本材料，render_color.py 產十圖。validate_color.py 驗原檔、三角座標、格式與保留隔離重建；verify_color_scene.py 重開實際 shader／索引／構圖。環境沿既有 numpy／trimesh／manifold3d／Pillow 與 Blender 4.3.2。

## 來源與權利
臺北旅遊網官方 2023 正照及 2020 廣角照片，僅核公開建築外觀。不含人物重製、室內、安全設施或地下空間。官方公開不等於 CC 或可任意再授權；原照只私人保留、不作貼圖、不隨模型公開，不保證商用。完整來源 URL／雜湊／限制見 COLOR-SOURCE-REGISTER.json。

## QA 與保留歷程
本次 COLOR-FORMAT-GEOMETRY-QA、SCENE-QA、FRAMING-QA、DELIVERY-QA 與獨審檔記錄實際模型和影像。舊 previews、舊報告與 ORIGINAL-MONOCHROME-README.md 保留作歷程，非本次色版驗證；上方十圖與 scene.blend 為新入口。原包、原色初版及保留隔離重建私人保存，不刪檔。
