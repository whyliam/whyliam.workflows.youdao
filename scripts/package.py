#!/usr/bin/env python3
"""Build a reproducible workflow containing only required runtime files."""
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parents[1]
target = root / 'whyliam.workflows.youdao.alfredworkflow'
files = ['youdao.py', 'splitargs.py', 'info.plist', 'version', 'License', 'README.md', 'docs/DEVELOPMENT.md']
files += sorted(p.name for p in root.glob('icon*.png'))
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
    for name in sorted(files):
        info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, (root / name).read_bytes())
print(str(target), target.stat().st_size, 'bytes')
