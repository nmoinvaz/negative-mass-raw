"""#96: the numbers of the sigma R = 8 and 16 sector runs that no log prints, recomputed from the stored eigenvalue arrays.

Reads (never writes) ../I96-win/{sectors-s8.log, eig/}, ../I96-dh610/{sectors-s16-p340.log, eig/, memwatch.log} and the
pilot's ../I96-win/eig/tanh_sigma16_m0.5.npz. Run from any directory with the venv python, -X utf8:

    sector_numbers.py [--mutate=cut|real|ab]

R1  every column of the sector logs that can be recounted from the npz is, in all 22 sectors (exit 1 if one differs);
R1b added after R1 failed at sigma R = 8 (README): where a window count or symmetry value differs from the log, the log's value
    must equal the recount with the cut's own eigenvalues left out (|mu| > cut), else FAIL; R1 itself is not loosened;
R2  |rho_A - rho_B| < 1e-6 rho in every sector (exit 1 otherwise);
R3  the leading |mu| v_c of A and B at P = 320 (pilot) and P = 340, sigma R = 16, m = 1/2 (data);
R4  dh610's largest rss and lowest MemAvailable (data).
Then the sector and window tables of the note's section 7 as markdown, per sigma R, and the residuals of both logs.
match_stable, persisting and real_cands are copies of tanh_spectrum.py's (lines 613, 625, 531). --mutate breaks one input
on purpose: cut (match tolerance 1e-3, not 1e-5), real (real tolerance 0.5, not 1e-9), ab (B times 1 + 2e-6)."""
import os
import re
import sys

import numpy as np

R = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(R)
MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), "")
if MUT not in ("", "cut", "real", "ab"):
    sys.exit(f"unknown --mutate={MUT}")
RUNS = {8: (os.path.join(RAW, "I96-win"), "sectors-s8.log"), 16: (os.path.join(RAW, "I96-dh610"), "sectors-s16-p340.log")}
MS = [0.5 + k for k in range(11)]
fails = []


def real_cands(mu, tol=1e-9):
    return mu[np.abs(mu.imag) < (0.5 if MUT == "real" else tol) * np.abs(mu)]


def match_stable(muA, muB, tol=1e-5, lo=1e-3):
    tol = 1e-3 if MUT == "cut" else tol
    cut = 0.0
    for z in muA:
        if abs(z) < lo:
            break
        if np.abs(muB - z).min() > tol * abs(z):
            cut = abs(z)
            break
    return cut


def persisting(muA_real, muB, tol=1e-4):
    n = 0
    for z in muA_real:
        j = int(np.argmin(np.abs(muB - z)))
        if abs(muB[j] - z) < tol * abs(z) and abs(muB[j].imag) < 1e-9 * abs(muB[j]):
            n += 1
    return n


def load(path):
    d = np.load(path)
    vc = float(d["vc"])
    muA, muB = d["muA"] * vc, d["muB"] * vc
    if MUT == "ab":
        muB = muB * (1 + 2e-6)
    return vc, muA[np.argsort(-np.abs(muA))], muB[np.argsort(-np.abs(muB))]


