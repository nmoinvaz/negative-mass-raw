"""
Coordinator's independent check of #8: the reduced polar system y' = J y (polar_matrix_generated.J_and_h, the object
under test) solves the (tt) equation and the angular trace of G_ab = 8 pi eps T_ab, re-derived here from scratch.

Shares no code with derive_nonradial.py, lincommon.py, reduce_polar.py, verify_polar*.py or polar_eqs.pkl. Its own
linearization: background g0 = diag(-al^2, aa^2, r^2, r^2 sin^2), polar perturbation in Regge-Wheeler gauge with
H2 = H0, h_tt = al^2 H0 Y e^{st}, h_tr = H1 Y e^{st}, h_rr = aa^2 H0 Y e^{st}, h_AB = r^2 K Y e^{st} Omega_AB, and
Phi = (p0 + e (F + i G) Y e^{st}) e^{-i w t} with F, G, s real (an identity in real s holds for complex s, J being
polynomial in s). T_ab = Re(d_a Phi* d_b Phi) - g_ab [ g^cd Re(d_c Phi* d_d Phi) / 2 + V(|Phi|^2) ],
V(x) = x/2 - Lam x^2/4 + mu x^3/6, KG: Box Phi = (1 - Lam |Phi|^2 + mu |Phi|^4) Phi (derive_nonradial.py's
docstring conventions). Y = P_l(cos theta) explicit, l = 2 and 3. delta Gamma and delta R_ab by the standard
first-order formulas; the background ODEs al', aa' (from E_tt, E_rr) and p0'' (KG) are solved here.

At each point every input is a random rational, pi included (pi enters only as the coupling 8 pi, in J as in
G_ab = 8 pi eps T_ab, so an identity for every value of that coupling holds for pi). J, J', h, h', h'' come from
running J_and_h's source on order-2 Taylor series in r with Fraction coefficients; floats in the generated source
(the exponent -1.0 and the quotient 1/3) are converted to exact fractions, and each conversion is logged.

Criteria, fixed before the first run:
  C0  separation: E_tt^(1) / (Y e^{st}) and the angular trace / (Y e^{st}) take the same value at cos theta = 3/5
      and 5/13 at every point; and the background E_thth^(0) is exactly 0 at every point (my own Bianchi control).
  C1  E_tt^(1) is exactly 0 at all 6 points (l = 2 at three, l = 3 at three; eps = +1, -1 alternating).
  C2  the angular trace E_thth^(1) + E_phph^(1)/sin^2 is exactly 0 at all 6 points.
Mutations (each must make the script exit 1):
  coef   J[0][0] scaled by 8/7;  eps   the coupling 8 pi eps T_ab with eps flipped in this derivation only;
  nojp   y'' = J y' (the J' y term dropped).
Exit 1 if any criterion fails.
Run 1 (ind8_run1.txt) failed C1 and C2 at every point because of a harness bug: the perturbation values were never
substituted (the printed residuals still contain F_0, H0_0, K_1, ...). The substitution was added; criteria unchanged.
"""
import os, sys, ast, random, time
from fractions import Fraction as Fr
import sympy as sp

NR = '/Users/nathan/Source/negative-mass/phase2/nonradial'
mut = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--mutate=')), None)
assert mut in (None, 'coef', 'eps', 'nojp')
T0 = time.time()

# ------------------------------------------------------------------ own linearization
t, r, th, ph = sp.symbols('t r theta phi', real=True)
s, w, eps, Lam, mu, PI = sp.symbols('s omega epsilon Lambda mu PI', real=True)
lsym = sp.Symbol('l', integer=True)
al, aa, p0 = [sp.Function(n)(r) for n in ('al', 'aa', 'p0')]
H0, H1, K, F, G = [sp.Function(n)(r) for n in ('H0', 'H1', 'K', 'F', 'G')]
X = [t, r, th, ph]


