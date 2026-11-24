import sys, time
sys.argv = ["x"]
sys.path.insert(0, "/home/nathan/Source/negative-mass-i161/notes/warp")
import sympy as sp
import planar_closure as pc
t0 = time.time()
def lap(m): print(f"{m}: {time.time()-t0:.1f}s", flush=True)
t, x = sp.symbols("t x", real=True)
b = sp.Function("b")(t, x)
R = pc.ps.ricci(pc.pg_metric(b), [t, x], lambda E, k: sp.diff(E, [t, x][k]), sp.simplify); lap("ricci pg")
xi = sp.Symbol("xi", real=True); u = sp.Function("u")(xi)
d = pc.C_static(u, xi) - pc.theta_prime(u, xi); lap("build C-theta'")
print(sp.simplify(d), flush=True); lap("simplify C - theta'")
uu = (1 - 1 / (1 + xi**2)**2) / 2
Cx = pc.C_static(uu, xi); lap("C u1 build")
print(sp.simplify(Cx.subs(xi, sp.Rational(1, 3))), flush=True); lap("C u1 at 1/3")
