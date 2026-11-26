"""Diagnostic for ind168 run 1's K10 (c) failure: the same integration in (G, p) at several steps, and in (ln G, ln p)."""
import math
import sys
import numpy as np


def cubic(Gv, pv, nv):
    s = nv * nv; b = Gv * Gv * s; kap = 1 - b + s; mu = 1 + 3 * s - b + 2 * s * s - 6 * b * s; c = 1 + 2 * s
    return [-2 * Gv * s * kap, -pv * (2 * Gv * (Gv * Gv - 1) * s * s + pv * mu), 4 * Gv * s * c * pv**4,
            pv**4 * (c * c * pv * pv - 4 * Gv * Gv * s * s)]


def huge(Gv, pv, nv):
    rts = np.roots(cubic(Gv, pv, nv))
    real = [z.real for z in rts if abs(z.imag) <= 1e-9 * max(1.0, abs(z))]
    return min(real, key=lambda z: z / pv**2)


def run(h, logvars):
    G0, z0, u0 = 1.0, 0.25, 1e-3
    s0 = u0 / 2; t0 = -0.5 * math.log(s0); p0 = s0 * G0 * (4 + z0); ub = math.exp(4.5 * s0) * u0
    n = int(round(10 / h)); worst = 0.0
    if logvars:
        X = np.array([math.log(G0), math.log(p0)])
        f = lambda t, X: np.array([math.exp(X[1] - X[0]), huge(math.exp(X[0]), math.exp(X[1]), math.exp(-t)) / math.exp(X[1])])
    else:
        X = np.array([G0, p0])
        f = lambda t, X: np.array([X[1], huge(X[0], X[1], math.exp(-t))])
    t = t0
    for i in range(n):
        k1 = f(t, X); k2 = f(t + h / 2, X + h / 2 * k1); k3 = f(t + h / 2, X + h / 2 * k2); k4 = f(t + h, X + h * k3)
        X = X + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t = t0 + (i + 1) * h
        tau = t - t0
        if logvars:
            y = math.exp(X[1] + 2 * t - X[0])
        else:
            y = X[1] / (math.exp(-2 * t) * X[0])
        zeta = y - 4
        bc = 1.14 * (z0 + 50 * ub * tau) * math.exp(-2 * tau)
        worst = max(worst, abs(zeta) / bc)
    return zeta, worst


for logvars in (False, True):
    for h in (1 / 100, 1 / 200, 1 / 400, 1 / 800):
        z, w = run(h, logvars)
        print(f"{'(ln G, ln p)' if logvars else '(G, p)'}  h = 1/{round(1 / h)}: zeta(tau = 10) = {z:.6e}, "
              f"largest |zeta|/bound(c) = {w:.4f}", flush=True)