def parse(log):
    txt = open(log, encoding="utf-8-sig").read()
    sec, win, res, times = {}, {}, {}, {}
    for ln in txt.splitlines():
        m = re.match(r"\s+([\d.]+) \| (\S+ \S+ \S+ \S+) \| ([\d.]+) / ([\d.]+) \| +([\d.]+) \| ([\d.e+-]+)$", ln)
        if m:
            sec[float(m.group(1))] = dict(A=m.group(3), B=m.group(4), cut=m.group(5), asym=m.group(6))
        m = re.match(r"\s+(\d+) \| +([\d.]+) \| +([\d.]+) \| +(\d+) / +(\d+) \| (\d+) / (\d+) \| +(\d+) / +(\d+), ([\d.e+-]+), "
                     r"(\d+) \| .* ([\d.e+-]+) on (\d+) eigenfunctions, (\d+) real", ln)
        if m:
            win[float(m.group(2))] = dict(lo=m.group(3), nwA=int(m.group(4)), nwB=int(m.group(5)), rwA=int(m.group(6)),
                                          rwB=int(m.group(7)), raA=int(m.group(8)), raB=int(m.group(9)), big=m.group(10),
                                          pers=int(m.group(11)), ident=m.group(12), nef=int(m.group(13)), nreal=int(m.group(14)))
        m = re.match(r"\s+residual .* m = ([\d.]+): worst ([\d.e+-]+)", ln)
        if m:
            res[float(m.group(1))] = m.group(2)
        m = re.match(r"\s+sigma R = +(\d+), m = +([\d.]+): done in (\d+) s", ln)
        if m:
            times[float(m.group(2))] = int(m.group(3))
    wall = re.findall(r"wall (\d+) s", txt)
    return sec, win, res, times, int(wall[-1]) if wall else None


def check(name, ok, detail):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        fails.append(name)


data = {}
for sig, (folder, logname) in RUNS.items():
    sec, win, res, times, wall = parse(os.path.join(folder, logname))
    rows = {}
    for m in MS:
        vc, muA, muB = load(os.path.join(folder, "eig", f"tanh_sigma{sig}_m{m:g}.npz"))
        cut = match_stable(muA, muB)
        lo = max(cut, 1e-3)
        wA, wB = muA[np.abs(muA) >= lo], muB[np.abs(muB) >= lo]
        aA, aB = real_cands(muA[np.abs(muA) > 1e-8]), real_cands(muB[np.abs(muB) > 1e-8])
        asym = max((np.abs(muA + z).min() / abs(z) for z in wA), default=0.0)
        xA = muA[np.abs(muA) > lo]  # the cut's own eigenvalues left out
        asym_x = max((np.abs(muA + z).min() / abs(z) for z in xA), default=0.0)
        k0 = next((k for k, z in enumerate(muA) if abs(z) == cut), None)
        rows[m] = dict(nwA_x=len(xA), asym_x=asym_x, tie=None if k0 is None else float(np.abs(muA)[k0] - abs(muA[k0])), vc=vc, muA=muA, muB=muB, cut=cut, nwA=len(wA), nwB=len(wB), rwA=len(real_cands(wA)),
                       rwB=len(real_cands(wB)), raA=len(aA), raB=len(aB), big=float(np.abs(aA).max()) if len(aA) else 0.0,
                       pers=persisting(aA, muB), asym=asym)
    data[sig] = (rows, sec, win, res, times, wall)

print("== R1: the logs' columns recounted from eig/*.npz (a difference is a FAIL)")
for sig, (rows, sec, win, res, times, wall) in data.items():
    bad = []
    for m, r in rows.items():
        s, w = sec[m], win[m]
        got = dict(A=f"{abs(r['muA'][0]):.8f}", B=f"{abs(r['muB'][0]):.8f}", cut=f"{r['cut']:.4f}", asym=f"{r['asym']:.1e}")
        bad += [f"m={m:g} {k}: log {s[k]} recount {got[k]}" for k in got if got[k] != s[k]]
        got = dict(lo=f"{max(r['cut'], 1e-3):.4f}", nwA=r["nwA"], nwB=r["nwB"], rwA=r["rwA"], rwB=r["rwB"], raA=r["raA"],
                   raB=r["raB"], big=f"{r['big']:.1e}", pers=r["pers"])
        bad += [f"m={m:g} {k}: log {w[k]} recount {got[k]}" for k in got if got[k] != w[k]]
    check(f"recount sigma R = {sig}", not bad and len(rows) == 11 == len(sec) == len(win),
          "11 sectors, 12 columns each, all equal to the log" if not bad else f"{len(bad)} differ, first: {bad[:3]}")

