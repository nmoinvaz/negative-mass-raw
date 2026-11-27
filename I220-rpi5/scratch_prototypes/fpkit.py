"""finite-part boundary kit for the reduction of G6: asymptotic series of the generators at theta -> pi/2 (x = pi/2 - theta, L = ln x)
and at theta -> 0, and the finite part (constant term) of a product."""
import sympy as sp

x, L, t = sp.symbols("x L t", positive=True)
s, r = sp.symbols("s r", positive=True)
q = sp.Symbol("q", positive=True)           # ln 2
z3 = sp.Symbol("z3")                        # zeta(3)
J2 = sp.Symbol("J2")                        # int_0^{pi/2} ln^2 cos
ORD = 9                                      # series order
K = 8                                        # shift for Laurent extraction


def logs_to_L(e):
    return sp.expand(e).subs(sp.log(x), L)


# ---- theta -> pi/2: x = pi/2 - theta, ell = ln sin x -----------------------------------------------------------------
ell1 = sp.series(sp.log(sp.sin(s) / s), s, 0, ORD).removeO()            # ln(sin s / s)
ell_s = sp.log(s) + ell1                                                 # ell as a function of s = x
C_s = sp.expand(-sp.integrate(sp.expand(2 * ell_s + 2 * q), (s, 0, s)))   # C(s) = -int_0^s (2 ell + 2 q), C(0) = 0
ell_x = L + ell1.subs(s, x)
u_x = sp.series(sp.cot(x), x, 0, ORD).removeO()
th_x = sp.pi / 2 - x
C_x = logs_to_L(C_s.subs(s, x))
D3_s = sp.expand(sp.Rational(7, 4) * z3 - 2 * sp.integrate(C_s.subs(s, r), (r, 0, s)))
D3_x = logs_to_L(D3_s.subs(s, x))
Lc_s = sp.expand(J2 - sp.integrate(sp.expand(ell_s.subs(s, r) ** 2), (r, 0, s)))
Lc_x = logs_to_L(Lc_s.subs(s, x))
ui_x = sp.series(sp.tan(x), x, 0, ORD).removeO()
EXP_PI2 = {"ell": ell_x, "u": u_x, "ui": ui_x, "th": th_x, "C": C_x, "D3": D3_x, "Lc": Lc_x}

# ---- theta -> 0 -------------------------------------------------------------------------------------------------------
ell_t = sp.series(sp.log(sp.cos(t)), t, 0, ORD).removeO()
u_t = sp.series(sp.tan(t), t, 0, ORD).removeO()
C_t = sp.expand(sp.integrate(sp.expand(2 * ell_t + 2 * q), (t, 0, t)))
D3_t = sp.expand(sp.integrate(sp.expand(2 * C_t.subs(t, r)), (r, 0, t)))
Lc_t = sp.expand(sp.integrate(sp.expand(ell_t.subs(t, r) ** 2), (r, 0, t)))
ui_t = sp.series(sp.cot(t), t, 0, ORD).removeO()
EXP_0 = {"ell": ell_t, "u": u_t, "ui": ui_t, "th": t, "C": C_t, "D3": D3_t, "Lc": Lc_t}


def _const_term(e, v, logsym=None):
    e = sp.expand(e * v**K)
    gens = (v, logsym) if logsym is not None else (v,)
    P = sp.Poly(e, *gens)
    key = (K,) + ((0,) if logsym is not None else ())
    return P.coeff_monomial(key)


def fp_pi2(expr, syms):
    """constant term (x^0 L^0) of expr at theta -> pi/2; syms: {'ell': symbol, ...} for the generators present"""
    sub = {syms[k]: EXP_PI2[k] for k in syms}
    return sp.simplify(_const_term(expr.subs(sub), x, L))


def fp_0(expr, syms):
    sub = {syms[k]: EXP_0[k] for k in syms}
    return sp.simplify(_const_term(expr.subs(sub), t))
