"""
Coordinator's independent check of #131: does he_surface.py's equality on he_type_exact's D catch any change of D, not
only the nsimplify rounding that its own control `nsimplify-back` plants?

It runs he_surface.main() (checks only) in-process from the worktree given as argv[1], with he_type.he_type_exact
replaced by this script's wrappers, and reads he_surface.RESULTS. The wrappers keep the type that he_type_exact gives and
change only the returned D, so a check fails only through #131's equality.
Usage: python ind131.py WORKTREE [--mutate=identity]

Criteria, fixed before the first run. The checks that call `classify` are axis, locus_points, null_points and
outside_description (read from the source before the run); planted calls he_type_exact directly, without `classify`.
  C1  wrapper returns (type, D) unchanged: all 14 checks pass.
  C2  wrapper returns D + 10^-80 where D != 0 (sign and zero-ness kept, value changed): exactly the classify checks
      that have a point with D != 0 fail, a nonempty subset of the four above, and no other check fails.
  C3  wrapper returns D + 10^-80 at D = 0 only (zero-ness changed, every nonzero D kept): exactly the classify checks
      that have a point with D = 0 fail, a nonempty subset of the four, and no other check fails.
  C4  C2 and C3 together cover all four classify checks.
Mutation (must make the script exit 1):
  identity  C2's and C3's wrappers return D unchanged: C2 and C3 must fail.
Exit 1 if any criterion fails.
"""
import io, sys, contextlib
import sympy as sp

WT = sys.argv[1]
mut = next((a.split('=', 1)[1] for a in sys.argv[2:] if a.startswith('--mutate=')), None)
assert mut in (None, 'identity')
sys.path.insert(0, WT + '/notes/warp')
saved = sys.argv
sys.argv = ['he_surface.py', '--no-controls']
import he_surface as hs  # noqa: E402
import he_type as ht  # noqa: E402
CLASSIFY = {"axis", "locus_points", "null_points", "outside_description"}
EXACT = ht.he_type_exact
tiny = sp.Rational(1, 10**80)
seen = {"nonzero": 0, "zero": 0}


def run(wrapper):
    ht.he_type_exact = wrapper
    hs.RESULTS.clear(); hs.D_CHANGED.clear(); hs.MUT.clear()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            hs.main()
        except SystemExit:
            pass
    ht.he_type_exact = EXACT
    return {n for n, ok in hs.RESULTS if not ok}, len(hs.RESULTS)


def w_same(R4):
    return EXACT(R4)


def w_nonzero(R4):
    typ, D = EXACT(R4)
    if D != 0:
        seen["nonzero"] += 1
        return typ, (D if mut == 'identity' else D + tiny)
    return typ, D


def w_zero(R4):
    typ, D = EXACT(R4)
    if D == 0:
        seen["zero"] += 1
        return typ, (D if mut == 'identity' else D + tiny)
    return typ, D


fails = []
print("# ind131: he_surface.py's D equality against wrappers that change only D" + (f", mutate={mut}" if mut else ""))
f1, n1 = run(w_same)
ok1 = not f1 and n1 == 14
print(f"  C1 unchanged D: {n1} checks, failing {sorted(f1)}: {'PASS' if ok1 else 'FAIL'}")
f2, n2 = run(w_nonzero)
ok2 = bool(f2) and f2 <= CLASSIFY
print(f"  C2 D + 1e-80 where D != 0 ({seen['nonzero']} calls): failing {sorted(f2)}: {'PASS' if ok2 else 'FAIL'}")
f3, n3 = run(w_zero)
ok3 = bool(f3) and f3 <= CLASSIFY
print(f"  C3 D + 1e-80 where D = 0 ({seen['zero']} calls): failing {sorted(f3)}: {'PASS' if ok3 else 'FAIL'}")
ok4 = (f2 | f3) == CLASSIFY
print(f"  C4 together: {sorted(f2 | f3)} against {sorted(CLASSIFY)}: {'PASS' if ok4 else 'FAIL'}")
for name, ok in (("C1", ok1), ("C2", ok2), ("C3", ok3), ("C4", ok4)):
    if not ok:
        fails.append(name)
sys.argv = saved
print("RESULT", "FAIL: " + ", ".join(fails) if fails else "PASS")
sys.exit(1 if fails else 0)
