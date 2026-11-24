import sympy as sp
t,x,rho,phi=sp.symbols("t x rho phi",real=True)
c,eps=sp.symbols("c eps",real=True)
g=sp.Function("g")(rho)
G1=sp.diff(g,rho)
W=sp.sqrt(G1**2+2*c**2)
u=c*x+g
X=[t,x,rho,phi]
def kform(sgn):
    # k~ = sgn*W th0 + (2c + sgn*eps*W) th1 + g' th2   (th1 = dx + u dt)
    return sp.Matrix([sgn*W + (2*c+sgn*eps*W)*u, (2*c+sgn*eps*W), G1, 0])
def Ocoef(k):
    # coefficient of dt^dx^drho in k^dk
    def dk(i,j): return sp.diff(k[j],X[i])-sp.diff(k[i],X[j])
    return k[0]*dk(1,2)+k[1]*dk(2,0)+k[2]*dk(0,1)
g2ode=eps*(G1**2+2*c**2)-G1/rho
def red(e):
    e=e.subs(sp.Derivative(g,(rho,2)),g2ode)
    return sp.simplify(e)
Ok=Ocoef(kform(1)); Om=Ocoef(kform(-1))
Okr=red(Ok); Omr=red(Om)
print(sp.factor(sp.simplify(Okr.subs(eps**2,1))))
G,Wy,r=sp.symbols("G W r")
# compare with formula using eps^2=1
for e in (1,-1):
    Wv=sp.sqrt(G1**2+2*c**2)
    fk=G1*(G1**2+4*c**2+5*c*e*Wv-2*c*G1/(rho*Wv))
    fm=G1*(G1**2+4*c**2-5*c*e*Wv+2*c*G1/(rho*Wv))
    print(e, sp.simplify(Okr.subs(eps,e)-fk), sp.simplify(Omr.subs(eps,e)-fm))
print(sp.simplify(Ok+Om))   # without ODE
