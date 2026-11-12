# 蘭潭嘉農鐘樓｜側背原面同族材料延伸

## 原模型與原彩色不變

本版只改 7,084 個原中性三角面的材料指標，原 5,074 頂點、10,240 三角面、86×86×150 mm、transform、全部原彩面、五種材質的 RGBA／Principled Base Color／roughness 均保留。STL、scene.blend、build_model.py、原五張預覽及原列印報告未改。鐘樓仍為校園附屬地標，不是教學館，不增加教學館棟數。

## 實際親看來源與日期

本輪重新讀取[嘉大秘書室蘭潭校景頁](https://website.ncyu.edu.tw/secretary/Subject/Detail/98820?nodeId=1762)，下載並親看[同頁鐘樓原圖](https://website.ncyu.edu.tw/secretary/ServerFile/Get/c7a8cdec-9171-47f5-86e7-5718708d76d0?nodeId=1762&sId=98820)。圖像 5030×3353，2,169,332 bytes，可辨帶鐘正面、相鄰左面、柱／線腳／球飾、真正貫通拱口／欄孔及內梯。沒有取得可完整確認背面的新照片。

實際讀到 JPEG 的 DateTimeOriginal／DateTimeDigitized 均為 2017:12:13 10:39:01，無時區、未獨立校時。網頁發佈日 2023-04-28 與更新時間 16:45 是頁面時間，不是拍攝日期，也不是2026現況證明。英文頁同幅圖不算獨立視角；原 sources.json 的歷史文字保留，本輪未重讀全部舊來源。照片、HTML、PDF與含來源照片對照圖不放入公開包。

照片反射有金黃色高光，本版不臆判金漆或特定合金，保留原低飽和銀灰材料近似。色值不是校色實測；不把日照、污跡與反射畫成固定色塊。

## 完整原面材料延伸

先精確重現原版每面材料，再只修改材料0。分類使用全部頂點、原構件範圍及實際支持平面，不以三角中心切上下半面、不切割幾何。獨立檢查另測每個新增面21個重心座標取樣點。每面原指標／新指標／理由存於 appearance-materials.json。

- 原 +X／+Y 外板與後側山牆外面，沿用 -X／-Y 已見暖灰米材料1。兩個剩餘外牆整面域補齊，沒有斜角截色；這是同棟同構件延續推估，不宣稱掌握未見背部銘文。
- 原四角柱的隱藏圓周、柱帽側邊和水平肩部、細柱頸、球飾，用既有銀灰材料2。原照片看得見球飾／柱帽的同族金屬表觀，隱藏面及遠角仍標明為推估。球飾使用完整既有球體與柱頸相交區域，避免因布林交線頂點不在理想球半徑上而留下碎片中性。
- 六道原線腳的側背垂直面和水平出沿沿用材料2，原內井面仍保中性。未把本體未知屋面當作線腳。
- 原鐘盤既有邊緣延伸原銀灰外緣與灰白盤邊。原灰白正面、兩條示意指針面與指針幾何全部保留，未調成照片上的時間，未複製鐘面或新增背鐘。

不加月桂、文字、數字、天線、鐘機、窗片或玻璃。所有拱口／欄孔仍為原真正開口，無封面。照片中精細金屬框、內部構件與厚重舊模型不完全一致，本版不改其幾何。

## 保留中性的完整分類

共 1,216 個中性面，分類如下：
- artificial_base_plinth_steps_and_bottom_column_contacts：253 面。
- top_slab_and_gable_thickness_or_inner_faces_unknown_roof_finish：64 面。
- inner_shaft_wall_faces_no_reliable_same_outer_finish：204 面。
- baluster_slot_inner_reveals_not_outer_wall：148 面。
- original_inner_stair_landing_and_merged_arch_junctions_unknown_finish：234 面。
- lower_arch_return_and_inner_structural_faces_missing_finish_boundaries：241 面。
- upper_pointed_arch_inner_reveals_not_outer_wall：72 面。

上述內部與開口厚面沒有足以支持整片單一外牆材料的分界；原加厚內梯、支承交接、屋面、山牆厚度與人工底座不冒充實測材質。中性不等於實物一定灰色。所有10,240面已納入原彩面、變更面或明確中性原因，無未分類面。

## 渲染與可重建驗證

同目錄備有原scene.blend、model.stl，執行：

    blender -b -t 1 --python-exit-code 1 -P build_appearance.py

七張900×800真網格渲染：front、rear、elevation、source-angle、left、right、top。Cycles CPU、96 samples、seed0、單執行緒、無降噪；無文字物件或stamp，PNG文字metadata移除。方向名是模型視角，不宣稱測繪方位。另兩張同相機原版對照僅還原原面材料指標，沿用新版燈光與相機，方便分辨材料差異。

BLEND逐點／逐面／transform／尺寸與原版核對，材質RGBA／Base Color／roughness不變；3MF每個頂點、三角面、材料指標與BLEND核對，原palette／unit／build項目保留。全新資料夾從原scene和本版腳本重建，3MF與材料JSON比較bytes，BLEND比較網格、指標、transform及材料值語義。原appearance-review是歷史報告，本版appearance-review-v2與appearance-freeze.json綁定新結果。校級checksum未修改，發布前需整合；本機驗證不是GitHub發布或遠端讀回。

## 原列印風險與範圍保留

原模型四方塔未見部位為對稱近似，尺寸為目視推估，非測繪。原報告單一連通殼、原法向、封閉網格、750層0.2mm輪廓檢查及每1mm抽層0.8mm opening分析保留。這些是原報告，本版未重跑幾何QA或真正切片工具路徑。

底座朝下，拱頂、欄孔、內梯、柱帽與球飾需支撐／橋接及移除路徑評估；角球／細柱仍可能脆弱。不保證免支撐、全面最小壁厚、任意縮小或任意多色切片器／AMS相容。沒有實體試印。
