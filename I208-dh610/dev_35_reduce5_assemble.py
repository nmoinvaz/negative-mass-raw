"""dev_35: the reduction of G_5 by hand, assembled in sympy (no numerics): I_5 = rest + cC C + cD D3 + cL Lc2 (dev_34), the D3 term by parts,
the C integrals to moments, Parseval for C^2 and theta C, the regularized u (Lc2, theta) term, the log-cosine moments from the Beta function.
Prints Omega3 and its difference from 22 pi^4/45 + 16 pi^2 ln^2 2/3 + 32 ln^4 2/3 - 320 zeta(3) ln 2 - 384 zeta(3)."""
import sys
sys.path.insert(0, "/home/nathan/Source/negative-mass-i208/notes/wormhole_largeD")
_a, sys.argv = sys.argv, sys.argv[:1]
import order5 as o5
import order4 as o4
sys.argv = _a
import sympy as sp

lg, S, u, C, D3, Lc, th, q, K = sp.symbols("ell S u C D3 Lc2 th q K")
w0, w1, w2, w3, w4 = sp.symbols("w0 w1 w2 w3 w4")
R = 1 / (1 - S)
l = -2 * lg
sc = u * (1 - S)
L = [-1, -2 * w0 + 4 * lg, -2 * w1 - 4 * w0 * lg + 16 * lg**2 + 16 * u * C]
Y = [1, 2 * lg, 4 * w0 * lg - 6 * lg**2, 4 * w1 * lg - 4 * lg**3 + 32 * lg**2 - 16 * w0 * lg + 32 * u * C - 16 * D3]
Om = [w0, w1, w2, w3, w4]
h3 = o5.hk(3, Om, l, R, Y + [0], L)
B = -32 * (lg + q) * C + 16 * S * C + 32 * Lc + 16 * sc * lg * (lg + 2 * q) - 4 * w1 * th - 2 * w1 * sc
L3 = -2 * h3 + 2 * u * B
LL = L + [L3]
h4 = S * LL[3] + sum(Y[j] * o5.cc(4 - j, Om, l, R) for j in range(4))
t1 = 8 * lg * h4 / S
t2 = 2 * sum(LL[3 - j] * l ** (j + 1) / sp.factorial(j + 1) for j in range(4))
o = list(Om)
o[4] = 0
t3 = 2 * sum(Y[j] * o5.cc(5 - j, o, l, R) for j in range(4)) / S
F3 = sum(LL[3 - j] * l**j / sp.factorial(j) for j in range(4))
t4 = -4 * (lg - w0) * F3
I5 = sp.expand((t1 + t2 + t3 + t4).subs(w0, -4 * q))


