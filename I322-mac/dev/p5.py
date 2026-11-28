import sys, time, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
import numpy as np
from scipy.integrate import quad
import remainder as rm
exec(open("/private/tmp/claude-501/-Users-nathan-Source-negative-mass-i322/07a7c86f-beae-4b72-bf6b-2793fd26190f/scratchpad/p4.py").read().split("I0 = quad")[0].split("sc = rm.hb.sc")[1].join(["sc = rm.hb.sc\n",""]) if False else "")
hs, hb = rm.hs, rm.hb
sc = hb.sc
K = 2/math.pi
A = sc.A_
def Hf2(r):
    def f(s):
        if abs(s) < 1e-4: return 1.0/(4*K)
        return K/A(s) - 0.5/s
    return quad(f, 0, r, epsabs=1e-14, epsrel=1e-13, limit=200)[0]
def integrand2(r):
    if abs(r) < 1e-8: return 1.0
    return 2*K*r*math.exp(-2*Hf2(r))/(A(r)*(1+r*r))
I0 = 1.0149036099284089
names = sys.argv[1].split(","); h = float(sys.argv[2]); VMAX = float(sys.argv[3])
Pis = [-0.1, 0.5, 1.0, 2.0]
Qp = []
for Pi in Pis:
    rho, R = rm.rho_of_Pi(Pi)
    Qp.append(-quad(integrand2, 0, rho, epsabs=1e-13, epsrel=1e-13, limit=200)[0]/I0)
print("Qpred", Qp)
V0, _, U0, U1 = rm.RECT0
rect = (V0, VMAX, U0, U1)
kc = rm.kchart()
Vq = (2, 3, 5, 8, 12, 16, 20, 30, 40)
for name in names:
    spec = hb.CLASSES[name] if name in hb.CLASSES else None
    su = hs.KSetup(-1.0, h, *rect, spec, kc=kc)
    ro = rm.stream_run(su.UL, su.UR, rect, h, Pis)
    cs = rm.c_at_S(ro)
    print(f"== {name} h={h} c = {cs}", flush=True)
    for k, Pi in enumerate(Pis):
        Vj, wr, ws = rm.remainder_series(ro, k, cs)
        w2 = wr - cs[1]*Vj*Qp[k]
        s = []
        for vq in Vq:
            if Vj[0] <= vq <= Vj[-1]:
                jj = np.argmin(np.abs(Vj - vq))
                s.append(f"{vq}:{w2[jj]: .3e}")
        print(f"  Pi={Pi:5.2f} Yrem2/R (units of data)  " + "  ".join(s))
