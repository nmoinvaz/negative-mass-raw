import sympy as sp
EPS=-1
rho=sp.Symbol("rho", real=True)
c=sp.Rational(-3,2)
K=-2*c/sp.pi
Af=1+c*(rho**2+1)+K*(rho+(rho**2+1)*sp.atan(rho))
Rf=sp.sqrt(rho**2+1); Phf=sp.sqrt(2)*sp.atan(rho)
psi=sp.atan(rho)
Vf=-c*(2-sp.cos(2*psi))-K*(sp.Rational(3,2)*sp.sin(2*psi)+psi*(2-sp.cos(2*psi)))
Vr=sp.simplify(Vf.rewrite(sp.atan))
V1=sp.diff(Vf,rho)/sp.diff(Phf,rho)           # V'(phi)
V2=sp.diff(V1,rho)/sp.diff(Phf,rho)
s2=sp.sqrt(2)
rp=Af*sp.diff(Rf,rho)/s2; rm=-rp
php=Af*sp.diff(Phf,rho)/s2; phm=-php
E=Af
a,ap,am,d,e,ep,em=sp.symbols("a ap am d e ep em")
r=Rf
# linear rhs from exploration
Lr = E*V1*e*r/2 + a*(E*Vf/2 + E/(2*r**2) + rm*rp/r**2) - am*rp/r - ap*rm/r + d*(-E*Vf*r/2 + E/(2*r))
Lp = -E*V1*d/2 + E*V2*e/2 + a*(phm*rp/r**2 + php*rm/r**2) - am*php/r - ap*phm/r - em*rp/r - ep*rm/r
g=rho*Rf/s2
# derivative operators on functions of rho: d/dp = (A/s2) d/drho, d/dm = -(A/s2) d/drho
Dp=lambda F: sp.diff(F,rho)*Af/s2
Dm=lambda F: -sp.diff(F,rho)*Af/s2
Y_pm_coefs = Lr - g*Lp - Dp(g)*em - Dm(g)*ep - Dp(Dm(g))*e   # Y_pm with a_pm = Lr, e_pm = Lp
Vhat = 2*Af**2/rho**2-(1+1/Rf**2)*Af*sp.diff(Af,rho)/rho+Af**2/Rf**4-2*Af/Rf**2
# u = Y/rho: u_pm = Y_pm/rho + (Y_p)(1/rho)_m + (Y_m)(1/rho)_p + Y (1/rho)_pm
Yp = ap - g*ep - Dp(g)*e
Ym = am - g*em - Dm(g)*e
Y = a-g*e
iq=1/rho
u_pm = Y_pm_coefs*iq + Yp*Dm(iq) + Ym*Dp(iq) + Y*Dp(Dm(iq))
M = u_pm + Vhat/2*Y/rho
M = sp.expand(M)
import mpmath as mp
for val in (sp.Rational(7,5), sp.Rational(-1,3), sp.Rational(23,10)):
    row = {}
    for sym in (a,e,ap,am,ep,em,d):
        co = M.coeff(sym)
        row[sym]=sp.N(co.subs(rho,val),20)
    print(val, row)
