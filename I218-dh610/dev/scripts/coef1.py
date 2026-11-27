import pickle, sympy as sp, numpy as np
from lin import rho, W, L
As, A1 = sp.symbols("As A1")
lam = sp.Symbol("lam")
M3s, gv, vars3 = pickle.load(open("l1h3.pkl", "rb"))
M3s = M3s.subs(W, sp.sqrt(lam)); gs = gv.subs(W, sp.sqrt(lam))
_M3 = sp.lambdify((rho, lam, As, A1), M3s, "numpy", cse=True)
_g = sp.lambdify((rho, lam, As, A1), gs, "numpy", cse=True)
def M3(r, l, a, a1):
    return np.array(_M3(r, l, a, a1), dtype=complex)
def gvec(r, l, a, a1):
    return np.array(_g(r, l, a, a1), dtype=complex).reshape(-1)
