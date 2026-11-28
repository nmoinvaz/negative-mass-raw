#!/usr/bin/env python3
"""Figure of #230: (top) the local exponent k_loc(r)/k_pred of the Ellis family at D = 4, 5, 6 against the areal radius of the throat, k_pred = 2(n-1);
(bottom) the exponent of the jump test against A = (2/pi)(phi_inf + b) with the closed form k = 2/(nA^2 - n - 1) for n = 2, 3, 4.
Standard-library SVG through the vendored data_graphs.py (the arriba graph-data primitives, unchanged). Reads runs of record.

    python3 make_figure.py [RAW_DIR [JT_DIR]]      writes RAW_DIR/figures/throat_scaling.svg and prints the same numbers as a table
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i230/notes/wormhole_evolution"))
import data_graphs as dg      # noqa: E402
import throat_scaling as ts   # noqa: E402

RAW = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
JT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAW, "runs")
I213 = os.path.join(os.path.dirname(RAW), "I213-dh610", "runs")
ellis = [("D = 4 (#213, tuned, h = 0.01)", os.path.join(I213, "D4_tuned_h0.01.npz"), 2),
         ("D = 5 (#213, tuned, h = 0.0035)", os.path.join(I213, "D5_tuned_h0.00353553.npz"), 3),
         ("D = 6 (A = 0.05, h = 0.003)", os.path.join(RAW, "runs", "D6_A0.05_h0.003_X200.npz"), 4)]
svg = dg.Svg(760)
svg.text(16, 24, "The expanding throat's exponent against the closed form", size=14, fill=dg.INK, weight="bold")
top = dg.caption(svg, 16, 40, "k_loc / k against r (Ellis family)", "k_loc = H^2/(dH/dtau); k = 2(n-1) = 2, 4, 6; the closed form's limit is 1")
px, py, pw, ph = 76, top, 640, 220
xm, ym = dg.axes(svg, px, py, pw, ph, (3.0, 300.0, "log"), (0.3, 1.02), "areal radius of the throat r/a", "k_loc / (2(n-1))", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
svg.line(px, ym(1.0), px + pw, ym(1.0), dg.INK_SOFT, 1)
legend = []
call = []
print(f"{'run':36s} {'r_end':>7s} {'k_loc(end)':>11s} {'k_inf':>9s} {'c(r=50)':>9s}")
for slot, (lab, path, n) in enumerate(ellis):
    if not os.path.exists(path):
        continue
    s = ts.summarize(path)
    r, kl = s["M"]["r"], s["kloc"] / (2.0 * (n - 1))
    ok = (r >= 3.0) & np.isfinite(kl)
    r, kl = r[ok], kl[ok]
    idx = np.unique(np.clip(np.searchsorted(r, np.exp(np.linspace(math.log(3.0), math.log(r[-3]), 500))), 0, len(r) - 3))
    pts = " ".join(f"{xm(a):.1f},{ym(min(max(b, 0.3), 1.02)):.1f}" for a, b in zip(r[idx], kl[idx]))
    svg.add(f'<polyline points="{pts}" fill="none" stroke="{dg.SERIES[slot]}" stroke-width="2"/>')
    legend.append((lab, dg.SERIES[slot]))
    if n == 3:
        j = int(np.searchsorted(r, 50.0))
        call.append((r[j], kl[j], f"D = 5, r = 50a: {kl[j]:.4f}"))
    print(f"{lab:36s} {s['r_end']:7.1f} {s['kl_end']:11.5f} {s['kinf']:9.5f} {s['c']:9.5f}")
dg.legend(svg, px + pw - 4, py + ph - 18, legend)
for xr, yk, txt in call:
    dg.callout(svg, xm(xr), ym(yk), txt, dx=-120, dy=70)
# lower panel
bot = py + ph + 70
top2 = dg.caption(svg, 16, bot, "k against A (jump test)", "A = (2/pi)(phi_inf + b), b the step added to the field's end value; points: k_inf of the runs; lines: k = 2/(nA^2 - n - 1)")
px2, py2, pw2, ph2 = 76, top2, 640, 240
xm2, ym2 = dg.axes(svg, px2, py2, pw2, ph2, (1.05, 1.9), (0.5, 20.0, "log"), "A (the amplitude of the closed form)", "k = H (tau_s - tau)", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
legend2 = []
for slot, n in enumerate((2, 3, 4)):
    a0 = math.sqrt((n + 1) / n) * 1.0005
    A = np.linspace(a0, 1.9, 400)
    k = 2.0 / (n * A ** 2 - n - 1)
    m = k < 20.0
    pts = " ".join(f"{xm2(a):.1f},{ym2(b):.1f}" for a, b in zip(A[m], k[m]))
    svg.add(f'<polyline points="{pts}" fill="none" stroke="{dg.SERIES[slot]}" stroke-width="2"/>')
    legend2.append((f"D = {n + 2}", dg.SERIES[slot]))
print(f"\n{'D':>2s} {'b':>7s} {'A':>9s} {'k pred':>9s} {'k_inf':>9s}")
import glob
for slot, n in enumerate((2, 3, 4)):
    paths = sorted(p for p in glob.glob(os.path.join(JT, f"D{n + 2}_S_b*.npz")) if "partial" not in p)
    for p in paths:
        s = ts.summarize(p)
        b = s["b"]
        A = ts.A_jump(n, b)
        kp = ts.k_jump(n, b)
        sh = dg.SHAPES[slot]
        dg.marker(svg, "circle", xm2(A), ym2(min(max(s["kinf"], 0.5), 20.0)), dg.SERIES[slot], f"D = {n + 2}, b = {b:+g}: k_inf = {s['kinf']:.4f}, predicted {kp:.4f}")
        print(f"{n + 2:2d} {b:+7.3f} {A:9.5f} {kp:9.4f} {s['kinf']:9.4f}")
for slot, n in enumerate((2, 3, 4)):
    A0 = math.sqrt(n / (n - 1))
    svg.add(f'<line x1="{xm2(A0):.1f}" y1="{py2}" x2="{xm2(A0):.1f}" y2="{py2 + ph2}" stroke="{dg.SERIES[slot]}" stroke-width="1" stroke-dasharray="4 4"/>')
    svg.text(xm2(A0) + 4, py2 + 12, "b = 0", size=11, fill=dg.SERIES[slot])
for slot, (lab, path, n) in enumerate(ellis):
    if os.path.exists(path):
        s = ts.summarize(path)
        dg.marker(svg, "diamond", xm2(math.sqrt(n / (n - 1))), ym2(s["kinf"]), dg.SERIES[slot], f"{lab}: k_inf = {s['kinf']:.5f}, predicted {2.0 * (n - 1):g}")
dg.legend(svg, 744, bot + 4, legend2 + [("diamonds: the Ellis family (b = 0)", dg.INK_SOFT)])
pt = [x for x in glob.glob(os.path.join(JT, "D6_S_b-0.03*.npz")) if "partial" not in x]
if pt:
    s6 = ts.summarize(pt[0])
    dg.callout(svg, xm2(ts.A_jump(4, s6["b"])), ym2(s6["kinf"]), f"D = 6, b = -0.03: k = {s6['kinf']:.2f}", dx=40, dy=30)
height = dg.footnote(svg, ["throat_scaling.py wip/i230-throat-kn (expansion.py, dn.py of #39)", "numba 0.68.1", "negative-mass-raw I230-dh610, I213-dh610"], dg.host_specs(),
                     ["shared machine, load average 13 to 18 of 20"], py2 + ph2 + 40)
os.makedirs(os.path.join(RAW, "figures"), exist_ok=True)
out = os.path.join(RAW, "figures", "throat_scaling.svg")
open(out, "w").write(svg.finish(height))
print("wrote", out)
