import sys,time
sys.path.insert(0,"/home/nathan/Source/negative-mass-i162/notes/warp")
import sympy as sp
import two_scalars as ts
t,x,rho,phi=sp.symbols("t x rho phi",positive=True)
X4=[t,x,rho,phi]
g=sp.Function("g")(rho)
G0,G1s=sp.symbols("G0 G1s")
R=sp.Rational
def point(cc,gv,eps,rho0,x0=R(1,3),t0=R(1,10)):
    g1=sp.diff(g,rho)
    rule2=eps*(g1**2+2*cc**2)-g1/rho
    rule3=sp.diff(rule2,rho).subs(sp.Derivative(g,(rho,2)),rule2)
    uu=cc*x+g
    th0,th1,th2=sp.Matrix([1,0,0,0]),sp.Matrix([uu,1,0,0]),sp.Matrix([0,0,1,0])
    W=sp.sqrt(g1**2+2*cc**2)
    a=(g1*th2+2*cc*th1)/sp.sqrt(2)
    b=W*(th0+eps*th1)/sp.sqrt(2)
    pt={rho:rho0,x:x0,t:t0}
    def simp(e):
        e=e.subs(sp.Derivative(g,(rho,3)),rule3).subs(sp.Derivative(g,(rho,2)),rule2)
        e=e.subs(sp.Derivative(g,rho),G1s).subs(g,G0)
        return sp.simplify(e.subs({G1s:gv,G0:R(1,5)}).subs(pt))
    def O(k):
        def dk(i,j): return sp.diff(k[j],X4[i])-sp.diff(k[i],X4[j])
        return simp(k[0]*dk(1,2)+k[1]*dk(2,0)+k[2]*dk(0,1))
    k,m=a+b,a-b
    t1=time.time()
    ok,om,why=ts.closure(a,b,X4,simp)
    return (sp.nsimplify(O(k)*2*sp.sqrt(2)) , sp.nsimplify(O(m)*2*sp.sqrt(2)), ok, why[:30], round(time.time()-t1,1))
# note: k = a+b = k~/sqrt2, O_k = O~/2 ... scaling: O(k)=O(k~)/2 ; times 2 -> need *2 not 2sqrt2
def predicted(cc,gv,eps,rho0):
    W=sp.sqrt(gv**2+2*cc**2)
    Ok=gv*(gv**2+4*cc**2+5*cc*eps*W-2*cc*gv/(rho0*W))
    Om=gv*(gv**2+4*cc**2-5*cc*eps*W+2*cc*gv/(rho0*W))
    return sp.simplify(Ok),sp.simplify(Om)
for (cc,gv,eps,rho0) in ((2,1,1,R(5,7)),(2,1,-1,R(5,7)),(-2,1,1,R(4,39)),(2,1,1,R(4,39)),(1,1,1,R(5,7)),(R(3),R(7,2),-1,R(2,3)),(1,0,1,R(5,7)),(-3,0,-1,R(1,2))):
    r=point(cc,gv,eps,rho0)
    print((cc,gv,eps,rho0),"predicted (Ok~,Om~):",predicted(cc,gv,eps,rho0),"coord*2:",sp.simplify(r[0]/sp.sqrt(2)),sp.simplify(r[1]/sp.sqrt(2)),r[2:])
