# 中央科學五館｜側背材料連續性增補

## 範圍

僅將 48 個原中性面指定為原白灰材料。1509 頂點／3246 三角面、物件 transform、150 × 144 × 108 mm 尺寸、所有原彩面、原材料 RGBA 與 roughness 全部不變。沒有新增頂點、窗、黃色面板、細欄杆或設備。原 STL、OBJ、scene.blend、建模腳本、三張 previews 與幾何 QA 保留。

## 這輪實看來源與限制

- [Commons 原照片](https://upload.wikimedia.org/wikipedia/commons/a/a4/NCU_Science_Building_V.JPG)：新下載完整 4000 × 3000 原圖並親看。EXIF DateTimeOriginal 為 2013-06-01 12:14:11。可見內院雙翼白灰磁磚、灰綠窗／簾、粉褐低遮屏、米白轉角陽台及右下黃板。原 sources.json 記錄 SSR2000、CC BY-SA 3.0／GFDL；本輪來源頁逾時，作者與授權資訊沿用原記錄，不宣稱新核驗授權頁。
- [校方無障礙校園頁](https://love.adm.ncu.edu.tw/NCU_counsel/NCU-barrier-free/)本輪重讀，確認 SB5 標為「科學五館 Science Building 5」。[官方實照](https://love.adm.ncu.edu.tw/NCU_counsel/NCU-barrier-free/images/SB5/1.jpg)首次 HTTP 503，正常重試成功，250 × 196 圖完整親看；支持同一內院材料配置，不是獨立外背證據，拍攝日期未知。
- [學系地圖](https://in.ncu.edu.tw/~ncu7141/)及其[科五圖示](https://in.ncu.edu.tw/~ncu7141/image/new_map/science5.png)已讀並親看；圖示是簡化插畫，只用辨識 L 形建物與所在，不作背面材色、窗數、尺寸或現況證據。
- 2015 新生導覽的科五頁可讀，但圖片直接下載 HTTP 403，未改路繞過，亦未計為本輪實看照片。防災 PDF、測量與現地調查本輪未取得。不聲稱 2026 完整現況、歷史色復原、校色量測或官方色票。

公開包只含文字來源 URL／用途／限制與雜湊，不含來源照片、插畫、PDF、HTML 或本機參考路徑。詳[來源記錄](appearance-review-v2/source-register.json)。

## 外牆與人工切面判別

原 build_model.py 以完整 L 形雙翼與左端高牆箱體聯集建模；原註解明說外背立面因資料不足刻意素面，沒有將建築切半或用剖切平面裁掉後半。y=56、x=57、x=-65、y=57 及端牆外露回折為這些完整量體的邊界外牆，不是人工剖切面。這項確認代表原模型意圖，不代表已測得真實建物深度或完整背面。

## 本輪新增材料分區

- y=56 的完整主翼／右翼後牆與女兒牆背面，共 34 原中性面；x=57 完整右翼外側 2 面。延續可見主牆白灰材料，明示是整構件材料連續性推估，不把大素面當成新證實的無窗背牆。
- 左端高牆 x=-65 外側 2 面、y=57 背面 2 面、x=-57 外露回折 6 面；主翼上端 x=40.5 外露面 2 面。同一白灰殼體的完整面延續，非逐面實照確認。
- 右翼前端 y=-60 的 10 個原中性三角面在粗化網格中跨越上白灰牆與照片中可疑的下層混材帶，沒有完整橫向分界。本輪整個支持面保留中性，不依三角中心、局部盒選或斜邊切出假色界。
- 其餘 853 面維持原中性，包括完整上述前端、平屋面、底座、原窗洞回折與未定片段；不把灰窗框／陰影凹面武斷改白。原灰粉褐遮屏、白灰支柱／廊板、米白陽台、灰綠窗背與淺灰通氣柱全部保留。沒有把整棟染粉，也沒有增加黃色地板、黃板、設備或窗。

新指定以「每一頂點都位於完整支持平面與其範圍」判定，只作用於原材料 0。原 v1 程式的中心條件保留以重現既有配色，但本輪新增判定不使用三角中心。所有逐面變更與原因均記錄於 appearance-materials.json。

## 重建與驗證

Blender 4.3.2，新 build_appearance.py 與原 scene.blend、model.stl 放同一目錄：

    blender -b -t 1 --python-exit-code 1 -P build_appearance.py

新七張 900 × 800 圖採 Cycles CPU、96 samples、seed 0、單執行緒、無降噪。兩張原版對照從新版場景只恢復原材料分派，相機位置、旋轉、正交比例、光照及輸出設定數值相同。PNG 去除文字／日期／路徑 metadata；新 BLEND 無來源影像或絕對渲染路徑。3MF 沿原三角面指定 base material，不拆面或重取樣。

BLEND 原新版逐點逐面、物件 transform／尺寸、材值與原彩面不變；3MF 逐點逐面／palette 與 BLEND 一致；獨立乾淨目錄重建作語義與 3MF bytes 比對，見[新版審核](appearance-review-v2/color-continuity-review.json)。原 appearance-review 保留為 v1 歷史，不覆寫原審核；本輪以 appearance-review-v2 與新版 freeze 為準。

幾何 QA 與列印能力分開：本次僅改材料，不重認證全域壁厚、正式切片或現場尺寸。突出陽台、廊板、架空遮屏、細柱與女兒牆孔上緣仍須支撐／橋接／可移除性檢查。尚未實體試印，不保證免支撐或可印；STL 無色正常，3MF 顯色依軟體支援，不含特定 AMS 對應。
