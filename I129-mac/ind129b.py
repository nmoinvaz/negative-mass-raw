"""
Coordinator's second independent check of #129: is arg D harmonic at S12? (arg D only)

ind129.py tested D for holomorphy through log|D| and a Cauchy-Riemann mode, and its C1-C3 failed at every setting by
the same 9.9e3 of the limit. polar_solver.PolarProblem.D is the determinant of orthonormalised planes times the exact
phase of the holomorphic determinant, so only arg D is the arg of an analytic function, and |D| is not; that premise
of ind129 was wrong, and its failures stand as recorded. This check tests arg D alone.

Shares no code with harm_circles.py or ind129.py's test functions; it reads harm_circles' caches (data). For phi =
arg(D / D(s0)) on the 64-point circles of radius rho1 = 0.05 L and rho2 = 0.025 L (L = 2.5):
  T1  C_0 of phi by this script's DFT, lap1 = 4 C_0 / rho^2, |grad phi| = |C_1| ... from the first mode (2 |C_1| / rho),
      pass iff |lap1| L^2 <= 1e-6 (1 + |grad phi| L), per radius (§5.5's criterion).
  TR  the two-radius estimate that removes the rho^4 term of the circle mean, m(rho) = lap rho^2 / 4 + b rho^4:
      lap_R = 4 (m1 rho2^4 - m2 rho1^4) / (rho1^2 rho2^2 (rho2^2 - rho1^2)), same criterion with |grad phi| at rho2.
Usage: python ind129b.py CACHEDIR FRESHDIR [--mutate=nonholo|half]

Criteria, fixed before the first run:
  C0  Planted at the 3 centres: g = (s - a)(s - c) e^{2s}, a = s0 + 0.8 - 0.5i, c = s0 - 0.6 + 0.7i, passes T1 (both
      radii) and TR at <= 1e-3 of the limit; g exp(i 1e-3 (Re s)^2 / L^2) fails T1 at both radii and TR.
  C1  S12, every box, point and radius (24 rows): T1 passes.
  C2  S12, every box and point (12 rows): TR passes.
  C3  The Mac's fresh S12 values of c075_l2 point 2 agree with the laptop's at all 129 points within
      |arg(D_mac / D_laptop)| <= 1e-9, and pass T1 at both radii and TR.
  Reported only: T1 and TR at S8 and S10; T1 applied to log|D| at S12 (ind129's failure); max |arg(D_S8 / D_S12)| and
  max |arg(D_S10 / D_S12)| over all cached points.
Mutations (each must make the script exit 1):
  nonholo  D times exp(i 1e-3 (Re s)^2 / L^2): C1 and C2 must fail.
  half     the circle mean over the first half of the circle only: C0 must fail.
Exit 1 if any criterion fails.
"""
import os, sys, pickle, time
import numpy as np

CD, FD = sys.argv[1], sys.argv[2]
mut = next((q.split('=', 1)[1] for q in sys.argv[3:] if q.startswith('--mutate=')), None)
assert mut in (None, 'nonholo', 'half')
T0 = time.time()
L, N, TOL = 2.5, 64, 1e-6
CENTRES = [0.575 + 0.75j, 1.05 + 1.5j, 1.525 + 2.25j]
R1, R2 = 0.05 * L, 0.025 * L
BOXES = ['p7603_l2', 'p7603_l3', 'c075_l2', 'p085_l3']
TH = 2 * np.pi * np.arange(N) / N
fails = []


def report(name, ok, detail):
    print(f"  {name}: {detail}: {'PASS' if ok else 'FAIL'}  [{time.time() - T0:.0f} s]", flush=True)
    if not ok:
        fails.append(name)


