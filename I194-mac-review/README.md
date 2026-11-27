# I194-mac-review: the coordinator's review of #194 (rerun, independent check ind194)

Machine: macOS (the coordinator's Mac, Apple M5), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`: numpy 2.5.4,
scipy 1.18.1), Rust 1.94.0, nice 10, at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/194.
Under review: branch `wip/i194-radial-crate` at 2ed755e, raw `I194-mac` at e7336a6. Written 2026-11-27 before the first run
of `ind194.py` and before the rerun.

## Rerun

From a detached worktree `~/Source/negative-mass-r194` at 2ed755e, in `phase2/radial`, with `RAYON_NUM_THREADS=2`:
`python taylor_radial.py --arc-log=<RAW>/run_09_arc.jsonl,<RAW>/run_05_stepA.jsonl,<RAW>/run_10_stepB.jsonl,<RAW>/run_07_stepC.jsonl
--supp-log=<RAW>/run_11_stepS.jsonl`, RAW = `I194-mac`. This is the note's command for `taylor_radial_output.txt` (run_13_final).
The expectation, written now: exit 1 with 17 passed, 4 failed (X1b of ε = −1, C1, C2, F), 1 skipped, and every line of
`taylor_radial_output.txt` again apart from wall times, loads and paths. The stage runs themselves are not rerun.

## ind194: the star and the family by a code that shares none of the crate

The coordinator's own shooting code in Python (scipy DOP853), written for this review. Shared with the crate: the field
equations of `phase2/boson_star.py`'s docstring (the model: V(s) = s/2 − λs²/4 + μs³/6, λ = 10240, μ = λ²/4.8, G_ab = 8πεT_ab,
Schwarzschild-like gauge), and the stored tables used as starting guesses only. Not shared: the variables, the integrator,
the start, the decay condition, the lapse normalization and the mass and charge integrals.
- Variables (φ, φ′, m, ln α) from r₀ = 1e-4 with the series φ = φ_c(1 + (2V′(φ_c²) − ω̃²)r²/6), α(0) = 1, m = (4π/3)ερ_c r³.
- The ground state by bisection on φ_c at fixed code frequency ω̃: the shot either crosses zero or turns up. The run stops
  where the shot leaves the decaying solution; M = m there, N = ∫4πr²ω̃φ²a/α dr, α(∞) = α(r)/√(1 − 2M/r) at the end,
  ω = ω̃/α(∞), α_c = 1/α(∞).
- The family in α_c (for C1) by a secant on ω̃ for the target α_c; the canonical family near its mass extremum (for X1) in φ_c.
- Error estimate: every quantity at rtol 1e-12 and 1e-13; their difference is printed beside it. It is a spread over two
  tolerances, not an enclosure.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K0 | The first law, a known identity through the same code: at ω = 0.90 and 0.95 for ε = +1, and at α_c = 2.0 for ε = −1, (dM/dx)/(dN/dx) along the family equals εω to 1e-7 relative (x = φ_c or ω̃, central differences) |
| K1 | The crossing. For ε = +1 and ε = −1, the ω where dM/dω = 0 (from a quartic fit of M against φ_c over nine stars about the extremum) agrees with the crate's dM/dω = 0 (0.9258444557595977280, 0.9289084310581665252) to 1e-9, and the two tolerances agree to 1e-10 |
| K2 | The 10 tokens where the crate and the stored phantom rows differ (C1: N at α_c = 2.0, 2.1, 2.4, 2.8, 3.5, 3.9; ω at 2.3, 2.8, 3.9; M at 2.4). At each, ind194's value rounded to the printed digits equals the crate's token, and the two tolerances agree to 0.1 of a half-unit |
| K3 | As a control on K2: at α_c = 1.5, 2.5 and 3.0, where the crate and the stored print agree, ind194's ω, N and M round to that common token |

Reported, not gated: ind194's ω, M and N at each row to 12 digits; the stored crossing of `RESULTS.md` (0.92890838) against K1.
σ₀² is not checked here: an independent eigenvalue solver needs the perturbation equations derived again, which this review
does not do (the runner's recommended task 3).

## Mutations (`--mutate=NAME`; each must make ind194 exit non-zero with exactly these criteria failing)

The targets are predicted from the code, not yet computed. A mutation that misses its targets is reported.

| mutation | change | targets |
|---|---|---|
| `eps-law` | K0 compares with −εω | K0 |
| `lam` | λ → 1.0001 λ in the model | K1, K2, K3 |
| `alpha-norm` | α(∞) taken as α at the last point, without the Schwarzschild factor | K0, K1, K2, K3 (ω and α_c move by about M/r_end) |

## Amendments

**A1, 2026-11-27, after run 1 (two processes; no K value printed).**
- Run 1's K0/K2/K3 process stopped in its coarse scan of the phantom family. At P = 5.02e-4 the code frequency in
  [0.05, 0.9999] gave no ground-state bracket (`ind194_run1_K023.txt`).
- The phantom rows of C1 are thin-walled stars of radius 80 to 170 (`phantom_family.txt`). Shooting from the centre in
  float64 cannot hold their plateau, so **K2 and K3 stay NOT COMPUTED**, which is a failure as worded. The crate's stars
  and the stored rows are not compared by this review.
- Run 1's K1 process printed nothing in 23 minutes, and the review stopped it. Development runs `dev_02` and `dev_03` timed
  one star at P₀: 14 s at rtol 1e-10 and 301 s at 1e-12. The two agree to 4.7e-12 in ω and 2.4e-11 in M. The tolerance
  pair becomes **1e-10 and 1e-11**; the bars of K0 and K1 are unchanged.
- K0's ε = −1 point moves from α_c = 2.0, a strong-field row, to the weak-field ε = −1 family at ω = 0.95. It is found
  as for ε = +1, by walking out in P from the crossing.

**A2, 2026-11-27, after run 2.**
- **K1 is not met as worded.** ind194 puts dM/dω = 0 at 0.9258444604861 (ε = +1) and 0.9289084358526 (ε = −1). These are
  +4.7e-9 and +4.8e-9 from the crate, while the two tolerances agree to 1.2e-11 and 6.2e-12.
- The suspect is ind194's own fit window. Nine stars over ±4 % in P, quartic, span ±4e-3 in ω. The fifth-order part of
  M over that window can move the root by up to about 1e-7 in ω (estimate), far more than the tolerance spread.
- **K1b** is added: the same procedure with nine stars over ±0.5 % in P (±5e-4 in ω), the same bars (1e-9 to the crate,
  1e-10 between the tolerances), and the per-star (P, ω, M, N) written to `ind194_run3_stars.jsonl`. K1 stays NOT MET.
  If K1b moves ind194's root to the crate's, the window was the cause.
- **K0 crashed** in run 2 on the review's own bug: `brentq` refuses rtol = 4e-16 (its floor is 8.9e-16). rtol becomes
  1e-15. No K0 value was printed.

## Runs (filled in as they are done)

| file | what |
|---|---|
