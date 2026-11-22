# I103-mac: coordinator's review of #103 (reruns and independent check of the exact sign of D)

Machine: the coordinator's MacBook Air M5. Issue: https://github.com/nmoinvaz/negative-mass/issues/103

- `rerun_he_type.txt`: stdout of `python notes/warp/he_type.py` from `wip/i103-dsign` at dfb772e (Python 3.14.7,
  nice 10, one thread), exit 0: 8 checks pass and all 9 controls fire. It equals the committed `he_type_output.txt`
  apart from the Python version, numN's float error (8.1e-16 here) and the run time. `rerun_he_type.time`: 228.53 s
  wall, 2526330880 bytes (2.35 GiB) maximum resident.
- `rerun_he_surface.txt`: `python notes/warp/he_surface.py` with the new he_type.py, exit 0, 14 checks and all
  controls. It differs from the committed `he_surface_output.txt` in the Python version, the run time and the note's
  count of changed D values, 0 of 356 (committed 1 of 356). 58.89 s wall, 123 MiB.
- `mut_nsimplify.txt`: `he_type.py --mutate=nsimplify`, exit 1: both D = +-10^-60 tensors become Type II and the six
  sign cases read 0, so `planted` fails.
- `ind103.py`: an independent check, given the worktree path. D of the planted tensors mu R0 from sympy's charpoly and
  discriminant on its own Lorentz transform, mpmath eigenvalues at 300 digits, a battery of 14 algebraic signs (zeros
  that are not syntactically 0, nested radicals, cancellations to 1e-100 and 1e-1000) and 2 inputs that must raise,
  through he_type.exact_sign, and he_type_exact's types. Criteria in its docstring, fixed before the first run.
  - `ind103_run1.txt`: PASS, 28 s.
  - `ind103_mut_{scale,nsimp,float}.txt`: each exits 1 on its required criteria.
