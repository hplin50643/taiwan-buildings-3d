"""Preserve original unlabelled rendered views for README preview aliases.
Architectural and research limitations remain in README.md.
"""
from pathlib import Path
from shutil import copyfile
P=Path(__file__).resolve().parent
for name in ['court-oblique', 'rear-oblique', 'top', 'entry-end']:
 copyfile(P/(name+'.png'),P/('review-'+name+'.png'))
