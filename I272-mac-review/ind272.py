#!/usr/bin/env python3
"""ind272: an independent time-domain check of #272's linear response of the Ellis throat (criteria in README.md beside this file).

    python3 ind272.py [--mutate=wrong-n|no-proj|width]

Imports nothing from the repository. Exit 1 when a check fails.
"""
import sys
import time

import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spl
from scipy.integrate import solve_ivp

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
LMAX, TMAX, DTOUT = 75.0, 30.0, 0.1
W2_195 = {2: 1.397052433715, 3: 2.984958930278}
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def background(n, l):
    sol = solve_ivp(lambda x, y: [y[1], (n - 1) * y[0] ** (1 - 2 * n)], (0.0, l[-1]), [1.0, 0.0], t_eval=l, method="Radau",
                    rtol=1e-12, atol=1e-14)
    r, rp = sol.y
    if n == 2:
        assert np.max(np.abs(r - np.sqrt(1 + l * l))) < 1e-9, "n = 2 background is not sqrt(1 + l^2)"
    return r, rp, (n - 1) * r ** (1 - 2 * n)


def operator(n, h):
    J = int(round(LMAX / h))
    l = (np.arange(J) + 0.5) * h
    r, rp, rpp = background(n, l)
    nn = n + 1 if MUT == "wrong-n" else n
    p = 2 * rpp / rp + nn * rp / r
    q = n * rp ** 2 / r ** 2 + rpp / r
    a = 1 / h ** 2 + p / (2 * h)          # coefficient of Y_{j-1}
    c = 1 / h ** 2 - p / (2 * h)          # coefficient of Y_{j+1}
    d = -2 / h ** 2 + q
    d = d.copy()
    d[0] += a[0]                          # Y_{-1} = Y_0: even about the throat
    A = sps.diags([a[1:], d, c[:-1]], [-1, 0, 1], format="csc")   # Y_J = 0 at l = LMAX
    return l, r, rp, A


def growing(A, guess):
    val, vec = spl.eigs(A, k=1, sigma=guess)
    valT, vecT = spl.eigs(A.T.tocsc(), k=1, sigma=guess)
    assert abs(val[0] - valT[0]) < 1e-8 * abs(val[0])
    return val[0].real, vec[:, 0].real, vecT[:, 0].real


def evolve(n, h):
    l, r, rp, A = operator(n, h)
    w2, v, u = growing(A, W2_195[n])
    W = np.sqrt(w2)
    width = 1.0 if MUT == "width" else 0.5
    sig = np.exp(-((l - 3.0) / width) ** 2 / 2)
    P = float(np.sum(sig * r / (rp ** 2 * r ** n)) * h)
    Y, S = np.zeros_like(l), sig.copy()
    uv = u @ v

    def project(Y, S):
        if MUT == "no-proj":
            return Y, S
        cc = u @ (S + W * Y) / (2 * W * uv)
        return Y - cc * v, S - cc * W * v

    Y, S = project(Y, S)
    dt = 0.4 * h
    every = int(round(DTOUT / dt))
    nsteps = int(round(TMAX / dt))
    ts, ys, vs = [0.0], [(9 * Y[0] - Y[1]) / 8], [(9 * S[0] - S[1]) / 8]
    AY = A @ Y
    for k in range(1, nsteps + 1):
        S = S + 0.5 * dt * AY
        Y = Y + dt * S
        AY = A @ Y
        S = S + 0.5 * dt * AY
        Y, S = project(Y, S)
        AY = A @ Y
        if k % every == 0:
            ts.append(k * dt)
            ys.append((9 * Y[0] - Y[1]) / 8)
            vs.append((9 * S[0] - S[1]) / 8)
    return w2, P, np.array(ts), np.array(ys), np.array(vs)


t0 = time.time()
RUN = {}
for n in (2, 3):
    for h in (0.01, 0.005):
        RUN[(n, h)] = evolve(n, h)
        print(f"  n = {n}, h = {h}: W^2 {RUN[(n, h)][0]:.10f}, P {RUN[(n, h)][1]:.6f} ({time.time() - t0:.0f} s)", flush=True)