def equations(l):
    Y = sp.legendre(l, sp.cos(th))
    E = sp.exp(s * t)
    g0 = sp.diag(-al ** 2, aa ** 2, r ** 2, r ** 2 * sp.sin(th) ** 2)
    h = sp.zeros(4, 4)
    h[0, 0] = al ** 2 * H0 * Y * E; h[0, 1] = h[1, 0] = H1 * Y * E; h[1, 1] = aa ** 2 * H0 * Y * E
    h[2, 2] = r ** 2 * K * Y * E; h[3, 3] = r ** 2 * sp.sin(th) ** 2 * K * Y * E
    gi = g0.inv()
    G0 = [[[sum(gi[a, d] * (sp.diff(g0[d, c], X[b]) + sp.diff(g0[d, b], X[c]) - sp.diff(g0[b, c], X[d])) for d in range(4)) / 2
            for c in range(4)] for b in range(4)] for a in range(4)]
    dG = [[[sum(gi[a, d] * (sp.diff(h[d, c], X[b]) + sp.diff(h[d, b], X[c]) - sp.diff(h[b, c], X[d])) for d in range(4)) / 2
            - sum(gi[a, d] * h[d, e] * G0[e][b][c] for d in range(4) for e in range(4))
            for c in range(4)] for b in range(4)] for a in range(4)]

    def ric(Ga, comp):
        a, b = comp
        return (sum(sp.diff(Ga[c][a][b], X[c]) for c in range(4)) - sum(sp.diff(Ga[c][a][c], X[b]) for c in range(4))
                + sum(Ga[c][c][d] * Ga[d][a][b] - Ga[c][b][d] * Ga[d][a][c] for c in range(4) for d in range(4)))

    def dric(comp):
        a, b = comp
        return (sum(sp.diff(dG[c][a][b], X[c]) for c in range(4)) - sum(sp.diff(dG[c][a][c], X[b]) for c in range(4))
                + sum(dG[c][c][d] * G0[d][a][b] + G0[c][c][d] * dG[d][a][b] - dG[c][b][d] * G0[d][a][c]
                      - G0[c][b][d] * dG[d][a][c] for c in range(4) for d in range(4)))
    comps = [(0, 0), (1, 1), (2, 2), (3, 3)]
    R0 = {cp: sp.simplify(ric(G0, cp)) for cp in comps}
    R0s = sum(gi[a, a] * R0[(a, a)] for a in range(4))                     # g0 diagonal
    dRc = {cp: dric(cp) for cp in comps}
    hup = gi * h * gi
    dRs = sum(gi[a, a] * dRc[(a, a)] for a in range(4)) - sum(hup[a, a] * R0[(a, a)] for a in range(4))   # R0_ab diagonal
    G0e = {cp: R0[cp] - g0[cp] * R0s / 2 for cp in comps}
    dGe = {cp: dRc[cp] - h[cp] * R0s / 2 - g0[cp] * dRs / 2 for cp in comps}
    # scalar stress tensor, linearized by d/de at e = 0
    e = sp.Symbol('e')
    Phi = (p0 + e * (F + sp.I * G) * Y * E) * sp.exp(-sp.I * w * t)
    Phc = (p0 + e * (F - sp.I * G) * Y * E) * sp.exp(sp.I * w * t)
    g = g0 + e * h; gie = gi - e * gi * h * gi
    S = lambda a, b: (sp.diff(Phc, X[a]) * sp.diff(Phi, X[b]) + sp.diff(Phi, X[a]) * sp.diff(Phc, X[b])) / 2
    x = Phc * Phi
    Vx = x / 2 - Lam * x ** 2 / 4 + mu * x ** 3 / 6
    tr = sum(gie[c, d] * S(c, d) for c in range(4) for d in range(4))
    Tf = lambda a, b: S(a, b) - g[a, b] * (tr / 2 + Vx)
    k = -1 if mut == 'eps' else 1
    out = {}
    for cp in comps:
        Tab = Tf(*cp)
        T0_ = sp.simplify(Tab.subs(e, 0))
        T1_ = sp.diff(Tab, e).subs(e, 0)
        out[cp] = (G0e[cp] - 8 * PI * k * eps * T0_, dGe[cp] - 8 * PI * k * eps * T1_)
    sqg = al * aa * r ** 2 * sp.sin(th)
    p0f = p0 * sp.exp(-sp.I * w * t)
    box = sum(sp.diff(sqg * gi[a, a] * sp.diff(p0f, X[a]), X[a]) for a in range(4)) / sqg
    kg = sp.simplify((box - (1 - Lam * p0 ** 2 + mu * p0 ** 4) * p0f) * sp.exp(sp.I * w * t))
    return out, kg, Y, E


