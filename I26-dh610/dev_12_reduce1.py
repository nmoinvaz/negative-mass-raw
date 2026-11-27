import sympy as sp
lg, S, u, C, D3, w0, w1, w2 = sp.symbols("ell S u C D3 w0 w1 w2")
c2s = 1 - S                      # cos^2
L0 = -1; L1 = -2*w0 + 4*lg
L2 = -2*w1 - 4*w0*lg + 16*lg**2 + 16*u*C
Y0 = 1; Y1 = 2*lg; Y2 = 4*w0*lg - 6*lg**2
Y3 = 4*w1*lg - 4*lg**3 + 32*lg**2 - 16*w0*lg + 32*u*C - 16*D3
c1 = w0 - 3*lg - 1 + c2s
c2 = -2*w0*lg + w1 + lg**2 - 2*lg + 2*lg*c2s
c3 = 2*w0*lg**2 - 2*w1*lg + w2 - 2*lg**3 - 2*lg**2 + 2*lg**2*c2s
c4 = -sp.Rational(4,3)*w0*lg**3 + 2*w1*lg**2 - 2*w2*lg + lg**4/3 - sp.Rational(4,3)*lg**3 + sp.Rational(4,3)*lg**3*c2s   # Omega3 dropped
h3 = S*L2 + c3 + Y1*c2 + Y2*c1 + Y3/2
I4 = 8*lg*h3/S + 2*(-2*lg*L2 + 2*lg**2*L1 + sp.Rational(4,3)*lg**3) + 2*(c4 + Y1*c3 + Y2*c2 + Y3*c1)/S
I4 = sp.expand(I4)
# parts
Cc = I4.coeff(C, 1); Dc = I4.coeff(D3, 1)
ell_part = sp.expand(I4.subs({C: 0, D3: 0}))
print("D3 coeff:", sp.factor(Dc))
print("C coeff :", sp.factor(Cc))
A = sp.expand(ell_part*S).subs(S, 0)   # A(ell) = S*I4_ell at S -> 0
A_full = sp.collect(sp.expand(ell_part*S), S)
print("S*I4_ell collected in S:", sp.collect(sp.expand(ell_part*S), S, evaluate=False).keys())
cA = sp.expand(ell_part*S).coeff(S, 0); cB = sp.expand(ell_part*S).coeff(S, 1); cC = sp.expand(ell_part*S).coeff(S, 2)
print("A (coeff of 1/S):", sp.collect(cA, lg))
print("B (S^0):", sp.collect(cB, lg))
print("S^1 coeff (should be 0):", cC)
print("w2 in A,B:", cA.has(w2), cB.has(w2))
import pickle
pickle.dump({"A": cA, "B": cB}, open("reduce1.pkl", "wb"))
