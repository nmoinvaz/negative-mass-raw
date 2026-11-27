import sys, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i232/notes/black_universe")
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i232/notes/wormhole_evolution")
import numpy as np, linear as L
import dev_nl_lib as D
c = -1.0
mem = L.ep.Member(c); b = mem.kappa*math.sqrt(2)
print("class R (right-ray pulse, left ray zero): horizon value and late Y against h")
prev = None
for h in (0.02, 0.01, 0.005):
    s = L.Setup(c, h, 14.0, dict(R=(1e-3, 3.0, 0.5)))
    r = s.run(xs=(0.0,))
    yh = r["Yh"]; t = r["t"][0]; y = r["Y"][0]
    i18 = np.argmin(abs(t-18)); 
    print(f"h={h}: Yh(p=14) = {yh[-1]:.4e}, Yh(p=10) = {yh[int(10/h)]:.4e}, |Y(x=0,t=18)| = {abs(y[i18]):.4e}", "" if prev is None else f"  ratio Yh(14): {prev[0]/yh[-1]:.3f}")
    prev = (yh[-1],)
print("nonlinear untuned drift (even part of Y on the diagonal), c=-1, against h")
for h in (0.02, 0.01, 0.005):
    su = L.Setup(c, h, 14.0, dict(R=(1e-9, 3.0, 0.5)))
    tn, yn, ye = D.nl_response(su)
    out = []
    for tt in (8, 10, 12):
        i = np.argmin(abs(tn - tt)); out.append(ye[i])
    print(f"h={h}: drift at t=8,10,12:", " ".join(f"{x:.3e}" for x in out), "  rate [8,12]:", f"{L.window_rate(tn, ye, 8, 12):.4f}")
