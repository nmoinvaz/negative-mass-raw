"""finite-part integration by parts on the generators lt = ln(2 cos th), u = tan th, ui = cot th, th, C = Cl2(pi - 2 th), D3, K2 = int lt^2, K3 = int lt^3"""
import sympy as sp

lt, u, ui, th, C, D3, K2, K3 = sp.symbols("lt u ui th C D3 K2 K3")
q = sp.Symbol("q", positive=True)
z3, z5 = sp.zeta(3), sp.zeta(5)
Jt2, Jt3 = sp.Symbol("Jt2"), sp.Symbol("Jt3")
x, L, t, s, r = sp.symbols("x L t s r", positive=True)
ORD, SHIFT = 10, 9


def dth(e):
    return (sp.diff(e, lt) * (-u) + sp.diff(e, u) * (1 + u**2) + sp.diff(e, ui) * (-(1 + ui**2)) + sp.diff(e, th) + sp.diff(e, C) * 2 * lt
            + sp.diff(e, D3) * 2 * C + sp.diff(e, K2) * lt**2 + sp.diff(e, K3) * lt**3)


def kit():
    logs = lambda e: sp.expand(e).subs(sp.log(x), L)
    ell1 = sp.series(sp.log(sp.sin(s) / s), s, 0, ORD).removeO()
    ell_s = sp.log(s) + q + ell1                                  # ln(2 sin x), x = pi/2 - th
    C_s = sp.expand(-sp.integrate(sp.expand(2 * ell_s), (s, 0, s)))
    D3_s = sp.expand(sp.Rational(7, 4) * z3 - 2 * sp.integrate(C_s.subs(s, r), (r, 0, s)))
    K2_s = sp.expand(Jt2 - sp.integrate(sp.expand(ell_s.subs(s, r) ** 2), (r, 0, s)))
    K3_s = sp.expand(Jt3 - sp.integrate(sp.expand(ell_s.subs(s, r) ** 3), (r, 0, s)))
    pi2 = {"lt": L + q + ell1.subs(s, x), "u": sp.series(sp.cot(x), x, 0, ORD).removeO(), "ui": sp.series(sp.tan(x), x, 0, ORD).removeO(),
           "th": sp.pi / 2 - x, "C": logs(C_s.subs(s, x)), "D3": logs(D3_s.subs(s, x)), "K2": logs(K2_s.subs(s, x)), "K3": logs(K3_s.subs(s, x))}
    lt_t = q + sp.series(sp.log(sp.cos(t)), t, 0, ORD).removeO()
    C_t = sp.expand(sp.integrate(sp.expand(2 * lt_t), (t, 0, t)))
    D3_t = sp.expand(sp.integrate(sp.expand(2 * C_t.subs(t, r)), (r, 0, t)))
    K2_t = sp.expand(sp.integrate(sp.expand(lt_t.subs(t, r) ** 2), (r, 0, t)))
    K3_t = sp.expand(sp.integrate(sp.expand(lt_t.subs(t, r) ** 3), (r, 0, t)))
    zero = {"lt": lt_t, "u": sp.series(sp.tan(t), t, 0, ORD).removeO(), "ui": sp.series(sp.cot(t), t, 0, ORD).removeO(), "th": t, "C": C_t, "D3": D3_t,
            "K2": K2_t, "K3": K3_t}
    return pi2, zero


_KIT = {}


def const_term(e, v, logsym=None):
    e = sp.expand(e * v**SHIFT)
    gens = (v, logsym) if logsym is not None else (v,)
    P = sp.Poly(e, *gens)
    return P.coeff_monomial((SHIFT,) + ((0,) if logsym is not None else ()))


def bnd(expr):
    """B[F] = FP_{pi/2} F - FP_0 F"""
    if not _KIT:
        _KIT["pi2"], _KIT["zero"] = kit()
    pi2, zero = _KIT["pi2"], _KIT["zero"]
    expr = sp.expand(expr).replace(lambda e: e.is_Pow and e.base == u and e.exp < 0, lambda e: ui ** (-e.exp))
    names = {"lt": lt, "u": u, "ui": ui, "th": th, "C": C, "D3": D3, "K2": K2, "K3": K3}
    syms = {k: v for k, v in names.items() if expr.has(v)}
    a = const_term(expr.subs({syms[k]: pi2[k] for k in syms}, simultaneous=True), x, L)
    b = const_term(expr.subs({syms[k]: zero[k] for k in syms}, simultaneous=True), t)
    return sp.expand(a - b)
