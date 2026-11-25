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
R3 = sp.Matrix([[R00,R01,R0p],[R01,R11,R1p],[R0p,R1p,Rpp]])
eta3 = sp.diag(-1,1,1)
print(sp.simplify((R3[0,0]+R3[1,1]+2*R3[2,2]).subs(s**2,1-c**2)))
N = R3 - lam*eta3
t=time.time()
P = sp.expand((N.det()).subs(s,sp.sqrt(1-c**2)))
print(time.time()-t)
Pp = sp.Poly(sp.expand(sp.simplify(P)), lam)
print([sp.factor(x) for x in Pp.all_coeffs()])
