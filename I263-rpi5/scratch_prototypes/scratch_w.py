import sympy as sp
lg, u, ui, th, C, D3, Lc, q = sp.symbols("ell u ui th C D3 Lc2 q")
W0, W1, W2 = sp.symbols("w0 w1 w2")
S = u**2/(1+u**2)
def dth(e):
    return (sp.diff(e, lg)*(-u) + sp.diff(e, u)*(1+u**2) + sp.diff(e, th) + sp.diff(e, C)*(2*lg+2*q) + sp.diff(e, D3)*2*C + sp.diff(e, Lc)*lg**2 + sp.diff(e, ui)*(-(1+ui**2)))
l = -2*lg; R = 1/(1-S)
def cc(m, Om):
    # c_m with l = -2 ell, 1/R = 1 - S, via order7's table
    import importlib
    return None
# c1, c2, c3 in ell and S
c1 = W0 - 3*lg - S
c2 = W1 - 2*W0*lg + lg**2 - 2*S*lg
c3 = 2*W0*lg**2 - 2*W1*lg + W2 - 2*lg**3 - 2*S*lg**2
# direct from table to be sure
Om = [W0, W1, W2, 0,0,0,0]
Rr = sp.Symbol('Rr')
def cct(m):
    ll = sp.Symbol('l')
    if m == 1: return Om[0] + 3*ll/2 - 1 + 1/Rr
    if m == 2: return Om[0]*ll + Om[1] + ll**2/4 + ll - ll/Rr
    if m == 3: return Om[0]*ll**2/2 + Om[1]*ll + Om[2] + ll**3/4 - ll**2/2 + ll**2/(2*Rr)
for m, cm in ((1, c1), (2, c2), (3, c3)):
    e = cct(m).subs({sp.Symbol('l'): -2*lg}).subs(1/Rr, 1-S)
    print(m, sp.simplify(sp.expand(e) - sp.expand(cm)))
g = 22*lg**2 - 8*W0*lg - 2*W1
g4poly = 12*lg**2 - 2*g          # without -32 u C
print("g4poly", sp.expand(g4poly))
# P: P' = g4 * u ; P = int_0^th
Ppoly = -sp.integrate(g4poly, lg)   # d/dth of -int g dell = -g * ell' = g u
PC = -32*(u*C + lg**2 + 2*q*lg - D3/2)
P = sp.expand(Ppoly + PC)
print("P", P)
g4 = g4poly - 32*u*C
print("dP - g4 u:", sp.simplify(sp.expand(dth(P) - g4*u)))
w4p_num = sp.expand(8*lg*c2 + 2*c3 + 8*W0*lg*c1*1 - P*1)
# w4p = (...)/S ; careful: 8 ell c2 etc. are over S but c's contain S
w4p = sp.simplify(sp.expand(8*lg*c2 + 2*c3 + 8*W0*lg*c1 - P)/S)
print("w4p", sp.simplify(w4p))
# numerator N = S w4p
Nn = sp.expand(sp.simplify(w4p*S))
print("S*w4p =", Nn)
