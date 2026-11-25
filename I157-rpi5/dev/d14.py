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
body = "ideal I = " + ",\n ".join(sp_(q) for q in G) + ", 1-s*u1;\n"
prog = '''
int t0 = rtimer;
ideal GB = std(I);
print("STD_DONE size " + string(size(GB)) + " dim " + string(dim(GB)) + " seconds " + string(rtimer - t0));
if (size(GB) < 8) { print(GB); }
'''
for tag, order in (("dp", "dp"), ("wp_a2b1", "wp(1,1,1,2,1)"), ("Dp", "Dp"), ("ab_first", "(dp(2),dp(3))")):
    var = "s,u1,u3,u4,a,b" if tag in ("dp","wp_a2b1","Dp") else "a,b,s,u1,u3,u4"
    if tag == "wp_a2b1":
        var = "s,u1,u3,u4,a,b"; order = "wp(1,1,1,1,2,1)"
    src = f"short = 0;\nring R = 32003,({var}),{order};\noption(redSB);\n" + body + prog + "quit;\n"
    f = f"{sys.argv[1]}/ord_{tag}.sing"
    open(f, "w").write(src)
    t = time.time()
    try:
        p = subprocess.run(["nice", "-n", "10", "Singular", "-q", f], capture_output=True, text=True, timeout=150, stdin=subprocess.DEVNULL)
        print(tag, "wall", round(time.time() - t), p.stdout.strip().replace("\n", " | ")[:300], p.stderr[:200], flush=True)
    except subprocess.TimeoutExpired:
        print(tag, "TIMEOUT 150 s", flush=True)
