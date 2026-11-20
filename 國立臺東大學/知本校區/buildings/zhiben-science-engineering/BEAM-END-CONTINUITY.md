# 左端上梁窄側：有界材色連續推論

僅原三角 1107、1110，x=-65、y=[-24.2,-22.2]、z=[35.2,36.5]，朝 -X 的完整矩形（2.5999984741 mm²），材 1→0。保留 2992 原三角與全部幾何、其餘 2990 面指派，原 10 白面不撤。現在 12 白、2980 中性；中性表示未知，不是實景灰材。

校方正斜照辨識左凸玻璃盒的灰白框上梁；窄端全深沒有逐像素清楚解析。此次只依同一上梁材族延續作有限推論，不宣稱色卡校準、照片完整深度測繪或幾何精準。右端、側柱深面、梁頂底背、玻璃回邊、下方實填支撐、混材牆與屋頂全部排除。既有列印厚化與簡化、缺天窗限制保留；未實際列印或驗證多色切片。

## 可重現重建

固定基準儲存庫 `hplin50643/taiwan-buildings-3d`，commit `8f90ae2478f00cce6832a07de537f7d333f6dbc0`，相對目錄 `國立臺東大學/知本校區/buildings/zhiben-science-engineering/`。`rebuild-baseline/` 附該版四個數字檔的原始位元組；腳本內 EXPECTED 鎖定各 SHA256，MANIFEST 亦列出。基準為 10 白面，不可拿後續版本替代。

使用 Blender 4.3.2（其內建 NumPy）：

```sh
blender -b --python-exit-code 1 -P rebuild_beam_end.py -- --baseline rebuild-baseline --out rebuilt
```

輸出 scene.blend、color-mesh.npz、appearance.3mf、beam-end-change.json。將 render_beam_end_views.py 放在 rebuilt 目錄，再以 Blender 執行該檔可生成原 10 視角。舊建模及著色程式保持歷史原樣；本 wrapper 是在固定基準之後新增的兩面步驟，不可僅重跑舊著色程式後宣稱新版完成。

保留所有材質 shader/RGBA/roughness、相機、world、燈光及 transform。僅同步兩面三種 RNA 材質表示與必要 scope/source_mesh_sha256 屬性；沒有 fake-user 變更。3MF 保留原八位小數座標字串，還原 float32 與 STL 精確一致，double 差最多 4.633e-9 mm；不宣稱四格式 double 位元完全相同。新增 object pid/pindex fallback 使 SDK 原生往返合法，不改逐面有效指派。

7 張完整視角及 3 張原設計細節視角，皆 1200×900、Cycles 48 samples、原畫面品質；細節圖刻意局部構圖不是全棟圖。原照片與私人編修實驗不在公開包。
