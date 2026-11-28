"""Validate the decoded RGBA pixels of the saved scene rerender."""
import sys
from pathlib import Path
sys.dont_write_bytecode=True
from export_display_webp import A, records, rgba
r=records(A)['front']
size,h=rgba(Path(sys.argv[1]))
assert list(size)==r['dimensions'] and h==r['rgba_sha256']
print('Saved scene front matches the current WebP pixels.')
