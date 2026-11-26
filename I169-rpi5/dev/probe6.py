import sympy as sp, mpmath as mp, random
exec(open("/tmp/claude-1000/-home-nathan-Source-negative-mass-i169/331aac0b-19cd-46a3-93e4-a8cf021dbd98/scratchpad/probe3.py").read().split("# case (b)")[0])
mp.mp.dps=60
Dc = Dpoly(b0=1,b1=0,b2=0).subs(v,0)
Pl = sp.Poly(sp.expand(Dc), a0,a1,a2)
mons = [m for m,_ in Pl.terms()]
coefs = [co for _,co in Pl.terms()]
xs = sp.symbols("xs")
fl = sp.lambdify((A0,A1,A2,B0,B1,B2), coefs, "mpmath")
def drank(Af,Bf,npts=30,xr=(0.3,1.7)):
    rows=[]
    for k in range(npts):
        x=sp.Rational(xr[0]*100+ (xr[1]-xr[0])*100*k//npts,100) if False else sp.nsimplify(xr[0]+(xr[1]-xr[0])*k/npts)
        vals=[sp.diff(Af,xs,i).subs(xs,x) for i in range(3)]+[sp.diff(Bf,xs,i).subs(xs,x) for i in range(3)]
        rows.append([mp.mpf(sp.N(c,60)) for c in fl(*[mp.mpf(sp.N(t,60)) for t in vals])])
    s=mp.svd_r(mp.matrix(rows),compute_uv=False)
    smax=max(s)
    return sum(1 for t in s if t>mp.mpf(10)**-30*smax)
fams = {
 "exp,exp": (sp.exp(xs), sp.exp(2*xs)),
 "exp,exp(-)": (sp.exp(xs), sp.exp(-xs)),
 "cosh,sinh": (sp.cosh(xs), sp.sinh(xs)),
 "cos,sin": (sp.cos(xs), sp.sin(xs)),
 "x,x^2": (xs, xs**2),
 "x,x^3": (xs, xs**3),
 "x^2,x^3": (xs**2, xs**3),
 "exp,x": (sp.exp(xs), xs),
 "exp,1/x": (sp.exp(xs), 1/xs),
 "x^2, 1 (A=x^2,B=1)": (xs**2, sp.Integer(1)),
 "x,1": (xs, sp.Integer(1)),
 "exp,1": (sp.exp(xs), sp.Integer(1)),
 "generic": (sp.exp(xs)+xs**2/3, sp.sin(xs)+xs**3),
}
for k,(Af,Bf) in fams.items():
    print(k, drank(Af,Bf))
