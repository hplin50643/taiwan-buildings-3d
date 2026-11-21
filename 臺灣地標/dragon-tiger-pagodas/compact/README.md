# 龍虎塔｜較小的二進位 STL

[下載二進位 STL（6.69 MB）](model-binary.stl) · [原 ASCII STL（固定 Release 附件）](https://github.com/hplin50643/taiwan-buildings-3d/releases/download/v1.0.0/dragon_tiger_pagodas_150mm.stl) · [材色範圍及原模型說明](../README.md)

這是同一模型的檔案格式轉換，**沒有減面或重新建模**。三角面數與排列均維持 133,722；尺寸仍為 150 × 124 × 109.5 mm。STL 沒有色彩及單位標記，請在切片軟體以 **mm** 匯入；彩色版本另見 [appearance.3mf](../appearance.3mf)。

原 ASCII 為 36,412,062 bytes；本檔為 6,686,184 bytes，減少約 81.64%。二進位 STL 使用 float32，與原 ASCII 數值相比，最大頂點位移為 0.000004227 mm。因此這不是逐位元組無損，也不宣稱數值完全零誤差；未簡化幾何，邊界尺寸相同。

## 驗證與限制

獨立解析確認所有頂點及法向量等於原 ASCII 轉 float32 的結果，三角順序完整保留。[轉換報告](conversion-report.json) 記錄大小、SHA256、尺寸及偏差；[網格檢查](validation.json) 通過有限座標、無退化面、封閉水密、每邊兩面、單連通體、繞序及正體積等檢查。這不等於實際列印測試或完整自交證明；原薄檐、欄柱、雕飾、支撐及近似尺度限制不變。

原 ASCII STL 不放在現行目錄；如需精確重現，請下載上方 [Release 附件](https://github.com/hplin50643/taiwan-buildings-3d/releases/download/v1.0.0/dragon_tiger_pagodas_150mm.stl)，或至[固定歷史提交](https://github.com/hplin50643/taiwan-buildings-3d/blob/8c322901224a590689401db4b72ec6878f391b9b/%E8%87%BA%E7%81%A3%E5%9C%B0%E6%A8%99/dragon-tiger-pagodas/model.stl)取回同一檔。使用明確輸入與輸出路徑：

```sh
python convert_ascii_to_binary.py --source /path/to/dragon_tiger_pagodas_150mm.stl --output /tmp/model-binary.stl
```

程式先校驗原檔，再校驗預期二進位 STL。另可執行 `python ../validate_model.py /tmp/model-binary.stl --longest-edge 150 --output /tmp/validation-rechecked.json`。本目錄的[現行校驗碼](SHA256SUMS)涵蓋重建程式及交付檔；[原轉換記錄](https://github.com/hplin50643/taiwan-buildings-3d/blob/8c322901224a590689401db4b72ec6878f391b9b/%E8%87%BA%E7%81%A3%E5%9C%B0%E6%A8%99/dragon-tiger-pagodas/compact/conversion-report.json)的相對路徑是當時的試驗位置。
