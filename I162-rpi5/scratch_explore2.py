import sys,os
sys.path.insert(0,"/home/nathan/Source/negative-mass-i162/notes/warp")
import sympy as sp
import phantom_source as ps
import two_scalars as ts
t,x,rho,phi=sp.symbols("t x rho phi",positive=True)
c=sp.Symbol("c",positive=True)
g=sp.Function("g")(rho)
X4=[t,x,rho,phi]
G0,G1=sp.symbols("G0 G1")
def closure_at(cc,gv,eps,rho0=sp.Rational(5,7)):
    rule2=eps*(sp.diff(g,rho)**2+2*cc**2)-sp.diff(g,rho)/rho
    rule3=sp.diff(rule2,rho).subs(sp.Derivative(g,(rho,2)),rule2)
    uu=cc*x+g
    th0,th1,th2=sp.Matrix([1,0,0,0]),sp.Matrix([uu,1,0,0]),sp.Matrix([0,0,1,0])
    g1=sp.diff(g,rho)
    W=sp.sqrt(g1**2+2*cc**2)
    a=(g1*th2+2*cc*th1)/sp.sqrt(2)
    b=W*(th0+eps*th1)/sp.sqrt(2)
    pt={rho:rho0,x:sp.Rational(1,3),t:sp.Rational(1,10)}
    def simp(e):
        e=e.subs(sp.Derivative(g,(rho,3)),rule3).subs(sp.Derivative(g,(rho,2)),rule2)
        e=e.subs(sp.Derivative(g,rho),G1).subs(g,G0)
        return sp.simplify(e.subs({G1:gv,G0:sp.Rational(1,5)}).subs(pt))
    return ts.closure(a,b,X4,simp)
for cc,gv in ((1,0),(2,0),(sp.Rational(1,2),0),(2,1)):
    for eps in (1,-1):
        ok,om,why=closure_at(cc,gv,eps)
        print(cc,gv,eps,ok,why)
