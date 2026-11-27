#!/usr/bin/env python3
"""Figure of the runs of record (#213): H/W against r/a on the throat diagonal, and k(r) = H (tau_s - tau) against r/a, finest h of each member.
Standard-library SVG through the vendored data_graphs.py (the arriba graph-data primitives, unchanged). Reads runs/D*.npz.

    python3 make_figure.py [RAW_DIR]      writes RAW_DIR/figures/expansion_H.svg and prints the same numbers as a table
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i213/notes/wormhole_evolution"))
import data_graphs as dg   # noqa: E402
import expansion as ex     # noqa: E402

RAW = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
runs = {}
for f in sorted(os.listdir(os.path.join(RAW, "runs"))):
    if f.startswith("D") and f.endswith(".npz"):
        R = ex.load_run(os.path.join(RAW, "runs", f))
        m = R["meta"]
        key = (m["n"], m["member"])
        if key not in runs or m["h"] < runs[key][0]:
            runs[key] = (m["h"], R)
order = [(2, "tuned"), (2, "0.01"), (2, "0.05"), (2, "0.2"), (3, "tuned"), (3, "0.05")]
color = {"tuned": dg.SERIES[0], "0.01": dg.SERIES[1], "0.05": dg.SERIES[2], "0.2": dg.SERIES[3]}
label = {"tuned": "p*_h + 1e-6", "0.01": "A = 0.01", "0.05": "A = 0.05", "0.2": "A = 0.2"}

series = []
print(f"{'D':>2s} {'member':>7s} {'h':>9s} {'H/W r=10':>9s} {'H/W r=25':>9s} {'H/W r=50':>9s} {'k':>8s} {'tau_s':>8s}")
for key in order:
    if key not in runs:
        continue
    h, R = runs[key]
    g = ex.diag_arrays(R)
    W = ex.W_EXACT[key[0]]
    cl = ex.classify(g["tau"], g["r"], g["H"], g["rho"], g["w"])
    ts = cl["tau_s"]
    ok = g["r"] >= 1.05
    r, H, tau = g["r"][ok], g["H"][ok], g["tau"][ok]
    rmono = np.maximum.accumulate(r)
    sel = np.unique(np.clip(np.searchsorted(rmono, np.exp(np.linspace(math.log(1.05), math.log(rmono[-1]), 700))), 0, len(r) - 1))
    series.append((key, h, r[sel], H[sel] / W, (H * (ts - tau))[sel]))
    vals = [float(np.interp(r0, g["r"], g["H"]) / W) if g["r"].max() > r0 else float("nan") for r0 in (10, 25, 50)]
    print(f"{key[0] + 2:2d} {key[1]:>7s} {h:9.5f} {vals[0]:9.3f} {vals[1]:9.3f} {vals[2]:9.3f} {cl['k']:8.4f} {ts:8.4f}")

svg = dg.Svg(760)
y0 = 64
svg.text(16, 24, "Throat diagonal of the symmetric expanding runs (family S), finest h of each member", size=14, fill=dg.INK, weight="bold")
legend_items = [(label[k], color[k]) for k in ("tuned", "0.01", "0.05", "0.2")]
dg.legend(svg, 744, 44, legend_items)
svg.text(16, 44, "solid: D = 4 (h = 0.01); dashed: D = 5 (h = 0.0035)", size=11)

def panel(y, ylo, yhi, ylog, ylabel, ytitle, ysub, yidx):
    top = dg.caption(svg, 16, y, ytitle, ysub)
    px, py, pw, ph = 76, top, 640, 250
    xm, ym = dg.axes(svg, px, py, pw, ph, (1.0, 300.0, "log"), (ylo, yhi, "log") if ylog else (ylo, yhi), "areal radius of the throat r/a", ylabel,
                     xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    return xm, ym, (px, py, pw, ph)

xm, ym, box = panel(y0 + 8, 0.03, 12.0, True, "H / W  (H = d ln r / d tau, W = linear rate)", "H/W against r/a",
                    "W = 1.182 / a (D = 4), 1.728 / a (D = 5); the band is the declared bar |H/W - 1| <= 10 % at r/a = 10, 25, 50", 3)
px, py, pw, ph = box
svg.add(f'<rect x="{px}" y="{ym(1.1):.1f}" width="{pw}" height="{ym(0.9) - ym(1.1):.1f}" fill="{dg.INK_SOFT}" opacity="0.15"/>')
svg.line(px, ym(1.0), px + pw, ym(1.0), dg.INK_SOFT, 1)
for r0 in (10, 25, 50):
    svg.line(xm(r0), py, xm(r0), py + ph, dg.INK_SOFT, 1)
for key, h, r, y, k in series:
    pts = " ".join(f"{xm(a):.1f},{ym(max(b, 0.031)):.1f}" for a, b in zip(r, y))
    dash = ' stroke-dasharray="6 4"' if key[0] == 3 else ""
    svg.add(f'<polyline points="{pts}" fill="none" stroke="{color[key[1]]}" stroke-width="2"{dash}/>')
bot = py + ph + 60
xm2, ym2, box2 = panel(bot, 0.0, 6.0, False, "k = H (tau_s - tau)", "k against r/a",
                       "tau_s from the linear fit of 1/H over the last e-fold of r; constant k means H = k/(tau_s - tau)", 3)
px2, py2, pw2, ph2 = box2
for kv in (2.0, 4.0):
    svg.line(px2, ym2(kv), px2 + pw2, ym2(kv), dg.INK_SOFT, 1)
for key, h, r, y, k in series:
    pts = " ".join(f"{xm2(a):.1f},{ym2(min(max(b, 0.0), 6.0)):.1f}" for a, b in zip(r, k))
    dash = ' stroke-dasharray="6 4"' if key[0] == 3 else ""
    svg.add(f'<polyline points="{pts}" fill="none" stroke="{color[key[1]]}" stroke-width="2"{dash}/>')
svg.text(px2 + pw2 - 4, ym2(2.0) - 6, "2", size=11, fill=dg.INK, anchor="end")
svg.text(px2 + pw2 - 4, ym2(4.0) - 6, "4", size=11, fill=dg.INK, anchor="end")
# callout: the tuned D = 4 member at r/a = 10
kt = [x for x in series if x[0] == (2, "tuned")][0]
j10 = int(np.argmin(np.abs(kt[2] - 10.0)))
dg.callout(svg, xm(kt[2][j10]), ym(kt[3][j10]), f"H/W = {kt[3][j10]:.2f} at r/a = 10", dx=-70, dy=-40)
height = dg.footnote(svg, ["expansion.py wip/i213-expanding-branch (dn.py of #39)", "numba 0.68.1", "negative-mass-raw I213-dh610"], dg.host_specs(),
                     ["shared machine, load average 12 to 20 of 20"], py2 + ph2 + 40)
os.makedirs(os.path.join(RAW, "figures"), exist_ok=True)
out = os.path.join(RAW, "figures", "expansion_H.svg")
open(out, "w").write(svg.finish(height))
print("wrote", out)
