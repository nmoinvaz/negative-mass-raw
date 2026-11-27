import sys, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i232/notes/black_universe")
import numpy as np, linear as L

c = float(sys.argv[1]) if len(sys.argv) > 1 else -1.0
h = float(sys.argv[2]) if len(sys.argv) > 2 else 0.01
P = 14.0
mem = L.ep.Member(c); kap = mem.kappa; b = kap * math.sqrt(2)
amp = 1e-3
sets = {"A": dict(L=(amp, 2.5, 0.5)), "B": dict(L=(amp, 3.5, 0.5)), "C": dict(L=(amp, 4.5, 0.5)), "R": dict(R=(amp, 3.0, 0.5))}
res = {}
for k, spec in sets.items():
    s = L.Setup(c, h, P, spec)
    r = s.run(xs=(0.0,))
    res[k] = (s, r)
    p = r["p"]; yh = r["Yh"]
    # fit Yh = c1 + c2 exp(b p) over p in [1, P]
    m = (p >= 1.0)
    Mx = np.vstack([np.ones(m.sum()), np.exp(b * p[m])]).T
    coef_, *_ = np.linalg.lstsq(Mx / np.abs(yh[m])[:, None], yh[m] / np.abs(yh[m]), rcond=None)
    resid = np.max(np.abs(Mx @ coef_ - yh[m]) / np.abs(yh[m]))
    print(f"set {k}: Yh fit c1 = {coef_[0]:+.4e}, c2 = {coef_[1]:+.4e}, max rel resid {resid:.2e}; |Y|(x=0, t=14) = {abs(r['Y'][0][np.argmin(abs(r['t'][0]-14))]):.3e}")
# projection: Y_comb = YA + l1 YB + l2 YC with (c1, c2) cancelled
def cfit(k):
    r = res[k][1]; p = r["p"]; yh = r["Yh"]; m = p >= 1.0
    Mx = np.vstack([np.ones(m.sum()), np.exp(b * p[m])]).T
    return np.linalg.lstsq(Mx, yh[m], rcond=None)[0]
cA, cB, cC = cfit("A"), cfit("B"), cfit("C")
Mat = np.array([[cB[0], cC[0]], [cB[1], cC[1]]])
lam = np.linalg.solve(Mat, -cA)
print("lambdas", lam)
tA = res["A"][1]["t"][0]
Ycomb = res["A"][1]["Y"][0] + lam[0] * res["B"][1]["Y"][0] + lam[1] * res["C"][1]["Y"][0]
Yhc = res["A"][1]["Yh"] + lam[0] * res["B"][1]["Yh"] + lam[1] * res["C"][1]["Yh"]
for tt in (6, 8, 10, 12, 14, 16, 18):
    i = np.argmin(abs(tA - tt))
    print(f"t={tA[i]:5.2f}  |Y_A|={abs(res['A'][1]['Y'][0][i]):.3e}  |Y_comb|={abs(Ycomb[i]):.3e}   Yh_A={res['A'][1]['Yh'][i]:+.3e} Yh_comb={Yhc[i]:+.3e}")
print("comb rates [6,10] [10,14] [14,18]:", [f"{L.window_rate(tA, Ycomb, a, a+4):.4f}" for a in (6, 10, 14)], " kappa =", f"{kap:.5f}")
# late-time profile slope: Y e^{-kappa t} against x at the last stored row
su, rr = res["A"]
