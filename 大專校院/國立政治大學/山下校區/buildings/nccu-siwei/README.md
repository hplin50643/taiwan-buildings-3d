# 國立政治大學｜四維堂（修復前外觀近似）

## 模型預覽


山下校區。本件為依公開實拍與官方平面外輪廓自建的完整建物外觀近似模型，不是測繪、BIM或結構工程資料。




### 有據材料彩色預覽

沿用 2023 官方正面與防災資料側照，為原中性 1230 面補上同建物材質連續性：兩長側牆／深柱、既有高窗與可分回折面。全線、另一側與後方完整外牆／服務塊垂直面包含明示推估；屋頂、服務塊頂面、底座等仍中性。不是完整四面測繪色復原。

| 正斜視 | 來源角度 | 正立面 |
| :---: | :---: | :---: |
| ![彩色正斜視](appearance/front.png) | ![彩色來源角度](appearance/source-angle.png) | ![彩色正立面](appearance/elevation.png) |
| 背向 | 俯視 | 新外觀下載 |
| ![彩色背向](appearance/rear.png) | ![彩色俯視](appearance/top.png) | [3MF](appearance.3mf) · [Blender](appearance.blend) |

| 左側 | 右側 | 原版比較 |
| :---: | :---: | :---: |
| ![左側](appearance/left.png) | ![右側](appearance/right.png) | [兩角度原版比較](appearance-review-v2/comparison.png) |

[來源、材料與未驗證範圍](APPEARANCE.md)。原4張模型圖檔保留，不再於README展示；原模型幾何、STL與scene不改。

## 特徵與證據限制

完整長跨距禮堂外輪廓、突出中央入口、三組高窗、側面深直柱與高窗、側出入口雨遮；不以普通教室層窗替代禮堂立面。

本輪親看 2023 官方正面主照及防災 PDF 第 49 頁側照；第 48 頁表日 2021-10-01，側照攝影日未載，2026 PDF 建立日不是攝影日。側照支持灰米洗石子牆、深柱與淺色窗框；兩長側全線連續性仍包含推估。既有 2026 場勘公告本輪未重讀，不能由此推定工程進度或已完工。仍為修復前外觀近似。

背面舞臺與服務空間僅按官方平面輪廓近似，不新造窗；其既有外牆顏色為同族連續性推估，非直接背照核實。屋頂採淺坡保守體量，未測繪預力屋面實際曲率。2026修復案未作成品現況推定。

第三方照片/PDF不隨包散布。完整網址、頁碼與各自支持的特徵見 [sources.json](sources.json)。不將來源網頁更新日視為攝影日。

## 3D列印檔案

- [model.stl](model.stl)：毫米，88.0 × 150.0 × 45.8 mm，含底座最長150 mm，各館獨立比例
- [scene.blend](scene.blend)：從交付STL匯入的可編輯網格；形狀與STL經比較一致
- [build_model.py](build_model.py)：獨立參數化重建來源；[requirements.txt](requirements.txt)
- [SHA256SUMS](SHA256SUMS)：逐檔校驗；STL SHA-256：b8c7c0d959a7c39c1ac9f647ffc4c9daf9f25accd5c33a1a34eb653d8b01619e

底座朝下列印。建議先以0.2 mm層高、0.4 mm噴嘴在自己的切片軟體檢視，確認簷口、雨遮、門楣與深凹窗的支撐需求。細窗框已加粗，仍須依材料、噴嘴及散熱調整。不要把數位QA解讀成免支撐保證。

## 可重現數位QA

1. Python執行 build_model.py 重建模型。
2. Blender背景執行 render_preview.py 生成實際STL正背、正立面、俯視與scene.blend。
3. Python依序執行 validate_model.py、check_contour_validity.py、check_thin_features.py；任何非零退出必須停止交付。

[validation.json](validation.json) 全部checks通過：原始STL法向、繞序、正體積、水密、每邊兩面、vertex link單環、單一連通表面、無分离内腔壳、重建SHA一致、Blend幾何一致與150mm限制。

[contour-validity-check.json](contour-validity-check.json)：以z=0.071mm起、0.2mm逐層，共229层，輪廓degree2闭合、单个與組合Polygon有效；不修補或吞掉invalid。

[thin-feature-check.json](thin-feature-check.json)：0.8mm參考寬度形態opening、1mm取样，最大損失比例0.02395%，超过1%層數0。此為輔助幾何篩檢，不是全面最小壁厚或工具路徑。

尚未做Cura/Prusa实际切片或實體試印，不宣稱保證可印。


## 2026-11-13 底座撤除誤用洗石子身份
本次重新取得並實看政大校史官方正面照片，沿用歷史2023引用。照片可辨垂直洗石子牆、淺窗框與前方鋪地，但不證實側門水平門檻材色。本次不把垂直牆材外推到人工底座。
原88×150×3mm底座z3頂面是90面完整連通共面域，89面已明示未知0；側門石材bounds選域未限制垂直法線，讓1601一面誤用洗石子1。只撤1601為原unknown0，90面完整域一致，不聲稱現實地坪同材、不推定白色鋪面，不切新界、不改geometry。原821頂點1770面與其餘1769材索引、6原材保持。側門底和人工底座共面且連接，不代表實建邊界已測量；其他v2側背連續材、雨遮與原首頁不改。
保留原7張900×800、96samples、單執行緒原生鏡頭照明及scene/STL/previews（原交付無OBJ）。歷史工程QA與限制照存，無實體試印；本次僅有限外觀撤誤。本次公開交付版的精確校驗範圍見 CHECKSUM-SCOPE.md；不附私人研究檔識別或摘要。


## 公開交付版審核範圍
本版保留模型、材質及七張原生視角圖像。研究過程的比較圖、來源下載副本及完整審核工作紀錄不隨本版交付；既有儲存庫歷史檔案未刪除。公開校驗表僅驗證明列的公開檔案，不代替私人證據鏈，亦不構成新的工程或試印認證。
