import sympy as sp, time
t,x,rho,phi = sp.symbols("t x rho phi", positive=True)
c=sp.Symbol("c",real=True); eps=sp.Symbol("eps")
g=sp.Function("g")(rho)
u=c*x+g
g1,g2,g3=g.diff(rho),g.diff(rho,2),g.diff(rho,3)
ux,ur=u.diff(x),u.diff(rho)
P=-(u*u.diff(x,2)+ux**2); Q=-(u.diff(rho,2)+ur/rho)/2; Z=u.diff(x,rho)/2; Y=u*u.diff(x,rho)/2+ux*ur; h=ur**2/2
A=P-h;B=-P-h
S00,S01,S11=A-Z**2/h,Q-Z*Y/h,B-Y**2/h
L2=[Z/h,Y/h,1]; L1=[S01/S11,1,0]; w2=-S11/h
def co(a): return [a[0]+a[1]*u,a[1],a[2]]
dX=lambda f: sp.diff(f,x); dR=lambda f: sp.diff(f,rho)
def Wd(a,b):
    a,b=co(a),co(b)
    return a[0]*(dX(b[2])-dR(b[1]))+a[1]*dR(b[0])+a[2]*(-dX(b[0]))
dw=[0,dX(w2),dR(w2)]
cl2,cl1=co(L2),co(L1)
Mx=sp.Matrix([cl2,dw,cl1]); det3=Mx.det()
E=Wd(L2,L2)+w2*Wd(L1,L1); Bc=Wd(L2,L1)+Wd(L1,L2)+det3/(2*w2)
for e in (1,-1):
    r2=e*(g1**2+2*c**2)-g1/rho
    r3=sp.diff(r2,rho).subs(g2,r2)
    red=lambda ex: ex.subs(g3,r3).subs(g2,r2)
    Ee=sp.simplify(red(E)); Be=sp.simplify(red(Bc)); w2e=sp.simplify(red(w2))
    print("eps",e,"E=",sp.factor(Ee)); print(" w2=",sp.factor(w2e)); print(" B=",sp.factor(Be))
    W=sp.sqrt(g1**2+2*c**2)
    print(" wB^2 check", sp.simplify(w2e*Be**2))
