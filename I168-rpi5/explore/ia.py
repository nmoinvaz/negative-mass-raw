from fractions import Fraction as Fr
class Iv:
    __slots__=("lo","hi")
    def __init__(s,lo,hi=None):
        s.lo=Fr(lo); s.hi=Fr(lo if hi is None else hi)
        assert s.lo<=s.hi
    @staticmethod
    def c(x): return x if isinstance(x,Iv) else Iv(x)
    def __add__(a,b): b=Iv.c(b); return Iv(a.lo+b.lo,a.hi+b.hi)
    __radd__=__add__
    def __neg__(a): return Iv(-a.hi,-a.lo)
    def __sub__(a,b): b=Iv.c(b); return Iv(a.lo-b.hi,a.hi-b.lo)
    def __rsub__(a,b): return Iv.c(b)-a
    def __mul__(a,b):
        b=Iv.c(b); v=[a.lo*b.lo,a.lo*b.hi,a.hi*b.lo,a.hi*b.hi]; return Iv(min(v),max(v))
    __rmul__=__mul__
    def __pow__(a,n):
        assert isinstance(n,int) and n>=0
        if n==0: return Iv(1)
        if n%2==1 or a.lo>=0: 
            r=Iv(1)
            for _ in range(n): r=r*a
            # exact for monotone cases
            if n%2==1: return Iv(a.lo**n,a.hi**n)
            return Iv(a.lo**n,a.hi**n)
        if a.hi<=0: return Iv(a.hi**n,a.lo**n)
        return Iv(Fr(0),max(a.lo**n,a.hi**n))
    def mag(a): return max(abs(a.lo),abs(a.hi))
    def __repr__(a): return f"[{float(a.lo):.6g},{float(a.hi):.6g}]"
def bisect_boxes(box, n):
    """box: list of (lo,hi) Fractions; split each coordinate into n equal parts; yield sub-boxes"""
    import itertools
    parts=[]
    for lo,hi in box:
        lo=Fr(lo);hi=Fr(hi); parts.append([(lo+(hi-lo)*i/n, lo+(hi-lo)*(i+1)/n) for i in range(n)])
    for combo in itertools.product(*parts): yield combo
