"""
Coordinator's independent check of #103: he_type.exact_sign and the two planted tensors with D = +-10^-60.

The object under test, he_type.exact_sign (and he_type_exact for C4), is imported from the worktree given as argv[1].
Everything else is written here: D comes from sympy's Matrix.charpoly and sp.discriminant on M = diag(-1, 1, 1) T (not
he_type's mixed_block, cubic or disc), the Lorentz transform is this script's own (a boost along e_2 with rapidity
artanh(3/5) and a rotation by the Pythagorean angle (3/5, 4/5) in the (e_1, e_2) plane), and the eigenvalue cross-check
is mpmath's at 300 digits.
Usage: python ind103.py WORKTREE [--mutate=scale|nsimp|float]

Criteria, fixed before the first run:
  C1  For T = mu R0, mu = 10^-10 2^(-1/3), R0 = diag(0, 1, -1) and R0 = e1 e2 + e2 e1 (3x3 blocks), and for the same T
      after this script's Lorentz transform, sp.simplify(D - target) == 0 with target +10^-60 and -10^-60.
  C2  At 300 digits, the eigenvalues of M after the transform: all three real (max |Im| < 10^-250) for the first, and a
      pair with |Im| > 10^-12 for the second.
  C3  exact_sign returns the known sign of each of 14 algebraic numbers built here (zeros that are not syntactically
      0, nested radicals, cancellations to 10^-100 and 10^-1000, and a rational), and raises (any exception) rather than
      return a sign for D with a Float and for D = (-2)^(1/3) - 1 (not real).
  C4  he_type_exact of this script's 4x4 tensors (C1's transformed blocks, e_3 entry -5/11) gives Type I and Type IV.
Mutations (each must make the script exit 1):
  scale  mu (1 + 10^-3) in C1's tensors: C1 must fail.
  nsimp  C3 judges with sign(nsimplify(D)) in place of exact_sign: C3 must fail.
  float  C3 judges with the sign of float(D): C3 must fail.
Exit 1 if any criterion fails.
"""
import sys, time
import mpmath as mp
import sympy as sp

WT = sys.argv[1]
mut = next((a.split('=', 1)[1] for a in sys.argv[2:] if a.startswith('--mutate=')), None)
assert mut in (None, 'scale', 'nsimp', 'float')
sys.path.insert(0, WT + '/notes/warp')
saved, sys.argv = sys.argv, sys.argv[:1]
import he_type as ht  # noqa: E402
sys.argv = saved
T0 = time.time()
Q = sp.Rational
fails = []


def report(name, ok, detail):
    print(f"  {name}: {detail}: {'PASS' if ok else 'FAIL'}  [{time.time() - T0:.0f} s]", flush=True)
    if not ok:
        fails.append(name)


lam = sp.Symbol('lam')
eta = sp.diag(-1, 1, 1)
mu = Q(1, 10**10) * sp.Integer(2) ** Q(-1, 3)
if mut == 'scale':
    mu = mu * (1 + Q(1, 1000))
R0s = [("Type I", sp.diag(0, 1, -1), Q(1, 10**60)),
       ("Type IV", sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]), -Q(1, 10**60))]
ch, sh = Q(5, 4), Q(3, 4)                                   # cosh, sinh of artanh(3/5)
B = sp.Matrix([[ch, 0, sh], [0, 1, 0], [sh, 0, ch]])        # boost mixing e_0 and e_2
Rr = sp.Matrix([[1, 0, 0], [0, Q(3, 5), -Q(4, 5)], [0, Q(4, 5), Q(3, 5)]])
Lt = B * Rr
assert Lt.T * eta * Lt == eta


def Dof(T):
    M = eta * T
    p = M.charpoly(lam)
    return sp.discriminant(p.as_expr(), lam)


