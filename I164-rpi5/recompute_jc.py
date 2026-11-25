#!/usr/bin/env python3
"""Recompute, from the tables printed in the slow-rotation papers, what J_c/A and the mode crossing are.

usage: python3 -I recompute_jc.py [--mutate=NAME]       (run from any directory; needs sympy for P5, else P5 is not run)
This is a recompute, not a quote. Inputs are the numbers printed in Table I and Table II of arXiv:2403.08387 v1 and in
Table 1 of arXiv:2301.05243 v2, parsed from their TeX (no retyping), and the static throat area printed in Sec. 2 of
arXiv:2301.05243 v2, A = 4 pi r0^2 exp(pi C / 2 r0), r0 = 1.

The main unstable mode is omega_I = w0 + J^2 D (D > 0), the second one omega_I = J^2 Ds (Ds < 0), with the papers' units
r0 = 1. Then J_c^2 = -w0 / D and the crossing J_x^2 = -w0 / (D - Ds).

Pass criteria, written down before the script was first run (the Fig. 6 readings were taken by eye from the 300 dpi
rendering of PDF p. 20 of 2403.08387 v1, axes calibrated on the printed tick labels, reading error about 0.00005):
  P1  J_x / A rounds to 0.013 (in [0.0125, 0.0135)) for C = 0, 0.05, 0.1, 0.2   (printed: "around J/A = 0.013")
  P2  J_c / A (static area at r = 0) is within 0.0001 of the Fig. 6 reading at C = 0, 1.0, 1.4:
      0.02139, 0.01668, 0.01386
  P3  the rows of Table 1 of 2301.05243 v2 equal the rows of Table I of 2403.08387 v1 for the C they share
  P4  Table 2 of 2301.05243 v2 equals Table II of 2403.08387 v1
  P5  the printed w(r) of 2403.08387 v1 (Eq. 12) tends to 2 J / r^3 for r -> infinity, which is the normalization
      g_{t phi} = -2 J sin^2(theta) / r of G = 1 (neither paper states G)
  P6  the minimum of the areal radius e^{-f} (r^2 + 1) of the static metric printed in Sec. II B of 2403.08387 v1 lies
      at r = C/2 (within 1e-6) for C = 0.5, 1.0, 1.4, so for C != 0 the surface r = 0 is not the minimal surface
Mutations (each must exit 1): delta cross area w table min
"""
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
M1 = HERE / "src/2403.08387v1/main.tex"
L2 = HERE / "src/2301.05243v2/paper8.tex"
MUT = None
for a in sys.argv[1:]:
    if a.startswith("--mutate="):
        MUT = a.split("=", 1)[1]
fails = []
notrun = []
EIGHT_PI = 8 * math.pi


def fail(msg):
    fails.append(msg)
    print("FAIL", msg)


def strip_comments(path):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in path.read_text(encoding="utf-8").splitlines())


def table_rows(text, label):
    """Rows (list of float lists) of the tabular that precedes \\label{label}."""
    i = text.index("\\label{" + label + "}")
    j = text.rfind("\\begin{tabular}", 0, i)
    k = text.index("\\end{tabular}", j)
    body = text[text.index("}", text.index("{", j + len("\\begin{tabular}")) + 1) + 1:k]  # skip the column spec
    body = body.replace("\\hline", " ")
    rows = []
    for r in body.split("\\\\"):
        cells = [c.strip() for c in r.split("&")]
        if cells and all(re.fullmatch(r"-?\d+(\.\d+)?", c) for c in cells):  # header rows hold macros, not numbers
            rows.append([float(c) for c in cells])
    return rows


def area_r0(C):
    return 4 * math.pi * math.exp(math.pi * C / 2)


def area_min(C):  # minimum of 4 pi e^{-f} (r^2 + 1) over r, at r = C/2, from the metric printed in Sec. II B of 2403.08387
    return 4 * math.pi * (C * C / 4 + 1) * math.exp(C * (math.pi / 2 - math.atan(C / 2)))