print("# ind8: own linearization of G_ab - 8 pi eps T_ab for the polar ansatz" + (f", mutate={mut}" if mut else ""), flush=True)
EQ = {}
for l in (2, 3):
    out, kg, Y, E = equations(l)
    EQ[l] = (out, kg, Y, E)
    print(f"  l = {l}: linearized, {time.time() - T0:.0f} s", flush=True)

# background ODEs from l = 2's zeroth order (independent of l)
out, kg, _, _ = EQ[2]
d1 = {sp.diff(al, r): sp.Symbol('dal'), sp.diff(aa, r): sp.Symbol('daa')}
Ett0 = out[(0, 0)][0]; Err0 = out[(1, 1)][0]
sol = sp.solve([Ett0, Err0], [sp.diff(al, r), sp.diff(aa, r)], dict=True)
assert len(sol) == 1, sol
dal_e, daa_e = sp.simplify(sol[0][sp.diff(al, r)]), sp.simplify(sol[0][sp.diff(aa, r)])
dd = sp.solve(kg, sp.diff(p0, r, 2))
assert len(dd) == 1
ddp_e = sp.simplify(dd[0].subs({sp.diff(al, r): dal_e, sp.diff(aa, r): daa_e}))
print(f"  background: al' and aa' from E_tt, E_rr; p0'' from KG ({time.time() - T0:.0f} s)", flush=True)
# second derivatives along the background
def along(expr):
    d = sp.diff(expr, r)
    return d.subs({sp.diff(p0, r, 2): ddp_e}).subs({sp.diff(al, r): dal_e, sp.diff(aa, r): daa_e})
dal2, daa2, ddp3 = along(dal_e), along(daa_e), along(ddp_e)

# ------------------------------------------------------------------ J_and_h on Taylor series
class TS:
    """a0 + a1 t + a2 t^2 with Fraction coefficients, truncated at t^2"""
    def __init__(self, c):
        self.c = tuple(Fr(v) for v in c)
    @staticmethod
    def lift(x):
        return x if isinstance(x, TS) else TS((num(x), 0, 0))
    def __add__(self, o): o = TS.lift(o); return TS(tuple(a + b for a, b in zip(self.c, o.c)))
    __radd__ = __add__
    def __neg__(self): return TS(tuple(-a for a in self.c))
    def __sub__(self, o): return self + (-TS.lift(o))
    def __rsub__(self, o): return TS.lift(o) + (-self)
    def __mul__(self, o):
        o = TS.lift(o); a, b = self.c, o.c
        return TS((a[0] * b[0], a[0] * b[1] + a[1] * b[0], a[0] * b[2] + a[1] * b[1] + a[2] * b[0]))
    __rmul__ = __mul__
    def inv(self):
        a0, a1, a2 = self.c
        return TS((1 / a0, -a1 / a0 ** 2, a1 ** 2 / a0 ** 3 - a2 / a0 ** 2))
    def __truediv__(self, o): return self * TS.lift(o).inv()
    def __rtruediv__(self, o): return TS.lift(o) * self.inv()
    def __pow__(self, n):
        n = intexp(n)
        if n < 0:
            return self.inv() ** (-n)
        out = TS((1, 0, 0))
        for _ in range(n):
            out = out * self
        return out


