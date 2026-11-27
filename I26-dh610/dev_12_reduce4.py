import sympy as sp, pickle
lg, w0, w1, w2, a = sp.symbols("ell w0 w1 w2 a")
d = pickle.load(open("reduce1.pkl", "rb"))
A4, B4 = d["A"].subs(w2, 0), d["B"]
gen = sp.sqrt(sp.pi)/2*sp.gamma((a+1)/2)/sp.gamma(a/2+1)
ser = sp.series(gen, a, 0, 5).removeO()
Jn = [sp.simplify(sp.expand_func(sp.factorial(n)*ser.coeff(a, n))) for n in range(5)]
def integral(A, B):
    PA = sp.Poly(A, lg); PB = sp.Poly(B, lg); tot = 0
    for (b,), c in PA.terms(): tot += -b*c*Jn[b-1]
    for (b,), c in PB.terms(): tot += c*Jn[b]
    return tot
L2s = sp.log(2)
Cpart = 64*(w0 - 1)*sp.pi**3/12
G40 = Cpart + integral(A4, B4)
G40 = G40.subs({w0: -4*L2s, w1: 2*sp.pi**2/3 + 8*L2s**2})
Om2 = sp.simplify(sp.expand(G40/(4*sp.pi)))
print("Omega2 =", Om2)
target = 80*sp.zeta(3) - sp.Rational(8, 3)*sp.pi**2*sp.log(2) - sp.Rational(32, 3)*sp.log(2)**3
print("minus target:", sp.simplify(sp.expand(Om2 - target)))
print(sp.N(Om2, 40))
