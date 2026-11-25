import sys, pickle, time
import sympy as sp
from sympy.polys.rings import ring
from sympy import QQ
Q = pickle.load(open(sys.argv[1]+"/Q_all.pkl","rb"))
c, S = sp.symbols("c S", real=True)
W = sp.symbols("W0:5", real=True)
Rg, cc, SSS, *Ws = ring([c, S] + list(W), QQ)
Qr = {k: Rg.from_expr(sp.sympify(v, locals={"c": c, "S": S, **{f"W{i}": W[i] for i in range(5)}})) for k, v in Q.items()}
# parity and structure
for k, v in Qr.items():
    cs = sorted(set(m[0] for m in v.monoms()))
    print(k, "c-degrees", cs, "S", sorted(set(m[1] for m in v.monoms())))
# equator
eq = {}
for k, v in Qr.items():
    e = Rg.zero
    for m, co in v.terms():
        if m[0] == 0:
            e += Rg.from_dict({m: co})
    eq[k] = e
    print("equator", k, len(e), "deg", max((sum(m[2:]) for m in e.monoms()), default=None))