FLOATS = []
def num(x):
    if isinstance(x, float):
        f = Fr(x).limit_denominator(1000)
        assert abs(float(f) - x) < 1e-15, x
        FLOATS.append((x, f)); return f
    return Fr(x)


def intexp(n):
    if isinstance(n, float):
        assert n == int(n), n
        FLOATS.append((n, int(n)))
    return int(n)


class Mat:
    def __init__(self, n, m): self.a = [[0] * m for _ in range(n)]
    def __setitem__(self, ij, v): self.a[ij[0]][ij[1]] = v
    def __getitem__(self, ij): return self.a[ij[0]][ij[1]]


class NP:
    @staticmethod
    def zeros(shape, dtype=None): return Mat(*shape)
    @staticmethod
    def array(x, dtype=None): return list(x)
    empty = zeros
    @staticmethod
    def result_type(*a): return None


src = open(os.path.join(NR, 'polar_matrix_generated.py')).read()
mod = ast.parse(src)
mod.body = [n for n in mod.body if not isinstance(n, (ast.Import, ast.ImportFrom))]
FN = {}


def run_J(r0, bgts, consts, PIv):
    ns = {'np': NP, 'pi': PIv}
    FLOATS.clear()
    exec(compile(mod, 'polar_matrix_generated', 'exec'), ns)
    al_t, aa_t, p0_t, u_t = bgts
    J, h = ns['J_and_h'](TS((r0, 1, 0)), al_t, aa_t, p0_t, u_t, *consts)
    J = [[TS.lift(J[i, j]) for j in range(6)] for i in range(6)]
    h = [TS.lift(v) for v in h]
    return J, h, list(FLOATS)


# ------------------------------------------------------------------ points
random.seed(8)
rnd = lambda lo, hi, d=97: Fr(random.randint(int(lo * d), int(hi * d)), d)
fails, notes = [], []
dsym = {}
for nm, f in (('H0', H0), ('H1', H1), ('K', K), ('F', F), ('G', G)):
    for kk in (2, 1):
        dsym[sp.diff(f, r, kk)] = sp.Symbol(f'{nm}_{kk}')
    dsym[f] = sp.Symbol(f'{nm}_0')
