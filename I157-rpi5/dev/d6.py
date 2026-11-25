import sys, time, pickle
sys.path.insert(0, "/home/nathan/Source/negative-mass-i157/notes/warp")
import sympy as sp
import three_scalars_ideal as I
from sympy import QQ
Rn = I.Rn
Qd, Dd = pickle.load(open(sys.argv[1]+"/Qdump.pkl", "rb"))
mk = lambda d: Rn.from_dict({m: QQ(a, b) for m, (a, b) in d.items()})
Q = {k: mk(v) for k, v in Qd.items()}; Dt = mk(Dd)
fl = sp.factor_list(Dt.as_expr())
print("factors of det:", [(len(sp.Poly(g).terms()), m, str(g)[:80]) for g, m in fl[1]], fl[0])
facs = [(Rn.from_expr(g), m) for g, m in fl[1]]
def parts(p):
    A = Rn.from_dict({(m[0], 0) + m[2:]: co for m, co in p.terms() if m[1] == 0})
    B = Rn.from_dict({(m[0], 0) + m[2:]: co for m, co in p.terms() if m[1] == 1})
    return A, B
for k, p in sorted(Q.items()):
    A, B = parts(p)
    row = []
    for (g, m) in facs:
        mult = 0
        cur = [x for x in (A, B) if x != 0]
        while True:
            qs = [x.div(g) for x in cur]
            if all(r_ == 0 for _, r_ in qs):
                mult += 1
                cur = [q_ for q_, _ in qs]
                if mult > 6: break
            else:
                break
        row.append(mult)
    print(k, "divisibility multiplicities by det's factors:", row, flush=True)
