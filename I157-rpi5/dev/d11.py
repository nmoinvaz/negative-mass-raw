import sys, pickle, time, subprocess
sys.path.insert(0, "/home/nathan/Source/negative-mass-i157/notes/warp")
import three_scalars_ideal as I
from sympy import QQ
from fractions import Fraction
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
names = ["a", "b", "u1", "u3", "u4"]
def sp_(q):
    parts = []
    for mon, co in sorted(q.terms(), reverse=True):
        co = Fraction(int(co.numerator), int(co.denominator))
        vs = "*".join(f"{n}^{e}" if e > 1 else n for n, e in zip(names, mon) if e)
        body = (str(abs(co.numerator)) + ("/" + str(co.denominator) if co.denominator != 1 else "")) if (abs(co) != 1 or not vs) else ""
        parts.append(("-" if co < 0 else "+") + body + ("*" if body and vs else "") + vs)
    o = "".join(parts)
    return o[1:] if o.startswith("+") else o
G = [subst(p) for _, p in gens]
src = "short = 0;\nring R = (0,u1),(a,b,u3),dp;\noption(redSB);\nideal I = " + ",\n ".join(sp_(q) for q in G) + ";\n" + '''
int t0 = rtimer;
ideal GB = std(I);
print("STD_DONE seconds " + string(rtimer - t0));
print(GB);
'''
open(sys.argv[1]+"/par1.sing", "w").write(src + "quit;\n")
t = time.time()
p = subprocess.run(["Singular", "-q", sys.argv[1]+"/par1.sing"], capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL)
print("wall", time.time() - t)
print(p.stdout[:3000]); print(p.stderr[:1000])
