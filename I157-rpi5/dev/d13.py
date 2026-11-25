import sys, pickle
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
R2_, a, b, v1, v3, v4 = ring("a,b,u1,u3,u4", QQ)
def subst(p):
    out = R2_.zero
    for mon, co in p.terms():
        f, e0, e1, e2, e3, e4 = mon
        out += co * ((a + v1) * QQ(1, 2)) ** e0 * v1 ** e1 * (b - v1) ** e2 * v3 ** e3 * v4 ** e4
    return out
A, B, U1, U3, U4 = sp.symbols("a b u1 u3 u4")
for j, (lab, p) in enumerate(gens):
    q = subst(p)
    # group by (deg a, deg b)
    grp = {}
    for mon, co in q.terms():
        grp.setdefault((mon[0], mon[1]), {})[(mon[2], mon[3])] = co
    print("=====", lab, "terms", len(q), "max deg a", max(m[0] for m in q.monoms()), "max deg b", max(m[1] for m in q.monoms()), "max deg u3", max(m[3] for m in q.monoms()))
    for key in sorted(grp)[:9]:
        e = sum(sp.Rational(int(co.numerator), int(co.denominator)) * U1**k[0] * U3**k[1] for k, co in grp[key].items())
        print("  a^%d b^%d :" % key, sp.factor(e))
