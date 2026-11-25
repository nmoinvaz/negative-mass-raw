# F for the accelerating bubble from route D's entries (printed by explore_acc0), as a polynomial in c
import sympy as sp
r,c,S,A,W0,W1,W2 = sp.symbols('R c S A W0 W1 W2')
R00 = -(-2*A*r*W1*c + r*S**2*W1**2 + 2*r*W0*W2*c**2 + 2*r*W1**2*c**2 - 2*W0*W1*c**2 + 2*W0*W1)/(2*r)
R01 = -(r*S**2*W2 - S**2*W1 + 2*W1)/(2*r)
R0p = S*c*(r*W2 - W1)/(2*r)
R11 = (-2*A*r*W1*c - r*S**2*W1**2 + 2*r*W0*W2*c**2 + 2*r*W1**2*c**2 - 2*W0*W1*c**2 + 2*W0*W1)/(2*r)
R1p = S*(-A*r*W1 + r*W0*W2*c + 2*r*W1**2*c - W0*W1*c)/(2*r)
Rpp = S**2*W1**2/2
red = lambda e: sp.expand(sp.rem(sp.Poly(sp.expand(e), S).as_expr(), S**2 + c**2 - 1, S))
print("I2:", red(R00+R11+2*Rpp))
F = R01*(R0p**2+R1p**2) + 2*Rpp*R0p*R1p
u = r*W2 - W1; v = W0*u + 2*r*W1**2; B0 = A*r*W1
z = 2*W1 + u*(1-c**2)
B = -z*(u**2*c**2 + (v*c - B0)**2) + 2*r*W1**2*u*(1-c**2)*c*(v*c - B0)
print("F - S^2 B/(8 r^3):", red(F - (1-c**2)*B/(8*r**3)))   # F has S^2 factor = 1 - c^2
P = sp.Poly(sp.expand(B), c)
for k in range(P.degree()+1):
    print("c^%d:"%k, sp.factor(P.coeff_monomial(c**k)))
print("c0 check:", sp.simplify(P.coeff_monomial(1) + (2*W1+u)*B0**2), " c1 check:", sp.simplify(P.coeff_monomial(c) - 2*B0*(v*(2*W1+u) - r*W1**2*u)))
