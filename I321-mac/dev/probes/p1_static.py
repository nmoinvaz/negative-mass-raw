import sympy as sp, time
t0=time.time()
t,rho,ang,ph=sp.symbols('t rho ang ph',real=True)
b,kap=sp.symbols('b kappa',positive=True)
X=[t,rho,ang,ph]
R2=b**2+rho**2; R=sp.sqrt(R2)
th0=sp.atan(rho/b)
c=-1/b**2
Z=rho+R2/b*sp.atan(rho/b)
A=1+c*R2+kap*Z
Af=sp.Function('A')(rho)
g=sp.diag(-Af,1/Af,R2,R2*sp.sin(ang)**2)
gi=g.inv()
n=4
Gam=[[[sum(gi[a,d]*(sp.diff(g[d,bb],X[cc])+sp.diff(g[d,cc],X[bb])-sp.diff(g[bb,cc],X[d])) for d in range(n))/2 for cc in range(n)] for bb in range(n)] for a in range(n)]
def ric(bb,d):
    s=sum(sp.diff(Gam[a][bb][d],X[a])-sp.diff(Gam[a][bb][a],X[d]) for a in range(n))
    s+=sum(Gam[a][a][k]*Gam[k][bb][d]-Gam[a][d][k]*Gam[k][bb][a] for a in range(n) for k in range(n))
    return sp.simplify(s)
Rtt,Rrr,Rthth=ric(0,0),ric(1,1),ric(2,2)
print('Ricci',time.time()-t0)
# eq: R_ab = -2 th_a th_b + V g_ab
Vs=sp.Symbol('Vs')
dth=sp.diff(th0,rho)
# thth: Rthth = V R2 -> V
Vsol=sp.simplify(Rthth/R2)
Vsol_A=Vsol
print('V(rho) =',Vsol)
Etr=sp.simplify((Rtt - Vsol*g[0,0]).subs(Af,A).doit())
Err=sp.simplify((Rrr + 2*dth**2 - Vsol*g[1,1]).subs(Af,A).doit())
Vc=Vsol.subs(Af,A).doit()
Vc=sp.simplify(Vc)
print('Ett',Etr,'Err',Err)
# scalar: -2 box th = V_th ; box th = (1/R2)(R2 A th')'
box=sp.diff(R2*A*dth,rho)/R2
Vth=sp.diff(Vc,rho)/dth
Esc=sp.simplify(-2*box-Vth)
print('Esc',Esc)
# A'' relation
print('R2 A\'\' - 2(A-1):',sp.simplify(R2*sp.diff(A,rho,2)-2*(A-1)))
print('A(0)',A.subs(rho,0),"A'(0)",sp.diff(A,rho).subs(rho,0),"A''(0)",sp.diff(A,rho,2).subs(rho,0))
print(time.time()-t0)
