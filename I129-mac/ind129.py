"""
Coordinator's independent check of #129: is D holomorphic at S12, not only arg D harmonic?

Shares no code with harm_circles.py. It reads harm_circles' caches (data: D at the 3 centres and on 64-point circles of
radius 0.05 L and 0.025 L, L = 2.5, for 4 boxes and 3 settings) and tests the complex function F = log(D / D(s0)), with
its own discrete Fourier transform on each circle, s = s0 + rho e^{i theta}:
    C_k = (1/N) sum_j F_j e^{-i k theta_j},   F_s ~ C_1 / rho,   F_sbar ~ C_{-1} / rho,   Delta F ~ 4 C_0 / rho^2.
  T1 (mean value, real and imaginary parts at once): |Delta F| L^2 <= 1e-6 (1 + |F_s| L).
     Re F = log|D| is untouched by the wrapper and was never tested by harm_circles; Im F is its arg D.
  T2 (Cauchy-Riemann, first antiholomorphic mode): |F_sbar| L <= 1e-6 (1 + |F_s| L). The cached D carries winding2's
     factor exp(-i Im H), H = (k+ + k-) R_s + s r_m, which is not holomorphic; T2 removes it with this script's own H.
     r_m comes from polar_solver.PolarProblem (the code that computes D, not the script under review); R_s from
     winding2's rule as harm_circles' docstring states it, written here.
The tolerance 1e-6 is §5.5's, applied to first derivatives in T2.
Usage: python ind129.py CACHEDIR FRESHDIR [--mutate=wrapper|harmarg|modulus]

Criteria, fixed before the first run:
  C0  Planted, at the 3 centres and both radii, through T1 and T2: g = (s - a)(s - c) e^{2s} with a = s0 + 0.8 - 0.5i,
      c = s0 - 0.6 + 0.7i passes both at <= 1e-3 of the limit; g exp(1e-3 (Re s)^2 / L^2) fails T1; g exp(i 1e-3 Re s / L)
      (a harmonic arg, not holomorphic) passes T1 at <= 1e-3 of the limit and fails T2.
  C1  S12, every box, point and radius (24 rows): T1 passes.
  C2  S12, 24 rows: T2 passes, with r_m and R_s equal to the laptop's printed values (r_m to 0.005, R_s to 0.05).
  C3  The Mac's fresh S12 values of c075_l2 point 2 (FRESHDIR) equal the laptop's at all 129 points within
      |log(D_mac / D_laptop)| <= 1e-9, and pass T1 and T2 at both radii.
  Reported only: T1 and T2 at S8 and S10; max |log(D_S8 / D_S12)| and |log(D_S10 / D_S12)| over all 12 x 129 points.
Mutations (each must make the script exit 1):
  wrapper  skip removing exp(-i Im H): C2 must fail.
  harmarg  D times exp(i 1e-3 Re s / L), which keeps arg D harmonic: C2 must fail and C1 pass.
  modulus  D times exp(1e-3 (Re s)^2 / L^2): C1 must fail.
Exit 1 if any criterion fails.
Run 1 (ind129_run1.txt) passed C0 and then stopped with an AssertionError in C1: it multiplied the cached D by
exp(+i Im H) before the logarithm, and Im H varies by about 100 rad around a circle (R_s ~ 405), so the principal log
does not apply. The log of winding2's factor is now added to the samples after the logarithm of the cached ratio, which
is the same function on a continuous branch. The criteria are unchanged.
"""
import os, sys, pickle, time
import numpy as np

CD, FD = sys.argv[1], sys.argv[2]
mut = next((q.split('=', 1)[1] for q in sys.argv[3:] if q.startswith('--mutate=')), None)
assert mut in (None, 'wrapper', 'harmarg', 'modulus')
T0 = time.time()
L, N, TOL = 2.5, 64, 1e-6
CENTRES = [0.575 + 0.75j, 1.05 + 1.5j, 1.525 + 2.25j]
RADII = (0.05 * L, 0.025 * L)
BOX = {'p7603_l2': (-1, 0.7603, 2, 24.11, 404.9), 'p7603_l3': (-1, 0.7603, 3, 24.11, 404.9),
       'c075_l2': (1, 0.75, 2, 23.76, 404.4), 'p085_l3': (-1, 0.85, 3, 27.94, 409.7)}   # eps, w, l, laptop r_m, R_s