def main():
    tm = strip_comments(M1)
    tl = strip_comments(L2)
    t1 = {r[0]: (r[1], r[2]) for r in table_rows(tm, "ImOm_coeff_main_moreC")}  # C -> (w0, D)
    t2 = {r[0]: r[1] for r in table_rows(tm, "ImOm_coeff_sec")}  # C -> Ds
    l1 = {r[0]: (r[1], r[2]) for r in table_rows(tl, "ImOm_coeff_main")}
    l2 = {r[0]: r[1] for r in table_rows(tl, "ImOm_coeff_sec")}
    print(f"Table I of 2403.08387: {len(t1)} rows; Table II: {len(t2)} rows; Table 1 of 2301.05243 v2: {len(l1)} rows; Table 2: {len(l2)} rows")
    if MUT == "delta":
        w0, D = t1[1.0]
        t1[1.0] = (w0, D * 0.8)
    if MUT == "table":
        w0, D = l1[0.4]
        l1[0.4] = (w0, D + 0.001)
    area = area_min if MUT == "area" else area_r0
    # ---- P6
    for c in (0.5, 1.0, 1.4):
        a, b = -5.0, 5.0
        g = (math.sqrt(5) - 1) / 2
        fun = lambda r: math.exp(-c * (math.atan(r) - math.pi / 2)) * (r * r + 1)
        x1, x2 = b - g * (b - a), a + g * (b - a)
        while b - a > 1e-10:
            if fun(x1) < fun(x2):
                b, x2 = x2, x1
                x1 = b - g * (b - a)
            else:
                a, x1 = x1, x2
                x2 = a + g * (b - a)
        rmin = 0.0 if MUT == "min" else (a + b) / 2
        if abs(rmin - c / 2) > 1e-6:
            fail(f"P6 C={c}: the minimum of the areal radius is at r = {rmin:.6f}, not C/2 = {c / 2}")
    print("P6 the minimum of e^{-f} (r^2 + 1) lies at r = C/2 for C = 0.5, 1.0, 1.4")
    if MUT == "cross":
        t2 = {c: -d for c, d in t2.items()}

    # ---- P3, P4
    shared = sorted(set(t1) & set(l1))
    for c in shared:
        if t1[c] != l1[c]:
            fail(f"P3 C={c}: Table I {t1[c]} differs from Table 1 of 2301.05243 {l1[c]}")
    print(f"P3 rows shared by the two main-mode tables: C = {shared}")
    if t2 != l2:
        fail(f"P4 second-mode tables differ: {t2} against {l2}")

    # ---- J_c / A for every row of Table I
    print("main mode: J_c = sqrt(-w0/D), A at r = 0 (static, as printed in 2301.05243 Sec. 2) and A at the minimal surface")
    print("   C      w0        D        J_c    A(r=0)   J_c/A(r=0)  8piJ_c/A(r=0)  J_c/A(min)  8piJ_c/A(min)")
    jc = {}
    for c in sorted(t1):
        w0, D = t1[c]
        j = math.sqrt(-w0 / D)
        jc[c] = j
        print(f"  {c:4.2f} {w0:8.3f} {D:9.3f} {j:8.4f} {area_r0(c):8.3f}   {j / area_r0(c):.5f}      {EIGHT_PI * j / area_r0(c) * 100:6.1f}%      "
              f"{j / area_min(c):.5f}     {EIGHT_PI * j / area_min(c) * 100:6.1f}%")
    # ---- P2
    for c, want in ((0.0, 0.02139), (1.0, 0.01668), (1.4, 0.01386)):
        got = jc[c] / area(c)
        if abs(got - want) > 0.0001:
            fail(f"P2 C={c}: J_c/A = {got:.5f} differs from the Fig. 6 reading {want} by more than 0.0001")
    # ---- crossings
    print("crossing of the main and the second mode (C <= 0.2): J_x = sqrt(-w0/(D - Ds))")
    cross = {}
    for c in (0.0, 0.05, 0.1, 0.2):
        w0, D = l1[c]
        den = D - t2[c]
        if den <= 0 or -w0 / den <= 0:
            fail(f"P1 C={c}: no real crossing (D - Ds = {den})")
            continue
        jx = math.sqrt(-w0 / den)
        cross[c] = jx / area(c)
        print(f"  C={c:4.2f}: J_x = {jx:.4f}, J_x/A = {cross[c]:.5f}, 8 pi J_x/A = {EIGHT_PI * cross[c] * 100:.1f}% of the limiting value")
        if not 0.0125 <= cross[c] < 0.0135:
            fail(f"P1 C={c}: J_x/A = {cross[c]:.5f} does not round to 0.013")
    # ---- numbers for the proposal
    if 1.0 in jc and len(cross) == 4:
        print(f"VALUE J_c/A at C=1 with the r=0 area: {jc[1.0] / area_r0(1.0):.4f}, i.e. {EIGHT_PI * jc[1.0] / area_r0(1.0) * 100:.1f}% of 1/(8 pi)")
        print(f"VALUE J_c/A at C=1 with the minimal-surface area: {jc[1.0] / area_min(1.0):.4f}, i.e. {EIGHT_PI * jc[1.0] / area_min(1.0) * 100:.1f}% of 1/(8 pi)")
        pcts = ", ".join(f"{EIGHT_PI * cross[c] * 100:.1f}" for c in (0.0, 0.05, 0.1, 0.2))
        print(f"VALUE crossing J_x/A at C = 0, 0.05, 0.1, 0.2 in percent of 1/(8 pi): {pcts}")
        print(f"VALUE J_c/A at C = 0: {jc[0.0] / area_r0(0.0):.4f}, i.e. {EIGHT_PI * jc[0.0] / area_r0(0.0) * 100:.1f}% of 1/(8 pi)")
    # ---- P5
    try:
        import sympy as sp
    except ImportError:
        notrun.append("P5")
        print("P5 NOT RUN: sympy is not installed")
        return
    r, C, r0, J, u = sp.symbols("r C r0 J u", positive=True)
    R2 = r ** 2 + r0 ** 2
    f = (C / r0) * (sp.atan(r / r0) - sp.pi / 2)
    pref = 2 if MUT == "w" else 3  # Eq. (12) of 2403.08387 v1 has 3 J / (2 C (C^2 + r0^2))
    w = pref * J / (2 * C * (C ** 2 + r0 ** 2)) * (1 - (1 + 2 * C * (C + r) / R2) * sp.exp(2 * f))
    s = sp.expand(sp.series(w.subs(r, 1 / u), u, 0, 5).removeO())
    c3 = sp.simplify(s.coeff(u, 3))
    c0, c1, c2 = (sp.simplify(s.coeff(u, k)) for k in (0, 1, 2))
    print(f"P5 w(r) at large r: coefficients of r^0, r^-1, r^-2, r^-3 = {c0}, {c1}, {c2}, {c3}")
    if (c0, c1, c2) != (0, 0, 0) or sp.simplify(c3 - 2 * J) != 0:
        fail(f"P5 w does not tend to 2 J / r^3: r^-3 coefficient {c3}")
    else:
        print("VALUE w -> 2 J / r^3 at large r (G = 1)")


main()
print(f"failures: {len(fails)}" + (f"; not run: {', '.join(notrun)}" if notrun else ""))
sys.exit(1 if fails else (3 if notrun else 0))
