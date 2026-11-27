import sys, time, pickle
import sympy as sp
from lin import *
exec(open("red.py").read().split("J = {k")[0].split("E = pickle")[1].split("\n",1)[1])  # reuse definitions (jets, D, tojet)
J, sol, Rd = pickle.load(open("red.pkl", "rb"))
F_1, F_2 = jet["F"][1], jet["F"][2]
H0_1, H1_1, K_1 = jet["H0"][1], jet["H1"][1], jet["K"][1]
alg = {}
for k in ("tt", "rr", "ang_tr"):
    alg[k] = sp.factor(sp.together(Rd[k]))
    print(k, "=", alg[k], "\n")
# are they proportional?
a, b, c = alg["tt"], alg["rr"], alg["ang_tr"]
print("tt/rr:", sp.simplify(a / b)); print("tt/ang_tr:", sp.simplify(a / c))
pickle.dump(alg, open("alg.pkl", "wb"))
