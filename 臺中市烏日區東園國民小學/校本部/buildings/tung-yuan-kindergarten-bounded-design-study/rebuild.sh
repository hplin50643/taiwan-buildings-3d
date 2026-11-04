#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p parts
# Rebuild the shipped nominal design reference; no outside workspace files or network.
blender -b --python-exit-code 1 --python reference-nominal/build.py > nominal-reference-build.log 2>&1
python verify_reference.py
blender -b --python-exit-code 1 --python analytic_source_miters.py > analytic-pre.log 2>&1
python relieve64.py > csg64-final-priority.log 2>&1
python export_csg64.py
blender -b --python-exit-code 1 --python analytic_source_miters.py > analytic.log 2>&1
python retriangulate_safe_pairs.py
python verify_binary.py
python verify_source_fronts.py > source-front.log
blender -b --python-exit-code 1 --python assemble_scene.py > assemble.log 2>&1
blender -b --python-exit-code 1 --python check_scene_collision.py > collision.log 2>&1

blender -b --python-exit-code 1 --python export_3mf.py > export3mf.log 2>&1
python label_previews.py
python sanitize_metadata.py
blender -b --python-exit-code 1 --python verify_actual_materials.py > material-readback.log 2>&1
blender -b --python-exit-code 1 --python check_scene_collision.py > collision.log 2>&1
python verify_3mf.py
python generate_public_qa.py
blender -b --python-exit-code 1 --python verify_3mf_materials.py > 3mf-material.log 2>&1
