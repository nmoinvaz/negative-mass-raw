import sympy as sp, time, pickle, itertools, sys
from sympy import QQ
from sympy.polys.matrices import DomainMatrix

kap_s = sp.Symbol('kappa', positive=True)
DOM = QQ   # set by setdom()
TRUNC = 12

def setdom(symbolic):
    global DOM
    DOM = QQ.frac_field(kap_s) if symbolic else QQ

def cv(x):
    return DOM.from_sympy(sp.sympify(x))

class Ser:
    """truncated bivariate series in (V,U), total degree <= TRUNC, coefficients in DOM"""
    __slots__ = ('d',)
    def __init__(self, d=None):
        self.d = {k: v for k, v in (d or {}).items() if v != DOM.zero and sum(k) <= TRUNC}
    @staticmethod
    def const(c):
        return Ser({(0, 0): cv(c) if not hasattr(c, 'numer') or isinstance(c, (int, sp.Basic)) else c})
    def _o(self, o):
        if isinstance(o, Ser): return o
        if DOM.of_type(o): return Ser({(0, 0): o})
        return Ser({(0, 0): cv(o)})
    def __add__(self, o):
        o = self._o(o); d = dict(self.d)
        for k, v in o.d.items(): d[k] = d.get(k, DOM.zero) + v
        return Ser(d)
    __radd__ = __add__
    def __neg__(self): return Ser({k: -v for k, v in self.d.items()})
    def __sub__(self, o): return self + (-self._o(o))
    def __rsub__(self, o): return self._o(o) - self
    def __mul__(self, o):
        o = self._o(o); d = {}
        for (i, j), a in self.d.items():
            for (p, q), b in o.d.items():
                if i + j + p + q <= TRUNC:
                    k = (i + p, j + q); d[k] = d.get(k, DOM.zero) + a * b
        return Ser(d)
    __rmul__ = __mul__
    def inv(self):
        c0 = self.d.get((0, 0), DOM.zero)
        assert c0 != DOM.zero
        ic = DOM.one / c0
        rest = Ser({k: v for k, v in self.d.items() if k != (0, 0)})
        u = Ser({(0, 0): ic})
        for _ in range(TRUNC + 1):
            u = Ser({(0, 0): ic}) - rest * u * ic
        return u
    def __truediv__(self, o): return self * self._o(o).inv()
    def __rtruediv__(self, o): return self._o(o) * self.inv()
    def __pow__(self, n):
        if n >= 0:
            r = Ser({(0, 0): DOM.one})
            for _ in range(n): r = r * self
            return r
        return (self.inv()) ** (-n)
    def dV(self): return Ser({(i - 1, j): v * i for (i, j), v in self.d.items() if i > 0})
    def dU(self): return Ser({(i, j - 1): v * j for (i, j), v in self.d.items() if j > 0})
    def jet(self, a, b):
        s = self
        for _ in range(a): s = s.dV()
        for _ in range(b): s = s.dU()
        return s
    def maxdeg_nonzero(self):
        return max([sum(k) for k in self.d], default=-1)
    def mindeg_nonzero(self):
        return min([sum(k) for k in self.d], default=None)

def pi_to_ser(coefs):
    """univariate series in Pi (list of DOM) -> bivariate with Pi = -V U"""
    return Ser({(k, k): c * (DOM.one if k % 2 == 0 else -DOM.one) for k, c in enumerate(coefs)})

# ---------------- univariate Pi series helpers (lists of DOM) ----------------
def u_mul(a, b, n):
    out = [DOM.zero] * (n + 1)
    for i, x in enumerate(a):
        if x == DOM.zero: continue
        for j, y in enumerate(b):
            if i + j > n: break
            out[i + j] += x * y
    return out

def u_compose(coefs_rho, rho_pi, n):
    """sum_k coefs_rho[k] * rho_pi^k as series in Pi to order n (Horner)"""
    out = [DOM.zero] * (n + 1)
    for c in reversed(coefs_rho):
        out = u_mul(out, rho_pi, n)
        out[0] += c
    return out

def series_in_rho(expr, rho, n):
    s = sp.series(expr, rho, 0, n + 1).removeO()
    p = sp.Poly(sp.expand(s), rho)
    co = [cv(0)] * (n + 1)
    for (k,), c in p.terms():
        co[k] = cv(c)
    return co

def build_background(b, nPi, symbolic):
    """b rational; returns dict of univariate Pi-series lists. kappa symbolic or rational (value in KAPVAL)"""
    rho = sp.Symbol('rho')
    kap = kap_s if symbolic else sp.Rational(KAPVAL)
    b = sp.Rational(b)
    R2 = b ** 2 + rho ** 2
    c = -1 / b ** 2
    Z = rho + R2 / b * sp.atan(rho / b)
    A = 1 + c * R2 + kap * Z
    nr = 2 * nPi + 4
    Aco = series_in_rho(A, rho, nr)
    # rho(Pi), g1 = 1 (G0 = 1)
    kapd = cv(kap)
    g = [DOM.zero, DOM.one] + [DOM.zero] * (nPi + 1)
    for k in range(2, nPi + 2):
        # sum_{n>=2} A_n rho^n at Pi^k
        rp = g[:k]  # known up to k-1
        tot = DOM.zero
        pw = rp[:]
        pw = u_mul(pw, rp, k)  # rho^2
        for n in range(2, k + 1):
            tot += Aco[n] * pw[k] if k < len(pw) else DOM.zero
            pw = u_mul(pw, rp, k)
        g[k] = tot / (2 * kapd) / (k - 1)
    rho_pi = g[:nPi + 2]
    N1 = nPi + 1
    rho_pi = rho_pi[:N1 + 1]
    out = {'rho': rho_pi}
    comp = lambda co: u_compose(co, rho_pi, N1)
    out['A'] = comp(Aco)
    # Omega0 = A/(2 kappa^2 Pi)
    Ap = out['A']
    assert Ap[0] == DOM.zero
    out['Om'] = [x / (2 * kapd ** 2) for x in Ap[1:]]  # one order lost
    out['r'] = comp(series_in_rho(sp.sqrt(R2), rho, nr))
    out['th'] = comp(series_in_rho(sp.atan(rho / b), rho, nr))
    Vexpr = (1 - sp.diff(rho * A, rho)) / R2
    th_rho = b / R2   # d theta / d rho
    V1expr = sp.diff(Vexpr, rho) / th_rho
    V2expr = sp.diff(V1expr, rho) / th_rho
    out['P0'] = comp(series_in_rho(Vexpr, rho, nr))
    out['P1'] = comp(series_in_rho(V1expr, rho, nr))
    out['P2'] = comp(series_in_rho(V2expr, rho, nr))
    out['Aco'] = Aco
    return out
KAPVAL = sp.Rational(1)
