import sys, time, pickle
sys.path.insert(0, "/home/nathan/Source/negative-mass-i157/notes/warp")
import three_scalars_ideal as I
from sympy import QQ
import sympy as sp
Rn = I.Rn
which = sys.argv[2]
Qd, Dd = pickle.load(open(sys.argv[1]+"/Qdump.pkl", "rb"))
mk = lambda d: Rn.from_dict({m: QQ(a, b) for m, (a, b) in d.items()})
Q = I.strip_axis({k: mk(v) for k, v in Qd.items()})
print("stripped sizes", {k: len(v) for k, v in Q.items()}, flush=True)
prog = '''
int t0 = rtimer;
ideal G = std(I);
if (G[1] == 1) { print("STD_DONE UNIT"); } else { print("STD_DONE notunit size " + string(size(G)) + " dim " + string(dim(G))); }
print("rtimer " + string(rtimer - t0));
if (size(G) < 12) { print(G); }
'''
p = int(sys.argv[3]) if len(sys.argv) > 3 else 32003
if which == "R1":
    g = I.rung_gens(Q, "R1") + [("sat", I.SAT)]
elif which == "R1d":
    # strip u1 powers and the equator det factor Phi' (valid where det h != 0 at the equator): dev probe only
    phi = I.Rs.from_expr(sp.sympify("4*u0**2*u1**2 - u1**4 + u1**2 + 2*u1*u2 + u2**2", locals={}) ) if False else None
    g0 = I.rung_gens(Q, "R1")
    u0_, u1_, u2_ = I.u0, I.u1, I.u2
    Phi = 4*u0_**2*u1_**2 - u1_**4 + u1_**2 + 2*u1_*u2_ + u2_**2
    g = []
    for lab, q in g0:
        while True:
            qq, rr = q.div(u1_)
            if rr == 0: q = qq
            else: break
        while True:
            qq, rr = q.div(Phi)
            if rr == 0: q = qq
            else: break
        g.append((lab + "_stripped", I.normalize(q)))
    g += [("sat", I.SAT)]
elif which == "R2":
    g = I.rung_gens(Q, "R2") + [("sat", I.SAT)]
elif which == "R3" or which.startswith(("Rc", "Rtop", "Rk")):
    g = I.rung_gens(Q, which) + [("sat", I.SAT)]
print(which, "generators", len(g), [len(q) for _, q in g], flush=True)
t = time.time()
out, wall = I.run_singular(f"dev_{which}_p{p}", g, prog, timeout=int(sys.argv[4]) if len(sys.argv) > 4 else 600, char=p)
print(which, "p", p, "wall", wall, "->", out, flush=True)
