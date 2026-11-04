# 奇美博物館｜原模型材色更新

| 彩色預覽 | 彩色預覽 | 彩色預覽 |
|---|---|---|
| ![前斜視](preview.png) | ![後斜視](rear.png) | ![正面](front.png) |
| ![背面](back.png) | ![左側](west.png) | ![右側](east.png) |
| ![頂視](top.png) | ![列柱門廊](entry-detail.png) | ![前翼窗帶](facade-detail.png) |
| ![圓頂細部](roof-detail.png) | | |

## 材色範圍
同一奇美主館既有模型補彩（count_delta 0）。原 17960 三角面、頂點、STL 與 build_model.py 完全保留，不加雕塑細節、庭園、噴泉、橋、人物或室內。原兩翼深度、端部和背面比例仍是舊模型概化，不因補色成為新測繪或精確現況。

- 官方逆光正面實景支持**前石質表面的白灰色族**：前立面、原可辨窗框和六柱門廊；深灰只用於既有前凹口底面，不把整面作玻璃，不新增梃線或修改洞口。
- 原肋狀圓頂**僅前半部**採節制灰色；後半、頂部整個原簡化天使／頂飾保持未證中性，沒有金色天使的色證，不借其名稱猜金色。
- 水平大屋頂、側後牆窗及展示底座中性。圓頂與前後材色截止是來源可見域／未知域界線，**不是實景換漆線**。所有材質只指定完整原面；若一面跨界，寧保中性，不切新面拼色。
- 照片逆光、未確證拍攝日，HEX 只是展示近似色族，非校準色票或某年復原。另館網 banner 是室內照，排除於外觀材色。
- 四個外觀材質標籤**不是已驗證四色耗材切片檔**；未實際列印，不保證免支撐。STL 本身不存顏色，本次不修改原尺寸及列印幾何。

## 檔案與重建
[彩色 3MF](appearance.3mf) · [彩色 Blender](scene.blend) · [原 STL](model.stl)

build_model.py 重建保留原幾何；colorize_model.py 只指定原面材料；export_appearance.py 輸出 3MF 基本材料；render_color.py 輸出十圖及場景。validate_color.py 驗三角座標、原檔、3MF 與隔離重建，verify_color_scene.py 重開實際 shader／面索引／構圖。使用既有 numpy／trimesh／manifold3d／Pillow 與 Blender 4.3.2；隔離重建目錄私人保留、不刪除。

## 來源與權利
臺南旅遊網公開官方正面實景作有限色族參考；網址與雜湊見 COLOR-SOURCE-REGISTER.json。公開可讀不等於 CC 或照片自由再授權；原照片只私人備存、不公開、不作紋理，不保證商用。未取得逐向照片的屋背／端面不自動延伸色證。

## QA 與原件歷程
本次 COLOR-FORMAT-GEOMETRY-QA、SCENE-QA、FRAMING-QA、DELIVERY-QA 與獨立視覺審核綁定新色版。舊 previews、舊驗證報告及 ORIGINAL-MONOCHROME-README.md 原樣保留，非本次色版入口；以上十圖與 scene.blend 為新色版。原檔不刪除，補色不增加建築套數。
