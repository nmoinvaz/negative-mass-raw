#!/usr/bin/env python3
"""#140: the window columns of #96's 22 sectors (sigma R = 8, 16; m = 1/2 .. 21/2) recounted from the stored arrays.

Reads (never writes, but --csv) ../I96-win/eig, ../I96-dh610/eig, ../I75-dh170 (supplementary) and the two sector logs. Imports the
window helper of tanh_spectrum.py, the code path of part_tanh, from --ts. Run with the venv python, -X utf8:

    retab.py [--tag=rpi5] [--ts=DIR_OF_tanh_spectrum.py] [--mutate=abscut|nearcut|notie] [--csv=FILE]

Order: (1) the planted window check of tanh_spectrum.py (part_window), unmutated, exit 1 before any stored array if it fails;
(2) per sector, the window of A and B from ts.window, the count by position (index of the cut's eigenvalue in A sorted by
decreasing modulus; the conjugate pair counted together), the count by exact modulus (squares of the stored doubles in
rational arithmetic), the cut's tie group, the margin to the nearest modulus outside it, and the values §7 and the logs print.
A3 window == position == exact, tie group = the cut's eigenvalue and its conjugate. A4 margin >= 1e-13. A5 the pilot (P = 320)
against the P = 340 file of sigma R = 16, m = 1/2. Exit 1 if A3, A4 or A5 fails. --mutate: abscut (ts.MUT = "abscut": the cut
from abs of a scalar), nearcut (a real value one ulp above the cut is added to A), notie (the position count leaves the
conjugate out). The csv holds only the machine-independent columns, so two machines' files diff."""
import argparse
import csv
import os
import platform
import re
import subprocess
import sys
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
ap = argparse.ArgumentParser()
ap.add_argument("--tag", default="rpi5")
ap.add_argument("--ts", default=os.path.expanduser("~/Source/negative-mass-i140/notes/warp"))
ap.add_argument("--mutate", default="", choices=["", "abscut", "nearcut", "notie"])
ap.add_argument("--csv", default="")
args = ap.parse_args()
sys.path.insert(0, args.ts)
import tanh_spectrum as ts  # noqa: E402

MS = [0.5 + k for k in range(11)]
RUNS = {8: ("I96-win", "sectors-s8.log"), 16: ("I96-dh610", "sectors-s16-p340.log")}
MARGIN = 1e-13
FAILS = []
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")


def check(name, ok, detail):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        FAILS.append(name)


def num(t):
    m = re.fullmatch(r"([\d.]+)×10([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)", t.strip())
    return float(m.group(1)) * 10 ** int(m.group(2).translate(SUP)) if m else float(t)


def git(*a):
    return subprocess.run(["git", "-C", args.ts, *a], capture_output=True, text=True).stdout.strip()


# ------------------------------------------------------------------------------------------------ the counts
def pos_count(sA, k):
    """Eigenvalues of A (sorted by decreasing |mu|) up to and including the last of {z, conj z}, z = sA[k]."""
    if args.mutate == "notie":
        return k + 1
    z = sA[k]
    return int(np.flatnonzero((sA == z) | (sA == np.conj(z))).max()) + 1


def exact_count(sA, k):
    """#{j : re_j^2 + im_j^2 >= re_k^2 + im_k^2}, the squares formed exactly. Only values within 1e-9 of the cut's modulus
    need the exact test."""
    sq = lambda x: Fraction(float(x.real)) ** 2 + Fraction(float(x.imag)) ** 2  # noqa: E731
    ab = np.abs(sA)
    c = ab[k]
    near = np.flatnonzero(np.abs(ab - c) <= 1e-9 * c)
    t = sq(sA[k])
    return int(np.sum(ab > c * (1 + 1e-9))) + sum(1 for j in near if sq(sA[j]) >= t)


