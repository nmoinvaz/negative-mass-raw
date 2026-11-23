"""
Coordinator's independent check of #132: F + r f' < 0 at every root r > 0 of (r f')' = 0 on the tanh wall.

Shares no code with he_tanh_bound.py (not read before writing this). Route: sympy from the tanh profile itself, and
mpmath at 50 digits from the tanh profile's own derivatives, with y = sigma r, p = sigma R_b, w = 2y, C = cosh 2p.
Usage: python ind132.py [--mutate=profile|msign|chain]

Criteria, fixed before the first run:
  C1  [tanh(y + p) - tanh(y - p)] / (2 tanh p) - (1 + C) / (cosh w + C) = 0 exactly (rewritten in exp).
  C2  With f = (1 + C)/(cosh w + C), r f' = w df/dw and (r f')' proportional to d/dw (w df/dw): the root condition is
      linear in C, it has one solution C*(w), and (F + r f')(w, C*(w)) = -w sinh w (cosh w - 1) m(w) /
      (Q (cosh w + C*)^2) exactly, with m = w (cosh w + 2) - 3 sinh w and Q = sinh w + w cosh w. Also r f' < 0 for w > 0,
      C > -1 (its sign is that of -(1 + C) w sinh w).
  C3  m > 0 on w > 0 by a route other than the series: m(0) = m'(0) = m''(0) = 0 and m''' = w sinh w exactly, so m''' > 0
      on w > 0 and m, m', m'' are increasing from 0.
  C4  For sigma R_b in {1e-3, 1e-2, 0.1, 0.5, 1, 2, 5, 10, 100}: own analytic derivatives of the tanh form agree with
      mp.diff to 1e-35 at 3 points; a scan of g(y) = f_y + y f_yy on y in [1e-6, p + 20] (4000 points, 50 digits) has
      exactly one sign change; at its refined root, r f' < 0, F + r f' < 0, and F + r f' equals C2's closed form
      within 1e-35.
  C5  At C = 1 (sigma R_b -> 0) the root of C*(w) = 1 gives F + r f' = -0.0536756031 within 1e-9 (#132's supremum).
Mutations (each must make the script exit 1):
  profile  tanh(y + p) + tanh(y - p) in C1's profile: C1 must fail.
  msign    m = w (cosh w + 2) + 3 sinh w in C2: C2 must fail.
  chain    m''' compared with w cosh w: C3 must fail.
Exit 1 if any criterion fails.
Run 1 (ind132_run1.txt) failed C2 in two ways, both in this script's code: (i) its root condition was the numerator of
d/dw (w df/dw), which carries f's positive factor (1 + C), so it had degree 2 in C; the criterion means the root
condition without that factor, as Psi = 0 is. (ii) Its zero test (expand, rewrite in exp, simplify) did not reduce the
identity to 0, while C4 confirmed it numerically at 9 values of sigma R_b to 1e-48. The code now divides out (1 + C)
(checking the remainder is 0) and tests zero by e^w = t and cancel. The criteria are unchanged.
"""
import sys, time
import sympy as sp
import mpmath as mp

mut = next((q.split('=', 1)[1] for q in sys.argv[1:] if q.startswith('--mutate=')), None)
assert mut in (None, 'profile', 'msign', 'chain')
T0 = time.time()
fails = []


def report(name, ok, detail):
    print(f"  {name}: {detail}: {'PASS' if ok else 'FAIL'}  [{time.time() - T0:.0f} s]", flush=True)
    if not ok:
        fails.append(name)


def zero(e):
    """Exact zero test: rewrite in exp, put e^w = t (and e^y, e^p = t, u), cancel the rational function."""
    e = sp.sympify(e).rewrite(sp.exp)
    e = e.subs({sp.exp(w): tt, sp.exp(y): tt, sp.exp(p): uu})
    return sp.cancel(sp.together(e)) == 0


y, p, w, C = sp.symbols('y p w C', positive=True)
tt, uu = sp.symbols('t u', positive=True)
# C1
sgn = 1 if mut == 'profile' else -1
f_tanh = (sp.tanh(y + p) + sgn * sp.tanh(y - p)) / (2 * sp.tanh(p))
f_cosh = (1 + sp.cosh(2 * p)) / (sp.cosh(2 * y) + sp.cosh(2 * p))
report("C1 profile identity", zero(f_tanh - f_cosh), "tanh form = (1 + C)/(cosh w + C) with w = 2y, C = cosh 2p")

