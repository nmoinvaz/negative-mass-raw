import sys
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i185/notes/warp")
sys.argv=[sys.argv[0]]
import sympy as sp, mpmath as mp
import det_classify as dc
F0,F1,F2,eta = dc.F0_,dc.F1_,dc.F2_,dc.ETA
N = sp.expand(dc.conical_N())
P = sp.Poly(N, F2)
co = [sp.lambdify((F0,F1,eta), c, "mpmath") for c in P.all_coeffs()]  # a3,a2,a1,a0
mp.mp.dps=30
data = {"(1.5,3000)": (1.1000635092399922, 1.4866535050756886, 3.646460486934916e-1, -5.3731825559191375e3, 1.1000625307577954),
        "(2,3000)": (1.708540628786698, 1.9796740664619765, 4.2720147841700107e-1, -4.417212183323207e3, 1.7085396459675593)}
for k,(x,f,f1,f2,xs) in data.items():
    a = [c(mp.mpf(f),mp.mpf(f1),mp.mpf(x)) for c in co]
    print(k, "x-x*=", x-xs, "kappa=", f*f-x*x-1)
    print("  a3,a2,a1,a0 =", [mp.nstr(v,6) for v in a])
    roots = mp.polyroots(a, maxsteps=200, extraprec=100)
    print("  roots F'':", [mp.nstr(r,8) for r in roots], " actual", f2)
    print("  N at actual:", mp.nstr(sum(a[i]*mp.mpf(f2)**(3-i) for i in range(4)),6))
    # at kappa=0 exactly
    print("  -a2/a3 =", mp.nstr(-a[1]/a[0],8), " a2 formula", 2*f1*x**3*(2*f1*(x*x+1)-f))
