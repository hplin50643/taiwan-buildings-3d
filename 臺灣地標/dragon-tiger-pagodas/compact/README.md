# 龍虎塔｜較小的二進位 STL

[下載二進位 STL（6.69 MB）](model-binary.stl) · [原 ASCII STL（36.41 MB）](../model.stl) · [材色範圍及原模型說明](../README.md)

這是同一模型的檔案格式轉換，**沒有減面或重新建模**。三角面數與排列均維持 133,722；尺寸仍為 150 × 124 × 109.5 mm。STL 沒有色彩及單位標記，請在切片軟體以 **mm** 匯入；彩色版本另見 [appearance.3mf](../appearance.3mf)。

原 ASCII 為 36,412,062 bytes；本檔為 6,686,184 bytes，減少約 81.64%。二進位 STL 使用 float32，與原 ASCII 數值相比，最大頂點位移為 0.000004227 mm。因此這不是逐位元組無損，也不宣稱數值完全零誤差；未簡化幾何，邊界尺寸相同。

## 驗證與限制

獨立解析確認所有頂點及法向量等於原 ASCII 轉 float32 的結果，三角順序完整保留。[轉換報告](conversion-report.json) 記錄大小、SHA256、尺寸及偏差；[網格檢查](validation.json) 通過有限座標、無退化面、封閉水密、每邊兩面、單連通體、繞序及正體積等檢查。這不等於實際列印測試或完整自交證明；原薄檐、欄柱、雕飾、支撐及近似尺度限制不變。

原 `../model.stl`、Release v1.0.0 附件及舊建模／配色驗證檔保留。原配色腳本硬綁 ASCII 雜湊，**不要用本檔覆蓋 `../model.stl`**。既有 SHA256SUMS、FREEZE-MANIFEST 與舊 QA 仍是原版本的證據，不包含本次新增 compact 目錄。此目錄有自己的 [SHA256SUMS](SHA256SUMS)。

可重現：在此目錄執行 `python convert_ascii_to_binary.py`，只讀上層原 ASCII，寫入本目錄二進位 STL；程式會先核原檔 SHA256，再核輸出 SHA256。可另外執行 `python ../validate_model.py model-binary.stl --longest-edge 150 --output validation-rechecked.json`。

目前 repository 本身已包含原 ASCII 及本二進位 STL。舊單色說明中「只在 Release／原始碼 ZIP 不含 STL」屬歷史交付方式，並非目前檔案狀態；Release 不刪除。
