"""development probe: does the vac_scalar knob change the scalar plane? (gamma = 10 and 300, l = 5, the crate's star and J tables)"""
import sys
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i196/phase2/nonradial")
import numpy as np
import taylor_drift as T
T.JTABLE_PATH[0] = "/Users/nathan/Source/negative-mass-raw/I196-mac/crate_jtable_l5.jsonl"
steps = "/Users/nathan/Source/negative-mass-raw/I196-mac/crate_star_steps.jsonl"
for g in (10.0, 300.0):
    res = {}
    for pl in ("crate_j", "crate_j_vac"):
        pp = T.build(5, "base", pl, 1e-10, steps)
        calls = []
        orig = pp._integrate_plane
        def spy(Y, ra, rb, s, nchunks=None, Jfun=None, _o=orig, _c=calls):
            _c.append((ra, rb, Jfun is not None and Jfun.__name__ if Jfun is not None else None))
            return _o(Y, ra, rb, s, nchunks, Jfun)
        pp._integrate_plane = spy
        D = pp.D(g)
        S, ph = pp.scalar_plane(g)
        res[pl] = (D, S, pp.vac_scalar, calls)
        print(g, pl, "vac_scalar", pp.vac_scalar, "D", D, "calls", calls)
    print("scalar plane max abs difference", float(np.abs(res["crate_j"][1] - res["crate_j_vac"][1]).max()))
    Jt = T.crate_j(T.JTABLE_PATH[0]).J(24.11, g)
    pp = T.build(5, "base", "crate_j_vac", 1e-10, steps)
    Jv = pp._Jvac(24.11, g)
    print("J table vs vacuum J at r = 24.11 (scalar block), max |diff| / max |J|:", float(np.abs(Jt[2:, 2:] - Jv[2:, 2:]).max() / np.abs(Jv[2:, 2:]).max()))
