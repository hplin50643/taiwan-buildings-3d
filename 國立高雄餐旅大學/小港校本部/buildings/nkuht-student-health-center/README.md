# 高餐學生健康活動中心｜六柱可見面局部銀灰

**雨棚、窗背及其他混材未完成分色。** `partial_color_incomplete=true`、`fully_colored_exterior=false`。原活動中心與附屬群體範圍保留，同slug不新增套數。

| 總覽 | 背側 | 南向 |
|---|---|---|
|![總覽](preview.png)|![背側](rear.png)|![南向](front.png)|
|![北向](back.png)|![西側](west.png)|![東側](east.png)|
|![頂面](top.png)|![西柱近景](entry-detail.png)|![東柱近景](facade-detail.png)|
|![柱列與雨棚](roof-detail.png)|||

## 材色範圍
同 `nkuht-student-health-center` 原項目，same-item、count_delta=0。**7854原三角面、STL與build_model.py字節不變**；不切面或補斜撐。原公開包無OBJ，不假稱保留。
- 六支原48邊圓柱，依原K=.1378645278805804、S=150/132、BASE=2.4和原中心／半徑／完整軸高重算北向半柱真facet：87＋48＋48＋48＋48＋48＝327原面銀灰。第一柱含原Boolean交接裁切細面。
- 以原facet朝向定完整半柱，每一三角全部頂點必須滿足有限平面與tangent端界及軸高；不靠STL法線門檻或中心點挑色。
- 全2036共面連通域均一、0撤色。其餘7527面中性：背半柱／柱帽、雨棚整片混鋼架透明皮、混玻璃框反光窗背、實心欄杆代理、主屋頂、附屬量體、橋／基座／下沉庭院等。
- 色／中性界是證據範圍，不是真實柱材接縫；原屋緣比例描繪、地坪高差、厚化柱徑與省略斜撐均不因本次補色追認為精測。

## 來源／日期與權利
親看建築師日照9738及9707作銀灰柱色族；9695夜照只對位，綠色燈光不當材料。拍攝日期未知，URL的2016/04發表路徑不是拍攝日期，不稱2026現況。
原照私人保存，不公開或貼圖；未確認CC／再散布授權、不保證商用。人物不建模、不公開來源人物照片。HEX為名義銀灰非校準色票。
GO是有界來源放行，不是發布核准或幾何重審；先期review-only文字只保留歷程。

## 格式與列印
[原STL](model.stl) · [逐面材色3MF](appearance.3mf) · [Blender](scene.blend)
原150mm展示長邊與S比例不變；圖量群體近似非精測BIM。STL無色；3MF與Blender真逐面材。兩材標籤不是驗證兩色／四色耗材切片；**未實際列印**，無切片路徑。

## 重建與 QA
原 `build_model.py` → `colorize_model.py` → `export_appearance.py` → `validate_color.py`；Blender `render_color.py`／`verify_color_scene.py`。
請使用原 requirements.txt 的 Shapely==2.1.2。本機預設2.2.0會將11個共面頂帽三角重新剖分（頂點／表面union／體積不變），不是原byte再現；保留該失敗歷程，以既有2.1.2私人隔離target重建後，原STL byte及色版NPZ皆精確再現。公開檔一直使用immutable原STL。
原字節／三角multiset、閉合正體積、3MF面材、完整隔離原build＋color重建、scene重開、十圖1200×900與圖文hash核對，程序不取代人工源控。
原README、單色previews／render／validation保留歷程，不冒充本次QA；不刪檔。

## English scope
Partial color:327 existing finite north-facing48gon column facets (87+5x48) nominalsilvergray. All7527 remaining faces neutral, including reversecolumns, caps, mixedcanopy/glazing and solidrail proxies. Original7854 triangles unchanged;no originalOBJ. Daylight evidence only, night illumination excluded. Captureunknown;2016 URL path notcapturedate. Original image-derived groupgeometry not newlycertified. Not testprinted or validatedfilament slicing.
