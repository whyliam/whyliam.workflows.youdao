#!/usr/bin/env python3
"""Create a minimal installable workflow without vendored packages or user data."""
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parents[1]
target = root / 'whyliam.workflows.youdao.alfredworkflow'
files = ['youdao.py', 'splitargs.py', 'info.plist', 'version', 'License', 'README.md']
files += sorted(p.name for p in root.glob('icon*.png'))
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
    for name in files:
        archive.write(root / name, name)
print(str(target), target.stat().st_size, 'bytes')
