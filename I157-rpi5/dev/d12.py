import sys, pickle, time, itertools
sys.path.insert(0, "/home/nathan/Source/negative-mass-i157/notes/warp")
import three_scalars_ideal as I
from sympy import QQ
Rn = I.Rn
Qd, Dd = pickle.load(open(sys.argv[1]+"/Qdump.pkl", "rb"))
mk = lambda d: Rn.from_dict({m: QQ(a, b) for m, (a, b) in d.items()})
Q = I.strip_axis({k: mk(v) for k, v in Qd.items()})
gens = I.rung_gens(Q, "Rk22")
print([l for l, _ in gens])
prog = '''
int t0 = rtimer;
ideal G = std(I);
print("STD_DONE size " + string(size(G)) + " dim " + string(dim(G)) + " seconds " + string(rtimer - t0));
print(G);
'''
subsets = [(0, 1), (0, 1, 2), (0, 1, 3), (0, 1, 2, 3), (1, 2, 3), (0, 2, 3)]
for sub in subsets:
    g = [gens[i] for i in sub] + [("sat", I.SAT)]
    out, wall = I.run_singular("dev_K22sub" + "".join(map(str, sub)) + "_p32003", g, prog, timeout=240, char=32003)
    print(sub, "wall", round(wall), (out or "TIMEOUT")[:400].replace("\n", " | "), flush=True)
