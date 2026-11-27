import pickle, sympy as sp, mpmath as mp
g0, A_sym, B_sym = pickle.load(open('red7_g0.pkl', 'rb'))
pi, z3, z5 = sp.pi, sp.zeta(3), sp.zeta(5)
q = sp.Symbol("q", positive=True)
z6 = pi**6 / 945
Aval = pi * (sp.Rational(3, 4) * z3**2 - sp.Rational(95, 96) * z6)
Bval = pi * (sp.Rational(9, 16) * z3**2 - sp.Rational(11, 4) * z6)
om5 = sp.expand(g0.subs({A_sym: Aval, B_sym: Bval}) / (4 * pi))
om5 = sp.expand(sp.simplify(om5))
print(om5)
mp.mp.dps = 60
print(mp.nstr(mp.mpf(str(sp.N(om5.subs(q, sp.log(2)), 60))), 50))
print("dev05 148-digit Omega5: 40860.4553545256873125440648260337042780393722154164854214585")
# collect by constants
P = sp.Poly(sp.expand(om5), q, pi, z3, z5)
for mon, cf in sorted(P.terms(), key=lambda t: -(t[0][0] + 2*t[0][1] + 3*t[0][2] + 5*t[0][3])):
    w = mon[0] + mon[1] + 3*mon[2] + 5*mon[3]
    print(mon, cf, "  weight", mon[0] + mon[1] + 3*mon[2] + 5*mon[3])
