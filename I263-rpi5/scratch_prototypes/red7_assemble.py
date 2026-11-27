import sys, time, pickle
sys.path.insert(0, '/home/nathan/Source/negative-mass-i263/notes/wormhole_largeD')
sys.argv = sys.argv[:1]
import sympy as sp, mpmath as mp
from red7_lib import *
I, Fs = pickle.load(open('red7_state5.pkl', 'rb'))
Bs = pickle.load(open('red7_bnd.pkl', 'rb'))
v5 = sp.Symbol("v5")
pi = sp.pi
z2, z4, z6 = pi**2/6, pi**4/90, pi**6/945
# J-tilde_n = int_0^{pi/2} ln^n(2 cos) = n! [a^n] (pi/2) Gamma(a+1)/Gamma(a/2+1)^2
a = sp.Symbol("a")
ser = sp.series((pi/2) * sp.gamma(a + 1) / sp.gamma(a/2 + 1)**2, a, 0, 8).removeO()
Jt = [sp.simplify(sp.expand_func(sp.factorial(n) * ser.coeff(a, n))) for n in range(8)]
Jt = [sp.expand(sp.nsimplify(j) if False else j) for j in Jt]
print("Jt:", [sp.simplify(j) for j in Jt[:7]])

# masters
z3, z5 = sp.zeta(3), sp.zeta(5)
A_sym, B_sym = sp.Symbol("Amast"), sp.Symbol("Bmast")        # <lt^2 C^2>, <lt^3 D3>: identified numerically (placeholders)
Cm = pi**7/3456 - pi**7/2880 + (pi/16) * (sp.Rational(61, 6) * z6 - 6 * z3**2)       # <K2^2> (Parseval, Euler sums)
Dm = 11 * pi**5 / 1440                                                                # <th^2 lt^2>
lt2D3 = (pi/4) * (5 * z5 - 2 * z2 * z3) + pi**3 * z3 / 32                              # <lt^2 D3>
masters = {
    (0, 0, 2, 0, 0): Cm,
    (1, 0, 1, 0, 0): sp.Rational(7, 8) * z3 * Jt[2] - lt2D3 / 2,
    (1, 0, 1, 0, 1): -A_sym / 4,
    (2, 0, 0, 0, 0): pi**5 / 360,
    (2, 0, 0, 0, 1): sp.Integer(0),
    (2, 0, 0, 0, 2): A_sym,
    (0, 0, 1, 1, 0): pi**2 / 8 * Jt[2] - Dm / 2,
    (0, 1, 0, 0, 3): B_sym,
    (1, 0, 0, 1, 0): pi * z3 / 4,
    (1, 0, 0, 1, 1): -pi**5 / 1440,
    (0, 0, 0, 2, 0): pi**3 / 24,
}
for b in range(7):
    masters[(0, 0, 0, 0, b)] = Jt[b]
P = sp.Poly(sp.expand(I), C, D3, K2, th, lt)
total = sum(b.subs({Jt2: Jt[2], Jt3: Jt[3]}) for _, b in Bs)
for m, cf in P.terms():
    total += cf * masters[m]
total = sp.expand(total)
print("G7 (v5 symbolic) free symbols:", total.free_symbols)
slope = sp.simplify(sp.diff(total, v5))
print("slope in v5:", slope)
g0 = sp.expand(total.subs(v5, 0))
pickle.dump((g0, A_sym, B_sym), open('red7_g0.pkl', 'wb'))
print("G7(v5=0) in A, B:", sp.collect(g0, [A_sym, B_sym], evaluate=False).keys())
print("coefficient of A:", sp.simplify(g0.coeff(A_sym)), " of B:", sp.simplify(g0.coeff(B_sym)))
