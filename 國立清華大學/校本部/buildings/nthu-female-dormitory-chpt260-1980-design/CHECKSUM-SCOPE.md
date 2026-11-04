# 校驗版本與原檔交付範圍說明

本說明是追加的發布補充，未修改本機原凍結模型、README、舊校驗表或原 FREEZE-MANIFEST.json。此處未修改凍結原件不表示遠端同名根校驗表仍保留舊 bytes；根表新版取代與巢狀表保留的差異詳見下文。原凍結清單不包含本補充。

現行根目錄 SHA256SUMS 僅核驗其明列的當前檔案，不涵蓋其自身、原 FREEZE-MANIFEST.json 或本次補充。PUBLICATION-SUPPLEMENT-MANIFEST.json 另列原公開交付檔與本說明的 bytes、SHA256 及 Git blob SHA；補充清單本身依 Git commit 識別，不自我循環。

材色、年代、模型範圍與原 QA 限制仍依原文件；本說明不補簽列印性、歷史建成狀態或全實景材色認證。

## 原根校驗表已由新版取代

原 README 所稱「所有原件完整保留」是原件留存範圍，不代表本次公開 payload 含全部歷史原 bytes。原根 `SHA256SUMS`（2736 bytes，SHA256 `4c2680e1d07007f57d2fab36b6fd824a21af56e8d242a1c12bf675712de3da74`，Git blob `13e76bb8129ccdbec5c86c4f2109f9a369dd73de`）屬舊版本。此次同一路徑交付的是新版校驗表，**不是保留舊表 bytes**。舊表保存在原 Git 歷史與私人完整備份中；本批公開 payload 沒有宣稱包含其完整公開別名。新版表與舊版表的用途及摘要不能互換。

