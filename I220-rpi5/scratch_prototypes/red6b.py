"""dev: the by-hand reduction of int_0^{pi/2} I6 (finite-part algebra) and its assembly into a closed form"""
import pickle
import sys
sys.path.insert(0, "/tmp/claude-1000/-home-nathan-Source-negative-mass-i220/e48dd6bd-94ac-46f2-8d9d-42321d8492dd/scratchpad")
import sympy as sp  # noqa: E402
import fpkit as F  # noqa: E402

lg, u, th, q = sp.symbols("ell u th q")
C, D3, Lc = sp.symbols("C D3 Lc2")
w1, w2, w3, w4 = sp.symbols("w1 w2 w3 w4")
parts = pickle.load(open("/tmp/claude-1000/-home-nathan-Source-negative-mass-i220/e48dd6bd-94ac-46f2-8d9d-42321d8492dd/scratchpad/I6_parts.pkl", "rb"))
# the pickle holds the symbols of proto6 (same names); map by name
names = {s.name: s for pc in parts.values() for s in pc.free_symbols}
sub = {names[n]: v for n, v in (("ell", lg), ("u", u), ("th", th), ("q", q), ("w1", w1), ("w2", w2), ("w3", w3), ("w4", w4)) if n in names}
parts = {k: sp.expand(v.subs(sub)) for k, v in parts.items()}
cCC, cCD, cCL = parts[(2, 0, 0)], parts[(1, 1, 0)], parts[(1, 0, 1)]
cC, cD, cL, cR = parts[(1, 0, 0)], parts[(0, 1, 0)], parts[(0, 0, 1)], parts[(0, 0, 0)]
print("cCC =", cCC, "| cCD =", cCD, "| cCL =", cCL)

ui = sp.Symbol("ui")
SYMS = {"ell": lg, "u": u, "ui": ui, "th": th, "C": C, "D3": D3, "Lc": Lc}
pi, z3, z5 = sp.pi, sp.zeta(3), sp.zeta(5)
J = sp.symbols("J0:8")


def bnd(expr):
    """B[F] = FP_{pi/2} F - FP_0 F for F in the generators; the constants of F.J2, F.z3 are the kit's symbols"""
    expr = sp.expand(expr).replace(lambda e: e.is_Pow and e.base == u and e.exp < 0, lambda e: ui ** (-e.exp))
    syms = {k: v for k, v in SYMS.items() if expr.has(v)}
    return sp.expand(F.fp_pi2(expr, syms) - F.fp_0(expr, syms))


F.J2 = F.J2
# keep J2 of the kit as symbol J[2], z3 of the kit as symbol zeta(3)
Jv_J2 = pi * (12 * q**2 + pi**2) / 24


def fix(e):
    return sp.expand(e).subs({F.J2: Jv_J2, F.z3: z3, F.q: q})


# ---- step Q: the three quadratic terms --------------------------------------------------------------------------
# M1: <u^2 (f - f') C^2>, f = a1 ell + a0:  u (f - f_ell) -> check the matching
f = 3072 * lg + 2048 * q + 4096
assert sp.expand(cCC - u**2 * 1024 * (3 * lg + 2 * q + 1)) == 0
assert sp.expand(f - sp.diff(f, lg) - 1024 * (3 * lg + 2 * q + 1)) == 0
b1 = bnd(u * f * C**2)
print("M1 boundary B[u f C^2] =", fix(b1))
# new linear C term: -4 u f (ell + q) C ; constants: -<f C^2>
# M2: <u C D3> = B[-ell C D3] + <ell (2 ell + 2 q) D3> + 2 <ell C^2>
b2 = bnd(-lg * C * D3)
print("M2 boundary B[-ell C D3] =", fix(b2))
# M3: <u^2 C Lc> = B[u C Lc] - <C Lc> - 2 <u (ell + q) Lc> - <u ell^2 C>
b3 = bnd(u * C * Lc)
print("M3 boundary B[u C Lc] =", fix(b3))


