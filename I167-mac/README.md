# I167-mac: conical shifts with det R₃ = 0 on all of η = x/ρ ∈ ℝ

Machine: the coordinator's Mac (nathans-macbook-air-m5-3, Apple M5, 10 cores, 32 GB, macOS). Worktree
`~/Source/negative-mass-i167`, branch `wip/i167-conical-global`. Issue: https://github.com/nmoinvaz/negative-mass/issues/167.
One process at a time, nice 10, `RAYON_NUM_THREADS=2`, `cargo build -j 2`. Rust 1.94.0; crates `multishoot =4.2.0`,
`multisolver =0.2.2`, `multidouble =5.1.0`. Python 3.14.7, sympy 1.14.0, mpmath 1.3.0, numpy 2.5.4
(`/Users/nathan/Source/negative-mass/.venv`).

This README is written before the first run of the crate. It states the route, the criteria, the grid and range, the
planted cases and the names of the controls. The targets of the controls are declared by an amendment after their
development runs (step 4 of the brief). Amendments are appended at the end, each dated and numbered, and none changes a
criterion, a grid, a range or a step tolerance after a run has shown data.

## Question

Is there a real solution F of N(F, F′, F″; η) = 0 on all of η ∈ ℝ, regular at η = 0, with the same limit F_∞ at η → +∞
and η → −∞? N is `det_classify.conical_N()`, the cubic in F″ of `det_classify.md` §6. The ends are the
two-parameter family of `conical_limit.md` §3,

    F = F_∞ + Σ a_{n,j}(F_∞, C) η⁻ⁿ (ln η)ʲ,   a₂,₀ = −2F_∞, a₄,₀ = C, a₄,₁ = F_∞(F_∞² + 7),

at η → +∞ and, by N(F₀, −F₁, F₂; −η) = N, its mirror F(−η) at η → −∞.

## Route

1. **Equation.** N = a₃F″³ + a₂F″² + a₁F″ + a₀ with a_c polynomials in (F, F′, η), printed in
   `notes/warp/conical_global.md`. Two facts found while planning, to be verified by the code, not assumed: a₃ = 2Fη²(F² − η²
   − 1) vanishes at η = 0 and at η² = F² − 1, and at η = 0 N reduces to 2F′²(F² − 1)(FF″ + F′²). So ∂N/∂F″ vanishes at η = 0
   when F′ = 0 (the even solutions), and the θ-form of #159 is not used near η = 0.
2. **Closure.** The state is (F, F′, F″). The Taylor recursion of the crate takes order k ≥ 1 of N = 0 and solves it for the
   coefficient F″ₖ (one division by ∂N/∂F″ at the step's start). N is then constant along the flow (N′ = 0 holds as the
   order-0 term is not imposed), and N = 0 is imposed by the end data. No hand-differentiated F‴ is typed.
3. **Ends.** At η = +200 the state (F, F′, F″) is the series of order n ≤ 13 (with logs) from (F_∞, C⁺); at η = −200 it is
   the mirror, (F, −F′, F″) of the series at |η| = 200 from (F_∞, C⁻). The coefficients are the formal series of
   `conical_limit.formal_series` recomputed in `conical_global.py` (not imported as numbers), through η⁻¹³ (stage k = 13 of
   the solver; its stages 3 … 13 must all be `solved` with the one free parameter a₄,₀), written to the crate as exact
   rational polynomials in (F_∞, a₄,₀). The size of the η⁻¹² and η⁻¹³ terms at 200 is the truncation estimate (an
   estimate, not an enclosure).
4. **Matching.** F″ is redundant with (F, F′) once N = 0 holds at both ends, so the left end gets a nuisance unknown e
   (F″ → F″ + e at η = −200), which the matching must return as 0. Unknowns: C⁻, e, C⁺, F_∞ (a global, pinned for each
   run). Rows: the three state differences at the matching node and the pin.
5. **Scan.** For each (F_∞, C) of the grid below, the inward integration from η = 200 by Taylor steps (double-double,
   order 30, tolerance 1e-32 on the last two terms), with the singularity locator of the crate, gives one verdict.
