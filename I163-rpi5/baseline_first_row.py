#!/usr/bin/env python3
"""beta_A at the 16 first-row gamma_1 of [GGS09a] Table I from #151's UNMODIFIED notes/ellis_efold.py (main 2455a0d),
same call as run_G's G5: method_A(g, W_A, L=30, lam=lam_of(g)). Prints repr() so the values round-trip.
usage: baseline_first_row.py <path to notes dir> [L]"""
import sys, time
sys.path.insert(0, sys.argv[1])
import ellis_efold as E
L = float(sys.argv[2]) if len(sys.argv) > 2 else 30.0
print("baseline_first_row: ellis_efold from", E.__file__, "L =", L, flush=True)
for g in E.TABLE:
    t0 = time.time()
    b = E.method_A(g, E.W_A, L=L, lam=E.lam_of(g))
    print(f"g={g!r} beta_A={b[0]!r} nroots={len(b)} T={E.T_of(b[0], g)!r} wall={time.time()-t0:.1f}s", flush=True)
