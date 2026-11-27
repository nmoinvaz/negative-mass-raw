# I232-mac-review: the coordinator's review of #232 (rerun, independent check ind232)

Machine: macOS (the coordinator's Mac), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`: sympy 1.14.0, mpmath 1.3.0,
numpy, numba), nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/232. Under review: branch `wip/i232-c1-linear`
at c4552dd (on #217's 45c261d), raw `I232-mac` at f5db91a. Written 2026-11-27 before the first run of `ind232.py` and before
the rerun.

## Rerun

`linear_derive.py`, `linear.py check`, `linear.py table` and `linear.py c1` from a detached worktree at c4552dd. Expectation:
12 of 12, 18 of 18, and the table and c1 outputs equal to `linear_output.txt` apart from timings.

## ind232: why c = −1 alone admits a regular solution that grows at κ (by hand, then in sympy)

#212's master equation, as printed in `notes/black_universe/README.md` Sec. 2, is
Y'' = (2/ρ − A′/A) Y′ + (1/R⁴ − A′/(AρR²) − 2/(AR²) + W²/A²) Y. With A ≈ A₁(ρ − ρ_h) at a simple horizon:
- **ρ_h ≠ 0:** the 2/ρ term is regular. The indicial exponents are s = ±W/A₁, and with tortoise x the solutions are
  e^{Wt}(ρ − ρ_h)^{±W/A₁}. The + branch is e^{Wv} times a smooth function (regular on the future horizon). The − branch is
  e^{Wu}, singular there. At W = κ = A₁/2 the − branch is (ρ − ρ_h)^{−1/2}, which diverges.
- **ρ_h = 0, the throat, c = −1:** 2/ρ and A′/A ≈ 1/ρ combine into Y′/ρ. The exponents shift to s = 1 ± W/A₁. With ρ ∝ −UV
  (Kruskal), Y = ρ^{1−W/A₁} e^{Wt} = V (−U)^{1−W/κ} up to a constant. At W = κ this is exactly V: smooth, nonzero on the
  future horizon and growing as e^{κv}. #212's condition u = Y/ρ → 0 keeps only s = 1 + W/A₁, which removes it.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | sympy: the indicial polynomial of the printed master equation at ρ_h = 0, c = −1 (A₁ = A′(0) = 4/π) has roots 1 ± W/A₁; at W = κ = 2/π, {1/2, 3/2} |
| K2 | sympy, by series in ρ at c = −1: with t the Killing time and x = ∫dρ/A, ρ^{1/2} e^{κt} = C e^{κ(t+x)}(1 + O(ρ)), i.e. the s = 1/2 solution at W = κ equals a constant times e^{κv} on the horizon |
| K3 | at c = −1.01 and −0.99 (ρ_h ≠ 0), the indicial roots at W = κ are ±1/2 to 1e-12, so the W = κ branch other than #212's diverges there: the regular growing solution at κ exists at c = −1 only |

## Mutations

| mutation | change | targets |
|---|---|---|
| `drop-2rho` | the 2/ρ term removed from the printed equation | K1 |
| `wrong-kappa` | κ = A₁ in place of A₁/2 | K1, K2 |

## Amendments

**A1, 2026-11-27, after run 1.**
- **K3 is not met as worded.** The roots at c = −1.01 and −0.99 are −0.499999999997 and −0.500000000003: 3e-12 from −1/2
  against the bar 1e-12. The cause is the review's numerics, not the equation. p₀ and q₀ were evaluated at a distance
  1e-14 from ρ_h ≈ ±0.0078, and the 2/ρ term then contributes about 1e-14/0.0078 ≈ 1e-12.
- **K3b** repeats K3 at a distance of 1e-20 with 40 digits, against the same bar. K3 stays NOT MET.
- The mutation `drop-2rho` stopped with an exception (complex roots could not be sorted) before any criterion was
  evaluated: a non-clean fire, kept. `wrong-kappa` fired its targets K1 and K2; K3 failed there as it fails unmutated.

## Runs (filled in as they are done)

| file | what |
|---|---|
