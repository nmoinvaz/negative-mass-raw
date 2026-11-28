#!/usr/bin/env python3
"""Figure of #246: (top) E/E_throat = 2 M_AH = r_AH^(n-1) of the apparent horizon against x+ - x+_f for S and G at D = 4, 5, 6 (finest h, delta = 1e-8, K = 28 at D = 5, 6; #41's and #253's
series at D = 4, K = 20); (bottom) the settled value (plateau mean over the last 1.0 of x+) against D, with G at delta = 1e-6 and 1e-8 and [ST17]'s E_f/E_throat = 1.00.
Standard-library SVG through the vendored data_graphs.py (arriba graph-data primitives, unchanged). Reads the runs of record and prints the same numbers as a table.

    python3 make_figure.py [RAW_DIR]      writes RAW_DIR/figures/settled_mass_d56.svg   (run from notes/wormhole_evolution of the worktree for the imports)
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i246/notes/wormhole_evolution"))
import data_graphs as dg            # noqa: E402
import settled_mass_d56 as d56      # noqa: E402

RAW = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
ROOT = os.path.dirname(RAW)
sm = d56.sm
HS = {3: d56.th.CRIT["H"][3], 4: d56.th.CRIT["H"][4]}


def load(n, fam, k, dl):
    return dict(np.load(os.path.join(RAW, "runs", d56.tag_of(n, fam, k, dl), "series.npz")))


curves = []          # (label, D, family, series, h, n)
s41 = dict(np.load(os.path.join(ROOT, "I41-rpi5", "runs", "h0.005_d1e-08", "series.npz")))
s253 = dict(np.load(os.path.join(ROOT, "I253-rpi5", "runs", "h0.005_d1e-08", "series.npz")))
curves += [("D = 4 S (#41)", 4, "S", s41, 0.005, 2), ("D = 4 G (#253)", 4, "G", s253, 0.005, 2)]
for n in (3, 4):
    for fam in ("S", "G"):
        curves.append((f"D = {n + 2} {fam}", n + 2, fam, load(n, fam, 2, 1e-8), HS[n][2], n))
svg = dg.Svg(760)
svg.text(16, 24, "The apparent horizon's mass at the Ellis threshold, D = 4, 5, 6", size=14, fill=dg.INK, weight="bold")
top = dg.caption(svg, 16, 40, "E/E_throat = 2 M_AH = r_AH^(n-1) after formation", "finest h, delta = 1e-8; S solid, G dashed; D = 4 from #41 and #253 (limit 1.57e6), D = 5, 6 to e^-f = 4.0e8")
px, py, pw, ph = 76, top, 640, 250
xm, ym = dg.axes(svg, px, py, pw, ph, (0.0, 12.0), (0.1, 6.0, "log"), "x+ - x+_f (time units from the first trapped cell)", "E/E_throat = 2 M_AH", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
svg.line(px, ym(1.0), px + pw, ym(1.0), dg.INK_SOFT, 1)
svg.text(px + 4, ym(1.0) - 4, "[ST17]: E_f/E_throat = 1.00", size=10)
slots = {4: 0, 5: 1, 6: 2}
legend = []
print(f"{'curve':16s} {'2M start':>9s} {'2M +2':>9s} {'2M end':>9s} {'x+ span':>8s}")
for lab, D, fam, s, h, n in curves:
    x = s["xp"] - s["xp"][0]
    y = 2.0 * s["M"]
    idx = np.unique(np.clip(np.searchsorted(x, np.linspace(0.0, x[-1], 700)), 0, len(x) - 1))
    pts = " ".join(f"{xm(a):.1f},{ym(max(b, 0.1)):.1f}" for a, b in zip(x[idx], y[idx]) if a <= 12.0)
    dash = ' stroke-dasharray="7 4"' if fam == "G" else ""
    svg.add(f'<polyline points="{pts}" fill="none" stroke="{dg.SERIES[slots[D]]}" stroke-width="2"{dash}/>')
    i2 = int(np.argmin(np.abs(x - 2.0)))
    print(f"{lab:16s} {y[0]:9.4f} {y[i2]:9.4f} {y[-1]:9.4f} {x[-1]:8.2f}")
    if fam == "S":
        legend.append((f"D = {D}", dg.SERIES[slots[D]]))
dg.legend(svg, px + pw - 4, py + ph - 14, legend + [("dashed: G", dg.INK_SOFT)])
bot = py + ph + 70
top2 = dg.caption(svg, 16, bot, "Settled E/E_throat against D", "plateau mean over the last 1.0 of x+, finest h; the bars are the finest-pair h difference (G at delta = 1e-8, 1e-6 shown separately)")
px2, py2, pw2, ph2 = 76, top2, 640, 220
xm2, ym2 = dg.axes(svg, px2, py2, pw2, ph2, (3.6, 6.4), (0.1, 2.0, "log"), "dimension D", "settled E/E_throat = 2 M", xfmt=lambda v: f"{v:g}" if abs(v - round(v)) < 1e-9 else "", yfmt=lambda v: f"{v:g}")
svg.line(px2, ym2(1.0), px2 + pw2, ym2(1.0), dg.INK_SOFT, 1)
print(f"\n{'D':>2s} {'S':>9s} {'G 1e-8':>9s} {'G 1e-6':>9s}   (plateau 2M, finest h)")
vals = {}
for D in (4, 5, 6):
    n = D - 2
    if D == 4:
        S_ = 2.0 * sm.settled_summary(s41, 0.005)["plat1"]
        G8 = 2.0 * sm.settled_summary(s253, 0.005)["plat1"]
        G6 = 2.0 * sm.settled_summary(dict(np.load(os.path.join(ROOT, "I253-rpi5", "runs", "h0.005_d1e-06", "series.npz"))), 0.005)["plat1"]
    else:
        S_ = 2.0 * d56.summary_n(load(n, "S", 2, 1e-8), HS[n][2], n)["plat1"]
        G8 = 2.0 * d56.summary_n(load(n, "G", 2, 1e-8), HS[n][2], n)["plat1"]
        G6 = 2.0 * d56.summary_n(load(n, "G", 2, 1e-6), HS[n][2], n)["plat1"]
    vals[D] = (S_, G8, G6)
    print(f"{D:2d} {S_:9.4f} {G8:9.4f} {G6:9.4f}")
    dg.marker(svg, "circle", xm2(D - 0.06), ym2(S_), dg.SERIES[0], f"D = {D} S: 2M = {S_:.4f}")
    dg.marker(svg, "square", xm2(D), ym2(G8), dg.SERIES[1], f"D = {D} G, delta = 1e-8: 2M = {G8:.4f}")
    dg.marker(svg, "diamond", xm2(D + 0.06), ym2(G6), dg.SERIES[2], f"D = {D} G, delta = 1e-6: 2M = {G6:.4f}")
dg.legend(svg, px2 + pw2 - 4, py2 + 14, [("S", dg.SERIES[0]), ("G, delta = 1e-8", dg.SERIES[1]), ("G, delta = 1e-6", dg.SERIES[2])])
dg.callout(svg, xm2(6.0), ym2(vals[6][1]), f"D = 6 G: {vals[6][1]:.2f} (1e-8), {vals[6][2]:.2f} (1e-6)", dx=-150, dy=-40)
height = dg.footnote(svg, ["settled_mass_d56.py (this branch), settled_mass.py (#41), settled_mass_g.py (#253)", "numba 0.68.1", "negative-mass-raw I246-dh610, I41-rpi5, I253-rpi5"], dg.host_specs(),
                     ["shared machine (dh610, load average 10 to 22 of 20)"], py2 + ph2 + 40, repo_url="https://github.com/nmoinvaz/negative-mass")
os.makedirs(os.path.join(RAW, "figures"), exist_ok=True)
out = os.path.join(RAW, "figures", "settled_mass_d56.svg")
open(out, "w").write(svg.finish(height))
print("wrote", out)
