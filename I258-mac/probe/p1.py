# probe 1: slice constraint operators H and M on exact pure-gauge solutions (c=-1)
import sys, math, numpy as np
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i258/notes/black_universe")
sys.argv = [sys.argv[0]]
import horizon_sector as hs
import linear as lin
kc = hs.KChart(-1.0)
par, tab = kc.par, kc.tab
eps = -1.0

def jets(V, U):
    return hs.jetsK(V, U, par, tab, 0.0)

def gauge(V, U, xi, eta):
    # xi, eta: callables returning (value, derivative)
    x, xp = xi(V); e, ep = eta(U)
    return hs.gaugeK(par, tab, V, U, x, xp, e, ep)

xi  = lambda V: (0.3 + 0.7*V + 0.2*V*V + 0.1*V**3, 0.7 + 0.4*V + 0.3*V*V)
eta = lambda U: (-0.2 + 0.5*U - 0.3*U*U + 0.15*U**3, 0.5 - 0.6*U + 0.45*U*U)

h = 1e-3
def fd(f, s, dV, dU, k=1):
    # directional first derivative along (dV,dU) in units where step = h: 4th order
    g = lambda m: f(s + m*h*dV, -s + m*h*dU)  # careful: f takes (V,U)
    return None

def field(s, a, b):
    # value of gauge solution at (V,U)=(s+a, -s+b)
    return gauge(s + a, -s + b, xi, eta)

def deriv(s, comp, dirv, order=1):
    # derivative along direction dirv=(dV,dU), central 4th order stencil, step h
    dV, dU = dirv
    vals = [field(s, m*h*dV, m*h*dU)[comp] for m in (-2,-1,0,1,2)]
    if order == 1:
        return (vals[0] - 8*vals[1] + 8*vals[3] - vals[4]) / (12*h)
    return (-vals[0] + 16*vals[1] - 30*vals[2] + 16*vals[3] - vals[4]) / (12*h*h)

T = (1.0, -1.0); N = (1.0, 1.0)
for s in (0.05, 0.4, 1.0, 1.7):
    x, d, r, rV, rU, pV, pU, V0, V1, V2, E, FV, FU, rhoV, rhoU = jets(s, -s)
    # background derivatives wrt Pi: r' = rV / s,  F' = FV/s, phi' = pV/s
    rp, Fp, php = rV/s, FV/s, pV/s
    dr = field(s,0,0)[0]; dF = field(s,0,0)[1]; dp = field(s,0,0)[2]
    drT = deriv(s,0,T); dFT = deriv(s,1,T); dpT = deriv(s,2,T)
    drTT = deriv(s,0,T,2)
    drN = deriv(s,0,N); dFN = deriv(s,1,N); dpN = deriv(s,2,N)
    # d_s of drN along slice: compute drN at s +- h via direct
    def drN_at(sv):
        vals = [field(sv, m*h, m*h)[0] for m in (-2,-1,1,2)]
        return (vals[0] - 8*vals[1] + 8*vals[2] - vals[3])/(12*h)
    drTN = (-drN_at(s+2*h) + 8*drN_at(s+h) - 8*drN_at(s-h) + drN_at(s-2*h))/(12*h)
    # delta r_VU from the evolution equation: use B0, Bp, Bm
    B0 = np.zeros((3,3)); Bp = np.zeros((3,3)); Bm = np.zeros((3,3))
    hs.coefK(s, -s, par, tab, 0.0, B0, Bp, Bm)
    u = np.array([dr, dF, dp]); uV = np.array([(deriv(s,q,T)+deriv(s,q,N))/2 for q in range(3)]); uU = np.array([(deriv(s,q,N)-deriv(s,q,T))/2 for q in range(3)])
    drVU = (B0 @ u + Bp @ uV + Bm @ uU)[0]
    H = drTT + 2*drVU + s*Fp*drT + s*rp*dFT + eps*s*s*php*php*dr + eps*r*s*php*dpT
    M = drTN + s*Fp*drN + s*rp*dFN + eps*r*s*php*dpN
    # direct constraints
    drVV = (deriv(s,0,T,2) + 2*0)  # placeholder
    print(f"s={s}: H={H:.3e} M={M:.3e}   scales |drTT|={abs(drTT):.2e} |drTN|={abs(drTN):.2e}")