def red_u(e):
    p = sp.Poly(sp.expand(e), u)
    return sp.expand(sum(cf * (S / (1 - S)) ** (k // 2) * u ** (k % 2) for (k,), cf in p.terms()))


I5 = red_u(I5)
cC = sp.together(sp.Poly(I5, C).coeff_monomial(C))
cD = sp.together(sp.Poly(I5, D3).coeff_monomial(D3))
cL = sp.together(sp.Poly(I5, Lc).coeff_monomial(Lc))
rest = sp.expand(sp.together(I5.subs({C: 0, D3: 0, Lc: 0})))
cot = 1 / u

# --- D3 by parts: cD = cD0 + cD1/S; antiderivative A_D (K' = -2 ell, F_n' = ell^n/S)
cDe = sp.expand(sp.simplify(cD * S))                    # polynomial in S, ell
cD0 = sp.simplify(cDe.coeff(S, 1) / 1)                   # coefficient of S: cD = cD0 + cD1/S
cD1 = sp.simplify(cDe.coeff(S, 0))
assert sp.simplify(cD - (cD0 + cD1 / S)) == 0
# cD0 = 32 (6 ell - 8 q): antiderivative 32 (6 M1 - 8 q th), M1 = -K/2
F0, F1, F2 = -cot, -lg * cot - th, -lg**2 * cot + K
p1 = sp.Poly(cD1, lg)
cD1c = [p1.coeff_monomial(lg**n) for n in range(3)]
assert sp.Poly(cD1, lg).degree() == 2
AD = 32 * (-3 * K - 8 * q * th) + sum(c * F for c, F in zip(cD1c, (F0, F1, F2)))
# check A_D' = cD in the derivation d/dth on generators (ell' = -u, th' = 1, K' = -2 ell, u' = 1 + u^2 = 1/(1-S), S' = 2 u (1-S) ... on S = sin^2 : S' = 2 sc)
def Dth(f):
    return (sp.diff(f, lg) * (-u) + sp.diff(f, th) + sp.diff(f, K) * (-2 * lg) + sp.diff(f, u) * (1 + u**2)
            + sp.diff(f, S) * 2 * u * (1 - S))
chk = sp.simplify((Dth(AD) - cD).subs(S, u**2 / (1 + u**2)))
print("A_D' - cD (sympy, S = u^2/(1+u^2)):", chk)
# --- C terms after the by parts, everything as a rational function of u (S = u^2/(1+u^2))
Su = u**2 / (1 + u**2)
totC = sp.together(sp.expand(((cC - 2 * AD).subs(K, 2 * q * th - C)).subs(S, Su)))
totC = sp.expand(sp.cancel(totC))
pol = sp.Poly(totC, C, th, lg)
print("C-coefficient after the by parts (coefficient of C^a th^b ell^c as function of u):")
for mon, cf in sorted(pol.terms()):
    print("  ", mon, sp.factor(cf))

# --- the boundary term [D3 A_D]: A_D(pi/2) with K = pi q, th = pi/2, cot ell^n -> 0
AD_half = sp.simplify(AD.subs({K: sp.pi * q, th: sp.pi / 2}).subs(u, sp.oo) if False else (32 * (-3 * sp.pi * q - 8 * q * sp.pi / 2) + cD1c[0] * 0 + cD1c[1] * (-sp.pi / 2) + cD1c[2] * (sp.pi * q)))
print("A_D(pi/2) =", AD_half)

# --- the moments J_n = int_0^{pi/2} ln^n cos (Beta function series), as order4.moments
a = sp.Symbol("a")
ser = sp.series(sp.sqrt(sp.pi) / 2 * sp.gamma((a + 1) / 2) / sp.gamma(a / 2 + 1), a, 0, 7).removeO()
J = [sp.simplify(sp.expand_func(sp.factorial(n) * ser.coeff(a, n))) for n in range(7)]
qv = sp.log(2)

# (i) u C P(ell): P = p0 + p1 ell + p2 ell^2, int u ell^n C = (2 J_{n+2} + 2 q J_{n+1})/(n+1)
P_ = sp.Poly(sp.expand(sp.simplify(totC.coeff(C, 0))), lg) if False else None
pcoef = {}
for mon, cf in pol.terms():
    if mon[0] == 0 and mon[1] == 0:
        pcoef[mon[2]] = sp.simplify(cf / u)
print("P(ell) coefficients:", pcoef)
Ci = sum(p * (2 * J[n + 2] + 2 * q * J[n + 1]) / (n + 1) for n, p in pcoef.items())
c2coef = [cf for mon, cf in pol.terms() if mon == (1, 0, 0)][0]
print("C^2 coefficient (of C, i.e. coefficient of C in cC - 2 A_D):", c2coef)
C2i = c2coef * sp.pi**5 / 360          # int_0^{pi/2} C^2 = pi^5/360 (Parseval)

# (iii) the rest
rest2 = sp.expand(sp.together(rest.subs(S, Su)))
rest_S = sp.expand(rest * S)
# rest = (A(ell) + S Bpoly(ell) + S th u (...)) / S
thu = sp.Poly(rest_S, th).coeff_monomial(th)            # coefficient of th (in rest*S)
print("theta coefficient in rest*S:", sp.simplify(thu))
rest_S0 = sp.expand(rest_S.subs(th, 0))
polyS = sp.Poly(red_u(rest_S0), S)
A_ = polyS.coeff_monomial(1)
B_ = polyS.coeff_monomial(S)
print("deg_S of rest*S:", polyS.degree())
Apoly = sp.Poly(A_, lg)
Bpoly = sp.Poly(B_, lg)
rest_int = 0
for (b,), cf in Apoly.terms():
    assert b >= 1
    rest_int += -b * cf * J[b - 1]
for (b,), cf in Bpoly.terms():
    rest_int += cf * J[b]
# (iv) regularized u (cL Lc2 + thu/S th): the divergent constants cancel (checked), remaining -1024 q J3 + k J1, k = coefficient of th u
kthu = sp.simplify(thu / (u * S)) if thu != 0 else 0
print("theta u coefficient:", sp.simplify(kthu))
reg = -1024 * q * J[3] + kthu * J[1]
G5_0 = (rest_int + Ci + C2i + reg).subs(q, qv)
G5_0 = G5_0.subs({w0: -4 * qv})
G5_0 = sp.simplify(sp.expand(G5_0))
print("G5(w3 = 0) with w1, w2 symbolic:", G5_0)

# --- solve G5 = 0 for Omega3 with the closed Omega1, Omega2, and compare with the PSLQ closed form
w1v = 2 * sp.pi**2 / 3 + 8 * qv**2
w2v = 80 * sp.zeta(3) - sp.Rational(8, 3) * sp.pi**2 * qv - sp.Rational(32, 3) * qv**3
G5 = sp.expand_log(G5_0, force=True).subs({w1: w1v, w2: w2v})
sol = sp.solve(sp.expand(G5), w3)
om3 = sp.simplify(sp.expand(sol[0]))
print("Omega3 from G5 = 0:", om3)
target = 22 * sp.pi**4 / 45 + 16 * sp.pi**2 * qv**2 / 3 + 32 * qv**4 / 3 - 320 * sp.zeta(3) * qv - 384 * sp.zeta(3)
print("difference from 22 pi^4/45 + 16 pi^2 ln^2 2/3 + 32 ln^4 2/3 - 320 zeta(3) ln 2 - 384 zeta(3):", sp.simplify(sp.expand(sp.expand_log(om3 - target, force=True))))
print("numeric:", sp.N(om3, 40), sp.N(target, 40))
