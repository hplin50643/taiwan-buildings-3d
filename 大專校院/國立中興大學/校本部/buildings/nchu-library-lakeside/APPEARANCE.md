# 中興圖書館臨湖前翼與轉角段｜左端外牆補色 v2

## 真實外牆缺色與人工截斷面分開處理

原模型是局部前翼，不是全館。**背側為人為截斷／剖切面，不是真實背立面，本輪維持中性，不塗成假背牆。** 屋頂、設備量體、底板與原標示牆同樣保留原狀；未將粉紫布條當作牆材。

本輪只修補左端既有真實外牆和原窗凹槽：88個原中性三角面延伸原右端與前翼米灰牆色 #C8BDA8，14個原中性三角面延伸原凹窗灰綠 #5E7472。窗戶是原模型已有的3長、4短槽，沒有新增窗陣、分格、窗洞或任何幾何。

左端精確色值及個別凹槽沒有新增近距離實照確認，**屬同建築、同類構件材料延續的合理近似**。不是宣稱左右立面完全對稱，也不是量測或2026現況認證。原有已著色面全數保留。

## 本輪實看來源

重新下載並親看[圖書館主辦活動頁](https://nchulibrary.wixsite.com/20201119)所用[空拍照片](https://static.wixstatic.com/media/514194_96384e63db5e42359e50a0cdb3db0e33~mv2.jpg/v1/fill/w_490%2Ch_327%2Cal_c%2Cq_80%2Cusm_0.66_1.00_0.01%2Cenc_avif%2Cquality_auto/514194_96384e63db5e42359e50a0cdb3db0e33~mv2.jpg)。可見前翼及右端淺米灰牆、暗凹窗和灰銀遮陽構件，支持材料家族延續；左側端牆不夠清楚，不作逐面確認。這是490×327低解析圖，光照與反射影響色彩，未校色。

活動年份不是拍攝年份；檔名不能取代EXIF。沒有將原文件中的2024 Commons照片當成本輪新看證據。來源照片僅本機參考，不納入公開包。

## 驗證與交付

- 原頂點、三角面、尺寸、transform及全部原已著色面保留；詳見[逐面驗證](appearance-review-v2/model-verification.json)。
- 原 model.stl、scene.blend、build_model.py及歷史列印檢查均不變。
- 3MF逐頂點、三角形及逐面材質與Blender一致；[乾淨重建檢查](appearance-review-v2/clean-rebuild-equality.json)。
- 七張圖片由交付網格實際渲染，無圖片內文字、文字物件或stamp。前後對照見[修補前正面](appearance-review-v2/before-front.png)、[修補前背面](appearance-review-v2/before-rear.png)，與appearance目錄新版同視角比較。
- 舊 appearance-review 為歷史 v1 審核，不冒充 v2 測試。

重建：將原scene.blend、model.stl和build_appearance.py放在同目錄，執行 `blender -b -t 1 --python-exit-code 1 -P build_appearance.py`。使用 `-- --skip-render` 可只重建模型與材質JSON。

## 限制

含底座150×72×91mm為原照片估計縮尺，並非測繪尺寸。局部截斷範圍、原屋頂進深及端窗分組等近似限制仍適用。玻璃為不透明表觀代理。沒有實體試印、沒有新增切片測試，原支撐／橋接／壁厚限制不因補色而解除。STL不保存色彩，請用appearance.3mf或appearance.blend。
