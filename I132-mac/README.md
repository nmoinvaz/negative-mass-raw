# I132-mac: coordinator's review of #132, the sign of F + r f' at the tanh wall's T1 roots

Machine: the coordinator's Mac (Apple M5, macOS, Python 3.14.7, sympy 1.14.0, mpmath 1.3.0), one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/132

| file | what |
|---|---|
| `rerun_he_tanh_bound.txt`, `.time` | `python notes/warp/he_tanh_bound.py` from e083aa1: exit 0, 7 checks pass, 10 controls fire, 494 s, 69 MiB; equal to the committed output except the timings |
| `rerun_mutate_shift.txt` | `--mutate=shift` alone: exit 1, fails `cover` only, its frozen target |
| `ind132.py` | independent check, no code shared with he_tanh_bound.py (criteria in its docstring, fixed before the first run) |
| `ind132_run1.txt` | run 1: C2 failed by two errors of this script's code (the root condition kept f's factor 1 + C; the zero test did not simplify), with C4 confirming the identity numerically |
| `ind132_run2.txt` | run 2, criteria unchanged: C1-C5 pass. m > 0 by m(0) = m'(0) = m''(0) = 0 and m''' = w sinh w; one root at each of 9 sigma R_b from 1e-3 to 100, F + r f' equal to the closed form within 2e-48; supremum -0.0536756031 |
| `ind132_mut_*.txt` | its mutations `profile`, `msign`, `chain`: each exits 1 on its target |
