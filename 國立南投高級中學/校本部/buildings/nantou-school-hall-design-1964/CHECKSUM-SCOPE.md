# 校驗版本與原檔交付範圍說明

本說明是追加的發布補充，未修改本機原凍結模型、README、舊校驗表或原 FREEZE-MANIFEST.json。此處未修改凍結原件不表示遠端同名根校驗表仍保留舊 bytes；根表新版取代與巢狀表保留的差異詳見下文。原凍結清單不包含本補充。

現行根目錄 SHA256SUMS 僅核驗其明列的當前檔案，不涵蓋其自身、原 FREEZE-MANIFEST.json 或本次補充。PUBLICATION-SUPPLEMENT-MANIFEST.json 另列原公開交付檔與本說明的 bytes、SHA256 及 Git blob SHA；補充清單本身依 Git commit 識別，不自我循環。

材色、年代、模型範圍與原 QA 限制仍依原文件；本說明不補簽列印性、歷史建成狀態或全實景材色認證。

## 歷史校驗表與精確公開別名

原 SHA256SUMS.txt 維持歷史 bytes。下列項目是原版路徑與摘要，不得用它們宣稱當前同名檔案已通過原版校驗（NOT_RECERTIFIED）。每列已將歷史摘要核對到公開的完整原檔別名；同名現行檔案仍須依新表及交付清單核驗。未列項目不獲豁免。

- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `BUILD-QA.json`，SHA256 `5e86d9399f8ca20f49d58ea44506a75a531cc2729eef4a5154b5655416e15a8c`。當前同路徑 SHA256：`本批未提供此同名路徑`。
  公開完整歷史別名：[original-classification-version/BUILD-QA.json](original-classification-version/BUILD-QA.json)、[original-classification-qa-aliases/ORIGINAL-BUILD-QA.json](original-classification-qa-aliases/ORIGINAL-BUILD-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `DOC-QA.json`，SHA256 `d78673f6ab041d3bf004dbd394c3e775f3ca3e428686d4042afe3e6ab40b9af4`。當前同路徑 SHA256：`本批未提供此同名路徑`。
  公開完整歷史別名：[original-classification-version/DOC-QA.json](original-classification-version/DOC-QA.json)、[original-classification-qa-aliases/ORIGINAL-DOC-QA.json](original-classification-qa-aliases/ORIGINAL-DOC-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `FORMAT-QA.json`，SHA256 `3a576d7584b0ce28105afe05638631755c714c655d1384108819e3206e67e403`。當前同路徑 SHA256：`本批未提供此同名路徑`。
  公開完整歷史別名：[original-classification-version/FORMAT-QA.json](original-classification-version/FORMAT-QA.json)、[original-classification-qa-aliases/ORIGINAL-FORMAT-QA.json](original-classification-qa-aliases/ORIGINAL-FORMAT-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `FRAMING-QA.json`，SHA256 `f05b1bc968281e54c39286488a7755e3bf2fd1729007ebb0388e65c29d0e70e2`。當前同路徑 SHA256：`93fa44abb1f0a9f9f28c80fa942c6a93328fef9bcbee741df2ca501396192a40`。
  公開完整歷史別名：[original-classification-version/FRAMING-QA.json](original-classification-version/FRAMING-QA.json)、[original-classification-qa-aliases/ORIGINAL-FRAMING-QA.json](original-classification-qa-aliases/ORIGINAL-FRAMING-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `IDENTITY-QA.json`，SHA256 `0f2ecc59827be2a7bd67d19ed0a7153c9fb2882051f024a3a5f69ee3f0c8fbe3`。當前同路徑 SHA256：`本批未提供此同名路徑`。
  公開完整歷史別名：[original-classification-version/IDENTITY-QA.json](original-classification-version/IDENTITY-QA.json)、[original-classification-qa-aliases/ORIGINAL-IDENTITY-QA.json](original-classification-qa-aliases/ORIGINAL-IDENTITY-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `PUBLICATION-DOC-QA.json`，SHA256 `7a5f6b6adf4a2f40873b1ddb702d23365d29c5b0355a1fafad6d0745c9f3fae7`。當前同路徑 SHA256：`本批未提供此同名路徑`。
  公開完整歷史別名：[original-classification-version/PUBLICATION-DOC-QA.json](original-classification-version/PUBLICATION-DOC-QA.json)、[original-classification-qa-aliases/ORIGINAL-PUBLICATION-DOC-QA.json](original-classification-qa-aliases/ORIGINAL-PUBLICATION-DOC-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `README.md`，SHA256 `33b1a48cdb45be8d9ffea063090e1ae5a77e119561eda1362156fc39c135fbef`。當前同路徑 SHA256：`dcbac0215229ad14ed43223a9eb917cf673b0036358701d29fe9abeb1f94311f`。
  公開完整歷史別名：[ORIGINAL-SOURCE-GAP-README.md](ORIGINAL-SOURCE-GAP-README.md)、[original-classification-version/README.md](original-classification-version/README.md)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `REBUILD-QA.json`，SHA256 `9ddecb3d44b0333d7e33d9006334de090f6f513a57a9084e8cdce37a27d71717`。當前同路徑 SHA256：`本批未提供此同名路徑`。
  公開完整歷史別名：[original-classification-version/REBUILD-QA.json](original-classification-version/REBUILD-QA.json)、[original-classification-qa-aliases/ORIGINAL-REBUILD-QA.json](original-classification-qa-aliases/ORIGINAL-REBUILD-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `SCENE-QA.json`，SHA256 `031f307ca58c630d98f1c6f9547e39e85c6d5644ae251a067ab154c40bf01f87`。當前同路徑 SHA256：`de38d1f3e3dd207c3ea3dead03810041c83612d8e332eab2a4fbf8054564d884`。
  公開完整歷史別名：[original-classification-version/SCENE-QA.json](original-classification-version/SCENE-QA.json)、[original-classification-qa-aliases/ORIGINAL-SCENE-QA.json](original-classification-qa-aliases/ORIGINAL-SCENE-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `SOURCE-VISUAL-QA.json`，SHA256 `48fb7284aa57df07fa6e6843fc487a371122b32d8eb413df7fa961437016274e`。當前同路徑 SHA256：`本批未提供此同名路徑`。
  公開完整歷史別名：[original-classification-version/SOURCE-VISUAL-QA.json](original-classification-version/SOURCE-VISUAL-QA.json)、[original-classification-qa-aliases/ORIGINAL-SOURCE-VISUAL-QA.json](original-classification-qa-aliases/ORIGINAL-SOURCE-VISUAL-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `back.png`，SHA256 `56154dbfeeb034ecadb50d6ac96988b9aa6a50ac2a5f304e9f0700aa60b53adc`。當前同路徑 SHA256：`14bfbe22d4e3cc25873d5804369561b229988716acfdbf3063b9592c97048de6`。
  公開完整歷史別名：[original-classification-version/back.png](original-classification-version/back.png)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `east.png`，SHA256 `c1c22476722b134cf5316eb4392c379cc5a55a6f57d9b8573ed09e098aa749d5`。當前同路徑 SHA256：`d0ef31a9eb68e668c823f94a8e850048342e578a637ad3c7c66c78a93d6f2733`。
  公開完整歷史別名：[original-classification-version/east.png](original-classification-version/east.png)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `front.png`，SHA256 `5207a441a283488b8870bd448ea16f6a852a06e98a613d9a74700f5de3b1eaeb`。當前同路徑 SHA256：`9a9e86796d32ccb0389cb518100b5deed6f76fa8a00fef66d5213084bc2d8b71`。
  公開完整歷史別名：[original-classification-version/front.png](original-classification-version/front.png)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `palette.json`，SHA256 `c73c1893786741e05852e49c4f96ea6abe10ab1f96e69b72a00635a6b1aeafec`。當前同路徑 SHA256：`a5bb36cb25571291557f3fb0e74b9f27efddd311ee9b995a145862d434323a14`。
  公開完整歷史別名：[original-classification-version/palette.json](original-classification-version/palette.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `preview.png`，SHA256 `f3d3f6208c996046e6c74a3c38312741c2c3865545dff837b1a105ac5813b683`。當前同路徑 SHA256：`7020a716af54948e080922cbf88b0c62a603e0cd617b3541e050caeb1ef90697`。
  公開完整歷史別名：[original-classification-version/preview.png](original-classification-version/preview.png)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `rear.png`，SHA256 `45f8f7800cf4574bfd9642ed8053c6f7bc6236c6dd0b7468b9a32b09c240657b`。當前同路徑 SHA256：`2d55e404b7c01b3d782fd82ad7da401a0b3e6e526491e4b52bc8aa01905c603c`。
  公開完整歷史別名：[original-classification-version/rear.png](original-classification-version/rear.png)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `scene.blend`，SHA256 `1a130488098d3389efae58a58ecbb1d07eb9d617ce44b6a07086d111e21afc53`。當前同路徑 SHA256：`73c2e9328faab16dd0ad5ab3f11f61d83edb657b660490343d48681c653af429`。
  公開完整歷史別名：[ORIGINAL-SOURCE-GAP-scene.blend](ORIGINAL-SOURCE-GAP-scene.blend)、[original-classification-version/scene.blend](original-classification-version/scene.blend)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `top.png`，SHA256 `f8383a0d37cc4c6b2ddf5dc268dbd2386b2c00142d467ad9ea50a8a9f5eb8719`。當前同路徑 SHA256：`b434b3d12cf0de2f99bb42908177a98da541b3cb8e1e6404f566ddc93604894d`。
  公開完整歷史別名：[original-classification-version/top.png](original-classification-version/top.png)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `537a10e96440dc3aff00398bc97b9572bde7584a13b30f633d2753694074abf5`；歷史 target `west.png`，SHA256 `824fc9bb6361b51eeba20681b34c0ba29b33a765cf9e556ad3035fe410f6ea76`。當前同路徑 SHA256：`1bb9547e7cd7c62978a983bb2984c12b42a87603e59c8cf9b7e46435aff5f522`。
  公開完整歷史別名：[original-classification-version/west.png](original-classification-version/west.png)。

