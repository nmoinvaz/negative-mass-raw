#!/usr/bin/env python3
"""Figure of #253: M_AH(x+ - x+_f) of family G against S, the late part, and the plateau against delta.
usage: plot_settled_mass_g.py RAWDIR OUT.svg      (RAWDIR holds runs/h0.005_d1e-08 etc. and runs/scan_G_h*.json; S from I41-rpi5)"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

raw, out = sys.argv[1], sys.argv[2]
I41 = os.path.expanduser("~/Source/negative-mass-raw/I41-rpi5/runs")
INK, INK2, GRID = "#191919", "#666666", "#e6e6e6"
BLUE, ORANGE = "#257de0", "#f47230"          # categorical slots 1 and 2 of the reference palette (light mode)


def load(p):
    return dict(np.load(os.path.join(p, "series.npz")))


G8, G6 = load(f"{raw}/runs/h0.005_d1e-08"), load(f"{raw}/runs/h0.005_d1e-06")
S8 = load(f"{I41}/h0.005_d1e-08")
plt.rcParams.update({"font.size": 10, "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.edgecolor": GRID, "axes.spines.top": False, "axes.spines.right": False, "svg.fonttype": "none"})
fig, ax = plt.subplots(1, 3, figsize=(15, 4.4), constrained_layout=True)


def line(a, s, c, ls, lab, x0=None):
    x = s["xp"] - s["xp"][0]
    a.plot(x, s["M"], color=c, lw=2, ls=ls, label=lab, solid_capstyle="round")


for a in ax[:2]:
    line(a, G8, BLUE, "-", "family G, δ = 1e-8")
    line(a, G6, BLUE, (0, (4, 3)), "family G, δ = 1e-6")
    line(a, S8, ORANGE, "-", "family S, δ = 1e-8")
    a.set_xlabel("x⁺ − x⁺_f")
    a.grid(True, color=GRID, lw=0.8)
    a.set_axisbelow(True)
ax[0].set_ylabel("M_AH = r_AH / 2   (a = 1)")
ax[0].set_title("From formation to the declared limit (h = 0.005)", loc="left", fontsize=10.5, color=INK)
ax[0].legend(frameon=False, loc="upper right")
ax[1].set_xlim(4.0, 9.4)
ax[1].set_ylim(0.2225, 0.2365)
ax[1].set_title("The plateau (same data)", loc="left", fontsize=10.5, color=INK)
ax[1].text(9.35, G8["M"][-1] + 0.0004, "G, δ = 1e-8", color=INK2, ha="right", fontsize=9)
ax[1].text(9.35, S8["M"][-1] + 0.0004, "S", color=INK2, ha="right", fontsize=9)

a = ax[2]
s41 = {r["delta"]: r for r in json.load(open(f"{I41}/scan_h0.01.json")) if "M_end" in r}
dS = sorted(d for d in s41 if d <= 1e-3)
a.plot(dS, [s41[d]["M_end"] for d in dS], color=ORANGE, lw=2, marker="o", ms=5, mec="white", mew=1.2, label="family S (h = 0.01)")
for h, mk in ((0.01, "o"), (0.005, "s")):
    p = f"{raw}/runs/scan_G_h{h:g}.json"
    if os.path.exists(p):
        rows = [r for r in json.load(open(p)) if "plat1" in r and r["delta"] <= 1e-3]
        a.plot([r["delta"] for r in rows], [r["plat1"] for r in rows], color=BLUE, lw=2 if h == 0.01 else 0, marker=mk, ms=5, mec="white", mew=1.2,
               label=f"family G (h = {h:g})")
a.set_xscale("log")
a.invert_xaxis()
a.set_xlabel("δ = p*ₕ − A   (closer to threshold to the right)")
a.set_ylabel("plateau of M_AH at the limit")
a.set_title("The settled mass against the distance from threshold", loc="left", fontsize=10.5, color=INK)
a.grid(True, color=GRID, lw=0.8)
a.set_axisbelow(True)
a.legend(frameon=False, loc="center right")
fig.savefig(out, format="svg")
print("wrote", out)
