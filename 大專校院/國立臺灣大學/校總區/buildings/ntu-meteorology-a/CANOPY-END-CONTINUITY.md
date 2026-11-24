# 氣象 A 館右雨棚端：兩面有限連續補色

僅原三角面 **1372、1373** 從未核中性 5 改為既有混凝土 4（#999B94）。1988 面中的其他 1986 指派、頂點、面序、法向、六材 RGBA／節點／粗糙度及原場景均保持。STL／OBJ／palette.json 原位元組保留。

原完整矩形面域位於 x=-2.5、y=-57.5..-48、z=20..21.799999237，面積 17.099992752 mm²；兩面共一條內邊、四條外邊。只右端，不含左端 1356/1357、棚底、後面、牆、階梯、柱或另一個小平台。完整域以原面共享邊查核，沒有切幾何或新材界。

## 來源與推論限制

[原公開攝影資產](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiPgSGB6Fs2CcOlbx8l9lFthfEaiwiDa6sG5NIi1l6mlUTepAUFaW8ryZeN9fJSM5M160_w4crtegeHIej5lVUjlAFlWD1tuOIw8EuMpHbJm-3OOSqEMwxxC6ww6GMj3BkW7K_sJIeXWg/s1600/1378208_505854842833256_1730926211_n.jpg) 沿原登錄的 2013-10-05 文章年代。此次取得圖 SHA256 `5eb066eb9dc1cdf4614dd2f897db16171517746424e6d2ac8e6e82bdd0fec8fb`，**不同於歷史登錄 `573b7309a72d804d4d8e8e9033f20827132b6df667c504818bb6b7dbedf5950b`**。差異原因未查明，不假定只是 metadata。此次 GO 基於此次實際像素與獨立審查，不聲稱與舊圖位元組相同。

照片右端可見與既有前端／頂面同混凝土族，由外前角至後方牆接點可辨；依此採有限同構件材料連續推論。名義 9.5 mm 模型深度不是照片量測，棚頂污漬與堆物不另當材料。來源年代不保證照片時鐘、2026 現況或精確色票。原來源照片不隨公開包交付，未認定再散布或商用照片授權。

仍為局部材色示意：大面磚牆未分色；未知跨基座大牆、背面與屋面仍中性。既有粗化幾何、未建外拱圈、未試印及非四色切片專案等限制全部保留。

## 可重現修改

固定基準 repo `hplin50643/taiwan-buildings-3d`，commit `8f90ae2478f00cce6832a07de537f7d333f6dbc0`，相對目錄 `國立臺灣大學/校總區/buildings/ntu-meteorology-a`。`baseline-rebuild-inputs.zip` 含 SHA 鎖定的原 model.stl、color-mesh.npz、scene.blend、appearance.3mf，無照片；其 SHA 在 wrapper 與 `baseline-inputs.json`。

```sh
unzip baseline-rebuild-inputs.zip -d baseline
blender -b --python rebuild_canopy_end.py -- --baseline baseline --out rebuilt
```

原 colorize_model.py／export_appearance.py／render_color.py 保留不覆寫；單獨重跑它們會回復歷史分色，必須再用本 wrapper。`render_canopy_end.py` 開啟改後原場景並沿原 10 視角、1200×900、Cycles 48 samples 渲染，**不重建或覆寫 scene**。

## 驗證摘要

原 STL↔NPZ↔Blend↔3MF 面序與幾何一致。完整 RNA 精確 8 處差異：2 polygon、2 loop_triangle、2 material attribute，及模型 scope／source_mesh_sha256；其他 camera、world、lights、材質、hidden caption/backdrop 全保留，無 orphan fake_user 改動。序列化排除 runtime/users/更新狀態/uv_sculpt 等，詳 QA。

3MF 原座標字串不重算，只有兩 p1 5→4 與原缺失 object default pid=1/pindex=5（供 SDK 編修往返）。所有三角已有顯式材，default 不變更其他面。strict SDK 零警告，私有材質修改回存、Blender 原生頂點＋材質修改回存與隔離重建均驗證；不是實體試印或 GUI slicer 測試。

私有 before/after 同相機模型比較不是來源照片配準。公開圖片是自有模型原視角渲染，不含原照。
