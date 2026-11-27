import pickle, sympy as sp
from sympy.printing.pycode import pycode
from lin import rho, W, L
As, A1 = sp.symbols("As A1"); lam = sp.Symbol("lam")
M4s, _ = pickle.load(open("sys4n.pkl", "rb"))
M3s, gv, vars3 = pickle.load(open("l1h3.pkl", "rb"))
M3s = M3s.subs(W, sp.sqrt(lam)); gs = gv.subs(W, sp.sqrt(lam))
def emit(name, args, mat, cplx=False):
    flat = [sp.simplify(e) for e in mat]
    reps, exprs = sp.cse(flat, optimizations="basic")
    lines = ["def %s(%s):" % (name, ", ".join(args))]
    for s, e in reps:
        lines.append("    %s = %s" % (s, pycode(e)))
    lines.append("    return (%s)" % ", ".join(("(%s)+0j" if cplx else "1.0*(%s)") % pycode(e) for e in exprs))
    return "\n".join(lines)
out = ["import math", "from math import sqrt", ""]
out.append(emit("m4_entries", ["rho", "lam", "L", "As", "A1"], M4s)); out.append("")
out.append(emit("m3_entries", ["rho", "lam", "As", "A1"], M3s)); out.append("")
out.append(emit("g3_entries", ["rho", "lam", "As", "A1"], gs)); out.append("")
out.append(emit("m4_entries_c", ["rho", "lam", "L", "As", "A1"], M4s, True)); out.append("")
out.append(emit("m3_entries_c", ["rho", "lam", "As", "A1"], M3s, True)); out.append("")
out.append(emit("g3_entries_c", ["rho", "lam", "As", "A1"], gs, True))
open("coef_gen.py", "w").write("\n".join(out) + "\n")
print(len("\n".join(out)), "chars")