for ip in range(6):
    l = 2 if ip < 3 else 3
    epsv = 1 if ip % 2 == 0 else -1
    r0, al0, aa0, p00, u0 = rnd(1, 9), rnd(0.8, 1.2), rnd(0.8, 1.2), rnd(0.01, 0.3), rnd(-2, -0.1)
    wv, sv, Lv, mv, PIv = rnd(0.5, 0.95), rnd(0.05, 3), rnd(0, 2), rnd(0, 2), rnd(2, 4)
    num_bg = {r: r0, al: al0, aa: aa0, p0: p00, sp.diff(p0, r): u0 * p00, w: wv, eps: epsv, Lam: Lv, mu: mv, PI: PIv, s: sv}
    val = lambda ex: sp.nsimplify(sp.sympify(ex).subs({sp.diff(p0, r): u0 * p00}).subs(num_bg), rational=True)
    a1, b1, p2 = val(dal_e), val(daa_e), val(ddp_e)
    two = {sp.diff(p0, r, 2): p2}
    a2, b2, p3 = [sp.nsimplify(sp.sympify(x).subs(two).subs({sp.diff(p0, r): u0 * p00}).subs(num_bg), rational=True)
                  for x in (dal2, daa2, ddp3)]
    Fv = lambda x: Fr(int(sp.numer(x)), int(sp.denom(x)))
    a1, b1, p2, a2, b2, p3 = map(Fv, (a1, b1, p2, a2, b2, p3))
    p1 = u0 * p00
    al_t, aa_t = TS((al0, a1, a2 / 2)), TS((aa0, b1, b2 / 2))
    p_t, dp_t = TS((p00, p1, p2 / 2)), TS((p1, p2, p3 / 2))
    u_t = dp_t / p_t
    J, h, fl = run_J(r0, (al_t, aa_t, p_t, u_t), (wv, Fr(epsv), sv, l * (l + 1), Lv, mv), PIv)
    if mut == 'coef':
        J[0][0] = J[0][0] * Fr(8, 7)
    y = [rnd(-3, 3) for _ in range(6)]
    J0 = [[J[i][j].c[0] for j in range(6)] for i in range(6)]
    J1 = [[J[i][j].c[1] for j in range(6)] for i in range(6)]
    mv_ = lambda M, v: [sum(M[i][j] * v[j] for j in range(6)) for i in range(6)]
    y1 = mv_(J0, y)
    y2 = mv_(J0, y1) if mut == 'nojp' else [a + b for a, b in zip(mv_(J1, y), mv_(J0, y1))]
    h0, h1, h2 = [v.c[0] for v in h], [v.c[1] for v in h], [2 * v.c[2] for v in h]
    dot = lambda a, b: sum(x * z for x, z in zip(a, b))
    vals = {'H0': (dot(h0, y), dot(h1, y) + dot(h0, y1), dot(h2, y) + 2 * dot(h1, y1) + dot(h0, y2)),
            'H1': (sv * y[0], sv * y1[0], sv * y2[0]), 'K': (y[1], y1[1], y2[1]),
            'F': (y[2], y1[2], y2[2]), 'G': (sv * y[4], sv * y1[4], sv * y2[4])}
    pert = {sp.Symbol(f'{nm}_{kk}'): sp.Rational(vals[nm][kk].numerator, vals[nm][kk].denominator) for nm in vals for kk in range(3)}
    bgd = {sp.diff(al, r, 2): sp.Rational(a2.numerator, a2.denominator), sp.diff(aa, r, 2): sp.Rational(b2.numerator, b2.denominator),
           sp.diff(al, r): sp.Rational(a1.numerator, a1.denominator), sp.diff(aa, r): sp.Rational(b1.numerator, b1.denominator),
           sp.diff(p0, r, 2): sp.Rational(p2.numerator, p2.denominator), sp.diff(p0, r): sp.Rational(p1.numerator, p1.denominator)}
    out, kg, Y, E = EQ[l]
    res = {}
    for c in (sp.Rational(3, 5), sp.Rational(5, 13)):
        sn = sp.sqrt(1 - c ** 2)
        angle = {sp.cos(th): c, sp.sin(th): sn}

        def ev(ex):
            ex = (ex / (Y * E)).subs(dsym).subs(pert).subs(bgd).subs(num_bg).subs(t, 0)
            ex = ex.subs(th, sp.acos(c))
            return sp.nsimplify(sp.simplify(ex))
        tt = ev(out[(0, 0)][1])
        trc = ev(out[(2, 2)][1] + out[(3, 3)][1] / sp.sin(th) ** 2)
        thth0 = sp.simplify(out[(2, 2)][0].subs(bgd).subs(num_bg).subs(th, sp.acos(c)))
        res[c] = (tt, trc, thth0)
    (tA, rA, bA), (tB, rB, bB) = res.values()
    c0 = (sp.simplify(tA - tB) == 0) and (sp.simplify(rA - rB) == 0) and bA == 0 and bB == 0
    c1, c2 = tA == 0 and tB == 0, rA == 0 and rB == 0
    print(f"  point {ip}: l = {l}, eps = {epsv:+d}, r = {r0}, s = {sv}, pi -> {PIv}: E_tt {tA}, angular trace {rA}, "
          f"background E_thth {bA}; C0 {'PASS' if c0 else 'FAIL'} C1 {'PASS' if c1 else 'FAIL'} C2 {'PASS' if c2 else 'FAIL'}"
          f"  (floats converted: {sorted(set((str(a), str(b)) for a, b in fl))})", flush=True)
    for nm, ok in (('C0', c0), ('C1', c1), ('C2', c2)):
        if not ok:
            fails.append(f"{nm} at point {ip}")
print(f"{time.time() - T0:.0f} s")
print("RESULT", "FAIL: " + "; ".join(fails) if fails else "PASS")
sys.exit(1 if fails else 0)
