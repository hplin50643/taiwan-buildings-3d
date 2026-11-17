#!/usr/bin/env python3
"""Verify documentation migration only; no network or repository writes."""
import argparse, hashlib, json
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument('--root', default='.')
a = p.parse_args()
root = Path(a.root).resolve()
report = json.loads(Path(__file__).with_name('migration.json').read_text(encoding='utf-8'))
errors = []
for row in report['files']:
    f = root / row['path']
    if not f.is_file():
        errors.append('missing: ' + row['path']); continue
    b = f.read_bytes()
    if len(b) != row['bytes'] or hashlib.sha256(b).hexdigest() != row['sha256']:
        errors.append('changed: ' + row['path'])
for row in report['renames']:
    if (root / row['old_path']).exists(): errors.append('old path still present: ' + row['old_path'])
if errors:
    print('FAIL\n' + '\n'.join(errors))
    raise SystemExit(1)
print('PASS:', len(report['files']), 'migration files; ', len(report['renames']), 'old paths absent')
