# 知本第一宿舍主要三列棟群｜外牆補色 v2

## 修補範圍與確定性

延伸既有米灰牆色 #CECABF 到三列住宿棟原後牆與左端牆；原後淺窗背面採 #72716A 暗灰褐不透明陰影代理，垂直窗側壁延續牆色。主屋頂另一端山牆及後側簷邊延續 #C6C8C3 灰白。共 1050 個原中性三角面改色，全部原已上色面與原材料RGBA、粗糙度保留。

**上述背向面與左端細部是同棟、同類構件的材料連續推估，不是新增逐面實照確認。** 原保守後窗數量／深度未改，不把暗凹槽聲稱為玻璃。原尺寸、棟距、窗數、屋頂坡度與進深仍為近似，補色不提高測繪確定性。

塔身存在藍灰／米白不規則拼貼，原面無法分離材料區域，維持中性；端陽台厚邊與凹部也不強行套牆色，不虛構細欄杆。底座、水平窗台／窗洞頂底、屋面下表面保留原狀。沒有新增窗陣、紋理、幾何或修改transform。

## 本輪重新下載並親看的官方照片

- [第一宿舍外觀](https://wdsa.nttu.edu.tw/var/file/9/1009/img/358/763118029.png)：三列棟群長廊近白／灰米牆、淡藍灰樓帶、塔頂紅板與塔身混合拼貼。遮蔽低層及遠側無法逐面認證。
- [校本部空拍](https://nwww.nttu.edu.tw/var/file/0/1000/randimg/ad_1911_3227092_53377.jpg)：核對右上三列棟群及紅褐屋面，不混入另一組宿舍。空拍解析度不足以校準背牆色值。

照片拍攝日期未核實，存取日不是攝影年，不宣稱2026現況認證。色值為受光線／陰影影響的外觀近似，非實際建材規格。來源照片只作本機參考，不納入公開包。

## 驗證與重建

原4346頂點、8688三角面及含底座150×110×47.70mm保留，詳見[逐頂點與逐面驗證](appearance-review-v2/model-verification.json)。3MF與Blender逐頂點、逐三角及逐面材質相符；[乾淨重建檢查](appearance-review-v2/clean-rebuild-equality.json)。原model.stl、scene.blend、build_model.py、previews及歷史幾何QA不改。

七張appearance圖片由交付實網格渲染，無圖內文字、文字物件或stamp。前後對照見[原正面](appearance-review-v2/before-front.png)、[原背面](appearance-review-v2/before-rear.png)，與新版同視角比較。舊appearance-review為歷史v1審核，不冒充本輪。

重建：把原scene.blend、model.stl與build_appearance.py放同目錄，執行 `blender -b -t 1 --python-exit-code 1 -P build_appearance.py`；加 `-- --skip-render` 可只重建模型。使用Blender4.3.2、96samples、單線程、關閉denoise。

## 列印限制

原外廊凹處、陽台與塔頂簷的支撐／橋接／壁厚限制不因補色解除。沒有實體試印或正式切片驗證，不保證免支撐。STL不保存色彩，使用appearance.3mf或appearance.blend；3MF無特定AMS映射。本輪僅本機完成，未上傳或發布。
