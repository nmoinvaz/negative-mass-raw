"""Cross-check of he_type.exact_sign on random algebraic expressions against sympy's evalf at 400 digits (not iv).

Planted truth: P = (e + 1)^3 - expand((e + 1)^3) is exactly 0 for any e; P + 10^-k is exactly +10^-k and P - 10^-k is
-10^-k (k = 30, 60, 90). A generic e has its sign compared with evalf(400), accepted where |value| > 10^-300.
Pass: exact_sign equals the planted sign on every built case, equals the evalf sign on every generic one.
usage: fuzz_sign.py <count> <seed> [nsimplify]; exit 1 on a mismatch. The third argument restores the old
nsimplify (he_type's MUT), a control that must produce mismatches.
"""
import random, sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, "/home/nathan/Source/negative-mass-i103/notes/warp")
import sympy as sp
import he_type as ht

Q = sp.Rational
count, seed = int(sys.argv[1]), int(sys.argv[2])
random.seed(seed)
ht.MUT = sys.argv[3] if len(sys.argv) > 3 else None


def atom():
    k = random.choice(["int", "rat", "sqrt", "cbrt"])
    if k == "int":
        return sp.Integer(random.randint(-9, 9))
    if k == "rat":
        return Q(random.randint(-9, 9), random.randint(1, 9))
    if k == "sqrt":
        return sp.sqrt(random.choice([2, 3, 5, 7]))
    return sp.cbrt(random.choice([2, 3]))


def expr(d):
    if d == 0:
        return atom()
    a, b = expr(d - 1), expr(d - 1)
    return random.choice([a + b, a - b, a * b, (a + b)**2])


n = bad = zeros = nonrat = 0
t0 = time.time()
for i in range(count):
    e = expr(random.choice([1, 2]))
    kind = random.choice(["generic", "zero", "plus", "minus"])
    P = (e + 1)**3 - sp.expand((e + 1)**3)
    k = random.choice([30, 60, 90])
    D, want = {"generic": (e, None), "zero": (P, 0), "plus": (P + Q(1, 10**k), 1), "minus": (P - Q(1, 10**k), -1)}[kind]
    t = time.time()
    got = ht.exact_sign(D)
    dt = time.time() - t
    if want is None:
        v = D.evalf(400)
        ref = 0 if abs(v) < sp.Float(10)**-300 else (1 if v > 0 else -1)
        ok = got == ref
    else:
        ok = got == want
    n += 1
    zeros += got == 0
    nonrat += not D.is_Rational
    bad += not ok
    print(f"{i:4d} {kind:8s} got {got:2d} {'ok' if ok else 'MISMATCH'} {dt:6.2f} s  {str(D)[:90]}", flush=True)
print(f"{n} expressions, {nonrat} not rational (the interval and minimal-polynomial branch), {zeros} decided 0, "
      f"{bad} mismatches, {time.time()-t0:.1f} s")
sys.exit(1 if bad else 0)