TH = 2 * np.pi * np.arange(N) / N
fails = []


def report(name, ok, detail):
    print(f"  {name}: {detail}: {'PASS' if ok else 'FAIL'}  [{time.time() - T0:.0f} s]", flush=True)
    if not ok:
        fails.append(name)


def modes(Fc, rho):
    """C_{-1}, C_0, C_1 of the samples Fc on the circle."""
    return [np.mean(Fc * np.exp(-1j * k * TH)) for k in (-1, 0, 1)]


def tests(Fc, rho):
    cm, c0, c1 = modes(Fc, rho)
    fs = abs(c1) / rho
    lim = TOL * (1 + fs * L)
    return abs(4 * c0 / rho ** 2) * L ** 2 / lim, abs(cm / rho) * L / lim     # T1 and T2 as ratios to the limit


def circ(s0, rho):
    return s0 + rho * np.exp(1j * TH)


# C0 planted
rows0, ok0 = [], True
for s0 in CENTRES:
    a, c = s0 + 0.8 - 0.5j, s0 - 0.6 + 0.7j
    g = lambda s: (s - a) * (s - c) * np.exp(2 * s)
    for rho in RADII:
        ss = circ(s0, rho)
        F = lambda h: np.log(h(ss) / h(s0))
        t1g, t2g = tests(F(g), rho)
        t1m, _ = tests(F(lambda s: g(s) * np.exp(1e-3 * s.real ** 2 / L ** 2)), rho)
        t1h, t2h = tests(F(lambda s: g(s) * np.exp(1j * 1e-3 * s.real / L)), rho)
        ok = t1g <= 1e-3 and t2g <= 1e-3 and t1m > 1 and t1h <= 1e-3 and t2h > 1
        ok0 &= ok
        rows0.append(f"{s0} rho {rho / L} L: holo {t1g:.1e}, {t2g:.1e}; modulus T1 {t1m:.3g}; harm-arg {t1h:.1e}, T2 {t2h:.3g}")
report("C0 planted", ok0, "; ".join(rows0))

# r_m and R_s for T2
sys.path.insert(0, '/Users/nathan/Source/negative-mass/phase2/nonradial')
import background as Bg  # noqa: E402
from polar_solver import PolarProblem  # noqa: E402
geom = {}
for name, (eps, w, l, rm_lt, rs_lt) in BOX.items():
    key = (eps, w)
    if key not in geom:
        geom[key] = PolarProblem(Bg.solve_star(w, eps), 2).rm
    rm = geom[key]
    cands = np.concatenate([0.1 + 1j * np.linspace(0.0, 2.5, 200), np.linspace(0.1, 2.0, 200) + 2.5j])
    kmin = min(min(np.sqrt(1 + (z - 1j * w) ** 2).real, np.sqrt(1 + (z + 1j * w) ** 2).real) for z in cands)
    BOX[name] = (eps, w, l, rm_lt, rs_lt, rm, rm + 40.0 / kmin)
print(f"     r_m, R_s: " + "; ".join(f"{n} {v[5]:.6f}, {v[6]:.6f} (laptop {v[3]}, {v[4]})" for n, v in BOX.items()), flush=True)
geo_ok = all(abs(v[5] - v[3]) <= 0.005 and abs(v[6] - v[4]) <= 0.05 for v in BOX.values())


def Hfun(s, w, rm, Rs):
    return (np.sqrt(1 + (s - 1j * w) ** 2) + np.sqrt(1 + (s + 1j * w) ** 2)) * Rs + s * rm


def lookup(cache, i, s):
    ks = [k for k in cache if k[0] == i]
    k = min(ks, key=lambda q: abs(q[1] - s))
    assert abs(k[1] - s) < 1e-10, f"no cached value near {s}"
    return cache[k]


