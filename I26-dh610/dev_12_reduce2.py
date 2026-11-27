import sympy as sp, mpmath as mp, pickle
mp.mp.dps = 40
d = pickle.load(open("reduce1.pkl", "rb"))
lg, w0, w1, w2 = sp.symbols("ell w0 w1 w2")
A, B = d["A"].subs(w2, 0), d["B"]
# J_n = int_0^{pi/2} ln^n cos
J = [mp.quad(lambda t: mp.log(mp.cos(t))**n, [0, mp.pi/2]) for n in range(5)]
ln2 = mp.log(2)
Jc = [mp.pi/2, -mp.pi/2*ln2, mp.pi/2*(ln2**2 + mp.pi**2/12), -mp.pi/2*(ln2**3 + mp.pi**2/4*ln2 + mp.mpf(3)/2*mp.zeta(3))]
for n in range(4): print("J", n, J[n], mp.nstr(J[n]-Jc[n], 3))
print("J4", J[4])
# G4(0) pieces
W0, W1 = -4*ln2, 2*mp.pi**2/3 + 8*ln2**2
def val(expr):
    return mp.mpf(sp.N(expr.subs({w0: sp.Float(str(W0), 40), w1: sp.Float(str(W1), 40)}), 40))
PA = sp.Poly(A, lg); PB = sp.Poly(B, lg)
intA = -sum(mp.mpf(val(PA.coeff_monomial(lg**b)))*b*J[b-1] for b in range(1, 5))
intB = sum(mp.mpf(val(PB.coeff_monomial(lg**b)))*J[b] for b in range(1, 4))
Cpart = 64*(W0-1)*mp.pi**3/12
G40 = Cpart + intA + intB
print("C part", Cpart, "intA", intA, "intB", intB)
print("G4(0) =", G40, " Omega2 = G4(0)/(4pi) =", G40/(4*mp.pi))
print("closed =", 80*mp.zeta(3) - mp.mpf(8)/3*mp.pi**2*ln2 - mp.mpf(32)/3*ln2**3)
# integral of tan * C
Cf = lambda t: mp.clsin(2, mp.pi - 2*t)
print("int tan C =", mp.quad(lambda t: mp.tan(t)*Cf(t), [0, 1, mp.pi/2]), mp.pi**3/12)
