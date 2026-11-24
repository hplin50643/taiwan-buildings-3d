# 政大志希樓：下層門廊柱外側四面材質修正

僅原面 **508、510、524、526** 由 1（鋁框代理）改為既有 0（灰洗石表觀族 `#999A90`）。原 1,026 面、頂點、拓撲、尺寸與 STL 完全不變；其餘 1,022 面指派不變，既有四柱正面 507、509、523、525 保留。六材面數為 `[495,165,44,116,150,56]`。

## 有限依據與界線
官方 PDF：https://osa.nccu.edu.tw/CSRC/files/169362228269a7c8ada230d.pdf ，SHA256 `6f3b5072196adbac6f78211bc29b340fd2eaf91e6a6edce31b38063a04a97c75`。實體第 36 頁填表日期為民國 110 年 10 月 1 日，非照片日期；實體第 37 頁為嵌圖 554／555。只供來源追溯，PDF 不隨公開包交付。

既有官方防災資料第 37 頁嵌圖 554 可辨兩個門口外側灰結構柱與亮鋁門框的不同。這次只將同一已修正柱正面的材族延至原模型兩外頰，並非新相片逐深度量測。左右各完整 2 原三角面，分別 x=−18、+18，y=−4.5…−2.5、z=3…12 mm，各 18 mm²，合計 36 mm²。數值來自模型，不是實物量測。局部窄回邊與陰影可見，柱腳有遮蔽，原模型 2 mm 深度是既有近似。不得外推上柱、鋁門窗框、簷底、背牆或其他整棟側域。2021 調查日期不等於照片拍攝年或 2026 現況。

第三方原照片／PDF／私人對照和編修測試不在公開包內。原工程限制、歷史幾何 QA、未實體試印和非四色切片警示仍有效。

## 精確重建
基準來自 `hplin50643/taiwan-buildings-3d` 固定 commit `8f90ae2478f00cce6832a07de537f7d333f6dbc0`，repo 目錄 `國立政治大學/山下校區/buildings/nccu-zhixi`。包內 `rebuild-baseline/` 保留該版本的 `model.stl`、`color-mesh.npz`、`scene.blend`、`appearance.3mf`；wrapper 逐檔 SHA256 鎖定。它不是從舊色碼任意新版執行，而是只改此確定基準四面：

```sh
blender -b -t 1 --python-exit-code 1 -P rebuild_pier_sides.py -- --baseline rebuild-baseline --out rebuilt
```

Blender 4.3.2 / NumPy。舊 `colorize_model.py` 仍是歷史前面修正版，直接重跑會回復本次四側面的舊材；沒有宣稱舊流程已更新。新 wrapper 產出 NPZ、3MF、scene 與精確變更 JSON；STL 直接保留。`render_pier_sides.py` 讀新 scene 渲染原 7 全景及 3 細節，不重建幾何、不保存渲染造成的相機改動。

## 原生保存與數位驗證
原 Blend 全場景 RNA 15 項必要差異：四面在 polygons／loop_triangles／material attribute 的 12 項材指派、物件 `scope` 和 `source_mesh_sha256` 兩項，以及既有無使用者 `Material.use_fake_user=False→True` 一項。此旗標僅確保孤立材及其原 shader node tree 不被儲存清除，不改其參數；原材清單、其他節點、相機、世界、燈、隱藏說明／底板與 transforms 均保留。

3MF 原 XML 只有四個 p1 與物件 fallback pid/pindex 兩項變更；fallback 為既有中性材 4、每一面仍有明確指派。原頂點數值字串、其他 XML 與 ZIP 內容保留。clean 重跑 NPZ／3MF／change JSON 逐 byte 相同，Blend RNA 語義相同，不聲稱 Blend 容器 byte 決定性。strict SDK 零警告、私人改材保存重讀和 Blender 私人頂點＋面材編輯保存重開均通過，未改公開原件；不等於 slicer 或實體列印驗證。

歷史 README 與舊 QA 完整保留，描述各自版本；新檔請使用本包 `MANIFEST.json`，不要拿歷史校驗表驗新版。