def sector(path):
    d = np.load(path)
    vc = float(d["vc"])
    muA, muB = d["muA"] * vc, d["muB"] * vc
    muA, muB = muA[np.argsort(-np.abs(muA))], muB[np.argsort(-np.abs(muB))]  # the order of part_tanh
    if args.mutate == "nearcut":
        w0 = ts.window(muA, muB)
        muA = np.append(muA, complex(float(np.nextafter(np.abs(w0.sA)[w0.k], 1.0)), 0.0))
        muA = muA[np.argsort(-np.abs(muA))]
    w = ts.window(muA, muB)
    sA, k = w.sA, w.k
    ab = np.abs(sA)
    z = sA[k]
    pair = (sA == z) | (sA == np.conj(z))
    want = 1 if z.imag == 0 else 2
    others = ab[~pair]
    return dict(vc=vc, w=w, nwA=len(w.A), nwB=len(w.B), cut=w.cut, sym=w.asym, k=k, pos=pos_count(sA, k),
                exact=exact_count(sA, k), tie=int(np.sum(ab == ab[k])), pair=int(pair.sum()), want=want,
                sign=np.sign(ab[k] - abs(z)), margin=float(np.min(np.abs(others - ab[k])) / ab[k]),
                leadA=float(ab[0]), leadB=float(np.abs(muB).max()))


# ------------------------------------------------------------------------------------------------ what is printed
def parse_md(path):
    txt = open(path, encoding="utf-8").read()
    out = {}

    def rows(title):
        i = txt.index(title)
        j = txt.find("\n### ", i + 5)
        return [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in txt[i:j].splitlines()
                if re.match(r"\| \d", ln)]
    for sig in RUNS:
        for r in (r for r in rows(f"### The σR = {sig} sectors") if len(r) == 7):  # not the residual table (3 columns)
            out.setdefault((sig, float(r[0])), {}).update(cut=r[5], sym=f"{num(r[6]):.1e}")
        for r in (r for r in rows(f"### Real eigenvalues and the window, σR = {sig}") if len(r) == 9):
            a, b = r[2].split(" / ")
            out.setdefault((sig, float(r[0])), {}).update(nwA=int(a), nwB=int(b))
    return out


def parse_log(path, sig, first_run_only=False):
    txt = open(path, encoding="utf-8-sig").read()
    if first_run_only:
        txt = txt.split("######## ")[1]
    out, cur = {}, sig
    for ln in txt.splitlines():
        m = re.match(r"-- sigma R = (\d+), v_c", ln)
        if m:
            cur = int(m.group(1))
        m = re.match(r"\s+([\d.]+) \| (\S+ \S+ \S+ \S+) \| ([\d.]+) / ([\d.]+) \| +([\d.]+) \| ([\d.e+-]+)$", ln)
        if m:
            out.setdefault((cur, float(m.group(1))), {}).update(cut=m.group(5), sym=m.group(6))
        m = re.match(r"\s+(\d+) \| +([\d.]+) \| +([\d.]+) \| +(\d+) / +(\d+) \| (\d+) / (\d+) \|", ln)
        if m:
            out.setdefault((int(m.group(1)), float(m.group(2))), {}).update(nwA=int(m.group(4)), nwB=int(m.group(5)))
    return out


def fmt_change(r, old):
    ch = []
    if old.get("nwA") is not None and old["nwA"] != r["nwA"]:
        ch.append(f"A {old['nwA']}→{r['nwA']}")
    if old.get("nwB") is not None and old["nwB"] != r["nwB"]:
        ch.append(f"B {old['nwB']}→{r['nwB']}")
    if old.get("sym") is not None and old["sym"] != f"{r['sym']:.1e}":
        ch.append(f"sym {old['sym']}→{r['sym']:.1e}")
    if old.get("cut") is not None and old["cut"] != f"{r['cut']:.4f}":
        ch.append(f"cut {old['cut']}→{r['cut']:.4f}")
    return ", ".join(ch)


# ------------------------------------------------------------------------------------------------ main
print(f"# retab.py {' '.join(sys.argv[1:])}")
print(f"# machine {platform.node()} {platform.machine()}, Python {platform.python_version()}, numpy {np.__version__}; "
      f"tanh_spectrum.py from {args.ts} at {git('rev-parse', '--short', 'HEAD')}"
      f"{' (with uncommitted changes)' if git('status', '--porcelain', '--', 'tanh_spectrum.py') else ''}")
