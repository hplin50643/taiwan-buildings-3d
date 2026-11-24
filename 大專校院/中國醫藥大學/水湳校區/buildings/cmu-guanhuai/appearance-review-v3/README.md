# 關懷大樓外牆補色 v3 審核

本輪只延伸既有灰白外帶與深灰凹帶材料，修改10,247個原中性面，沒有新增幾何、窗或屋頂格線。原網格、transform、尺寸、全部已彩面和原RGBA／roughness保留。只在本機完成，未發布或遠端讀回，未宣稱CI通過。

## 本輪報告

- [逐點逐面BLEND／3MF核對](model-verification.json)，35,282頂點／70,600三角面。
- [原材料值核對](material-value-verification.json)，diffuse RGBA、線性Base Color RGBA及roughness精確相等。
- [完整原面支持界核對](boundary-continuity-audit.json)，不用重心塗色，未將人工底座、屋帽或露台混合切面誤當可延伸外牆。
- [乾淨重建](clean-rebuild-equality.json)，原scene＋新版腳本重新產生，模型語意一致、3MF及materials JSON逐byte一致。
- [九張官方來源實看](source-review.json)，來源為2021-10-28文章，逐張拍攝日期不明；只放URL、雜湊和觀察，不散布來源照片。
- [相機一致性](camera-consistency.json)、[七新版與兩原版實看](color-continuity-review.json)、[本輪渲染綁定](render-manifest-v3.json)。900×800，Cycles CPU，96 samples，seed 0，單執行緒，無降噪／stamp／PNG文字。
- [外部／內嵌媒體檢查](embedded-media-check.json)，無來源照片或PDF依賴。

[原版正面](original-front.png)和[原版背面](original-rear.png)是恢復全部原材料索引後，以新版相同相機、燈光及96 samples重新渲染，不是舊32 samples預覽。七張新版在[appearance](../appearance/)。

基準為main commit 123e103381f4d7eb98627857d9b720b8e497ecaa 的本棟套件。原九張previews及歷史列印QA保持不動；舊appearance-review為歷史，不能認證v3材料或新圖。未實體試印，原短首段、另向／三面根、parity flags、支撐和尺度限制不變。完整來源、推估及限制見[APPEARANCE](../APPEARANCE.md)。
