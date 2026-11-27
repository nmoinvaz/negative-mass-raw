import pickle, sympy as sp
from lin import rho, W, L, R2
As, A1 = sp.symbols("As A1")
Nn, H2sol, sys3 = pickle.load(open("l1sys2.pkl", "rb"))
Ne = sp.simplify(Nn.subs({As: 1, A1: 0}))
p, q = sp.symbols("p q")
T = sp.diag(R2**sp.Rational(1, 2)**0 * R2**(sp.Symbol('p') / 2), R2**(sp.Symbol('q') / 2))
for pv, qv in [(0, 0), (-2, 0), (-2, -1), (-4, -2), (-4,-3), (-2,-2)]:
    T = sp.diag(R2**sp.Rational(pv, 2), R2**sp.Rational(qv, 2))
    N2 = sp.simplify(T.inv() * Ne * T - T.inv() * sp.diff(T, rho))
    lead = [sp.limit(e / rho**k, rho, sp.oo) for e in N2 for k in [0]]  # placeholder
    # large-rho leading behaviour of each entry
    out = []
    for e in N2:
        s = sp.series(e.subs(rho, 1 / sp.Symbol("x")), sp.Symbol("x"), 0, 1).removeO() if True else None
        out.append(sp.simplify(s))
    print((pv, qv), out)
