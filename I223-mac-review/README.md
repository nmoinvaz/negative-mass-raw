# I223-mac-review: the coordinator's review of #223 (rerun, independent check ind223)

Machine: macOS (the coordinator's Mac, Apple M5), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`: numpy 2.5.4,
scipy 1.18.1, sympy 1.14.0, mpmath 1.3.0), nice 10, at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/223.
Under review: branch `wip/i223-black-bounce` at a44d49d (`bounce.py` 2db4b58), raw `I223-rpi5` at 476bed0. Written
2026-11-27 before the first run of `ind223.py` and before the rerun.

## Rerun

From a detached worktree `~/Source/negative-mass-r223` at a44d49d, in `notes/black_universe`: `bounce.py check`, `planted`,
`planted_complex`, `complex S_m0.2 S_m0.3 B1_q0.77`, and `count` at R2 for S_m1 and B1_q0.5. The expectation, written now:
`check` exits 0 with 55 of 55; the planted values and the complex pairs equal the runner's logs to their printed digits; the
two counts give the runner's roots (`I223-rpi5`) to 1e-9 relative. The other 218 count runs are not rerun.

## ind223: the growing modes of horizon members by a finite-difference eigenvalue problem

The coordinator's own code. It shares the potential V̂(x) and A(x) of `bounce.py`'s `Bg` class (the derivation the runner
checked symbolically), and nothing of its shooting, Sturm count or spectral check.
- The tortoise coordinate x* from dx/dx* = A(x) (scipy DOP853, rtol 1e-12) on [−L, L] about x = x_h + 1. V̂ is set to 0
  where A < 1e-300.
- The operator −∂²_{x*} + V̂ by second-order finite differences with Dirichlet ends; negative eigenvalues −W² from
  `scipy.linalg.eigh_tridiagonal`. Grids h = 0.1 and 0.05, L = 3000.
- Members whose static region has no throat (x_h > 0), where the problem is self-adjoint: S m = 0.75, 1, 5 and B1 q = 0, 0.5.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | At each of the five members, the number of eigenvalues with W ≥ 0.005 equals the README's count of real modes with W ≥ 0.005 (S m = 0.75, 1, 5: one each; B1 q = 0: one; B1 q = 0.5: two), each W agrees with the README's value within 2e-3 relative at h = 0.05, and h = 0.1 and 0.05 agree within 2e-3 |

Reported, not gated: every eigenvalue with W ≥ 1e-3; the weak modes below 0.005, which need L ≫ 1/W.

## Mutations (`--mutate=NAME`; each must make ind223 exit non-zero with exactly these criteria failing)

The targets are predicted from the code, not yet computed. A mutation that misses its targets is reported.

| mutation | change | targets |
|---|---|---|
| `vhat-scale` | V̂ × 1.05 | K1 |
| `no-tortoise` | x in place of x* | K1 |

## Amendments

## Runs (filled in as they are done)

| file | what |
|---|---|
