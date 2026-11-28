#!/usr/bin/env python3
"""Figure of #296: the tests T1 and T2 against the departure threshold eps, and the symmetric member's reading against eps (h = 0.005).
usage: python3 settled_mass_eps_graph.py [OUT.svg]     (default OUT: settled_mass_eps.svg in notes/wormhole_evolution of the worktree)
The numbers come from the same functions as settled_mass_eps.py analyze (the stored runs of #266, #267, #283, #295, read only).
The graph primitives are phase2/nonradial/data_graphs.py (the arriba graph-data skill's), unchanged."""
import math
import os
import subprocess
import sys

import numpy as np

WT = os.path.expanduser("~/Source/negative-mass-i296")
HERE = os.path.join(WT, "notes", "wormhole_evolution")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(WT, "phase2", "nonradial"))
import data_graphs as dg                  # noqa: E402
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "settled_mass_eps.svg")
sys.argv = ["x"]
import settled_mass_eps as se             # noqa: E402

allp = (se.REF,) + se.TRAIN9 + se.TEST_NAMES
scan = (1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2)
rows = {}
for eps in scan:
    P = se.readall(allp, eps)
    PV = se.sub_ref(P, P[se.REF])
    r = {}
    for lab, Pv, kind in (("fixed", P, "P3"), ("V3", PV, "P3")):
        r[("T1", lab)] = float(np.max(np.abs(se.fit_pred(Pv, se.TRAIN9, se.SIX, se.M0, kind)["res"])))
        r[("T2", lab)] = float(np.max(np.abs(se.fit_pred(Pv, se.TRAIN9 + se.SIX, se.THREE, se.M0, kind)["res"])))
    rows[eps] = r
sym = {eps: se.read(se.REF, eps) for eps in scan}
print("eps      T1 fixed   T1 V3      T2 fixed   T2 V3      | B = 0: r_th - 1   rdot_th")
for eps in scan:
    r = rows[eps]
    print(f"{eps:<8g} {r[('T1', 'fixed')]:.2e}   {r[('T1', 'V3')]:.2e}   {r[('T2', 'fixed')]:.2e}   {r[('T2', 'V3')]:.2e}   | {sym[eps]['rth'] - 1:+.3e}  {sym[eps]['rdot']:+.3e}")

svg = dg.Svg(760)
X0, PW, PH = 86, 560, 220
y = 28
y = dg.caption(svg, 16, y, "Largest miss of the refit against the departure threshold eps",
               "h = 0.005; T1: refit over the nine, predict the six; T2: fifteen, predict the three; V3: B = 0's reading at the same eps subtracted")
xm, ym = dg.axes(svg, X0, y, PW, PH, (7e-4, 7e-2, "log"), (1e-6, 1e-3, "log"), "departure threshold eps (|odd| / r_tuned)", "max |M - predicted|",
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.0e}")
svg.add(f'<line x1="{X0}" y1="{ym(6e-5):.1f}" x2="{X0 + PW}" y2="{ym(6e-5):.1f}" stroke="{dg.INK}" stroke-width="1" stroke-dasharray="5 4"/>')
svg.text(X0 + 8, ym(6e-5) + 15, "bar 6e-5", size=11, fill=dg.INK)
SER = {("T1", "fixed"): ("circle", dg.SERIES[0]), ("T2", "fixed"): ("circle", dg.SERIES[1]), ("T1", "V3"): ("diamond", dg.SERIES[0]), ("T2", "V3"): ("diamond", dg.SERIES[1])}
for key, (sh, col) in SER.items():
    pts = [(xm(eps), ym(rows[eps][key])) for eps in scan]
    for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
        svg.line(x1, y1, x2, y2, col, 1.5)
    for eps in scan:
        dg.marker(svg, sh, xm(eps), ym(rows[eps][key]), col, f"{key[0]} ({key[1]}) at eps = {eps:g}: max |M - predicted| = {rows[eps][key]:.2e}")
dg.callout(svg, xm(1e-2), ym(rows[1e-2][("T2", "fixed")]), f"T2 at 1e-2: {rows[1e-2][('T2', 'fixed')]:.1e} (fails)", dx=-34, dy=-40)
dg.better_hint(svg, X0, y, PW, PH, "right", label="lower", reverse=True)
dg.legend(svg, X0 + PW, y - 10, [("T1, M_0 fixed", dg.SERIES[0]), ("T2, M_0 fixed", dg.SERIES[1]), ("T1, V3 (diamond)", dg.SERIES[0]), ("T2, V3 (diamond)", dg.SERIES[1])])

y1 = y + PH + 84
y = dg.caption(svg, 16, y1, "The symmetric member B = 0 read at eps: r_th - 1 and rdot_th should be 0 (static member)",
               "h = 0.005; the reading is the pair's mean profile; dotted: slope 2 in eps (the second-order part of the unstable mode)")
xm2, ym2 = dg.axes(svg, X0, y, PW, PH, (7e-4, 7e-2, "log"), (1e-6, 1e-1, "log"), "departure threshold eps (|odd| / r_tuned)", "magnitude at B = 0",
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.0e}")
for lab, key, sh, col, c2 in (("|r_th - 1|", "rth", "circle", dg.SERIES[2], 1.41), ("|rdot_th|", "rdot", "square", dg.SERIES[3], 3.24)):
    val = {eps: abs(sym[eps][key] - (1.0 if key == "rth" else 0.0)) for eps in scan}
    for eps in scan:
        dg.marker(svg, sh, xm2(eps), ym2(val[eps]), col, f"B = 0 {lab} at eps = {eps:g}: {val[eps]:.3e} ({val[eps] / eps ** 2:.2f} eps^2)")
    svg.add(f'<line x1="{xm2(7e-4):.1f}" y1="{ym2(c2 * 7e-4 ** 2):.1f}" x2="{xm2(7e-2):.1f}" y2="{ym2(c2 * 7e-2 ** 2):.1f}" stroke="{col}" stroke-width="1" stroke-dasharray="2 3"/>')
dg.callout(svg, xm2(1e-2), ym2(abs(sym[1e-2]['rdot'])), f"rdot_th = {sym[1e-2]['rdot']:+.2e} at 1e-2", dx=-30, dy=-36)
dg.legend(svg, X0 + PW, y - 10, [("|r_th - 1| (1.4 eps^2)", dg.SERIES[2]), ("|rdot_th| (3.24 eps^2)", dg.SERIES[3])])
try:
    commit = subprocess.check_output(["git", "-C", HERE, "rev-parse", "--short", "HEAD"], text=True).strip()
except (subprocess.SubprocessError, OSError):
    commit = "?"
height = dg.footnote(svg, [f"settled_mass_eps.py at negative-mass {commit}", "chain: #41 via #253", "member: #225 via #266", "speed: #267, #255", "stored runs of #266, #267, #283, #295"], dg.host_specs(),
                     ["T1 already exceeds the bar at eps = 1e-3 (7.2e-5 at W3, as #283's P3); V3 and the eps scan are post hoc, declared before the test points were read"], y1 + PH + 100,
                     repo_url="https://github.com/nmoinvaz/negative-mass")
open(out, "w").write(svg.finish(height))
print("wrote", out)
