import sys, pickle
sys.path.insert(0, "/home/nathan/Source/negative-mass-i157/notes/warp")
import three_scalars_ideal as I
from sympy import QQ
import sympy as sp
Rn = I.Rn
Qd, Dd = pickle.load(open(sys.argv[1]+"/Qdump.pkl", "rb"))
mk = lambda d: Rn.from_dict({m: QQ(a, b) for m, (a, b) in d.items()})
Q = I.strip_axis({k: mk(v) for k, v in Qd.items()})
for R in ("R1", "R2"):
    for lab, p in I.rung_gens(Q, R):
        degs = [max(m[i] for m in p.monoms()) for i in range(1, 6)]
        print(R, lab, "terms", len(p), "deg u0..u4", degs, "total", max(sum(m) for m in p.monoms()))
for lab, p in I.coef_gens(Q, top=1):
    p = I.normalize(p)
    degs = [max(m[i] for m in p.monoms()) for i in range(1, 6)]
    print("top1", lab, "terms", len(p), "deg", degs)
