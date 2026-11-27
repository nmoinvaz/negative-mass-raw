import sys, os, numpy as np
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i255/notes/wormhole_evolution"))
import throat_locus as tl, dn, threshold
from scipy.optimize import curve_fit
raw = os.path.expanduser("~/Source/negative-mass-raw/I225-dh610/runs/stall")
def load(D, h):
    La = tl.load_run(f"{raw}/stall_D{D}_h{h}_side-1.npz"); Lb = tl.load_run(f"{raw}/stall_D{D}_h{h}_side1.npz")
    common = np.intersect1d(La["s"], Lb["s"]); ia, ib = np.searchsorted(La["s"], common), np.searchsorted(Lb["s"], common)
    mean = lambda k: 0.5*(La[k][ia]+Lb[k][ib])
    return dict(t=mean("t"), tau=mean("tau"), r=mean("r"), l=mean("l"), f=mean("f"), v=mean("v"), odd=0.5*(Lb["r"][ib]-La["r"][ia]))
def rdot(tau, r, win=0.5):
    out = np.full(len(r), np.nan)
    dt = np.median(np.diff(tau)); k = max(2, int(round(win/dt)))
    for i in range(k, len(r)-k, max(1,k//10)):
        out[i] = np.polyfit(tau[i-k:i+k+1], r[i-k:i+k+1], 1)[0]
    return out
for D, hs in ((5, "0.00176777"), (4, "0.005")):
    d = load(D, hs)
    rd = rdot(d["tau"], d["r"])
    ok = np.isfinite(rd) & (d["t"] >= 6.5) & (d["t"] <= 12.0) & (abs(d["odd"]) < 1e-3)
    tau, y = d["tau"][ok], rd[ok]
    f = lambda x, a, c, kap: a + c*np.exp(-kap*(x-tau[0]))
    try:
        p, cov = curve_fit(f, tau, y, p0=[y[-1], y[0]-y[-1], 0.5])
        print(f"D={D} h={hs}: rdot_inf {p[0]:+.5f} c {p[1]:+.5f} kappa {p[2]:.4f}; window t in [{d['t'][ok][0]:.2f},{d['t'][ok][-1]:.2f}] n={ok.sum()} rms resid {np.sqrt(np.mean((f(tau,*p)-y)**2)):.2e}; se {np.sqrt(np.diag(cov))}")
    except Exception as e:
        print("fit fail", D, e)
    for tt in (6, 7, 8, 9, 10, 11, 12, 13):
        k = np.argmin(abs(d["t"]-tt)); print(f"   t={d['t'][k]:.2f} tau {d['tau'][k]:.3f} r {d['r'][k]:.5f} rdot {rd[k]:+.5f} odd {d['odd'][k]:+.1e}")
# energies on the initial ray
for D in (4, 5):
    n = D-2
    h = 0.001
    N = int(40/h)
    for B in (0.1,):
        s = np.arange(N+1)*h
        sol, q = dn.ellis_dense(n, 40/np.sqrt(2)+2)
        r = sol(s/np.sqrt(2))[0]
        w, xc = 0.5, 3.0
        g = np.exp(-(s-xc)**2/(2*w*w)); gs = -(s-xc)/(w*w)*g
        I2 = np.trapezoid(r**n*gs**2, s); I1 = np.trapezoid(r**n*gs, s)
        print(f"D={D}: I2 = int r^n g_s^2 ds = {I2:.5f}; I1 = int r^n g_s ds = {I1:.5f}; r(3) {sol(3/np.sqrt(2))[0]:.4f}")
