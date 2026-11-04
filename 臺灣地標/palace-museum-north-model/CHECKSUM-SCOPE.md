# 校驗版本說明：當前交付補充

本檔為 append-only 發布補充。原凍結模型、幾何、材色、歷史文件與兩份校驗表均未修改。

- `SHA256SUMS.txt` 是原版歷史校驗表，保留原位元組，不是新增色版的完整校驗入口。下列精確項目不追認為當前檔案通過（NOT_RECERTIFIED）；其餘項目仍照表驗證。
- 無副檔名的 `SHA256SUMS` 核對其所列的當前檔案，不含自身與 FREEZE，也不宣稱涵蓋這次新增的兩份發布補充。
- `PUBLICATION-SUPPLEMENT-MANIFEST.json` 記錄全部原凍結公開 payload 與本說明的大小、SHA256、Git blob SHA；它不循環包含自身，其位元組由發布 Git commit 與批次交付 manifest 綁定。
- 此說明只釐清校驗版本，不提高原來源、幾何、材色、數位 QA 或實體列印可信度。完整限制仍見原 README。

## 原歷史表中不適用於新色版的精確項目

- `README.md`：舊表 SHA256 `b74047069eb513f8acd071c6b0ac5175f559a6b9d5eea30f5b574ccde256074a`；當前 SHA256 `dcb24c1c40ab6fd269862aa3de769da0d0357a63f3d1a4dae0837fc820714d6c`。舊項 NOT_RECERTIFIED，當前值由新 `SHA256SUMS` 與交付 manifest 核對。
- `scene.blend`：舊表 SHA256 `688de99719cb7e380d972898d9990dd032252be6791672266c18519e772efabc`；當前 SHA256 `827b708cf98b90064f6af864de8396d37c4dbbd6998aa57364ed6bd753265d7a`。舊項 NOT_RECERTIFIED，當前值由新 `SHA256SUMS` 與交付 manifest 核對。

[返回模型說明](README.md) · [當前檔案校驗表](SHA256SUMS) · [發布補充清單](PUBLICATION-SUPPLEMENT-MANIFEST.json)
