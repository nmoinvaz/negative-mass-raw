# I218-mac-review: the coordinator's review of #218 (rerun, independent check ind218)

Machine: macOS (the coordinator's Mac), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`: numpy 2.5.4, scipy 1.18.1,
sympy 1.14.0, mpmath 1.3.0), nice 10, at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/218. Under
review: branch `wip/i218-polar-mads` at 4c8c5ca, raw `I218-dh610` at 2c4663c. Written 2026-11-27 before the first run of
`ind218.py` and before the rerun.

## Rerun

From a detached worktree at 4c8c5ca, in `notes/black_universe`: `polar_derive.py check`, `polar.py planted`, and two
count runs, polar ℓ = 2 at c = −0.3 and M-AdS at c = 0.5 (each at R2). The expectation, written now: 20 PASS and 7 PASS, the
planted values to their printed digits, and the two counts (0, and 1 with the printed W) equal to the runner's logs.

## ind218: the Ellis polar QNMs by complex scaling

The coordinator's own code, sharing only the master potentials as printed in `polar.md`:
- ℓ = 1, derived: V = 1/R⁴;
- its Darboux partner, [ABCKY23]'s master potential at L = 2: V = 2/R² − 3/R⁴;
- ℓ = 2: V = 6/R² − 3/R⁴;
- the ℓ = 1 test scalar: V = 2/R² + 1/R⁴.

Here R² = 1 + x² (Ellis, a = 1), and x is proper radial distance, which is also the tortoise coordinate since A = 1.

Method: −u″ + V u = ω² u on x ∈ [−L, L], uniformly complex-scaled, x = s e^{iθ}, θ = 0.9. The scaling rotates the
continuum by −2θ and exposes quasinormal modes with |arg ω²| < 2θ. The derivative is a fourth-order five-point stencil
with Dirichlet ends; the eigenvalue nearest a target comes from `scipy.sparse.linalg.eigs` in shift-invert mode. The
setting is L = 40 at h = 0.02 and 0.01, with ω the root with Re ω > 0.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | The fundamental QNM of V = 1/R⁴ equals `polar.md`'s 0.681367187 − 0.617753448i within 1e-6, and equals that of 2/R² − 3/R⁴ within 1e-6 (the Darboux partners are isospectral), at h = 0.01, with h = 0.02 within 1e-5 |
| K2 | ℓ = 2: the fundamental QNM of 6/R² − 3/R⁴ equals 1.737692 − 0.305138i within 2e-6 |
| K3 | The test scalar 2/R² + 1/R⁴ gives 1.5727 − 0.5297i within 1e-3, and differs from K1's by more than 0.5 (the two ℓ = 1 problems are different) |

## Mutations

| mutation | change | targets |
|---|---|---|
| `V-scale` | every potential × 1.01 | K1, K2, K3 (a 1 % scale moves ω by about 3e-3) |
| `no-scaling` | θ = 0 | K1, K2, K3 |

## Amendments

**A1, 2026-11-27, after run 1.**
- **K1 is not met**: |ℓ = 1 − polar.md| = 5.1e-6 and |ℓ = 1 − Darboux partner| = 1.0e-5 against 1e-6, while h = 0.02 and
  0.01 agree to 7.6e-9.
- The cause is the review's domain. With θ = 0.9 the outgoing wave of ω = 0.68 − 0.62i decays as exp(−0.146|s|), only to
  2.9e-3 at L = 40, and the two partner potentials have different tails (1/x⁴ against 2/x²). For ℓ = 2 the decay is
  exp(−1.17|s|), and K2 passes.
- **K1b** adds the same bars at L = 160 (decay 7e-11), h = 0.02 and 0.01. K1 stays NOT MET.

## Runs (filled in as they are done)

| file | what |
|---|---|
| `rerun.sh`, `rerun/` | `polar_derive.py check`: 20 PASS, the same verdict lines as the runner's `derive_check.txt`. `polar.py planted`: 7 PASS, every verdict line equal to its first 120 characters. `count` ℓ = 2 at c = −0.3: no root, as the runner's. `mads` at c = 0.5: one mode, W = 1.709787002854765 against 1.7097870028547713. The expectation is met |
| `ind218_run1.txt` | run 1: **exit 1, K1 not met** (A1). ℓ = 1 at L = 40 is off by 5.1e-6, and its Darboux partner by 1.0e-5: the review's domain. K2 passes: ℓ = 2 1.7376918464 − 0.3051377413i, 3.0e-7 from `polar.md`. K3 passes: the test scalar 1.5727083913 − 0.5297008824i, 0.90 from ℓ = 1 |
| `ind218_run1_mut_*.txt` | `V-scale` fails K1, K2, K3; `no-scaling` fails K1, K2, K3 |
| `ind218_run2.txt` | run 2 (A1, L = 160): **exit 0, K1b passes.** ℓ = 1 0.6813671876 − 0.6177534480i, 6.0e-10 from `polar.md`; its Darboux partner 0.6813671875 − 0.6177534480i, 1.2e-10 from it; h spread 2.3e-9. The two ℓ = 1 potentials are isospectral to 1e-10 |
| `ind218_run2_mut_V-scale.txt` | a slip of the review: the two flags reached the script as one argument, so this ran unmutated at L = 40 (it repeats run 1). Kept |
| `ind218_run3_mut_V-scale.txt` | `V-scale` with K1b: fails K1b, K2 and K3 |
