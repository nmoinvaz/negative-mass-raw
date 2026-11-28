import sympy as sp
lg, u, ui, th, C, D3, Lc2, q, J2 = sp.symbols("ell u ui th C D3 Lc2 q J2")
w0, w1, w2 = sp.symbols("w0 w1 w2")
def dth(e):
    return (sp.diff(e, lg)*(-u) + sp.diff(e, u)*(1+u**2) + sp.diff(e, th) + sp.diff(e, C)*(2*lg+2*q) + sp.diff(e, D3)*2*C + sp.diff(e, Lc2)*lg**2 + sp.diff(e, ui)*(-(1+ui**2)))
S = u**2/(1+u**2)
Lc1 = (C - 2*q*th)/2
c1 = w0 - 3*lg - S
c2 = w1 - 2*w0*lg + lg**2 - 2*S*lg
c3 = 2*w0*lg**2 - 2*w1*lg + w2 - 2*lg**3 - 2*S*lg**2
g = 22*lg**2 - 8*w0*lg - 2*w1
P = -sp.integrate(sp.expand(12*lg**2 - 2*g), lg) - 32*(u*C + lg**2 + 2*q*lg - D3/2)
g4 = 12*lg**2 - 2*g - 32*u*C
print("P' - g4 u =", sp.simplify(dth(P) - g4*u))
w4p = (8*lg*c2 + 2*c3 + 8*w0*lg*c1 - P)/S
a1, a2, a3 = 8*w1 + 8*w0**2 + 64*q, 32 - 28*w0, -sp.Rational(20, 3)
Wn = (-2*w2*ui + a1*(-lg*ui - th) + a2*(-lg**2*ui - 2*Lc1) + a3*(-lg**3*ui - 3*Lc2)
      + 32*(-C*lg + 2*Lc2 + 2*q*Lc1) + 16*D3*ui - 20*Lc2 - 8*w0*Lc1)
res = sp.simplify(dth(Wn).subs(ui, 1/u) - w4p)
print("W' - w4p =", res)
lim = sp.expand(Wn.subs({ui: 0, C: 0, D3: 0}).subs({th: sp.pi/2, Lc2: J2}))
print("lim", lim)
