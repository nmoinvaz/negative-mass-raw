#!/usr/bin/env python3
"""extract.py PAPERSROOT TEXTROOT: for each PAPERSROOT/<id>/paper.pdf write TEXTROOT/<id>.pypdf.txt (pypdf, page marks) and
TEXTROOT/<id>.pdftotext.txt (pdftotext -layout). Skips existing. Run with: uv run --no-project --with pypdf python -I extract.py ..."""
import os
import subprocess
import sys

from pypdf import PdfReader

root, out = sys.argv[1:3]
os.makedirs(out, exist_ok=True)
for d in sorted(os.listdir(root)):
    pdf = os.path.join(root, d, "paper.pdf")
    if not os.path.isfile(pdf):
        continue
    a = os.path.join(out, d + ".pypdf.txt")
    b = os.path.join(out, d + ".pdftotext.txt")
    if not os.path.exists(a):
        try:
            r = PdfReader(pdf)
            with open(a, "w") as f:
                for i, p in enumerate(r.pages, 1):
                    f.write(f"\n=====PAGE {i}=====\n")
                    f.write(p.extract_text() or "")
        except Exception as e:  # noqa: BLE001
            print("pypdf failed", d, e)
    if not os.path.exists(b):
        subprocess.run(["pdftotext", "-layout", pdf, b], check=False)
    print(d, os.path.getsize(a) if os.path.exists(a) else 0, os.path.getsize(b) if os.path.exists(b) else 0)
