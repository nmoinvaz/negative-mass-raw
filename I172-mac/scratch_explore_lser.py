"""Laurent series in nu with powers of T = ln eta; coefficients in the fraction field QQ(Fi, C)."""
import sympy as sp
from sympy import QQ
from sympy.polys.fields import field
K, Fi, C, Bb = field("Fi,C,Bb", QQ)
INF = 10**9

class L:
    __slots__ = ("d", "prec")
    def __init__(self, d=None, prec=INF):
        self.d = {k: v for k, v in (d or {}).items() if v != 0}
        self.prec = prec
        self.d = {k: v for k, v in self.d.items() if k[0] < prec}
    @staticmethod
    def const(c, prec=INF): return L({(0, 0): K(c) if not isinstance(c, type(Fi)) else c}, prec)
    def val(self): return min((n for n, j in self.d), default=self.prec)
    def __add__(s, o):
        o = o if isinstance(o, L) else L.const(o)
        r = dict(s.d)
        for k, v in o.d.items(): r[k] = r.get(k, 0) + v
        return L(r, min(s.prec, o.prec))
    __radd__ = __add__
    def __neg__(s): return L({k: -v for k, v in s.d.items()}, s.prec)
    def __sub__(s, o): return s + (-(o if isinstance(o, L) else L.const(o)))
    def __rsub__(s, o): return (-s) + o
    def __mul__(s, o):
        if not isinstance(o, L):
            o = K(o) if not isinstance(o, type(Fi)) else o
            return L({k: v * o for k, v in s.d.items()}, s.prec)
        vs, vo = s.val(), o.val()
        pr = min(s.prec + vo, o.prec + vs)
        r = {}
        for (n1, j1), v1 in s.d.items():
            for (n2, j2), v2 in o.d.items():
                if n1 + n2 < pr:
                    kk = (n1 + n2, j1 + j2)
                    r[kk] = r.get(kk, 0) + v1 * v2
        return L(r, pr)
    __rmul__ = __mul__
    def shift(s, m):
        return L({(n + m, j): v for (n, j), v in s.d.items()}, s.prec + m if s.prec < INF else INF)
    def inv(s):
        v = s.val(); assert s.d
        a = [(j, c) for (n, j), c in s.d.items() if n == v]
        assert len(a) == 1 and a[0][0] == 0, ("leading term not T-free", a)
        a0 = a[0][1]
        rel = s.prec - v  # relative precision
        r = L({(n - v, j): c / a0 for (n, j), c in s.d.items() if n > v}, rel)  # (1 + r) s = a0 nu^v
        # 1/(1+r) = sum (-r)^k until valuation >= rel
        out = L({(0, 0): K(1)}, rel); term = L({(0, 0): K(1)}, rel)
        mr = -r
        while True:
            term = term * mr
            term = L(term.d, rel)
            if not term.d: break
            out = out + term
        out = L(out.d, rel)
        return L({(n - v, j): c / a0 for (n, j), c in out.d.items()}, rel - v)
    def __truediv__(s, o):
        if not isinstance(o, L): return s * (K(1) / (K(o) if not isinstance(o, type(Fi)) else o))
        return s * o.inv()
    def sqrt(s):
        v = s.val(); assert v % 2 == 0
        a = [(j, c) for (n, j), c in s.d.items() if n == v]
        assert len(a) == 1 and a[0][0] == 0
        a0 = a[0][1]
        # sqrt of a rational constant a0
        num, den = a0.numer, a0.denom
        rn = sp.sqrt(sp.Rational(1)) 
        a0e = a0.as_expr()
        sa = sp.sqrt(a0e)
        assert sa.is_Rational, ("leading coeff not a rational square", a0e)
        sa = K(sa)
        rel = s.prec - v
        r = L({(n - v, j): c / a0 for (n, j), c in s.d.items() if n > v}, rel)
        # sqrt(1+r) = sum binom(1/2,k) r^k
        out = L({(0, 0): K(1)}, rel); term = L({(0, 0): K(1)}, rel); k = 0
        while True:
            k += 1
            term = term * r
            term = L(term.d, rel)
            if not term.d: break
            out = out + term * K(sp.binomial(sp.Rational(1, 2), k))
        return L({(n + v // 2, j): c * sa for (n, j), c in out.d.items()}, rel + v // 2)
    def Dt(s):
        r = {}
        for (n, j), v in s.d.items():
            if n: r[(n, j)] = r.get((n, j), 0) - n * v
            if j: r[(n, j - 1)] = r.get((n, j - 1), 0) + j * v
        return L(r, s.prec)
    def show(s, upto=None):
        for (n, j), v in sorted(s.d.items()):
            if upto is None or n <= upto: print(f"   nu^{n} T^{j}: {sp.factor(v.as_expr())}")
        print("   known below nu^%s" % s.prec)
    def expr(s):
        nu, T = sp.symbols("nu T")
        return sum(v.as_expr() * nu**n * T**j for (n, j), v in s.d.items())
