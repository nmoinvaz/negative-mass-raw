import sys, time
import numpy as np
sys.argv = [sys.argv[0]] + sys.argv[1:]
from exp1 import *   # B, P, rm, M, lam, V, series, start_series, integ ...
from scipy.integrate import solve_ivp

def fr(r): return 1 - 2*M/r
def integ_ray(s, T, rtol=1e-11, sign=-1):
    """r = rm + sign*1j*p, p from T to 0; y = (Z, fZ') e^{s r*}; start from the series at r = rm + sign i T"""
    R = rm + sign*1j*T
    # series at complex R
    ys = start_series_c(s, R)
    def A(sig):
        p = np.exp(sig) - 1.0
        r = rm + sign*1j*p
        f = fr(r)
        a = (sign*1j)*(1.0 + p)/f*np.array([[s, 1.0], [s*s+V(r), s]])
        return np.block([[a.real, -a.imag], [a.imag, a.real]])
    ya = np.array(ys, dtype=complex)
    sol = solve_ivp(lambda sg, y: A(sg)@y, (np.log(1+T), 0.0), np.r_[ya.real, ya.imag], method='Radau', jac=lambda sg, y: A(sg), rtol=rtol, atol=1e-14)
    return sol.y[0, -1]+1j*sol.y[2, -1], sol.y[1, -1]+1j*sol.y[3, -1], sol.t.size

def start_series_c(s, R):
    u, ux, n, e = series(s, R)
    f = fr(R)
    ur = -ux/R**2
    return np.array([u, f*ur - s*u])

if __name__ == '__main__':
    zf = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    smin = 0.01
    T = zf*(40+20*l)/smin + 50
    Rz = rm + T
    print('T', T, flush=True)
    for s in (0.0001+0.12j, -0.0005+0.12j, -0.001+0.12j, -0.001+0.23j, -0.001+0.01j):
        t0 = time.time()
        yr, pr, nr = integ_ray(s, T)
        t1 = time.time()-t0
        yr2, pr2, nr2 = integ_ray(s, T, rtol=1e-13)
        print(s, 'ray y1', yr, 'q', pr/yr, 'steps', nr, 'time', round(t1, 2), '| rtol13/11-1', abs(yr2/yr-1), flush=True)
        t0 = time.time()
        ys = start_series(s, Rz)[0]
        yz, pz, nz = integ(s, Rz, ys)
        print('   real-r series start y1/ray-1', abs(yz/yr-1), 'steps', nz, 'time', round(time.time()-t0, 2), flush=True)
