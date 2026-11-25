import sys
sys.argv = ["x"]
sys.path.insert(0, "/home/nathan/Source/negative-mass-i161/notes/warp")
import sympy as sp
import planar_closure as pc
xi = sp.Symbol("xi", real=True)
for lab, uu in [("u1", (1 - 1 / (1 + xi**2)**2) / 2), ("u2", 1 / (2 * (1 + xi**2))), ("u3", 1 / (3 * (1 + xi**2)**2))]:
    K = sp.factor(sp.diff(uu * sp.diff(uu, xi), xi))
    print(lab, "K =", K)
    for pt in [sp.Rational(1, 3), 1, sp.Rational(3, 2), 2, sp.Rational(5, 2)]:
        print("   xi =", pt, " K =", sp.simplify(K.subs(xi, pt)), " C =", sp.simplify(pc.C_static(uu, xi).subs(xi, pt)) if sp.simplify(K.subs(xi, pt)) != 0 else "n/a (K = 0)")
