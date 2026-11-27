# I39-mac-review: the coordinator's review of #39 (rerun, independent check ind39)

Machine: macOS (the coordinator's Mac, Apple M5, arm64), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`:
numpy, scipy, sympy, numba 0.68.1), nice 10, at most 2 processes. Issue:
https://github.com/nmoinvaz/negative-mass/issues/39. Under review: branch `wip/i39-throat-evolution` at 3a233b6, raw
`I39-dh610` at ae8bff6. Written 2026-11-27 before the first run of `ind39.py` and before the rerun.

## Rerun

`rerun.sh`, from a detached worktree `~/Source/negative-mass-r39` at 3a233b6, in `notes/wormhole_evolution`.
- Chain A: `python checks.py` (the numba kernel, 11 checks), then `DN_NO_NUMBA=1 python checks.py --kernel=numpy`.
- Chain B: `python derive.py` (25 symbolic checks), then ind39.

The expectation, written now: the same verdicts as `runs/run01_checks.log` and `derive/run02_derive.log`, with numbers
equal to the declared tolerances. numba's and numpy's floating point may differ in the last digits across machines.

## ind39

- **K1, the equations.** For D = 4 and D = 5 (n = 2, 3), the coordinator's own brute-force Ricci tensor in sympy of
  ds² = −2e^{−f}du dv + r² dΩ_n² (Christoffel symbols from the metric matrix, a code written for this review), with
  R_ab = Σ ε_k ∂_aφ_k ∂_bφ_k and □φ_k = 0. Solving R_uv, R_θθ and □φ for r_uv, f_uv and φ_uv gives the evolution
  equations; R_uu and R_vv give the constraints. These are compared:
  - symbolically with `dn.py`'s docstring equations;
  - numerically with `dn.F_np` (the code under test, numpy kernel), at 20 random states per n with a ghost and a normal
    field (ε = −1, +1).
- **K2, a case #39 did not run.** The tuned growth rate at D = 6 (n = 4), by `checks.py`'s own `bisect_A`, `fate_run` and
  `fit_growth` with its declared window (1e-3, 1e-2), bracket 0.01 and tolerance 1e-10. Settings: h = 0.01/√3 and
  0.005/√3, the D = 5 pair scaled by √(2/3), and X = 12. W = √4.68662054311946479 (#195's crate). This re-solves a case
  with the code under test; it is not independent of that code.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | For n = 2 and 3, sympy finds r_uv, f_uv and φ_uv from the field equations equal to `dn.py`'s three docstring equations, residual 0. `dn.F_np` agrees with them at 20 random states per n to 1e-12 relative |
| K2 | At D = 6, W_fit at each of the two h is within 1% of W, and the two agree within 0.5% (the bars of #39's G1) |

## Mutations (`--mutate=NAME`; each must make ind39 exit non-zero with exactly these criteria failing)

The targets are predicted from the code, not yet computed. A mutation that misses its targets is reported.

| mutation | change | targets |
|---|---|---|
| `theta-coef` | `dn.MUT = "theta_coef"` (the code's own mutation of the sphere term) before K1's numerical comparison | K1 |
| `wrong-W` | K2 compares with 1.02 W | K2 |

## Amendments

**A1, 2026-11-27, after run 1.** K2 failed as worded. At h = 0.01/√3 the fit is meaningless (slopes 0.007 and 0.049,
W_fit 0.028); at h = 0.005/√3 it gives 2.1604. The coarse h was the review's choice, scaled from D = 5, and is too
coarse for D = 6. K2 stays NOT MET. **K2b** applies the same bars (1% to W, 0.5% between the two h) to the pair
h = 0.005/√3 and 0.0025/√3, with X = 12 and the same window, bracket and tolerance. The mutation `wrong-W` is rerun on
K2b.

## Runs (filled in as they are done)

| file | what |
|---|---|
| `rerun.sh`, `rerun_derive.log`, `rerun_checks_numba.log`, `rerun_checks_numpy.log` | derive: 25 of 25 pass. checks with the numba kernel: 11 of 11 pass (I1, K, P1, P2, P3, C1, C2, G1 at D = 4 and 5, F1, S). checks with the numpy kernel and numba absent: 10 of 11 pass and K is skipped. These are the verdicts of #39's runs of record |
| `ind39_run1.log` | run 1: **exit 1, K1 passes, K2 fails.** K1: the coordinator's brute-force Ricci tensor gives `dn.py`'s r_uv, f_uv and φ_uv for n = 2 and 3 (sympy residual 0), and `dn.F_np` agrees with them to 2.8e-16 at 40 random states. The constraint comes out as r_uu + f_u r_u = −(r/n)Σε φ_u². K2: at h = 0.01/√3 the fit is meaningless (W_fit 0.028); at 0.005/√3 it gives 2.160443. K2 stays NOT MET as worded; A1 adds K2b |
| `ind39_run2_k2b.txt` | run 2 (A1): **K2b passes.** W_fit = 2.160443 at h = 0.005/√3 and 2.162520 at 0.0025/√3, against W = 2.164860 (−2.0e-3 and −1.1e-3). The two agree to 9.6e-4, and the A*_h ratio is 4.005, the h² seed |
| `ind39_run2_mut_*.txt` | `wrong-W` fails exactly K2b (−2.2e-2 against 1.02 W). `theta-coef` fails exactly K1 (`dn.F_np` off by up to 1.0 relative) |
