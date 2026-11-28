import sys
sys.argv=[sys.argv[0]]
sys.path.insert(0,"/Users/nathan/Source/negative-mass-i185/notes/warp")
import conical_eta0 as ce
import numpy as np
for fi,c in ce.FLOOR_PTS:
    r = ce.floor_flow(fi,c,-1.0)
    sol = r["sol"]
    F0,P0 = r["F0"], r["P0"]
    kap = 2*abs(F0)/(1-F0**2)
    line = f"({fi},{c}) fold={r['fold']} tend={r['tend']:.3f} yend={np.round(r['yend'],5)} P0={P0:.3g}"
    for lag in (5,10,20):
        t1 = r["t0"]-lag
        if t1 > sol.t[-1]:
            y1 = sol.sol(t1)
            pred = abs(P0)**-0.5 + np.sqrt(kap)/2*(t1-r["t0"])
            line += f"  lag{lag}: meas/pred={y1[1]**-0.5/pred:.4f}"
    print(line)