def Fcircle(cache, i, rho, name, unwrap=True):
    eps, w, l, _, _, rm, Rs = BOX[name]
    s0 = CENTRES[i]
    ss = circ(s0, rho)
    D = np.array([lookup(cache, i, s) for s in ss])
    D0 = lookup(cache, i, s0)
    if mut == 'harmarg':
        D = D * np.exp(1j * 1e-3 * ss.real / L); D0 = D0 * np.exp(1j * 1e-3 * s0.real / L)
    if mut == 'modulus':
        D = D * np.exp(1e-3 * ss.real ** 2 / L ** 2); D0 = D0 * np.exp(1e-3 * s0.real ** 2 / L ** 2)
    R = D / D0
    assert np.abs(np.angle(R)).max() < 2.5
    F = np.log(R)
    if unwrap and mut != 'wrapper':     # log of winding2's factor added to the samples: ~100 rad, so not inside the log
        F = F + 1j * (Hfun(ss, w, rm, Rs).imag - Hfun(s0, w, rm, Rs).imag)
    return F


def load(name, setting, d=CD):
    return pickle.load(open(os.path.join(d, f"harm_circles_{name}_{setting}.pkl"), 'rb'))


summary = {}
for setting in ('S8', 'S10', 'S12'):
    t1max, t2max, rows = 0.0, 0.0, []
    for name in BOX:
        cache = load(name, setting)
        for i in range(3):
            for rho in RADII:
                t1, t2 = tests(Fcircle(cache, i, rho, name), rho)
                t1max, t2max = max(t1max, t1), max(t2max, t2)
                rows.append((name, i, rho / L, t1, t2))
    summary[setting] = (t1max, t2max, rows)
    nf1 = sum(r[3] > 1 for r in rows); nf2 = sum(r[4] > 1 for r in rows)
    print(f"     {setting}: T1 max ratio {t1max:.3g} ({nf1} of 24 fail), T2 max ratio {t2max:.3g} ({nf2} of 24 fail)", flush=True)
r12 = summary['S12'][2]
report("C1 S12 mean value of log D", all(r[3] <= 1 for r in r12), f"max ratio {summary['S12'][0]:.3g} over 24 rows")
report("C2 S12 Cauchy-Riemann", geo_ok and all(r[4] <= 1 for r in r12),
       f"r_m, R_s match the laptop: {geo_ok}; max ratio {summary['S12'][1]:.3g} over 24 rows; worst "
       f"{max(r12, key=lambda r: r[4])[:3]}")

# reported: direct error of S8 and S10 against S12
for setting in ('S8', 'S10'):
    worst = 0.0
    for name in BOX:
        a_, b_ = load(name, setting), load(name, 'S12')
        for k, v in b_.items():
            if k in a_:
                worst = max(worst, abs(np.log(a_[k] / v)))
    print(f"     max |log(D_{setting} / D_S12)| over all cached points: {worst:.3e}", flush=True)

# C3 the Mac's fresh S12 values
try:
    fr, lt = load('c075_l2', 'S12', FD), load('c075_l2', 'S12')
    diffs = [abs(np.log(v / lookup(lt, 2, k[1]))) for k, v in fr.items() if k[0] == 2]
    t3 = [tests(Fcircle(fr, 2, rho, 'c075_l2'), rho) for rho in RADII]
    ok3 = len(diffs) == 129 and max(diffs) <= 1e-9 and all(a <= 1 and b <= 1 for a, b in t3)
    det3 = (f"{len(diffs)} points, max |log(D_mac / D_laptop)| = {max(diffs):.3e}; T1, T2 ratios "
            f"{[(f'{a:.3g}', f'{b:.3g}') for a, b in t3]}")
except Exception as ex:  # noqa: BLE001
    ok3, det3 = False, f"raised {type(ex).__name__}: {ex}"
report("C3 Mac re-solve of c075_l2 point 2", ok3, det3)
print("RESULT", "FAIL: " + ", ".join(fails) if fails else "PASS", f"[{time.time() - T0:.0f} s]")
sys.exit(1 if fails else 0)
