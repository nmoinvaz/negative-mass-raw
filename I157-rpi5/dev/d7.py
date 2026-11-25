import sys, time, pickle
sys.path.insert(0, "/home/nathan/Source/negative-mass-i157/notes/warp")
import sympy as sp
import three_scalars_ideal as I
from sympy import QQ
Rn = I.Rn
Qd, Dd = pickle.load(open(sys.argv[1]+"/Qdump.pkl", "rb"))
mk = lambda d: Rn.from_dict({m: QQ(a, b) for m, (a, b) in d.items()})
Q = {k: mk(v) for k, v in Qd.items()}; Dt = mk(Dd)
g = I.rung_gens(Q, "R1")
for lab, p in g:
    e = p.as_expr()
    fl = sp.factor_list(e)
    print(lab, len(p), [(len(sp.Poly(f, *sp.symbols("s u0 u1 u2 u3 u4")).terms()), m, str(f)[:70]) for f, m in fl[1]], flush=True)