print("== planted truth: tanh_spectrum.py part_window, unmutated, before any stored array")
ts.MUT = ""
ts.part_window()
if ts.FAILED:
    print("FAILED: " + ", ".join(ts.FAILED) + "; no stored array is read")
    sys.exit(1)
ts.MUT = "abscut" if args.mutate == "abscut" else ""
print(f"== mutation: {args.mutate or 'none'}")

md = parse_md(os.path.join(args.ts, "tanh_spectrum.md"))
logs = {}
for sig, (folder, name) in RUNS.items():
    logs.update(parse_log(os.path.join(RAW, folder, name), sig))
res = {}
for sig, (folder, _) in RUNS.items():
    for m in MS:
        res[(sig, m)] = sector(os.path.join(RAW, folder, "eig", f"tanh_sigma{sig}_m{m:g}.npz"))

print("== md against the logs (data): the values §7 prints that the sector logs do not print")
bad = [f"{key}: md {md[key][f]}, log {logs[key][f]}" for key in md for f in ("nwA", "nwB", "sym", "cut") if str(md[key][f]) != str(logs[key][f])]
print("  none differ" if not bad else "  " + "; ".join(bad))

print("== A3, A4: window of A (ts.window) against the count by position and by exact modulus; the margin")
for sig in RUNS:
    print(f"\n| σR = {sig}, m | cut | A window | by position | exact modulus | cut's tie group | abs(array) − abs(scalar) | "
          "margin | B window | symmetry | §7: A / B, symmetry | change |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    tot = np.zeros(4, int)
    for m in MS:
        r, old = res[(sig, m)], md[(sig, m)]
        s = {1.0: "+", 0.0: "0", -1.0: "−"}[float(r["sign"])]
        print(f"| {m:g} | {r['cut']:.4f} | {r['nwA']} | {r['pos']} | {r['exact']} | {r['tie']} | {s} | {r['margin']:.1e} | "
              f"{r['nwB']} | {r['sym']:.1e} | {old['nwA']} / {old['nwB']}, {old['sym']} | {fmt_change(r, old) or '—'} |")
        tot += [r["nwA"], r["nwB"], old["nwA"], old["nwB"]]
    print(f"\n  σR = {sig} totals over 11 sectors: A {tot[0]} (§7 {tot[2]}), B {tot[1]} (§7 {tot[3]})")
print()
for sig in RUNS:
    rs = [(m, res[(sig, m)]) for m in MS]
    bad = [f"m={m:g}: window {r['nwA']}, position {r['pos']}, exact {r['exact']}, tie {r['tie']}/{r['pair']} (want {r['want']})"
           for m, r in rs if not (r["nwA"] == r["pos"] == r["exact"] and r["tie"] == r["pair"] == r["want"])]
    check(f"A3 sigma R = {sig}", not bad, "window = position = exact modulus in 11 of 11 sectors, the cut's tie group is its "
          "eigenvalue and its conjugate" if not bad else f"{len(bad)} of 11 differ: " + "; ".join(bad))
    low = [(m, r["margin"]) for m, r in rs if r["margin"] < MARGIN]
    check(f"A4 sigma R = {sig}", not low, f"smallest margin {min(r['margin'] for _, r in rs):.1e} (limit {MARGIN:g}), "
          f"{len(rs) - len(low)} of 11 sectors at or above it" + (f"; below: {[f'{m:g}' for m, _ in low]}" if low else ""))

print("== A5: sigma R = 16, m = 1/2, the pilot (I96-win, P = 320) against the sector run (I96-dh610, P = 340)")
pil = sector(os.path.join(RAW, "I96-win", "eig", "tanh_sigma16_m0.5.npz"))
sec = res[(16, 0.5)]
for name, r in (("pilot  P = 320", pil), ("sector P = 340", sec)):
    print(f"  {name}: cut {r['cut']:.6f}, A window {r['nwA']} (position {r['pos']}, exact {r['exact']}), B window {r['nwB']}, "
          f"symmetry {r['sym']:.1e}, margin {r['margin']:.1e}, leading |mu| v_c A {r['leadA']:.12f}, B {r['leadB']:.12f}")
dA, dB = abs(pil["leadA"] - sec["leadA"]) / sec["leadA"], abs(pil["leadB"] - sec["leadB"]) / sec["leadB"]
ok = (dA <= 1e-8 and dB <= 1e-8 and f"{pil['cut']:.4f}" == f"{sec['cut']:.4f}" and pil["nwA"] == pil["pos"] == pil["exact"]
      and pil["margin"] >= MARGIN)
check("A5", ok, f"leading |mu| v_c differ by {dA:.1e} (A) and {dB:.1e} (B) relative (limit 1e-8), cuts {pil['cut']:.4f} and "
      f"{sec['cut']:.4f}, the pilot passes A3 and A4 ({pil['nwA']} = {pil['pos']} = {pil['exact']}, margin {pil['margin']:.1e})")

print("\n== A6: every window count or symmetry value of §7's tables that differs, old (§7) → new")
rows = [(sig, m, res[(sig, m)], md[(sig, m)]) for sig in RUNS for m in MS]
diff = [(sig, m, fmt_change(r, old)) for sig, m, r, old in rows if fmt_change(r, old)]
for sig, m, ch in diff:
    print(f"  σR = {sig}, m = {m:g}: {ch}")
print(f"  {len(diff)} of 22 sectors differ" if diff else "  none differs")
lg = [(sig, m, fmt_change(r, logs[(sig, m)])) for sig, m, r, _ in rows if fmt_change(r, logs[(sig, m)])]
print("  against the sector logs: " + ("; ".join(f"σR = {s}, m = {m:g}: {c}" for s, m, c in lg) if lg else "none differs"))

csvname = args.csv or os.path.join(HERE, f"retab_{args.tag}{'_' + args.mutate if args.mutate else ''}.csv")
with open(csvname, "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["sigma", "m", "nwA", "nwB", "position", "exact", "cut4", "sym2"])
    for sig in RUNS:
        for m in MS:
            r = res[(sig, m)]
            wr.writerow([sig, f"{m:g}", r["nwA"], r["nwB"], r["pos"], r["exact"], f"{r['cut']:.4f}", f"{r['sym']:.1e}"])
print(f"\n  machine-independent columns written to {os.path.basename(csvname)}")

if args.mutate == "":
    print("\n== supplementary (data, not part of the acceptance): sigma R = 2 and 4, the 22 sectors of I75-dh170, against "
          "tanh_spectrum_output.txt (#75's full run)")
    old75 = parse_log(os.path.join(args.ts, "tanh_spectrum_output.txt"), 2, first_run_only=True)
    for sig in (2, 4):
        n = [0, 0, 0, 0]
        symold, symnew, dif = 0.0, 0.0, []
        for m in MS:
            r = sector(os.path.join(RAW, "I75-dh170", f"tanh_sigma{sig}_m{m:g}.npz"))
            old = old75[(sig, m)]
            n[0] += r["nwA"]; n[1] += r["nwB"]; n[2] += old["nwA"]; n[3] += old["nwB"]
            symold, symnew = max(symold, float(old["sym"])), max(symnew, r["sym"])
            ch = fmt_change(r, old)
            if ch:
                dif.append(f"m = {m:g}: {ch}")
            if not (r["nwA"] == r["pos"] == r["exact"]) or r["margin"] < MARGIN:
                dif.append(f"m = {m:g}: A3/A4 would fail (window {r['nwA']}, position {r['pos']}, exact {r['exact']}, "
                           f"margin {r['margin']:.1e})")
        print(f"  σR = {sig}: window totals A / B: new {n[0]} / {n[1]}, #75's log {n[2]} / {n[3]}; largest symmetry value new "
              f"{symnew:.1e}, #75's log {symold:.1e}; sectors that differ: " + ("; ".join(dif) if dif else "none"))

print()
if FAILS:
    print("FAILED: " + ", ".join(FAILS))
    sys.exit(1)
print("all checks passed")
