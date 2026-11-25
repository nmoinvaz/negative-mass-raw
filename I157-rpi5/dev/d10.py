import sys, pickle, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i157/notes/warp")
import three_scalars_ideal as I
from sympy import QQ
import sympy as sp
from sympy.polys.rings import ring
Rn = I.Rn
Qd, Dd = pickle.load(open(sys.argv[1]+"/Qdump.pkl", "rb"))
mk = lambda d: Rn.from_dict({m: QQ(a, b) for m, (a, b) in d.items()})
Q = I.strip_axis({k: mk(v) for k, v in Qd.items()})
gens = I.rung_gens(Q, "Rk22")
# new ring in (a, b, u1, u3, u4): u0 = (a + u1)/2, u2 = b - u1
R2_, a, b, v1, v3, v4 = ring("a,b,u1,u3,u4", QQ)
def subst(p):
    out = R2_.zero
    for mon, co in p.terms():
        f, e0, e1, e2, e3, e4 = mon
        assert f == 0
        out += co * ((a + v1) * QQ(1, 2)) ** e0 * v1 ** e1 * (b - v1) ** e2 * v3 ** e3 * v4 ** e4
    return out
t0 = time.time()
for lab, p in gens:
    q = subst(p)
    # classify monomials by (deg_a, deg_b)
    kinds = {}
    for mon, co in q.terms():
        k = (min(mon[0], 1), min(mon[1], 2))
        kinds[k] = kinds.get(k, 0) + 1
    low = {k: v for k, v in kinds.items() if k in ((0, 0), (0, 1))}
    # part linear in a, b^0: coefficient of a^1 b^0
    A1 = R2_.from_dict({(0, 0) + m[2:]: co for m, co in q.terms() if m[0] == 1 and m[1] == 0})
    A0b2 = R2_.from_dict({(0, 0) + m[2:]: co for m, co in q.terms() if m[0] == 0 and m[1] == 2})
    print(lab, "terms", len(p), "->", len(q), "not in (a, b^2): monomials with a^0 b^0 or a^0 b^1:", sum(low.values()),
          "| coeff of a:", sp.factor(A1.as_expr()) if len(A1) < 30 else f"{len(A1)} terms",
          "| coeff of b^2:", sp.factor(A0b2.as_expr()) if len(A0b2) < 30 else f"{len(A0b2)} terms", flush=True)
print(time.time() - t0)