# =====================================================================================================================
# assembly
# =====================================================================================================================
qs = q
z2, z4 = pi**2 / 6, pi**4 / 90
Jv = [pi / 2, -pi * q / 2, pi * (12 * q**2 + pi**2) / 24, pi * (-6 * z3 - pi**2 * q - 4 * q**3) / 8,
      pi * (240 * q**4 + 120 * pi**2 * q**2 + 1440 * q * z3 + 19 * pi**4) / 480,
      pi * (-19 * pi**4 * q - 1080 * z5 - 60 * pi**2 * z3 - 720 * q**2 * z3 - 40 * pi**2 * q**3 - 48 * q**5) / 96]
M_C2 = pi**5 / 360
M_lC2 = -q * pi**5 / 360
M_thC = pi / 4 * z3
M_uC = [sp.expand((2 * Jv[b + 2] + 2 * q * Jv[b + 1]) / (b + 1)) for b in range(4)]
M_l2D3 = sp.Rational(3, 4) * z3 * Jv[2] + pi / 4 * (2 * q * z4 + 5 * z5 - 2 * z2 * z3)
M_CLc = sp.Rational(7, 8) * z3 * Jv[2] - M_l2D3 / 2
Lcs, Cs, D3s = Lc, C, D3


def Dth(e):
    """d/dtheta on the generators ell, u, th, C, D3, Lc"""
    return (sp.diff(e, lg) * (-u) + sp.diff(e, u) * (1 + u**2) + sp.diff(e, th) + sp.diff(e, C) * (2 * lg + 2 * q) + sp.diff(e, D3) * 2 * C
            + sp.diff(e, Lc) * lg**2)


const = sp.Integer(0)           # constants of the steps
Ct = sp.expand(cC)              # coefficient of C, to be extended
Dt = sp.expand(cD)
Lt = sp.expand(cL)
Rt = sp.expand(cR)

# ---- Q ---------------------------------------------------------------------------------------------------------
# M1
const += fix(b1) - (3072 * M_lC2 + (2048 * q + 4096) * M_C2)
Ct += -4 * u * f * (lg + q)
# M2
const += -512 * fix(b2) - 1024 * M_lC2
Dt += -512 * lg * (2 * lg + 2 * q)
# M3
const += -2048 * fix(b3) + 2048 * M_CLc
Ct += 2048 * u * lg**2
Lt += 4096 * u * (lg + q)

# ---- D ---------------------------------------------------------------------------------------------------------
Dt = sp.expand(Dt)
pu = sp.collect(Dt, u, evaluate=False)
print("D3 coefficient u-powers:", list(pu.keys()))
Eq = pu.get(u**-2, 0)                      # coefficient of u^-2 = 1/S - 1
P0 = pu.get(sp.Integer(1), 0)
c1 = Eq                                    # coefficient of 1/S
c0 = sp.expand(P0 - Eq)                    # polynomial part
a_b = [sp.Poly(c0, lg).coeff_monomial(lg**b) for b in range(3)]
assert sp.Poly(c0, lg).degree() <= 2
beta = [sp.Poly(c1, lg).coeff_monomial(lg**b) for b in range(4)]
assert sp.Poly(c1, lg).degree() <= 3
Pfun = [th, (C - 2 * q * th) / 2, Lc]
A = sum(a_b[b] * Pfun[b] for b in range(3))
Fb = lambda b: -lg**b / u - (b * Pfun[b - 1] if b else 0)   # noqa: E731
A += sum(beta[b] * Fb(b) for b in range(4))
A = sp.expand(A)
chk = sp.expand(Dth(A) - (c0 + c1 * (1 + u**-2)))
print("D-step: A' - cD =", sp.simplify(chk))
const += fix(bnd(A * D3))
AC = sp.expand(-2 * A * C)
# AC has u^-1 ell^b C terms, theta C, C^2, Lc C
Ct += sp.expand(sum(t_ for t_ in sp.Add.make_args(AC) if t_.has(C) and not t_.has(C**2) and not t_.has(Lc)).subs({}) / C)
rest_AC = sp.expand(AC - sum(t_ for t_ in sp.Add.make_args(AC) if t_.has(C) and not t_.has(C**2) and not t_.has(Lc)))
# remaining: C^2 and C Lc terms (constant coefficients) : theta C counted in the C coefficient above
cC2 = rest_AC.coeff(C, 2)
cCLc = sp.expand(rest_AC - cC2 * C**2).coeff(Lc, 1).coeff(C, 1)
assert sp.expand(rest_AC - cC2 * C**2 - cCLc * C * Lc) == 0, rest_AC
const += cC2 * M_C2 + cCLc * M_CLc