print("# ind103: exact sign of D for he_type_exact (#103)" + (f", mutate={mut}" if mut else ""), flush=True)
tensors = []
for name, R0, tgt in R0s:
    T = mu * R0
    Tp = Lt.T * T * Lt
    d0, d1 = Dof(T), Dof(Tp)
    ok = sp.simplify(d0 - tgt) == 0 and sp.simplify(d1 - tgt) == 0
    report(f"C1 {name}", ok, f"D = {sp.simplify(d0)} untransformed, {sp.simplify(d1)} transformed, target {tgt}")
    tensors.append((name, Tp))
    mp.mp.dps = 300
    Mn = mp.matrix([[mp.mpf(sp.N(v, 320)) for v in row] for row in (eta * Tp).tolist()])
    ev = mp.eig(Mn, left=False, right=False)
    mi = max(abs(mp.im(e)) for e in ev)
    ok2 = (mi < mp.mpf(10) ** -250) if name == "Type I" else (mi > mp.mpf(10) ** -12)
    report(f"C2 {name}", ok2, f"max |Im lambda| = {mp.nstr(mi, 5)} at 300 digits")
    mp.mp.dps = 15

s2, s3, s6, c2 = sp.sqrt(2), sp.sqrt(3), sp.sqrt(6), sp.cbrt(2)
u = Q(1, 10**100)
zA = (s2 + s3) ** 2 - 5 - 2 * s6                              # 0
zB = sp.sqrt(3 + 2 * s2) - 1 - s2                             # 0 (denesting)
zC = (c2 + c2 ** 2) ** 3 - 6 - 6 * c2 - 6 * c2 ** 2           # 0: (c + c^2)^3 = 6 + 6c + 6c^2 for c^3 = 2
cases = [("(sqrt2 + sqrt3)^2 - 5 - 2 sqrt6", zA, 0), ("sqrt(3 + 2 sqrt2) - 1 - sqrt2", zB, 0),
         ("(c + c^2)^3 - 6 - 6c - 6c^2, c = cbrt2", zC, 0),
         ("zA + 10^-100", zA + u, 1), ("zA - 10^-100", zA - u, -1),
         ("zB + 10^-100", zB + u, 1), ("zB - 10^-100", zB - u, -1),
         ("zC + 10^-1000", zC + Q(1, 10**1000), 1), ("zC - 10^-1000", zC - Q(1, 10**1000), -1),
         ("sqrt(10^200 + 1) - 10^100", sp.sqrt(10**200 + 1) - 10**100, 1),
         ("10^100 - sqrt(10^200 + 1)", 10**100 - sp.sqrt(10**200 + 1), -1),
         ("2^(1/3) 3^(1/2) - 6^(5/6) + 10^-100", sp.cbrt(2) * s3 - sp.Integer(6) ** Q(5, 6) + u, None),
         ("-3/7", -Q(3, 7), -1), ("sqrt2 - 1414213562373095/10^15", s2 - Q(1414213562373095, 10**15), 1)]
# the 12th: 2^(1/3) 3^(1/2) = 2^(1/3) 3^(1/2), while 6^(5/6) = 2^(5/6) 3^(5/6) > it, so the sign is -1
cases[11] = (cases[11][0], cases[11][1], -1)


def judge(D):
    if mut == 'nsimp':
        n = sp.nsimplify(D)
        return 1 if n > 0 else -1 if n < 0 else 0
    if mut == 'float':
        f = float(D)
        return 1 if f > 0 else -1 if f < 0 else 0
    return ht.exact_sign(D)


wrong = []
for name, D, want in cases:
    try:
        got = judge(D)
    except Exception as e:  # noqa: BLE001
        got = f"raised {type(e).__name__}"
    if got != want:
        wrong.append(f"{name}: got {got}, want {want}")
for name, D in (("D with a Float", sp.sqrt(2) - sp.Float('1.4142')), ("(-2)^(1/3) - 1", sp.Integer(-2) ** Q(1, 3) - 1)):
    try:
        got = judge(D)
        wrong.append(f"{name}: returned {got}, should raise")
    except Exception:  # noqa: BLE001
        pass
report("C3 exact_sign battery", not wrong, f"{len(cases)} signs and 2 raises; wrong: {wrong}")
print(f"     (premise: sp.nsimplify(10^-60) = {sp.nsimplify(Q(1, 10**60))})", flush=True)

got4 = []
for name, Tp in tensors:
    T4 = sp.zeros(4, 4)
    T4[:3, :3] = Tp
    T4[3, 3] = -Q(5, 11)
    got4.append(ht.he_type_exact(T4)[0])
report("C4 he_type_exact", got4 == ["I", "IV"], f"types {got4}, expected ['I', 'IV']")
print("RESULT", "FAIL: " + ", ".join(fails) if fails else "PASS", f"[{time.time() - T0:.0f} s]")
sys.exit(1 if fails else 0)
