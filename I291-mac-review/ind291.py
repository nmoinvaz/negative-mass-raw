#!/usr/bin/env python3
"""ind291: the ensemble slope of G's throat speed at D = 4, B = 0.02 from #291's raw pairs (criteria in README.md beside this file).

    python3 ind291.py [--mutate=one-member|t-not-tau|wide]

Imports nothing from the repository. Exit 1 when a check fails.
"""
import os
import sys

import numpy as np

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
RAW = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "I291-mac")
HW = 1.0 if MUT == "wide" else 0.25
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def member(h, k):
    base = "runs" if k == 0 else f"runs_k{k}"
    z = np.load(os.path.join(RAW, base, "G_B0.02", f"h{h:g}", "e12", "member", "locus.npz"))
    sa, sb = z["s_a"].tolist(), z["s_b"].tolist()
    ia, ib = {s: i for i, s in enumerate(sa)}, {s: i for i, s in enumerate(sb)}
    com = sorted(set(sa) & set(sb))
    A = np.array([ia[s] for s in com]); B = np.array([ib[s] for s in com])
    t = 0.5 * (z["t_a"][A] + z["t_b"][B])
    tau = 0.5 * (z["tau_a"][A] + z["tau_b"][B])
    r = 0.5 * (z["r_a"][A] + z["r_b"][B])
    return t, tau, r


def ensemble(h):
    ks = [0] if MUT == "one-member" else range(8)
    mem = [member(h, k) for k in ks]
    t0 = max(m[0][0] for m in mem); t1 = min(m[0][-1] for m in mem)
    grid = mem[0][0][(mem[0][0] >= t0) & (mem[0][0] <= t1)]
    r = np.mean([np.interp(grid, m[0], m[2]) for m in mem], axis=0)
    tau = np.mean([np.interp(grid, m[0], m[1]) for m in mem], axis=0)
    return grid, tau, r


def speed(tau, r, tq):
    sel = np.abs(tau - tq) <= HW
    c2, c1, _ = np.polyfit(tau[sel] - tq, r[sel], 2)
    return c1


out = {}
for h in (0.01, 0.005):
    t, tau, r = ensemble(h)
    ts = np.arange(9.0, 18.21, 0.05)
    ts = ts[ts <= t[-1] - HW - 0.05]
    taus = np.interp(ts, t, tau)
    v = np.array([speed(tau, r, tq) for tq in taus])
    win = (ts >= 15.0) & (ts <= 18.2)
    x = np.log(ts[win] if MUT == "t-not-tau" else taus[win])
    p = np.polyfit(x, np.log(np.abs(v[win])), 1)[0]
    lnv = np.log(np.abs(v))
    rate = -np.gradient(lnv, ts)
    rt = [float(np.interp(tq, ts, rate) * tq) for tq in (10.0, 13.0, 16.0)]
    out[h] = dict(p=p, rt=rt, tend=ts[win][-1])
    print(f"  h = {h}: t up to {t[-1]:.2f}; window [15, {ts[win][-1]:.2f}] ({win.sum()} samples); slope {p:+.4f}; rate x t at 10, 13, 16 = "
          + ", ".join(f"{x_:.3f}" for x_ in rt) + f"; v(15) {np.interp(15.0, ts, v):+.3e}")

NOTE_P = {0.01: -2.413, 0.005: -2.304}
dp = max(abs(out[h]["p"] - NOTE_P[h]) for h in out)
check("K1", dp <= 0.05, f"slope against the note's -2.413, -2.304: worst {dp:.3f} (bar 0.05)")
NOTE_RT = (2.11, 2.23, 2.32)
drt = max(abs(a - b) for h in out for a, b in zip(out[h]["rt"], NOTE_RT))
spread = max((max(out[h]["rt"]) - min(out[h]["rt"])) / np.mean(out[h]["rt"]) for h in out)
check("K2", drt <= 0.05 and spread < 0.231, f"rate x t worst {drt:.3f} from 2.11, 2.23, 2.32 (bar 0.05); spread over the mean {spread:.1%} (bar 23.1 %)")
s1 = {h: abs(out[h]["p"] + 2.9) <= 0.58 for h in out}
check("K3", True, "S1 with this estimator: " + ", ".join(f"h = {h}: {out[h]['p']:+.3f} {'met' if s1[h] else 'not met'}" for h in out) + " (reported, not gated)")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)
