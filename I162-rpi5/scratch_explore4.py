import sys,time
sys.path.insert(0,"/home/nathan/Source/negative-mass-i162/notes/warp")
import sympy as sp
import two_scalars as ts
t,x,rho,phi=sp.symbols("t x rho phi",positive=True)
X4=[t,x,rho,phi]
def Ofrob(k):
    def dk(i,j): return sp.diff(k[j],X4[i])-sp.diff(k[i],X4[j])
    return sp.simplify(k[0]*dk(1,2)+k[1]*dk(2,0)+k[2]*dk(0,1))
def test(name,a,b):
    t0=time.time()
    k,m=a+b,a-b
    ok,om,why=ts.closure(a,b,X4,sp.simplify)
    print(name,"O_k",Ofrob(k),"O_m",Ofrob(m),"closure",ok,why,"om",list(om),round(time.time()-t0,1))
c=sp.Symbol("c",positive=True)
g=sp.Function("g")(rho)
# P1
test("P1 closed const",sp.Matrix([0,0,1,0]),sp.Matrix([1,0,0,0]))
# P2 boosted: k=e^{-chi} d(t+x), m=e^{chi} d(t-x+rho^2/2), chi=c x + g(rho)
chi=c*x+g
k=sp.exp(-chi)*sp.Matrix([1,1,0,0]); m=sp.exp(chi)*sp.Matrix([1,-1,rho,0])
test("P2 boosted",(k+m)/2,(k-m)/2)
# P3 Frobenius-fail
test("P3 frob fail",sp.Matrix([1,0,0,0]),sp.Matrix([0,0,x,0]))
# P4 compat fail: k=dt, m=(1+t rho) drho  => a=(k+m)/2
k=sp.Matrix([1,0,0,0]); m=sp.Matrix([0,0,1+t*rho,0])
test("P4 compat fail",(k+m)/2,(k-m)/2)
# planar u = c x + d: a=c th1, b=c th0
u=c*x+sp.Symbol("d")
th0,th1=sp.Matrix([1,0,0,0]),sp.Matrix([u,1,0,0])
test("planar",c*th1,c*th0)
# c=0 nu^dnu for b(rho)=g, eps
eps=sp.Symbol("eps")
for ee in (1,-1):
    nu=sp.Matrix([1+ee*g,ee,0,0]); dr=sp.Matrix([0,0,1,0])
    print("eps",ee,"nu+ ^ d nu+:",Ofrob(dr+nu),"nu- ^ dnu-:",Ofrob(dr-nu), "g'=",sp.diff(g,rho))