# C2
f = (1 + C) / (sp.cosh(w) + C)
rf1 = w * sp.diff(f, w)
N0 = sp.numer(sp.together(sp.diff(rf1, w)))
N, rem = sp.div(sp.Poly(sp.expand(N0), C), sp.Poly(1 + C, C))    # f's positive factor (1 + C), as Psi excludes it
assert rem.is_zero
N = N.as_expr()
Np = sp.Poly(sp.expand(N), C)
sols = sp.solve(N, C)
m = w * (sp.cosh(w) + 2) + (3 if mut == 'msign' else -3) * sp.sinh(w)
Q = sp.sinh(w) + w * sp.cosh(w)
ok2 = Np.degree() == 1 and len(sols) == 1
if ok2:
    Cs = sols[0]
    E = (1 - f + rf1).subs(C, Cs)
    target = -w * sp.sinh(w) * (sp.cosh(w) - 1) * m / (Q * (sp.cosh(w) + Cs) ** 2)
    ok2 = zero(sp.together(E - target))
signf = sp.simplify(rf1 / (-(1 + C) * w * sp.sinh(w) / (sp.cosh(w) + C) ** 2))
ok2b = signf == 1
report("C2 elimination", ok2 and ok2b, f"degree of the root condition in C: {Np.degree()}, solutions {len(sols)}; "
       f"F + r f' at C* = -w sinh w (cosh w - 1) m / (Q (cosh w + C*)^2): {ok2}; r f' = -(1 + C) w sinh w / "
       f"(cosh w + C)^2: {ok2b}")

# C3
m0 = w * (sp.cosh(w) + 2) - 3 * sp.sinh(w)
d1, d2, d3 = sp.diff(m0, w), sp.diff(m0, w, 2), sp.diff(m0, w, 3)
want3 = w * (sp.cosh(w) if mut == 'chain' else sp.sinh(w))
ok3 = all(sp.simplify(q.subs(w, 0)) == 0 for q in (m0, d1, d2)) and zero(d3 - want3)
report("C3 m > 0 by m''' = w sinh w", ok3, f"m(0), m'(0), m''(0) = {[sp.simplify(q.subs(w, 0)) for q in (m0, d1, d2)]}; "
       f"m''' = {sp.simplify(d3)}")

# C4
mp.mp.dps = 50


def jets(yv, pv):
    tp, tm, k = mp.tanh(yv + pv), mp.tanh(yv - pv), 2 * mp.tanh(pv)
    f0 = (tp - tm) / k
    f1 = ((1 - tp ** 2) - (1 - tm ** 2)) / k
    f2 = -2 * (tp * (1 - tp ** 2) - tm * (1 - tm ** 2)) / k
    return f0, f1, f2


def closed(wv, Cv):
    mv = wv * (mp.cosh(wv) + 2) - 3 * mp.sinh(wv)
    return -wv * mp.sinh(wv) * (mp.cosh(wv) - 1) * mv / ((mp.sinh(wv) + wv * mp.cosh(wv)) * (mp.cosh(wv) + Cv) ** 2)


rows, ok4 = [], True
for pv in ['1e-3', '1e-2', '0.1', '0.5', '1', '2', '5', '10', '100']:
    pv = mp.mpf(pv)
    dd = max(abs(mp.diff(lambda t: jets(t, pv)[0], yy, k) - jets(yy, pv)[k]) for yy in (mp.mpf('0.3'), pv, pv + 1)
             for k in (1, 2))
    g = lambda t: (lambda j: j[1] + t * j[2])(jets(t, pv))
    hi = pv + 20
    ys = [mp.mpf('1e-6') + (hi - mp.mpf('1e-6')) * i / 4000 for i in range(4001)]
    gs = [g(t) for t in ys]
    br = [(ys[i], ys[i + 1]) for i in range(4000) if gs[i] * gs[i + 1] < 0]
    ok = dd < mp.mpf(10) ** -35 and len(br) == 1
    if len(br) == 1:
        yr = mp.findroot(g, br[0], solver='anderson')
        f0, f1, _ = jets(yr, pv)
        rf, E = yr * f1, 1 - f0 + yr * f1
        cl = closed(2 * yr, mp.cosh(2 * pv))
        ok = ok and rf < 0 and E < 0 and abs(E - cl) < mp.mpf(10) ** -35
        rows.append(f"p = {mp.nstr(pv, 3)}: root y = {mp.nstr(yr, 10)}, F + r f' = {mp.nstr(E, 12)} (closed form "
                    f"differs {mp.nstr(abs(E - cl), 2)}), r f' = {mp.nstr(rf, 6)}")
    else:
        rows.append(f"p = {mp.nstr(pv, 3)}: {len(br)} sign changes")
    ok4 &= ok
report("C4 roots of the tanh form", ok4, "; ".join(rows))

# C5
Cstar = sp.lambdify(w, sols[0] if sols else w, 'mpmath')
w0 = mp.findroot(lambda t: Cstar(t) - 1, mp.mpf(2))
E0 = closed(w0, mp.mpf(1))
report("C5 supremum at C = 1", abs(E0 - mp.mpf('-0.0536756031')) < 1e-9, f"w = {mp.nstr(w0, 15)}, F + r f' = {mp.nstr(E0, 15)}")
print("RESULT", "FAIL: " + ", ".join(fails) if fails else "PASS", f"[{time.time() - T0:.0f} s]")
sys.exit(1 if fails else 0)