6. **Locator.** After each step the radius of the Taylor series of the fastest-growing field is estimated from the last
   coefficients by extrapolating the ratio rₖ = |cₖ₋₁/cₖ| = R(1 + γ/k + …) to 1/k → 0 (Domb–Sykes); the sign pattern of the
   coefficients gives the side. The walk continues until R ≤ 1e-6, and the singular η is η* = η_n ∓ R. Its error bar is the
   spread of the estimates over the last five steps: **a spread over the steps' extrapolations, not an enclosure.**

## Grid and range (fixed before the first run)

- F_∞ ∈ {0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4} and {−0.5, −1, −2}: 11 values. The negative ones test the symmetry
  (F, F′, F″) → (−F, −F′, −F″) of N, under which (F_∞, C) → (−F_∞, −C).
- C ∈ ±{0, 1, 3, 10, 30, 100, 300, 1000, 3000}: 17 values, so the range is [−3000, 3000]. 187 points.
- Series at |η| = 200, order n ≤ 13. Floor of the inward walk: η_min = 1e-6.
- Taylor plan: order 30, tolerance 1e-32, largest step 10. Re-integration for the step-halving check: order 36, tolerance
  1e-38, largest step 5.

## Verdicts of the scan

Each grid point gets exactly one:

- **SINGULAR(η*, bar, kind)**: the locator stopped at R ≤ 1e-6. kind is read from the state at the last step: `F->0` if |F| ≤
  1e-2 min(1, |F_∞|)... (the numbers are printed with the verdict; the kind is a label for the printed quantities, not a
  separate criterion): `F->0` (F → 0 with |F′| → ∞), `a3->0` (the F″³ coefficient a₃ → 0 with F finite and F″ → ∞), `fold`
  (∂N/∂F″ → 0 with F, F′, F″ finite), `F->inf` (|F| → ∞), `other`.
- **FLOOR**: the walk reached η_min = 1e-6 with no singular verdict. F, F′, F″ and p = ηF′ are reported at η = 1e-2, 1e-4,
  1e-6. It is `bounded` if |F′(1e-6)| ≤ 2|F′(1e-2)| (F′ finite as η → 0; for F′ ∝ 1/η the ratio would be 1e4) and `log`
  otherwise.
