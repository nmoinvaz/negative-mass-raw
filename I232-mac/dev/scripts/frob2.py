import sympy as sp
rho=sp.Symbol("rho"); w=sp.Symbol("w")
c=-1
K=-2*sp.Integer(c)/sp.pi
A=1+c*(rho**2+1)+K*(rho+(rho**2+1)*sp.atan(rho))
R2=rho**2+1
Ap=sp.diff(A,rho)
kap=(Ap.subs(rho,0)/2)
W=w*kap
p = -2 + rho*Ap/A
q = -rho**2*(1/R2**2 - Ap/(A*rho*R2) - 2/(A*R2) + W**2/A**2)
ps=sp.series(p,rho,0,4).removeO(); qs=sp.series(q,rho,0,4).removeO()
p0,p1=[sp.simplify(ps.coeff(rho,k)) for k in (0,1)]
q0,q1=[sp.simplify(qs.coeff(rho,k)) for k in (0,1)]
print("p0",p0,"q0",sp.simplify(q0),"p1",p1,"q1",sp.simplify(q1))
s=sp.Symbol("s")
ind=sp.expand(s*(s-1)+p0*s+q0)
print("indicial:", sp.factor(ind))
sol=sp.solve(ind,s); print("exponents", sol)
for sv in sol:
    print("s=",sv, " p1*s+q1 =", sp.simplify(p1*sv+q1))
# at w=1 (W=kappa): s = 1 +- w/2 -> 1/2, 3/2; log coefficient ~ p1*s_small + q1
sv=sp.Rational(1,2)
print("w=1: resonance condition p1*s+q1 =", sp.simplify((p1*sv+q1).subs(w,1)))
