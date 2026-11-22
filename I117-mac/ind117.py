"""
Coordinator's independent check of #117's box b25_l2 (eps = -1, omega = 0.7603, l = 2, Re s in [2, 5], |Im s| <= 10).

Shares no code with winding2.py, zerilli_zeros.py or collect_i117.py. It imports background.solve_star and
polar_solver.PolarProblem.D, the object under test, and rebuilds winding2's R_s rule (r_m + 40 / min Re k on the contour)
and its zero-free phase factor exp(-i Im[(k+ + k-)(R_s - r_m) + (k+ + k- + s) r_m]) from winding2.py's definitions.
Unlike winding2 it walks the FULL rectangle, lower half included (no doubling), with its own refinement rule, and plants
its own zeros and a pole.

Usage: python ind117.py [--mutate=reverse|noplant]

Criteria, fixed before the first run:
  C1  winding of D on the full rectangle, counterclockwise, within 0.05 of 0, with every phase step <= 0.3 rad after
      refinement (refinement bisects any step above 0.3 rad of D or of the planted products; segment floor 1e-4).
  C2  guard: every final segment is bisected once more; for each, |step - (half1 + half2)| < 0.1 rad.
  C3  planted zeros: D (s - a)(s - b), a = 3.7 + 6.3i, b = 3.0 - 3.1i, winding within 0.05 of +2.
  C4  planted pole: D / (s - c), c = 4.0 + 8.0i, winding within 0.05 of -1.
  Reported, no criterion: min |D| on the contour, the number of evaluations, D(2) and D(5) against the runner's
      w_b25_l2 values (-1.773e-03, -1.895e-04), and max |D(conj s) - conj D(s)| / |D(s)| over mirrored samples.
Mutations (each must make the script exit 1):
  reverse  walk the rectangle clockwise: C3 and C4 must fail.
  noplant  the planted factor of C3 replaced by 1: C3 must fail.
Exit 1 if any criterion fails.
"""
import os, sys, pickle, time
import numpy as np
NR = '/Users/nathan/Source/negative-mass/phase2/nonradial'
sys.path.insert(0, NR)
import background as B
from polar_solver import PolarProblem

EPS, W, L = -1, 0.7603, 2
X0, X1, Y = 2.0, 5.0, 10.0
A, Bz, C = 3.7 + 6.3j, 3.0 - 3.1j, 4.0 + 8.0j
STEP, GUARD, FLOOR = 0.3, 0.1, 1e-4
mut = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--mutate=')), None)
assert mut in (None, 'reverse', 'noplant')
HERE = os.path.dirname(os.path.abspath(__file__))

star = B.solve_star(W, EPS)
P = PolarProblem(star, L, rtol=1e-8)
kpm = lambda s: (np.sqrt(1 + (s - 1j * W) ** 2), np.sqrt(1 + (s + 1j * W) ** 2))
corners = [complex(X1, -Y), complex(X1, Y), complex(X0, Y), complex(X0, -Y)]   # counterclockwise
edges = [(corners[i], corners[(i + 1) % 4]) for i in range(4)]
P.Rs_fixed = P.rm + 40.0 / min(min(k.real for k in kpm(a + (b - a) * t)) for a, b in edges for t in np.linspace(0, 1, 400))

cf = os.path.join(HERE, "ind117_cache.pkl")
cache = pickle.load(open(cf, 'rb')) if os.path.exists(cf) else {}
nnew = [0]


def D(s):
    key = complex(round(s.real, 12), round(s.imag, 12))
    if key not in cache:
        a, b = kpm(key)
        cache[key] = P.D(key) * np.exp(-1j * ((a + b) * (P.Rs_fixed - P.rm) + (a + b + key) * P.rm).imag)
        nnew[0] += 1
        if nnew[0] % 10 == 0:
            pickle.dump(cache, open(cf + '.tmp', 'wb')); os.replace(cf + '.tmp', cf)
    return cache[key]


plant = (lambda s: 1.0) if mut == 'noplant' else (lambda s: (s - A) * (s - Bz))
pole = lambda s: 1.0 / (s - C)
funcs = [lambda s: D(s), lambda s: D(s) * plant(s), lambda s: D(s) * pole(s)]
step = lambda f, z0, z1: np.angle(f(z1) / f(z0))

pts = []
for a, b in edges:
    n = max(2, int(round(abs(b - a) / 0.5)))
    pts += [a + (b - a) * k / n for k in range(n)]
if mut == 'reverse':
    pts = pts[::-1]
pts.append(pts[0])

t0 = time.time()
unresolved = False
i = 0
while i < len(pts) - 1:
    z0, z1 = pts[i], pts[i + 1]
    if max(abs(step(f, z0, z1)) for f in funcs) > STEP:
        if abs(z1 - z0) < FLOOR:
            unresolved = True; i += 1; continue
        pts.insert(i + 1, (z0 + z1) / 2); continue
    i += 1
segs = list(zip(pts[:-1], pts[1:]))
wind = [sum(step(f, z0, z1) for z0, z1 in segs) / (2 * np.pi) for f in funcs]
maxstep = max(abs(step(funcs[0], z0, z1)) for z0, z1 in segs)
gdef = max(abs(step(f, z0, z1) - step(f, z0, (z0 + z1) / 2) - step(f, (z0 + z1) / 2, z1)) for f in funcs for z0, z1 in segs)
pickle.dump(cache, open(cf + '.tmp', 'wb')); os.replace(cf + '.tmp', cf)

c1 = abs(wind[0]) < 0.05 and maxstep <= STEP and not unresolved
c2 = gdef < GUARD
c3 = abs(wind[1] - 2) < 0.05
c4 = abs(wind[2] + 1) < 0.05
print(f"# ind117 b25_l2 (eps {EPS:+d}, w {W}, l {L}), full rectangle Re s in [{X0}, {X1}], Im s in [-{Y}, {Y}], "
      f"R_s = {P.Rs_fixed:.2f}, r_m = {P.rm:.2f}" + (f", mutate={mut}" if mut else ""))
print(f"C1 winding of D {wind[0]:+.4f}, max step {maxstep:.3f} rad, {len(segs)} segments, unresolved {unresolved}: {'PASS' if c1 else 'FAIL'}")
print(f"C2 guard: max |step - (half1 + half2)| = {gdef:.2e} rad: {'PASS' if c2 else 'FAIL'}")
print(f"C3 planted zeros {A}, {Bz}: winding {wind[1]:+.4f} (expect +2): {'PASS' if c3 else 'FAIL'}")
print(f"C4 planted pole {C}: winding {wind[2]:+.4f} (expect -1): {'PASS' if c4 else 'FAIL'}")
mind = min(abs(D(z)) for z, _ in segs)
d2, d5 = D(complex(X0, 0)), D(complex(X1, 0))
mir = [abs(D(z.conjugate()) - np.conj(D(z))) / abs(D(z)) for z in list(cache) if z.conjugate() in cache and z.imag > 0]
print(f"reported: min |D| {mind:.3e}; D(2) = {d2:.4e} (runner -1.773e-03), D(5) = {d5:.4e} (runner -1.895e-04); "
      f"mirror defect max {max(mir) if mir else float('nan'):.2e} over {len(mir)} pairs; {len(cache)} cached points, "
      f"{nnew[0]} new, {time.time() - t0:.0f} s")
fails = [n for n, ok in (('C1', c1), ('C2', c2), ('C3', c3), ('C4', c4)) if not ok]
print("RESULT", "FAIL: " + ", ".join(fails) if fails else "PASS")
sys.exit(1 if fails else 0)
