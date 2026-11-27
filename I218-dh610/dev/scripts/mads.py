"""dev: radial modes of the M-AdS wormholes (c > 0): Dirichlet (Y -> const) at the AdS end, analytic throat crossing"""
import sys, math, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, "/home/nathan/Source/negative-mass-i218/notes/black_universe")
import stability as st

RES = {"R1": dict(rtol=1e-9, rmax0=150.0, rmaxW=30.0, delta=0.3, nW=60, ads=1.0),
       "R2": dict(rtol=1e-12, rmax0=300.0, rmaxW=45.0, delta=0.2, nW=150, ads=2.0)}

def Aexact(fam, r):
    return fam.A(r)

def ads_start(fam, W, p):
    """rho0 and (Y, Y') from the Dirichlet series Y = 1 + y2/rho^2 + y4/rho^4 at the AdS end"""
    c = fam.c
    r0 = -p["ads"] * max(100.0, 400.0 * W / c, 100.0 / math.sqrt(c))
    y2 = (W**2 - 4 * c**2 - 4 * c) / (24 * c**2)
    y4 = (W**4 - 40 * W**2 * c + 272 * c**4 + 416 * c**3 + 24 * c**2 * (4 - 3 * W**2)) / (1920 * c**4)
    Y = 1 + y2 / r0**2 + y4 / r0**4
    Yp = -2 * y2 / r0**3 - 4 * y4 / r0**5
    return r0, Y, Yp

def rhs_rho(fam, W):
    e = fam.eps
    def f(r, s):
        Y, Yr = s
        A = fam.A(r); Ap = fam.Ap(r); R2 = r * r + 1
        P1 = -2 * e / (r * R2) + 2 * r / R2 - Ap / A
        P0 = -e / R2**2 + e * Ap / (A * r * R2) - 2 / (A * R2)
        return [Yr, P1 * Yr + P0 * Y + W * W * Y / A**2]
    return f

def left_ads(fam, W, rm, p):
    r0, Y, Yp = ads_start(fam, W, p)
    d = p["delta"]; rtol = p["rtol"]
    s = np.array([Y, Yp]); s /= np.hypot(*s)
    # real ro-form from r0 up to -d (renormalize in chunks)
    f = rhs_rho(fam, W)
    r = r0; ln = 0.0
    while r < -d - 1e-12:
        r2 = min(-d, r + max(5.0, abs(r) * 0.5))
        sol = solve_ivp(f, [r, r2], s, method="DOP853", rtol=rtol, atol=[1e-30, 1e-30])
        s = sol.y[:, -1]; s /= np.hypot(*s); r = r2
    # throat: arc in the upper half plane from -d to +d
    Yl, Yrl = s
    sol = solve_ivp(lambda th, y: st.rhs_arc(fam, W, d)(th, y), [np.pi, 0.0], [Yl + 0j, Yrl + 0j], method="DOP853", rtol=rtol, atol=1e-30)
    Yc, Yrc = sol.y[:, -1]
    flag = (np.sign(Yl) == np.sign(Yc.real), abs(Yc.imag) / abs(Yc))
    # x-form from +d to rm : state (rho, Y, Y_x), Y_x = A Y'
    st0 = np.array([d, Yc.real, (Yrc * fam.A(d)).real]); st0[1:] /= np.hypot(st0[1], st0[2])
    stop = st.make_ev(lambda x, ss: ss[0] - rm, 1, True)
    s, ln, nn = st.run_chunks(st.rhs_x(fam, W), st0, +1, W, rtol, [1e-12, 1e-30, 1e-30], stop, None)
    return s[0], s[1], s[2], flag

def mismatch(fam, W, p):
    rm = 1.0
    _, Yl, Ylx, flag = left_ads(fam, W, rm, p)
    # right solution from stability.py with matching RES keys
    fam.res = dict(rtol=p["rtol"], rmax0=p["rmax0"], rmaxW=p["rmaxW"], delta=p["delta"])
    _, Yr, Yrx, _ = st.right_solution(fam, W, rm)
    return Yl * Yrx - Ylx * Yr

def scan(c, res, W_lo=0.01, W_hi=8.0, log=print):
    p = RES[res]
    fam = st.Fam(c, "R2")
    Ws = np.exp(np.linspace(math.log(W_lo), math.log(W_hi), p["nW"]))
    t0 = time.time()
    D = np.array([mismatch(fam, W, p) for W in Ws])
    roots = []
    for i in range(len(Ws) - 1):
        if np.sign(D[i]) != np.sign(D[i + 1]):
            roots.append(brentq(lambda W: mismatch(fam, W, p), Ws[i], Ws[i + 1], xtol=1e-13, rtol=1e-12))
    return roots, D, Ws, time.time() - t0

if __name__ == "__main__":
    c = float(sys.argv[1]); res = sys.argv[2]
    roots, D, Ws, el = scan(c, res)
    print("c=%g %s: roots %s  (%.1fs)" % (c, res, roots, el))
    print("D signs first/last:", np.sign(D[0]), np.sign(D[-1]), " W^2 of roots:", [r * r for r in roots])
