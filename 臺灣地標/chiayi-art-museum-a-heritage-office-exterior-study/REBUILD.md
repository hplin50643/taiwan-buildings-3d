# 重建

使用 requirements.txt 所列 Python 套件執行 `python build_model.py`、`python validate_model.py`；Blender 4.3.2 執行 `blender -b --python render_model.py`，再 `blender -b scene.blend --python verify_scene.py`。請在副本重建，程式會改寫同資料夾輸出。scene.blend1不是交付檔。


## 展示檔驗證

- 現行檔案：`sha256sum -c SHA256SUMS`；`python3 verify_preview_webp.py`（需 Pillow）另核對 WebP 的尺寸及解碼 RGBA。
- 渲染器仍在副本輸出 PNG；可用 `python3 verify_preview_webp.py /副本/previews` 核對新渲染像素，不需要在目前目錄保留 PNG。
- [固定交付版本](https://github.com/hplin50643/taiwan-buildings-3d/tree/57bd0886210a4ec7882adfe23f23c699ceabaa42/%E8%87%BA%E7%81%A3%E5%9C%B0%E6%A8%99/chiayi-art-museum-a-heritage-office-exterior-study)的原 PNG、當時 SHA256SUMS 與 manifest 皆維持原樣。此處兩份清單僅核對目前目錄。
