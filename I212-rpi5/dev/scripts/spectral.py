"""dev: independent spectral (Chebyshev collocation) eigenvalue check of  Y_xx = Cx Y_x + Dx Y + W^2 Y"""
import sys
sys.path.insert(0, '/home/nathan/Source/negative-mass-i212/notes/black_universe')
import numpy as np
from scipy.integrate import solve_ivp
import stability as st

def cheb(N):
    x = np.cos(np.pi*np.arange(N+1)/N)
    c = np.hstack([2, np.ones(N-1), 2])*(-1)**np.arange(N+1)
    X = np.tile(x, (N+1, 1)).T
    dX = X - X.T
    D = np.outer(c, 1/c)/(dX + np.eye(N+1))
    D = D - np.diag(D.sum(axis=1))
    return D, x

def grid(fam, XL, XR, N):
    D, xc = cheb(N)
    x = (XR - XL)/2 + (XR + XL)/2*xc        # nodes in [-XL, XR], decreasing
    # rho(x), A, A/rho, A' at nodes
    if fam.rh is None:                      # Ellis: rho = x, A = 1
        rho = x.copy(); A = np.ones_like(x); Ar = A/rho; Ap = np.zeros_like(x)
        return D*2/(XL + XR), x, rho, A, Ar, Ap
    # reference point x = 0 <-> rho_ref
    rref = 0.0 if fam.rh < 0 else fam.rh + 1.0
    order = np.argsort(x)
    xs = x[order]
    rho = np.empty_like(x); A = np.empty_like(x); Ar = np.empty_like(x)
    # integrate zeta = ln z for x<0 side (toward horizon), rho for x>0
    zref = rref - fam.rh
    # left side: x from 0 down to -XL in zeta variable
    fz = lambda xx, s: [fam.a_over_z(np.exp(s[0]))]
    neg = xs[xs < 0]; pos = xs[xs >= 0]
    z_of = {}
    if len(neg):
        sol = solve_ivp(fz, [0, -XL*1.0001], [np.log(zref)], method='DOP853', rtol=1e-13, atol=1e-13, t_eval=neg[::-1])
        zl = np.exp(sol.y[0])[::-1]
        z_of_neg = dict(zip(neg, zl))
    if len(pos):
        fr = lambda xx, s: [fam.A(fam.rh + np.exp(s[0])) / np.exp(s[0])]
        sol = solve_ivp(fr, [0, XR*1.0001], [np.log(zref)], method='DOP853', rtol=1e-13, atol=1e-13, t_eval=pos)
        zp = np.exp(sol.y[0])
        z_of_pos = dict(zip(pos, zp))
    z = np.array([z_of_neg[v] if v < 0 else z_of_pos[v] for v in x])
    rho = fam.rh + z
    at = np.array([fam.a_over_z(v) for v in z])
    A = z*at
    Ar = at if fam.rh == 0.0 else A/rho
    Ap = fam.Ap(rho)
    return D*2/(XL + XR), x, rho, A, Ar, Ap

def spectrum(c, N=401, XL=45.0, XR=45.0, uform=False):
    fam = st.Fam(c, 'R2')
    D1, x, rho, A, Ar, Ap = grid(fam, XL, XR, N)
    print('min |rho| on grid', np.min(np.abs(rho)))
    D2 = D1 @ D1
    if uform:
        R2 = rho*rho + 1
        Vh = 2*Ar**2 - (1 + 1/R2)*Ar*Ap + A*A/R2**2 - 2*A/R2
        L = D2 - np.diag(Vh)
    else:
        Cx, Dx = st.coef_x(fam, rho, A, Ar, Ap)
        L = D2 - Cx[:, None]*D1 - np.diag(Dx)
    Li = L[1:-1, 1:-1]
    ev = np.linalg.eigvals(Li)
    return ev

if __name__ == '__main__':
    c = float(sys.argv[1]); N = int(sys.argv[2]); XL = float(sys.argv[3]); XR = float(sys.argv[4])
    ev = spectrum(c, N, XL, XR, uform=(c <= -1.0))
    pos = ev[(ev.real > 1e-4) & (ev.real < 100)]
    print('eigenvalues with 1e-4 < Re lambda < 100:')
    for e in sorted(pos, key=lambda z: z.real):
        print('  lambda =', e, ' W =', np.sqrt(e))