print("== R1b: where R1 differs, does the log equal the recount without the cut's own eigenvalues (|mu| > cut)?")
for sig, (rows, sec, win, res, times, wall) in data.items():
    diff, unexplained = [], []
    for m, r in rows.items():
        if r["nwA"] != win[m]["nwA"] or f"{r['asym']:.1e}" != sec[m]["asym"]:
            diff.append(m)
            if r["nwA_x"] != win[m]["nwA"] or f"{r['asym_x']:.1e}" != sec[m]["asym"]:
                unexplained.append(m)
    ties = [m for m, r in rows.items() if r["tie"] is not None]
    check(f"R1b sigma R = {sig}", not unexplained,
          f"sectors where the log's A window count or symmetry differs from the recount: {[f'{m:g}' for m in diff] or 'none'}; "
          f"of them reproduced without the cut's eigenvalues: {len(diff) - len(unexplained)}; "
          f"np.abs(array) - abs(scalar) at the cut's eigenvalue, here: "
          + ", ".join(f"{m:g}:{rows[m]['tie']:+.0e}" for m in ties))
nmis = 0
ntot = 0
for sig, (folder, logname) in RUNS.items():
    for m in MS:
        for key in ("muA", "muB"):
            a = np.load(os.path.join(folder, "eig", f"tanh_sigma{sig}_m{m:g}.npz"))[key]
            nmis += int(np.sum(np.abs(a) != np.array([abs(z) for z in a])))
            ntot += len(a)
print(f"  here (numpy {np.__version__}, {os.uname().machine}) np.abs(array) differs from abs(scalar) in the last bit for "
      f"{nmis} of {ntot} stored eigenvalues, so a comparison |mu| >= cut with the two paths is decided by rounding")

print("== R2: A and B on the leading |mu| v_c of every sector (the issue: 1e-6)")
for sig, (rows, *_rest) in data.items():
    d = {m: abs(abs(r["muA"][0]) - abs(r["muB"][0])) for m, r in rows.items()}
    rel = {m: d[m] / abs(rows[m]["muA"][0]) for m in d}
    print(f"  sigma R = {sig}: |A - B| per sector (absolute) " + " ".join(f"{m:g}:{d[m]:.1e}" for m in d))
    check(f"ab sigma R = {sig}", all(v < 1e-6 for v in rel.values()),
          f"largest relative |A - B| {max(rel.values()):.1e} at m = {max(rel, key=rel.get):g} (limit 1e-6); rho_A {abs(rows[0.5]['muA'][0]):.10f}, "
          f"rho_B {abs(rows[0.5]['muB'][0]):.10f}, |A - B| {d[0.5]:.2e}")

print("== R3: sigma R = 16, m = 1/2, P = 320 (pilot, I96-win) against P = 340 (dh610)")
vc0, a0, b0 = load(os.path.join(RAW, "I96-win", "eig", "tanh_sigma16_m0.5.npz"))
vc1, a1, b1 = load(os.path.join(RUNS[16][0], "eig", "tanh_sigma16_m0.5.npz"))
for name, x, y in (("A", a0, a1), ("B", b0, b1)):
    print(f"  {name}: |mu| v_c = {abs(x[0]):.12f} (P = 320), {abs(y[0]):.12f} (P = 340), difference {abs(y[0]) - abs(x[0]):+.2e}, "
          f"relative {abs(abs(y[0]) - abs(x[0])) / abs(x[0]):.1e}")
print(f"  A (P = 320) against B (P = 330): {abs(abs(a0[0]) - abs(b0[0])):.2e}; A (P = 340) against B (P = 350): "
      f"{abs(abs(a1[0]) - abs(b1[0])):.2e}")
print(f"  the leading four of A at P = 340: " + " ".join(f"{z.real:+.6f}{z.imag:+.6f}i" for z in a1[:4]))

print("== R4: dh610's memwatch.log (rss of every tanh_spectrum.py process, MemAvailable, once a minute; report only)")
ts, rss, avail = [], [], []
for ln in open(os.path.join(RUNS[16][0], "memwatch.log"), encoding="utf-8-sig"):
    m = re.match(r"(\S+) rss_kib (\d+) MemAvailable: (\d+) kB", ln)
    if m:
        ts.append(m.group(1)), rss.append(int(m.group(2))), avail.append(int(m.group(3)))
