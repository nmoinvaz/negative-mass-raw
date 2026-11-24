"""Re-solve #133's Rodal root r = 5.07635399285, w = 1.030003 (nearest inadmissible) from a start 1e-3 away, 60 digits."""
import mpmath as mp, sympy as sp, runpy, sys
sys.argv = ['x']
ns = {}
src = open('ind133b.py').read().split('# ---- D6 exact ----')[0]
exec(compile(src, 'ind133b-head', 'exec'), ns)
ph, A, Bv, W = ns['ph'], ns['A'], ns['Bv'], ns['W']
fE = sp.lambdify((ph, A, Bv, W), [ns['E1s'], ns['E2s']], 'mpmath')
mp.mp.dps = 60
sg, Rb, vv = mp.mpf(4), mp.mpf(5), mp.mpf(1)
def jets(r):
    tp, tm = mp.tanh(sg * (r + Rb)), mp.tanh(sg * (r - Rb)); k = 2 * mp.tanh(sg * Rb)
    f = (tp - tm) / k; f1 = sg * ((1 - tp**2) - (1 - tm**2)) / k; f2 = -2 * sg**2 * (tp * (1 - tp**2) - tm * (1 - tm**2)) / k
    return vv * (1 - f), vv * r * f1, vv * r**2 * f2, f2 + f1 / r
def G(r, w):
    p, a_, b_, _ = jets(r); return fE(p, a_, b_, w)
sol = mp.findroot(G, (mp.mpf('5.07735399285'), mp.mpf('1.031003')), tol=mp.mpf(10)**-50, maxsteps=200)
r, w = sol
J = mp.matrix([[mp.diff(lambda x: G(x, w)[i], r), mp.diff(lambda x: G(r, x)[i], w)] for i in range(2)])
print(f"r = {mp.nstr(r, 15)}, w = {mp.nstr(w, 12)}, |E| = {mp.nstr(max(abs(q) for q in G(r, w)), 3)}, det J = {mp.nstr(mp.det(J), 5)}, T = {mp.nstr(jets(r)[3], 6)}")
print("match", abs(r - mp.mpf('5.07635399285')) < 1e-10 and abs(w - mp.mpf('1.030003')) < 1e-6)
