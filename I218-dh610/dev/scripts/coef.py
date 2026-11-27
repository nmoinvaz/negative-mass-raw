import pickle, sympy as sp, numpy as np
from lin import rho, W, L
As, A1 = sp.symbols("As A1")
lam = sp.Symbol("lam")
M4s, _ = pickle.load(open("sys4n.pkl", "rb"))
Nn, H2sol, sys3 = pickle.load(open("l1sys2.pkl", "rb"))
N2s = Nn.subs(W, sp.sqrt(lam))
_M4 = sp.lambdify((rho, lam, L, As, A1), M4s, "numpy", cse=True)
_N2 = sp.lambdify((rho, lam, As, A1), N2s, "numpy", cse=True)
def M4(r, l, LL, a, a1):
    return np.array(_M4(r, l, LL, a, a1), dtype=complex)
def N2(r, l, a, a1):
    return np.array(_N2(r, l, a, a1), dtype=complex)