# ---- C ---------------------------------------------------------------------------------------------------------
Ct = sp.expand(Ct)
pc = sp.collect(Ct, u, evaluate=False)
print("C coefficient u-powers:", list(pc.keys()))
cm1 = sp.expand(pc.get(u**-1, 0))
print("u^-1 part of the C coefficient after the D step:", sp.simplify(cm1))
assert cm1 == 0
c1u = sp.expand(pc.get(u, 0))
c2u = sp.expand(pc.get(u**2, 0))
c0u = sp.expand(pc.get(sp.Integer(1), 0))
# u^1 ell^b
for b in range(5):
    cb = sp.Poly(c1u, lg).coeff_monomial(lg**b)
    if b >= 4:
        assert cb == 0
    const += cb * M_uC[b] if b < 4 else 0
# u^2 theta
c2th = sp.Poly(c2u, th).coeff_monomial(th)
assert sp.expand(c2u - c2th * th) == 0, c2u
b4 = fix(bnd(u * th * C))
const += c2th * (b4 - M_thC - M_uC[0] - 2 * (fix(bnd(-th * (lg + q)**2 / 2)) + sp.Rational(1, 2) * (Jv[2] + 2 * q * Jv[1] + q**2 * Jv[0])))
# theta C and the others (u^0)
c0t = sp.Poly(c0u, th)
assert c0t.degree() <= 1
c0th = c0t.coeff_monomial(th)
c0c = c0t.coeff_monomial(1)
assert sp.expand(c0c) == 0, c0c
const += c0th * M_thC

# ---- L ---------------------------------------------------------------------------------------------------------
Lt = sp.expand(Lt)
pl = sp.collect(Lt, u, evaluate=False)
assert list(pl.keys()) == [u], pl.keys()
g = pl[u]
G = sp.integrate(g, lg)
assert G.subs(lg, 0) == 0
const += fix(bnd(-G * Lc)) + sum(sp.Poly(G, lg).coeff_monomial(lg**b) * Jv[b + 2] for b in range(4))

# ---- rest -----------------------------------------------------------------------------------------------------
J6s = sp.Symbol("J6s")
Jf = Jv + [J6s]
Rt = sp.expand(Rt)
for term in sp.Add.make_args(Rt):
    c_, rest_ = term.as_independent(u, th, lg)
    d = rest_.as_powers_dict()
    a, k, b = d.get(u, 0), d.get(th, 0), d.get(lg, 0)
    if a == -2 and k == 0:
        assert b >= 1
        const += c_ * (-b * Jf[b - 1] - Jf[b])
    elif a == 0 and k == 0:
        const += c_ * Jf[b]
    elif a == 1 and k == 1:
        const += c_ * (fix(bnd(-th * lg**(b + 1) / (b + 1))) + Jf[b + 1] / (b + 1))
    else:
        raise ValueError(("unhandled rest term", term))
const = sp.expand(const)
print("coefficient of J6 left:", sp.simplify(const.coeff(J6s, 1)))
const = const.subs(J6s, 0)

wsub = {w1: 2 * pi**2 / 3 + 8 * q**2, w2: 80 * z3 - sp.Rational(8, 3) * pi**2 * q - sp.Rational(32, 3) * q**3,
        w3: 22 * pi**4 / 45 + sp.Rational(16, 3) * pi**2 * q**2 + sp.Rational(32, 3) * q**4 - 320 * z3 * q - 384 * z3}
G6_0 = sp.expand(const.subs(w4, 0).subs(wsub))
slope = sp.simplify(sp.diff(const, w4))
print("slope in w4:", slope)
Om4c = sp.expand(sp.simplify(G6_0 / (4 * pi)))
print("G6(0) =", sp.collect(sp.expand(G6_0), pi))
print("Omega4 closed =", Om4c)
import mpmath as mp
mp.mp.dps = 60
val = sp.N(Om4c.subs({q: sp.log(2)}), 60)
print("Omega4 closed (numeric) =", val)
pickle.dump((G6_0, Om4c), open("/tmp/claude-1000/-home-nathan-Source-negative-mass-i220/e48dd6bd-94ac-46f2-8d9d-42321d8492dd/scratchpad/G6_closed.pkl", "wb"))
