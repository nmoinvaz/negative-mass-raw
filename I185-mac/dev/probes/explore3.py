import sys, json, subprocess
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i185/notes/warp")
sys.argv=[sys.argv[0]]
import sympy as sp, numpy as np
import det_classify as dc
from scipy.integrate import solve_ivp
F0,F1,F2,eta = dc.F0_,dc.F1_,dc.F2_,dc.ETA
N = sp.expand(dc.conical_N())
P = sp.Poly(N, F2)
co = [sp.lambdify((F0,F1,eta), c, "numpy") for c in P.all_coeffs()]
BIN="/Users/nathan/Source/negative-mass-i185/notes/warp/conical_global/target/release/conical_global"
def coefs(f,f1,x): return [c(f,f1,x) for c in co]
def rhs(tau, y, st):
    x,f,f1 = y
    a3,a2,a1,a0 = coefs(f,f1,x)
    r = np.roots([1.0, a2, a1*a3, a0*a3*a3])
    r = r[np.abs(r.imag) < 1e-9*(1+np.abs(r.real))].real
    w = r[np.argmin(np.abs(r - st["w"]))]
    st["w"] = w
    return [a3, f1*a3, w]
def run(fi, c, xs, tau_end, label):
    out = subprocess.run([BIN,"walk",str(fi),str(c),str(xs),"30","1e-30","0.01"],capture_output=True,text=True).stdout
    j = json.loads(out.strip().splitlines()[-1])
    print(label, "walk:", j)
    s = j["state"]
    F,F1,F2v = [v[0] for v in s]; x = j["x"]
    a3,a2,a1,a0 = coefs(F,F1,x)
    st = {"w": a3*F2v}
    ev = lambda t,y,st: 1
    sol = solve_ivp(rhs, [0,tau_end], [x,F,F1], args=(st,), method="DOP853", rtol=1e-12, atol=1e-14, dense_output=False, t_eval=np.linspace(0,tau_end,41))
    print(sol.status, sol.message)
    for t,(xx,ff,ff1) in zip(sol.t, sol.y.T):
        a3,a2,a1,a0 = coefs(ff,ff1,xx)
        print(f"  tau={t:8.3f} x={xx:.12f} F={ff:.9f} F'={ff1:.9f} kappa={ff*ff-xx*xx-1:+.3e} a2={a2:+.3e} a3={a3:+.3e}")
run(1.5, 3000, 1.1000625307577954+1e-3, 40, "(1.5,3000)")
