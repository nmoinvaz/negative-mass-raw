"""dev13: quadratic fit of w(eps) - 1 = s1 eps + s2 eps^2 (+ s3 eps^3 as a control) to #212's rates at c = -1 +- {1e-2, 1e-3, 1e-4}, from the stored logs of dev06."""
import json, sys
import numpy as np
for res in ("R1", "R2"):
    rows = [json.loads(l) for l in open("dev06_wc_%s.log" % res) if l.startswith("{")]
    sel = [r for r in rows if round(abs(r["eps"]), 6) in (0.01, 0.001, 0.0001)]
    eps = np.array([r["eps"] for r in sel]); y = np.array([r["w"] - 1 for r in sel])
    for deg, name in ((2, "second order"), (3, "third order")):
        # least squares of y / eps on 1, eps, ..., eps^(deg-1), relative weights
        Mx = np.vstack([eps ** k for k in range(1, deg + 1)]).T
        wgt = 1 / eps ** 2                            # fit y with relative weight 1/eps (errors of W are absolute)
        coef = np.linalg.lstsq(Mx / eps[:, None] , y / eps, rcond=None)[0]
        print(res, name, "points", len(sel), " s1 =", coef[0], " s2 =", coef[1], " s3 =" if deg == 3 else "", coef[2] if deg == 3 else "")