- **THROUGH**: FLOOR and bounded. The walk continues through η = 0 to η = −200 and fits (F_∞⁻, C⁻) to the state there.
  It is **GLOBAL** if |F_∞⁻ − F_∞| ≤ 1e-10 and the integrated state at −200 differs from the series of (F_∞, C⁻) by at
  most 1e-10 in F and in ηF′ (the issue's matching), with F, F′ finite at 0; otherwise **REGULAR, limits differ**.

## Criteria (each can fail; each is coded as worded)

| id | criterion | tool |
|---|---|---|
| A1 `n_table` | the crate's N at 40 fixed rational points (F, F′, F″, η) equals sympy's `det_classify.conical_N()` and the N rebuilt from D by `conical_limit.build_N()` to relative 1e-26 | crate, sympy |
| A2 `series_residual` | at η = +200 and −200, for (F_∞, C) ∈ {(1, 0), (−1, 2), (1/3, −1), (2, 1/2), (4, 3000), (0.25, −3000)}: \|N\| / Σ\|terms of N\| ≤ 1e-20 on the crate's state; and the crate's end state equals mpmath's evaluation of the series (50 digits) to 1e-26 relative | crate, mpmath |
| A3 `series_stages` | `formal_series` through η⁻¹³: every stage solved, free parameter a₄,₀ only, a₄,₁ = F_∞(F_∞² + 7), odd coefficients zero | sympy |
| B1 `plant_linear` | the matching code on (1 + η²)F″ + 4ηF′ + 2(F − α) = 0, exact solution F = α + (a + bη)/(1 + η²), a ≠ 0 ≠ b, ends = truncated expansions at ±20 (order 12): recovers (C⁻, C⁺, e) = (a, b, 0) to 1e-20 and the path equals the exact solution at the nodes to 1e-22 | crate |
| B2 `plant_cubic` | the same on N_q = M·N_p, M = 1 + F′² + F″² (cubic in F″, other roots complex): to 1e-18 | crate |
| B3 `plant_blowup` | the locator on F″ = 2F³ (F = 1/(η* − η), kind `F->inf`) and on FF″ + F′² = 0 (F² linear, F ~ √(η − η*), kind `F->0`), each inward and outward from two starts, η* known: located to 1e-8, error bar ≤ 1e-8 | crate |
| C1 `step_halving` | for (F_∞, C) ∈ {(1, 0), (2, 1/2), (0.5, −30), (3, 100)} the inward state at η = 3 from the two plans (order 30 against 36) differs by ≤ 1e-20 in F, F′, F″ | crate |
| C2 `n_along_path` | max over the steps of \|N\| / Σ\|terms\| at the step endpoints, for every scan point, up to the step at which R ≤ 1e-3, is ≤ 1e-18 | crate |
| C3 `independent` | own mpmath integration (20 digits, `odefun`, F″ the root of the cubic by Newton from the series branch, no Rust and no `multishoot`) of (F, F′) from η = 200 to η = 4 for (1, 0), (2, 1/2), (0.5, −30) equals the crate's state to 1e-9 in F and F′. Shared with the crate: the equation N (typed, `det_classify`) and the series | mpmath |
| D1 `scan` | 187 points, each with one verdict; each SINGULAR has an error bar ≤ 1e-8; each FLOOR reports its three states | crate |
| D2 `symmetry` | the verdicts of (F_∞, C) and (−F_∞, −C) for F_∞ ∈ {0.5, 1, 2}, all 17 C: the same class, and η* equal to 1e-8 | crate |
| E1 `bisect` | for each F_∞ and each adjacent pair of C grid values whose verdict classes (SINGULAR kind, FLOOR log, FLOOR bounded) differ: bisection in C (DD) until C_hi − C_lo ≤ 1e-13 (1 + \|C\|), recording the verdicts at both ends. The check is that every bisection ends with the two verdict classes still different at the ends | crate |
| E2 `connect` | each C_c of E1 at which a verdict is FLOOR-bounded or THROUGH is refined by the shooting solve (8 nodes plus the matching node) of the connection problem with F_∞ pinned; it converges (‖F‖ ≤ 1e-24) or is reported as not converged. A converged connection has e ≤ 1e-20, and its re-integration from +200 by a plan independent of the solve's matches the −200 series to 1e-10 (F and ηF′) | crate |

If the scan shows no FLOOR-bounded verdict and no bisection ends at one, E2 has nothing to refine and is reported as
not applicable, and this is the answer: no global solution found on the grid and range, with the first singular η of each
point.

## Controls (`conical_global.py --mutate=NAME` must exit non-zero with its named checks failing)

Targets are declared by amendment after their development runs.

| name | change | intended check |
|---|---|---|
| `eq-coeff` | one coefficient of N in the crate changed | A1, and A2 |
| `series-coeff` | one series coefficient (a₄,₁) changed in the crate | A2 |
| `match-sign` | the mirror end takes +F′ in place of −F′ | B1, B2 |
| `plant-locator` | the locator's side test inverted | B3 |
| `halving` | the second plan's order set equal to the first and its tolerance to 1e-20 | C1 |
| `n-drift` | the recursion stops imposing order k = 3 of N | C2, C1 |
| `indep-eq` | the independent integration uses −3Fη² → −2Fη² in a₁ | C3 |
| `sym-break` | the symmetric scan uses (−F_∞, +C) | D2 |
| `bisect-end` | the bisection compares the wrong class at the upper end | E1 |

## Rules for the runs

Every stdout goes to a numbered log here (`dev_NN_*.log`, `run_NN.log`, `ctl_<name>.log` with `.rc`). No log is
overwritten; reruns are numbered. A run longer than 1 h of wall time is stopped by its PID and reported. Memory is only
reported (`/usr/bin/time -l`). Nothing in the scan is certified: every number is **numerical evidence**.