def rich(n, k):
    return (4 * RUN[(n, 0.005)][k] - RUN[(n, 0.01)][k]) / 3


TS = RUN[(2, 0.005)][2]
assert np.allclose(TS, RUN[(2, 0.01)][2])
TQ = (8, 10, 12, 15, 20, 25)
idx = {t: int(round(t / DTOUT)) for t in TQ}
out = {}
for n in (2, 3):
    w2, P = rich(n, 0), rich(n, 1)
    y, v = rich(n, 3), rich(n, 4)
    rate = -np.gradient(np.log(np.abs(v)), DTOUT)
    out[n] = dict(w2=w2, P=P, y=y, v=v, rate=rate)
    print(f"  D = {n + 2}: W^2 {w2:.10f} (#195 {W2_195[n]}), P {P:.6f}")
    print("    t     Y(t,0)     v          rate      rate*t    v/P")
    for t in TQ:
        i = idx[t]
        print(f"    {t:3d}   {y[i]:.5f}   {v[i]:.3e}   {rate[i]:.4f}    {rate[i] * t:.3f}    {v[i] / P:.4f}")

k1 = {n: abs(out[n]["w2"] / W2_195[n] - 1) for n in (2, 3)}
check("K1", all(x <= 1e-5 for x in k1.values()), f"W^2 against #195: relative {k1[2]:.1e} (D = 4), {k1[3]:.1e} (D = 5); bar 1e-5")

Y4 = (0.4323, 0.4403, 0.4451, 0.4494, 0.4530, 0.4547)
R4 = (0.283, 0.245, 0.216, 0.182, 0.144, 0.119)
o = out[2]
dP = abs(o["P"] / 0.4577 - 1)
dy = max(abs(o["y"][idx[t]] / yv - 1) for t, yv in zip(TQ, Y4))
dr = max(abs(o["rate"][idx[t]] / rv - 1) for t, rv in zip(TQ, R4))
check("K2", dP <= 1e-3 and dy <= 0.01 and dr <= 0.05, f"D = 4: P {o['P']:.5f} (0.4577, {dP:.1e}); Y(t,0) worst {dy:.1e} (bar 1e-2); rate worst {dr:.1e} (bar 5e-2)")

rt = [o["rate"][idx[t]] * t for t in (15, 20, 25)]
dk3 = max(abs(a / b - 1) for a, b in zip(rt, (2.74, 2.89, 2.97)))
rise = rt[2] / rt[0] - 1
check("K3", dk3 <= 0.10 and rise < 0.15, f"D = 4: rate*t at 15, 20, 25 = {rt[0]:.3f}, {rt[1]:.3f}, {rt[2]:.3f} (worst {dk3:.1e} from the note's); rise {rise:.1%} (an exponential: 67 %)")

Y5 = (0.4088, 0.4687, 0.5258, 0.6077, 0.7367, 0.8592)
o = out[3]
dP5 = abs(o["P"] / 0.1036 - 1)
dy5 = max(abs(o["y"][idx[t]] / yv - 1) for t, yv in zip(TQ, Y5))
vp = [o["v"][idx[t]] / o["P"] for t in (10, 20)]
dv5 = max(abs(vp[0] / 0.282 - 1), abs(vp[1] / 0.242 - 1))
check("K4", dP5 <= 1e-3 and dy5 <= 0.02 and dv5 <= 0.05, f"D = 5: P {o['P']:.5f} (0.1036, {dP5:.1e}); Y(t,0) worst {dy5:.1e} (bar 2e-2); v/P at 10, 20 = {vp[0]:.4f}, {vp[1]:.4f} (worst {dv5:.1e}, bar 5e-2)")

bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}; {time.time() - t0:.0f} s", flush=True)
sys.exit(1 if bad else 0)
