import sympy as sp, time
r,c,s,lam = sp.symbols('r c s lam')
W0,W1,W2 = sp.symbols('W0 W1 W2')
w,w1,w2 = W0,W1,W2
R00 = -(2*w*w1*s**2 + 2*r*w*w2*c**2 + r*w1**2*(1+c**2))/(2*r)
R01 = -(w1*(1+c**2) + r*w2*s**2)/(2*r)
R0p = (r*w2 - w1)*s*c/(2*r)
R11 = (2*w*w1*s**2 + 2*r*w*w2*c**2 + r*w1**2*(3*c**2-1))/(2*r)
R1p = (w*(r*w2-w1) + 2*r*w1**2)*s*c/(2*r)
Rpp = w1**2*s**2/2
red = lambda e: sp.factor(sp.expand(e).subs(s**2,1-c**2)) if True else e
u = r*w2 - w1; v = w*u + 2*r*w1**2; z = 2*w1 + u*s**2
print("R01 vs z:", sp.simplify((R01 + z/(2*r)).subs(s,sp.sqrt(1-c**2))))
print("R0p:", sp.simplify(R0p - u*s*c/(2*r)), "R1p:", sp.simplify(R1p - v*s*c/(2*r)))
F = R01*(R0p**2+R1p**2) + 2*Rpp*R0p*R1p
Fx = sp.simplify(F.subs(s,sp.sqrt(1-c**2)))
Fref = (1-c**2)*c**2/(8*r**3)*(-(2*w1+u*(1-c**2))*(u**2+v**2) + 2*r*u*v*w1**2*(1-c**2))
print("F - ref:", sp.simplify(Fx-Fref))
# minors certificate: R0p*md + R1p*me = -(F)
N = sp.Matrix([[R00+lam,R01,R0p],[R01,R11-lam,R1p],[R0p,R1p,Rpp-lam]])
md = N[0,0]*N[1,2]-N[0,1]*N[0,2]; me = N[1,1]*N[0,2]-N[0,1]*N[1,2]
cert = sp.simplify((R0p*md + R1p*me + F).subs(s,sp.sqrt(1-c**2)))
print("certificate residual:", cert)
