#!/usr/bin/env python3
"""fig6_reader_check.py OUTDIR: runs paper/figures/make_figures.py's fig6_wormhole on the checkout's growth.csv with its output folder
replaced by OUTDIR (nothing is written into the checkout), and prints how its reader splits the markers. Run from paper/figures."""
import csv
import os
import sys

sys.path.insert(0, os.getcwd())
import make_figures as mf  # noqa: E402

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
mf.OUT = out
rows = list(csv.DictReader(open(os.path.join(mf.ROOT, "notes", "wormhole_largeD", "growth.csv"))))
ts = [r["source"].startswith("TS13") for r in rows]
print(f"rows {len(rows)}; source.startswith('TS13'): {sum(ts)} rows (open orange markers), the other {len(ts) - sum(ts)} drawn as 'this work'")
mf.fig6_wormhole()
p = os.path.join(out, "fig6_wormhole_largeD.pdf")
print(f"fig6_wormhole ran on growth.csv; wrote {p} {os.path.getsize(p)} bytes")
