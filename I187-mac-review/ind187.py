#!/usr/bin/env python3
"""ind187: #187's rows checked by rounding, l = 3 out of sample against scipy, and CAP5c recomputed (criteria in
README.md beside this file).

    python3 ind187.py [--mutate=NAME] [--nm=DIR]
"""
import argparse
import json
import os
import re
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["k1-ulp", "k2-l", "k3-pair"])
ap.add_argument("--nm", default="/Users/nathan/Source/negative-mass/phase2/nonradial")
A = ap.parse_args()
MUT = A.mutate
JL = os.path.join(HERE, "jsonl")
CSV5 = os.path.join(HERE, "..", "I114-win", "convergence_l5_w0.7603.partial.csv")
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def crate_rows(l):
    """{(variant, gamma): row} and {variant: r_m} from the rerun's dd jsonl of this l"""
    rows, rms = {}, {}
    for ln in open(os.path.join(JL, f"rows_l{l}_dd.jsonl")):
        r = json.loads(ln)
        if r.get("cmd") == "rowsetup":
            rms = {v["variant"]: v["rm"] for v in r["variants"]}
        elif r.get("cmd") == "row":
            rows[(r["variant"], float(r["gamma"]))] = r
    return rows, rms


def unit(tok):
    """one unit of the token's last printed digit"""
    m = re.fullmatch(r"([+-]?)(\d+)(?:\.(\d*))?(?:e([+-]\d+))?", tok)
    nd = len(m.group(3) or "")
    ex = int(m.group(4) or 0)
    return Decimal(10) ** (ex - nd)


def within(x, tok):
    """|x - tok| / (half a unit of tok's last digit)"""
    return abs(x - Decimal(tok)) / (unit(tok) / 2)


def gfind(rows, v, g):
    for (vv, gg), r in rows.items():
        if vv == v and abs(gg - g) <= 1e-9 * max(1.0, abs(g)):
            return r
    return None


# ---- K1: the stored rows by rounding ----
ROW = re.compile(r"gamma=\s*(\S+): D_base=(\S+)\s+signs=(\[.*?\])\s+rel\.spread \(same r_m\)=(\S+)\s+"
                 r"D\(r_m~34\)=(\S+)\s+q_int=(\S+) q_ext=(\S+)\s+\((\d+)s\)(.*)")
HEAD = re.compile(r"^(.+?)\s*: r_m=(\S+)$")
HNAME = {"base (rtol1e-10, phi_cut1e-9, R60)": "base", "rtol 1e-12": "tol", "phi_cut 1e-12 (larger r_m)": "phi",
         "background R=90": "r90", "r0 = 3e-3": "r0"}
ok1, worst, nrow, ntok, bad1 = True, (0.0, ""), 0, 0, []
for l in (2, 4, 5, 6):
    rows, rms = crate_rows(l)
    for ln in open(os.path.join(A.nm, f"convergence_l{l}_output.txt")):
        ln = ln.rstrip("\n")
        h = HEAD.match(ln)
        if h and h.group(1) in HNAME:
            r = within(Decimal(repr(rms[HNAME[h.group(1)]])), h.group(2))
            ntok += 1
            if r > Decimal("1.000000001"):
                ok1 = False
                bad1.append(f"l{l} header {h.group(1)} r_m {rms[HNAME[h.group(1)]]} vs {h.group(2)}")
            continue
        m = ROW.match(ln)
        if not m:
            continue
        nrow += 1
        g = float(m.group(1))
        capped = "over 4 variants" in m.group(9)
        vs = ["base", "phi", "r90", "r0"] + ([] if capped else ["tol"])
        R = {v: gfind(rows, v, g) for v in vs}
        if any(R[v] is None for v in vs):
            ok1 = False
            bad1.append(f"l{l} g={g}: crate rows missing {[v for v in vs if R[v] is None]}")
            continue
        D = {v: Decimal(R[v]["d"]) for v in vs}
        dbase = D["base"] + (unit(m.group(2)) if MUT == "k1-ulp" else 0)
        same = [D[v] for v in (["r90", "r0"] if capped else ["tol", "r90", "r0"])]
        spread = (max(same) - min(same)) / abs(sum(same) / len(same))
        pairs = [("D_base", dbase, m.group(2)), ("D34", D["phi"], m.group(5)),
                 ("q_int", Decimal(R["base"]["q_int"]), m.group(6)), ("q_ext", Decimal(R["base"]["q_ext"]), m.group(7)),
                 ("spread", spread, m.group(4))]
        for name, x, tok in pairs:
            r = within(x, tok)
            ntok += 1
            if r > worst[0] and not (MUT == "k1-ulp" and name == "D_base"):
                worst = (float(r), f"l{l} g={g} {name}")
            if r > Decimal("1.000000001"):
                ok1 = False
                bad1.append(f"l{l} g={g} {name}: {x:.12e} vs {tok} ({float(r):.3f} half-units)")
        ntok += 1
        if not (m.group(3) == "[np.float64(-1.0)]" and all(D[v] < 0 for v in vs)):
            ok1 = False
            bad1.append(f"l{l} g={g} signs {m.group(3)}")
