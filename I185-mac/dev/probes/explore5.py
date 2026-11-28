import sys, json, subprocess
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i185/notes/warp")
sys.argv=[sys.argv[0]]
import sympy as sp, numpy as np
import det_classify as dc
from scipy.integrate import solve_ivp
F0,F1,F2,eta = dc.F0_,dc.F1_,dc.F2_,dc.ETA
N = sp.expand(dc.conical_N())
Fs,Ps,Qs,es = sp.symbols("F P Q e")
Nt = sp.expand(sp.expand(N.subs({F0:Fs, F1:Ps/es, F2:(Qs-Ps)/es**2, eta:es}))*es**4)
pq = sp.Poly(Nt, Qs)
cq = [sp.lambdify((Fs,Ps,es), c, "numpy") for c in pq.all_coeffs()]
BIN="/Users/nathan/Source/negative-mass-i185/notes/warp/conical_global/target/release/conical_global"
def rhs(t, y, st):
    F,P = y
    e = np.exp(t)
    c = [f(F,P,e) for f in cq]
    r = np.roots(c)
    r = r[np.abs(r.imag) < 1e-9*(1+np.abs(r.real))].real
    Q = r[np.argmin(np.abs(r - st["Q"]))]
    st["Q"] = Q
    return [P, Q]
def run(fi, c, tend, label):
    j = json.loads(subprocess.run([BIN,"walk",str(fi),str(c)],capture_output=True,text=True).stdout)
    f = j["floor"][-1] if j["floor"] else None
    if f is None: print(label, "no floor", j["class"], j["kind"]); return
    F,F1,F2v = [v[0] for v in f]; x = j["x_last"]
    P = x*F1; Q = x*x*F2v + P
    st = {"Q": Q}
    t0 = np.log(x)
    print(label, "start t0=%.3f F=%.6g P=%.6g Q=%.6g"%(t0,F,P,Q))
    sol = solve_ivp(rhs, [t0, tend], [F,P], args=(st,), method="DOP853", rtol=1e-12, atol=1e-30, t_eval=np.linspace(t0,tend,9))
    print("  status", sol.status, sol.message[:60])
    for t,(FF,PP) in zip(sol.t, sol.y.T):
        print(f"   t={t:10.2f} F={FF:.8g} P={PP:.6g}  P*t^2={PP*t*t:.5g}  P^-1/2={PP**-0.5 if PP>0 else float('nan'):.5g}")
for fi,c in ((0.25,3000),(0.5,100),(0.25,1000),(0.75,300),(-0.5,-100)):
    run(fi,c,-2000.0,f"({fi},{c})")