i, j = int(np.argmax(rss)), int(np.argmin(avail))
print(f"  {len(ts)} samples, {ts[0]} to {ts[-1]}")
print(f"  largest rss {rss[i] / 2**20:.2f} GiB at {ts[i]}; lowest MemAvailable {avail[j] / 2**20:.2f} GiB at {ts[j]}; "
      f"last rss {rss[-1] / 2**20:.2f} GiB")

for sig, (rows, sec, win, res, times, wall) in data.items():
    vc = rows[0.5]["vc"]
    print(f"\n== sigma R = {sig}: sector table (section 4's form; the log's symmetry column), wall {wall} s = {wall / 3600:.2f} h, "
          f"sector times {min(times.values())} to {max(times.values())} s, sum {sum(times.values())} s")
    print("| m | leading μv_c (a quadruple ±a ± ib) | \\|μ\\|v_c, A | \\|μ\\|v_c, B | next \\|μ\\|v_c | stable to 10⁻⁵ above | symmetric to |")
    print("|---|---|---|---|---|---|---|")
    for m, r in rows.items():
        cand = [z for z in r["muA"][:4] if z.imag > 0 and z.real >= 0]
        z = cand[0] if cand else r["muA"][0]
        print(f"| {m:g} | {abs(z.real):.5f} + {abs(z.imag):.5f}i | {abs(r['muA'][0]):.6f} | {abs(r['muB'][0]):.6f} | "
              f"{abs(r['muA'][4]):.6f} | {sec[m]['cut']} | {sec[m]['asym']} |")
    print(f"\n== sigma R = {sig}: window table (section 5's form)")
    print("| m | window \\|μ\\|v_c ≥ | eigenvalues in it (A / B) | real in it (A / B) | real with \\|μ\\|v_c > 10⁻⁸ (A / B) | largest | "
          "reproduced by B | identity, worst | eigenfunctions (real) |")
    print("|---|---|---|---|---|---|---|---|---|")
    tot = np.zeros(4, int)
    for m, w in win.items():
        print(f"| {m:g} | {w['lo']} | {w['nwA']} / {w['nwB']} | {w['rwA']} / {w['rwB']} | {w['raA']} / {w['raB']} | {w['big']} | "
              f"{w['pers']} | {w['ident']} | {w['nef']} ({w['nreal']}) |")
        tot += [w["nwA"], w["nwB"], w["rwA"], w["rwB"]]
    ra = [w["raA"] for w in win.values()]
    rb = [w["raB"] for w in win.values()]
    print(f"\n  totals over {len(win)} sectors: eigenvalues in the windows {tot[0]} / {tot[1]}, real in the windows {tot[2]} / "
          f"{tot[3]}; real with |mu| v_c > 1e-8 per sector {min(ra)} to {max(ra)} (A) / {min(rb)} to {max(rb)} (B), the largest "
          f"{max(float(w['big']) for w in win.values()):.1e}; reproduced by B {sum(w['pers'] for w in win.values())}; "
          f"eigenfunctions per sector {min(w['nef'] for w in win.values())} to {max(w['nef'] for w in win.values())}; "
          f"worst identity {max(float(w['ident']) for w in win.values()):.1e}; real_identity eigenfunctions with a real "
          f"eigenvalue {min(w['nreal'] for w in win.values())} to {max(w['nreal'] for w in win.values())}")

print("\n== residual ||S psi - v M psi|| / ||S psi|| of the leading eigenfunctions, worst, from the two logs (data)")
print("| m | σR = 8 (P = 200) | σR = 16 (P = 340) |")
print("|---|---|---|")
for m in MS:
    print(f"| {m:g} | {data[8][3][m]} | {data[16][3][m]} |")

print()
if fails:
    print("FAILED: " + ", ".join(fails))
    sys.exit(1)
print("all checks passed")