def c0c1(ph):
    sel = slice(0, N // 2) if mut == 'half' else slice(None)
    return np.mean(ph[sel]), np.mean(ph * np.exp(-1j * TH))


def t1(ph, rho):
    m, c1 = c0c1(ph)
    grad = 2 * abs(c1) / rho
    return abs(4 * m / rho ** 2) * L ** 2 / (TOL * (1 + grad * L))


def tr(ph1, ph2):
    m1, _ = c0c1(ph1)
    m2, c1 = c0c1(ph2)
    lap = 4 * (m1 * R2 ** 4 - m2 * R1 ** 4) / (R1 ** 2 * R2 ** 2 * (R2 ** 2 - R1 ** 2))
    grad = 2 * abs(c1) / R2
    return abs(lap) * L ** 2 / (TOL * (1 + grad * L))


def circ(s0, rho):
    return s0 + rho * np.exp(1j * TH)


def arg_ratio(f, s0, rho):
    ph = np.angle(f(circ(s0, rho)) / f(s0))
    assert np.abs(ph).max() < 2.5
    return ph


rows0, ok0 = [], True
for s0 in CENTRES:
    a, c = s0 + 0.8 - 0.5j, s0 - 0.6 + 0.7j
    g = lambda s: (s - a) * (s - c) * np.exp(2 * s)
    b = lambda s: g(s) * np.exp(1j * 1e-3 * np.real(s) ** 2 / L ** 2)
    gs = [t1(arg_ratio(g, s0, r), r) for r in (R1, R2)] + [tr(arg_ratio(g, s0, R1), arg_ratio(g, s0, R2))]
    bs = [t1(arg_ratio(b, s0, r), r) for r in (R1, R2)] + [tr(arg_ratio(b, s0, R1), arg_ratio(b, s0, R2))]
    ok = max(gs) <= 1e-3 and min(bs) > 1
    ok0 &= ok
    rows0.append(f"{s0}: holo {max(gs):.1e}, non-harmonic min {min(bs):.3g}")
report("C0 planted", ok0, "; ".join(rows0))


def lookup(cache, i, s):
    k = min((q for q in cache if q[0] == i), key=lambda q: abs(q[1] - s))
    assert abs(k[1] - s) < 1e-10
    v = cache[k]
    return v * np.exp(1j * 1e-3 * s.real ** 2 / L ** 2) if mut == 'nonholo' else v


def fcache(cache, i):
    return np.vectorize(lambda s: lookup(cache, i, complex(s)), otypes=[complex])


def load(name, setting, d=CD):
    return pickle.load(open(os.path.join(d, f"harm_circles_{name}_{setting}.pkl"), 'rb'))


res = {}
for setting in ('S8', 'S10', 'S12'):
    r1, rr, rmod = [], [], []
    for name in BOXES:
        cache = load(name, setting)
        for i, s0 in enumerate(CENTRES):
            f = fcache(cache, i)
            p1, p2 = arg_ratio(f, s0, R1), arg_ratio(f, s0, R2)
            r1 += [t1(p1, R1), t1(p2, R2)]
            rr.append(tr(p1, p2))
            if setting == 'S12':
                for rho in (R1, R2):
                    lm = np.log(np.abs(f(circ(s0, rho)) / f(s0)))
                    rmod.append(t1(lm, rho))
    res[setting] = (r1, rr, rmod)
    print(f"     {setting}: T1 max {max(r1):.3g} ({sum(x > 1 for x in r1)} of 24 fail), TR max {max(rr):.3g} "
          f"({sum(x > 1 for x in rr)} of 12 fail)" + (f"; T1 on log|D| max {max(rmod):.3g}, min {min(rmod):.3g}"
                                                       if rmod else ""), flush=True)
report("C1 S12 T1", all(x <= 1 for x in res['S12'][0]), f"max {max(res['S12'][0]):.3g} over 24 rows")
report("C2 S12 TR", all(x <= 1 for x in res['S12'][1]), f"max {max(res['S12'][1]):.3g} over 12 rows")
for setting in ('S8', 'S10'):
    worst = 0.0
    for name in BOXES:
        a_, b_ = load(name, setting), load(name, 'S12')
        worst = max([worst] + [abs(np.angle(a_[k] / v)) for k, v in b_.items() if k in a_])
    print(f"     max |arg(D_{setting} / D_S12)| over all cached points: {worst:.3e} rad", flush=True)
try:
    fr, lt = load('c075_l2', 'S12', FD), load('c075_l2', 'S12')
    d = [abs(np.angle(v / lt[min((q for q in lt if q[0] == 2), key=lambda q: abs(q[1] - k[1]))])) for k, v in fr.items()
         if k[0] == 2]
    f = fcache(fr, 2)
    p1, p2 = arg_ratio(f, CENTRES[2], R1), arg_ratio(f, CENTRES[2], R2)
    v3 = [t1(p1, R1), t1(p2, R2), tr(p1, p2)]
    ok3 = len(d) == 129 and max(d) <= 1e-9 and max(v3) <= 1
    det3 = f"{len(d)} points, max |arg(D_mac / D_laptop)| = {max(d):.3e}; T1, T1, TR = {[f'{x:.3g}' for x in v3]}"
except Exception as ex:  # noqa: BLE001
    ok3, det3 = False, f"raised {type(ex).__name__}: {ex}"
report("C3 Mac re-solve of c075_l2 point 2", ok3, det3)
print("RESULT", "FAIL: " + ", ".join(fails) if fails else "PASS", f"[{time.time() - T0:.0f} s]")
sys.exit(1 if fails else 0)
