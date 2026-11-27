import sys
sys.path.insert(0, "/home/nathan/Source/negative-mass-i218/notes/black_universe")
from polar_derive import *
r = reduce_l2(); M4 = matrix_l2(r)
R = sp.Symbol("R2")
def show(e):
    e = sp.simplify(e)
    return sp.factor(e.subs(rho**2 + 1, R))
names = ["H0'", "Pi'", "K'", "F'"]
cols = ["H0", "Pi", "K", "F"]
for i in range(4):
    for j in range(4):
        print("M[%s,%s] =" % (names[i], cols[j]), sp.simplify(M4[i, j]))
r1 = reduce_l1(); M3 = matrix_l1(r1)
for i, n in enumerate(["H0'", "H2'", "F'"]):
    for j, cn in enumerate(["H0", "H2", "F"]):
        print("M3[%s,%s] =" % (n, cn), sp.simplify(M3[i, j]))
g, _ = gauge_l1()
print("g =", [sp.simplify(x) for x in g])
