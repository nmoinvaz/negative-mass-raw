import sympy as sp, pickle
lg, S, w0, w1, w2, a = sp.symbols("ell S w0 w1 w2 a")
c2s = 1 - S
L0 = -1; L1 = -2*w0 + 4*lg
Y1 = 2*lg; Y2 = 4*w0*lg - 6*lg**2
c1 = w0 - 3*lg - 1 + c2s
c2 = -2*w0*lg + w1 + lg**2 - 2*lg + 2*lg*c2s
c3 = 2*w0*lg**2 - 2*w1*lg + w2 - 2*lg**3 - 2*lg**2 + 2*lg**2*c2s
h2 = S*L1 + c2 + Y1*c1 + Y2/2
I3 = sp.expand(8*lg*h2/S + 2*(L1*(-2*lg) + L0*(4*lg**2)/2) + 2*(c3 + Y1*c2 + Y2*c1)/S)
A3 = sp.expand(I3*S).coeff(S, 0); B3 = sp.expand(I3*S).coeff(S, 1)
print("order 3: S*I3 powers", sp.expand(I3*S).coeff(S, 2))
print("A3 =", sp.collect(A3, lg)); print("B3 =", sp.collect(B3, lg))
# J_n from the Beta function: int_0^{pi/2} cos^a = sqrt(pi)/2 Gamma((a+1)/2)/Gamma(a/2+1)
gen = sp.sqrt(sp.pi)/2*sp.gamma((a+1)/2)/sp.gamma(a/2+1)
ser = sp.series(gen, a, 0, 5).removeO()
Jn = [sp.simplify(sp.expand_func(sp.factorial(n)*ser.coeff(a, n))) for n in range(5)]
for n, j in enumerate(Jn): print("J", n, "=", sp.nsimplify(sp.simplify(j)))
def integral(A, B):
    PA = sp.Poly(A, lg); PB = sp.Poly(B, lg)
    tot = 0
    for (b,), c in PA.terms():
        assert b >= 1, "constant term in A: divergent"
        tot += -b*c*Jn[b-1]
    for (b,), c in PB.terms():
        tot += c*Jn[b]
    return sp.simplify(tot)
A3 = A3.subs(w2, 0)
G3 = integral(A3, B3)
print("G3 =", G3)
sol = sp.solve(G3.subs(w0, -4*sp.log(2)), w1)
print("Omega1 =", [sp.simplify(x) for x in sol], " target 2pi^2/3 + 8 ln^2 2 =", sp.N(2*sp.pi**2/3 + 8*sp.log(2)**2, 25), [sp.N(x, 25) for x in sol])
