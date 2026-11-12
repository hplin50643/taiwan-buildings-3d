# 2026-11-12 前圓柱局部配色校驗範圍

根 SHA256SUMS 核驗本次候選的當前檔案，FRONT-COLUMN-FREEZE-MANIFEST.json 保存完整凍結清單；兩者不自我循環。舊校驗表、README 與受替換 QA 保留於 qa/front-column-previous/，只供歷史查核，不驗證本次新檔案。原 FREEZE-MANIFEST.json、PUBLICATION-SUPPLEMENT-MANIFEST.json 及 INDEPENDENT-COLOR-VISUAL-QA.json 保留原版本作用域，不視為本次重簽。

以下保留先前補充原文（如有），只描述先前版本。

# 校驗版本與原檔交付範圍說明

本說明是追加的發布補充，未修改本機原凍結模型、README、舊校驗表或原 FREEZE-MANIFEST.json。此處未修改凍結原件不表示遠端同名根校驗表仍保留舊 bytes；根表新版取代與巢狀表保留的差異詳見下文。原凍結清單不包含本補充。

現行根目錄 SHA256SUMS 僅核驗其明列的當前檔案，不涵蓋其自身、原 FREEZE-MANIFEST.json 或本次補充。PUBLICATION-SUPPLEMENT-MANIFEST.json 另列原公開交付檔與本說明的 bytes、SHA256 及 Git blob SHA；補充清單本身依 Git commit 識別，不自我循環。

材色、年代、模型範圍與原 QA 限制仍依原文件；本說明不補簽列印性、歷史建成狀態或全實景材色認證。

## 原根校驗表已由新版取代

原 README 所稱「所有原件完整保留」是原件留存範圍，不代表本次公開 payload 含全部歷史原 bytes。原根 `SHA256SUMS`（1594 bytes，SHA256 `464ef2b19a8239a2dc4256eff14331a70d2913ea9c00c18af618c89f84273779`，Git blob `811cd53c0558b00855144741ad6a3326184dfa44`）屬舊版本。此次同一路徑交付的是新版校驗表，**不是保留舊表 bytes**。舊表保存在原 Git 歷史與私人完整備份中；本批公開 payload 沒有宣稱包含其完整公開別名。新版表與舊版表的用途及摘要不能互換。

## 不在本批凍結 payload 內的歷史巢狀校驗表

原 `geometry/v2/SHA256SUMS`（3452 bytes，SHA256 `968a3ce736f0bb5de4a95edbf8198cd0dcd8dbab5ca1fcb85ea634d0f278fe29`，Git blob `e6ce9461b90b4f71d1b80ae20cec330485506830`）未列入本批原凍結公開 payload，亦不冒列為本補充清單的交付檔。原 repo 的同一路徑保留原 blob、不刪除，並另有私人完整備份。其歷史表不驗證本批新根目錄材色檔；發布時須另核原路徑 bytes 及其明列目標。這與上節根表被新版取代不同，不能合併宣稱所有原表均同路徑原 bytes。


## 歷史 README 移位後的相對導航

`original-version/README.md` 是原根目錄 README 的完整歷史 bytes。第9行的相對導航仍依原根位置，不是移入 original-version 後的有效導航；本次保留原文，不將這兩個舊連結認證為當前正確連結。

- 「返回西子灣校區」原 href `../../README.md`：原位置指校區 README；移位後落到不存在的 buildings/README.md。請改用本說明的[西子灣校區圖鑑](../../README.md)。
- 「返回全校圖鑑」原 href `../../../README.md`：原位置指中山大學 README；移位後落到校區 README，雖存在但不符「全校」標籤。請改用本說明的[中山大學全校圖鑑](../../../README.md)。

這是兩項明列的歷史導航限制，不豁免其他連結，也不修改原凍結 README。
