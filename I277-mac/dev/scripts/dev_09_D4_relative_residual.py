import sys, math, numpy as np
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i277/notes/black_universe")
import planted_family as pf
# relative constraint residual of the stored ray data, central differences, per h, and with the nojac mutation
for nojac in (False, True):
    for c, beta in pf.CASES:
        fam = pf.Family(c, beta)
        out = []
        for h in pf.HS:
            Np, Nm = int(round(pf.XP[c] / h)), int(round(pf.XM / h))
            Sp, Sm, _ = pf.ray_data(fam, pf.RHO_C, pf.V0, Np, h, Nm, nojac=nojac)
            cs = []
            for S in (Sp, Sm):
                r, f, p = S
                rpp = (r[2:] - 2 * r[1:-1] + r[:-2]) / h ** 2
                fp = (f[2:] - f[:-2]) / (2 * h)
                rp = (r[2:] - r[:-2]) / (2 * h)
                pp = (p[2:] - p[:-2]) / (2 * h)
                t = np.stack([rpp, fp * rp, -0.5 * r[1:-1] * pp ** 2])
                cs.append(float((np.abs(t.sum(axis=0)) / np.abs(t).max(axis=0)).max()))
            out.append(cs)
        print(f"nojac={nojac} c={c} beta={beta:+}: rel C++ " + " ".join(f"{o[0]:.2e}" for o in out) + " | rel C-- " + " ".join(f"{o[1]:.2e}" for o in out), flush=True)
