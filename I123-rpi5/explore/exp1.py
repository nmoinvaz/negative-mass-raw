import sys, time
sys.path.insert(0, '/home/nathan/Source/negative-mass-i123/phase2/nonradial')
import numpy as np
from scipy.integrate import solve_ivp
import background as B
from polar_solver import PolarProblem
eps, w, l = -1, 0.7603, int(sys.argv[1]) if len(sys.argv) > 1 else 2
st = B.solve_star(w, eps); P = PolarProblem(st, l, rtol=1e-8)
rm, M = P.rm, P.Mext
lam = (l-1)*(l+2)/2.0
print('rm', rm, 'M', M)
def V(r):
    f = 1 - 2*M/r
    return 2*f*(lam**2*r**2*((lam+1)*r+3*M)+9*M**2*(lam*r+M))/(r**3*(lam*r+3*M)**2)
def Wx(x):  # V = x^2 f W
    N = lam**2*(lam+1+3*M*x)+9*M**2*x**2*(lam+M*x); Dn = lam+3*M*x
    return 2*N/Dn**2
def series(s, R, nmax=400):
    """u(x)=sum a_n x^n at x=1/R; returns u, u_x with optimal truncation"""
    # W coefficients by power series division/ taylor via numpy
    # W(x) series: compute via polynomial arithmetic to order nmax
    n = nmax
    Nc = np.zeros(n+1); Nc[0] = lam**2*(lam+1); Nc[1] = 3*M*lam**2
    Nc[2] += 9*M**2*lam; Nc[3] += 9*M**3
    # 1/Dn^2 = lam^-2 (1+ 3M x/lam)^-2 = lam^-2 sum (j+1)(-3M/lam)^j x^j
    inv = np.array([(j+1)*(-3*M/lam)**j for j in range(n+1)])/lam**2
    Wc = 2*np.convolve(Nc, inv)[:n+1]
    a = np.zeros(n+2, dtype=complex); a[0] = 1
    x = 1.0/R
    u = 0j; ux = 0j; best = np.inf; nstop = 0
    for k in range(n):
        # coefficient equation at x^k: k(k+1)a_k - 2M(k-1)(k+1)a_{k-1} + 2s(k+1)a_{k+1} - sum W_j a_{k-j} = 0
        conv = np.dot(Wc[:k+1], a[k::-1][:k+1]) if k >= 0 else 0
        am1 = a[k-1] if k >= 1 else 0
        a[k+1] = (conv - k*(k+1)*a[k] + 2*M*(k-1)*(k+1)*am1)/(2*s*(k+1))
        term = abs(a[k+1])*abs(x)**(k+1)
        if term < 1e-19 or (term > best and k > 3): nstop = k+1; break
        best = min(best, term)
        nstop = k+1
    xs = x**np.arange(nstop+1)
    u = np.sum(a[:nstop+1]*xs)
    ux = np.sum(np.arange(1, nstop+1)*a[1:nstop+1]*x**np.arange(0, nstop))
    return u, ux, nstop, best
def start_series(s, R):
    u, ux, n, e = series(s, R)
    f = 1-2*M/R
    ur = -ux/R**2
    return np.array([u, f*ur - s*u]), n, e
def start_wkb(s, R, amp=False):
    k0 = np.sqrt(s*s+V(R))
    return np.array([k0**-0.5, -k0**0.5]) if amp else np.array([1, -k0])
def integ(s, R, ya, rtol=1e-11):
    def A(rho):
        r = np.exp(rho); f = 1-2*M/r
        a = (r/f)*np.array([[s, 1.0], [s*s+V(r), s]])
        return np.block([[a.real, -a.imag], [a.imag, a.real]])
    ya = np.array(ya, dtype=complex)
    sol = solve_ivp(lambda rho, y: A(rho)@y, (np.log(R), np.log(rm)), np.r_[ya.real, ya.imag], method='Radau', jac=lambda rho, y: A(rho), rtol=rtol, atol=1e-14)
    return sol.y[0, -1]+1j*sol.y[2, -1], sol.y[1, -1]+1j*sol.y[3, -1], sol.t.size
if __name__ == '__main__':
    smin = 0.01
    zf = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    Rz = rm + zf*(40+20*l)/smin + 50
    print('Rz', Rz, flush=True)
    for s in (0.0001+0.12j, -0.0005+0.12j, -0.001+0.12j, -0.001+0.23j, -0.001+0.01j):
        t0 = time.time()
        ys, n, e = start_series(s, Rz)
        z1, p1, ns = integ(s, Rz, ys)
        z5 = integ(s, Rz, ys, rtol=1e-13)[0]
        z2 = integ(s, Rz, start_wkb(s, Rz, True))[0]
        print(s, 'series n', n, 'steps', ns, 'y1', z1, '| rtol13 vs 11', abs(z5/z1-1), '| wkbamp start vs series', abs(z2/z1-1), 'time', time.time()-t0, flush=True)
