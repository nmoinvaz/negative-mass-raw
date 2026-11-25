import sys, time, pickle
sys.path.insert(0, "/home/nathan/Source/negative-mass-i157/notes/warp")
import three_scalars_ideal as I
from sympy import QQ
Rn = I.Rn
Qd, Dd = pickle.load(open(sys.argv[1]+"/Qdump.pkl", "rb"))
mk = lambda d: Rn.from_dict({m: QQ(a, b) for m, (a, b) in d.items()})
Q = {k: mk(v) for k, v in Qd.items()}; Dt = mk(Dd)
print("Dt", Dt)
# split into even/odd in S
def parts(p):
    A = Rn.from_dict({(m[0], 0) + m[2:]: co for m, co in p.terms() if m[1] == 0})
    B = Rn.from_dict({(m[0], 0) + m[2:]: co for m, co in p.terms() if m[1] == 1})
    return A, B
t0 = time.time()
for k, p in sorted(Q.items()):
    A, B = parts(p)
    for nm, X in (("A", A), ("B", B)):
        if X == 0: continue
        q_, r_ = X.div(Dt)
        print(k, nm, "len", len(X), "quot len", len(q_), "rem len", len(r_) if hasattr(r_, '__len__') else r_, time.time()-t0, flush=True)