check("K1", ok1 and nrow > 0, f"{nrow} rows, {ntok} tokens; largest |crate - token| {worst[0]:.3f} of half a unit "
      f"({worst[1]})" + (f"; failed {len(bad1)}: " + "; ".join(bad1[:6]) if bad1 else ""))

# ---- K3: CAP5c recomputed (before K2, which takes minutes) ----
sc = {}
for ln in open(CSV5):
    r = json.loads(ln)
    if isinstance(r, list):
        sc[(r[0], float(r[1]))] = r[2]
rows5, _ = crate_rows(5)
pair = {"base": "base (rtol1e-10, phi_cut1e-9, R60)", "tol": "rtol 1e-12", "phi": "phi_cut 1e-12 (larger r_m)",
        "r90": "background R=90", "r0": "r0 = 3e-3"}
if MUT == "k3-pair":
    pair["phi"] = pair["base"]
want = {"base": 5.4e-9, "tol": 3.1e-9, "phi": 4.7e-8, "r90": 8.0e-10, "r0": 4.2e-9}
got, ok3 = {}, True
for v, k in pair.items():
    c = gfind(rows5, v, 6000.0)
    d = abs(float(Decimal(c["d"]) / Decimal(repr(sc[(k, 6000.0)])) - 1))
    got[v] = d
    ok3 &= float(f"{d:.1e}") == want[v]
ok3 &= max(got.values()) > 1e-8
check("K3", ok3, ", ".join(f"{v} {got[v]:.2e} (reported {want[v]:.1e})" for v in pair) +
      f"; largest {max(got.values()):.2e} against the bar 1e-8")

# ---- K2: l = 3 out of sample against scipy ----
sys.path.insert(0, A.nm)
import background as B  # noqa: E402
from polar_solver import PolarProblem  # noqa: E402
import time  # noqa: E402

LS = 4 if MUT == "k2-l" else 3
st = B.solve_star(0.7603, -1)
P, Pphi = PolarProblem(st, LS), PolarProblem(st, LS, phi_cut=1e-12)
rows3, _ = crate_rows(3)
ok2, notes = True, []
for g in (0.3, 40.0):
    t0 = time.time()
    zz, _ = P.interior_zerilli(g)
    f = 1 - 2 * P.Mext / P.rm
    s = {"D": P.D(g), "D34": Pphi.D(g), "q_int": f * zz[1] / zz[0], "q_ext": P.zerilli_q(g)}
    cb, cp = gfind(rows3, "base", g), gfind(rows3, "phi", g)
    c = {"D": float(cb["d"]), "D34": float(cp["d"]), "q_int": float(cb["q_int"]), "q_ext": float(cb["q_ext"])}
    for k in s:
        rel = abs(c[k] / s[k] - 1)
        good = rel <= 1e-7 and (c[k] > 0) == (s[k] > 0)
        ok2 &= good
        notes.append(f"g={g} {k}: crate {c[k]:+.10e} scipy {s[k]:+.10e} rel {rel:.1e}")
    notes.append(f"(scipy {time.time() - t0:.0f} s)")
check("K2", ok2, "; ".join(notes))

bad = [n for n, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}", flush=True)
sys.exit(1 if bad else 0)
