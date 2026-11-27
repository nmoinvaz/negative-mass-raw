import sys, time
sys.path.insert(0, '/home/nathan/Source/negative-mass-i263/notes/wormhole_largeD')
sys.argv = sys.argv[:1]
import sympy as sp
import order7 as o7
t0 = time.time()
lg, u, ui, th, C, D3, Lc, q = o7.X_LG, o7.X_U, o7.X_UI, o7.X_TH, o7.X_C, o7.X_D3, o7.X_LC, o7.X_Q
w = sp.symbols("w0:6")
S = sp.Symbol("S")
R = 1/(1 - S)
l = -2*lg
Om = list(w) + [0, 0]
Y = [sp.Integer(1), 2*lg, 4*w[0]*lg - 6*lg**2, 4*w[1]*lg - 4*lg**3 + 32*lg**2 - 16*w[0]*lg + 32*u*C - 16*D3]
L = [sp.Integer(-1), -2*w[0] + 4*lg, -2*w[1] - 4*w[0]*lg + 16*lg**2 + 16*u*C]
h3 = o7.hk(3, Om, l, R, Y, L)
sc = u*(1 - S)
Bf = -32*(lg + q)*C + 16*S*C + 32*Lc + 16*sc*lg*(lg + 2*q) - 4*w[1]*th - 2*w[1]*sc
L = L + [-2*h3 + 2*u*Bf]
cx = lambda m, o=Om: o7.cc(m, o, l, R)
fa = sp.factorial
pc = o7.x_pieces()
# substitute S-dependent pieces: pieces are in terms of u only (S = u^2/(1+u^2))
Su = u**2/(1+u**2)
def inS(e):
    return e
g = pc["g"]; P = pc["P"]; Wn = pc["Wn"]; lim = pc["lim"]
cC = pc["cC"]
lims = lim.subs(o7.X_J2, sp.Symbol("J2"))
Wfull = Wn - lims
F3 = sum(L[3-j]*l**j/fa(j) for j in range(4))
def Fp(j, lo, hi):
    return sum(L[j-qq]*l**qq/fa(qq) for qq in range(lo, hi+1))
def Sk(k, upto, o=Om):
    return sum(Y[j]*cx(k-j, o) for j in range(upto))
O0 = w[0]
t = []
t.append(8*lg*Sk(6, 4)/S)
t.append(2*Fp(6, 3, 6))
t.append(2*(Sk(7, 4) - Om[6])/S)
t.append(-4*(lg - O0)*Fp(5, 2, 5))
t.append(8*O0*lg*Sk(5, 4)/S)
t.append(-2*(g + cC*u*C)*Fp(4, 1, 4))
t.append(-2*P*(S*L[3] + Sk(4, 4))/S)
t.append(-2*Wfull*u*F3)
tot = sum(t)
tot = tot.subs(X := o7.X_W[0], w[0]) if False else tot
# the pieces use o7.X_W symbols w0..w2, same names as here: unify
rep = {o7.X_W[0]: w[0], o7.X_W[1]: w[1], o7.X_W[2]: w[2]}
tot = tot.subs(rep).subs(ui, 1/u)
tot = tot.subs(w[0], -4*q)
tot = sp.expand(tot)
print("expanded", len(tot.args), time.time()-t0)
tot = sp.expand(sp.cancel(tot.subs(S, u**2/(1+u**2))))
print("cancelled", time.time()-t0)
Pl = sp.Poly(tot, C, D3, Lc)
print("monomials (C,D3,Lc2):", sorted(Pl.monoms()))
import pickle
pickle.dump({m: cf for m, cf in Pl.terms()}, open('parts7.pkl', 'wb'))
print(time.time()-t0)
