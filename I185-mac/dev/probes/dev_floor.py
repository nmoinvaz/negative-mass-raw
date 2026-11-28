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
class Blow(Exception): pass
def rhs(t, y, st):
    F,P = y
    e = np.exp(t)
    c = [f(F,P,e) for f in cq]
    r = np.roots(c)
    ok = np.abs(r.imag) < 1e-7*(1+np.abs(r.real))
    r = r[ok].real
    Q = r[np.argmin(np.abs(r - st["Q"]))]
    st["Q"] = Q
    return [P, Q]
def ev_blow(t,y,st): return 1e6 - abs(y[1])
ev_blow.terminal = True
def run(fi, c, tend=-6000.0):
    j = json.loads(subprocess.run([BIN,"walk",str(fi),str(c)],capture_output=True,text=True).stdout)
    f = j["floor"][-1]
    F,F1,F2v = [v[0] for v in f]; x = j["x_last"]
    P = x*F1; Q = x*x*F2v + P
    st = {"Q": Q}; t0 = np.log(x)
    sol = solve_ivp(rhs, [t0, tend], [F,P], args=(st,), method="DOP853", rtol=1e-12, atol=1e-30, events=ev_blow)
    kap = 2*F/(1-F*F)
    tb_pred = t0 - 2*P**-0.5/np.sqrt(kap) if P>0 and kap>0 else float("nan")
    return dict(t0=t0, F=F, P=P, Q=Q, tend=sol.t[-1], Fend=sol.y[0,-1], Pend=sol.y[1,-1], status=sol.status, tb_pred=tb_pred, signQ=np.sign(Q))
pts = [(0.25,30),(0.25,100),(0.25,300),(0.25,1000),(0.25,3000),(0.5,100),(0.5,300),(0.5,1000),(0.5,3000),(0.75,1000),(0.75,3000),(-0.5,-3000),(-0.5,-1000),(-0.5,-300),(-0.5,-100)]
for fi,c in pts:
    r = run(fi,c)
    print(f"({fi},{c}) F={r['F']:.5g} P={r['P']:.4g} Q={r['Q']:.3g} -> status {r['status']} t_end={r['tend']:.4f} F_end={r['Fend']:.4g} P_end={r['Pend']:.3g}  t_b_pred={r['tb_pred']:.4f}")
