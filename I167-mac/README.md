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


## Amendment A1 (2026-11-25, after the development runs `dev_01` to `dev_13`, before any run of record)

Each item says what the development runs showed. No threshold was loosened. Items 1 to 3 were agreed with the coordinator
(hc, 2026-11-25); items 4 to 8 fix wording and design of cases the README could not run as written; items 9 to 11 add
checks, as the coordinator asked.

1. **A2 as first worded failed.** With the series through n ≤ 13 the residual |N|/Σ|terms| at η = 200 is 3.2e-19 at
   (F_∞, C) = (1, 0) against 1e-20 (`dev_01_series_k13.log`). mpmath at 60 digits reproduces the crate's N to every digit
   (`dev_02_a2probe.log`: N = −9.8e-28 for n ≤ 9, −1.5495e-33 for n ≤ 13, 1.8e-36 for n ≤ 14), so it is series truncation.
   The series order was then raised to n ≤ 17 (chosen after that run; it gives 4.3e-25 at (1, 0)). The threshold stays
   1e-20. The n ≤ 13 table is kept in raw (`dev_01_tables_k13.rs`). The coefficients of orders 14 to 17 get their own check
   A3b `series_order`: N of the n ≤ 17 series vanishes through ν²³ and not at ν²⁴, in exact rationals at 12 pairs
   (F_∞, C): (1, 0), (−1, 2), (1/3, −1), (2, 1/2) (the four of #159's `num_inward`) and (−3/2, 1), (1/2, −3), (3, 5),
   (−1/4, 1/3), (5/2, −7), (2/3, 3/2), (−2, −1/2), (4, 10).
2. **Adaptive start.** At the literal start η = 200, 58 of the 187 grid points fail C2 (`dev_03_scan_grid.log`) and A2's
   pair (0.25, −3000) fails 1e-20 (3.8e-5). Each point is started at the smallest L ∈ {200, 800, 3200, 12800, 51200}
   whose series residual is ≤ 1e-20 and walked to 200 and on; the verdict, L and both start residuals are reported. A2
   and C2 are gated on the adaptive start. Their first wording is printed as `NOT MET (as first worded)` with the
   count and does not gate the exit code.
3. **Locator stop.** Under the declared stop R ≤ 1e-6 two points ((±1, ±3000), η* = 3.6e-6) have an error bar 2.4e-8 > 1e-8,
   which is not met as first worded and is printed. A pass with R ≤ 1e-8 is added. It also shows that the first pass stops
   too early at 7 of the 187 points (`dev_09_scan_refined.log`): at (1.5, 1000), (2, 1000), (3, 3000), (4, 3000),
   (1, 1000) and their mirrors the five consistent estimates with R ≤ 1e-6 came from a nearby complex pair of singularities
   (|Im| < 1e-6), not from a real one, and the walk continues through the κ = 0 curve analytically. **The pass with
   R ≤ 1e-8 is the verdict of record** (D1 and every check that reads a verdict use it, and the bisection and the forward scan
   walk with R ≤ 1e-8); the first pass is printed beside it with its disagreements.
4. **Kind labels** (labels, not criteria). A singular point is `F->0` if F vanishes at η* like Δ^α with α from the locator's
   fit, α > 0 and |R F′/F| = α to 10%; `F->inf` if α < 0 and |R F′/F| = |α| to 10%, or |F| ≥ 1e3 max(1, |F_∞|); `fold` if the fitted
   α is 5/2 to 0.1 (F″ has a square-root branch point, ∂N/∂F″ → 0 on the branch) or ∂N/∂F″ is below 1e-6 of the sum of its terms;
   `a3->0` if |F² − η² − 1| ≤ 1e-3 (F² + η² + 1) (the F″³ coefficient 2Fη²(F² − η² − 1) vanishes); otherwise `other`. For `F->0`
   the prediction 2/(η*² + 4) from the leading balance −η²(η² + 1)F″²[(η² + 2)F′² + 2FF″] = 0 is printed with the fit.
5. **README "Route" 1, the word "even".** The statement that F′(0) = 0 solutions are even does not follow: ∂N/∂F″ = 0 there, so
   η = 0 is singular for them. The question is handled by E0 (item 9): crossing η = 0 with F′(0) ≠ 0, and the exponents at F′(0) = 0.
6. **B1, B2.** Ends at ±40 with 16 terms of the expansion (±20 with 12 terms leaves a truncation of 1e-17, which cannot give
   1e-20). Newton starts from the exact solution perturbed by 0.2 of (2% of each node value plus 1e-3, 10% of C⁻ and C⁺,
   0.05 for e); the cubic case does not converge from 0.5 of it (dev run 2025-11-25, log of the planted case), the linear one does from 1. The
   recursion was first checked along the exact solution: both agree with it to 4.6e-28 over 120 steps (`plant walk`).
   `halving` changes the first plan to order 14 and tolerance 1e-12 (the first wording, a second plan equal to the first,
   cannot fail). `n-drift` targets C2 only.
7. **C1 and C3 comparison points.** (0.5, −30) has η* = 7.07, above the comparison points 3 and 4 of the first wording; its point is
   η = 10 in both.
8. **Exit code.** Lines printed `NOT MET (as first worded)` are results and do not gate the exit code; the amended criteria gate it.
9. **E0 `eta0_local`** (new), symbolic: (a) N(η = 0) = 2F′²(F² − 1)(FF″ + F′²); (b) ∂N/∂F″ at η = 0 is 2F′²F(F² − 1); (c) for F′(0) ≠ 0 and
   F(0) ∉ {0, ±1} the equation solves order by order, each order linear in the next Taylor coefficient with a nonzero coefficient (two
   rational points, 7 orders), F″(0) = −F′(0)²/F(0): an analytic two-parameter family; (d) F − f ~ cη^p: the leading coefficient is
   2f(f² − 1)c³p⁵(p − 1), so for f ∉ {0, ±1} only p = 1 or c = 0; (e) F(0) = 0: N(0) = −2F′⁴, and the leading coefficient is −2c⁴p⁵(2p − 1), zero
   only at p = 1/2 (F ~ √η, not regular); (f) F(0) = 1: order 1 gives F″(0) = 1/6 − F′(0)² for F′(0) ≠ 0 (a one-parameter family), and the even
   branch F = 1 + b₁η² + …, order 4: 64b₁³(5b₁ − 2) = 0, so b₁ = 2/5 or F ≡ 1. (d) to (f) rest on **hypothesis H₀**: F − f has a leading term cη^p,
   real c ≠ 0, with termwise derivatives. Control `eta0-sign`.
10. **E3 `forward`** (new): F(0) ∈ {0.1, 0.25, 0.5, 0.75, 1.5, 2, 3, 5, −0.5, −2}, F′(0) ∈ ±{0.01, 0.1, 1, 10, 100}, F″(0) = −F′²/F, walked to +200 and −200 with
    R ≤ 1e-8. Each walk must end in SINGULAR with bar ≤ 1e-8; LOGLOG (the ν⁰ part A₀ = p²(p² − q)(p² + q) = 0, q = −p² for p > 0 and q = +p² for p < 0, to 0.2
    in |q/p² + sgn p|); FAMILY (the 2-d fit of the series at ±200 has |ΔF|, |Δ(ηF′)| ≤ 1e-10 and F″ to 1e-6); or NONFINITE at the κ locus (F″ overflows the double range near a zero of the F″³
    coefficient; |F² − η² − 1| ≤ 1e-6 there, η* only to 1e-6). The minus side of (f, f₁) must equal the plus side of (f, −f₁) in class and in η* to 1e-8, and max |N(0)| ≤ 1e-18.
    A solution FAMILY on both sides with equal limits would be a global solution. Control `fwd-class`. Criteria written after `dev_04_forward.log` and `dev_09_forward.log`.
11. **E4 `even_pm1`** (new): the even solution through F(0) = 1, F = 1 + 2/5 η² − 22/125 η⁴ + … (exact rationals, 30 terms), satisfies N = 0 exactly through order 62; walks from
    η₀ = 1/20 and 1/10 (series tails < 1e-60) to 200 agree to 1e-12 in F and p; at 200, |q/p² + 1| ≤ 0.2 (the log-log regime: F grows like ln ln η, no limit). Control `even-series`.

## Amendment A2 (2026-11-25, control targets, after the development runs `dev_12` and `dev_13`)

Thirteen controls, each `conical_global.py --mutate=NAME`. A control runs only the checks it names, so "no other check fails" holds
by construction; the expected outcome is exit 1 with exactly the named checks printed `[FAIL]`. What each did in the development
run (`dev_12_controls/`, and `dev_13_controls/` for the two repaired ones):

| name | change | target checks | development result |
|---|---|---|---|
| `eq-coeff` | the crate's N: −6 → −5 on F F′² F″ η² | `n_table`, `series_residual` | N differs by 2.7e-2 of Σ\|terms\| (threshold 1e-26); no L meets 1e-20 |
| `series-coeff` | the crate's a₄,₁ × 1.01 | `series_residual` | no L meets 1e-20 for any of the 6 pairs |
| `a16-coeff` | a₁₆,₀ × 1.001 in the exact-rational check | `series_order` | nonzero orders [22, 24] at all 12 pairs (expected [24]) |
| `match-sign` | the mirror end takes +F′ | `plant_linear`, `plant_cubic` | \|C⁻ − a\| 8.9, \|e\| 1.4e-5, \|C⁺ − b\| 0.22, nodes 0.11 (thresholds 1e-20, 1e-22) |
| `plant-locator` | the locator's side test inverted | `plant_blowup` | no walk finds its singularity (8 of 8) |
| `halving` | the first plan is order 14, tol 1e-12 | `step_halving` | differences 2.1e-8, 2.2e-8, 6.2e-10, 3.4e-9 (threshold 1e-20) |
| `n-drift` | the recursion leaves F″₃ = 0 | `n_along_path` | max \|N\|/Σ\|terms\| 3.5e-4 (threshold 1e-18) |
| `indep-eq` | the independent integration has −6 → −5.9999 on F F′² F″ η² | `independent` | \|dF\| 1.5e-3, 2.4e-3, 8.2e-5 (threshold 1e-9). A first try with −5.99 ran over 19 min and was stopped by PID (`dev_13_controls/stopped_indep-eq_minus599_over19min.log`); −4 crashed in `polyroots` (dev_12), and the check now counts any exception or a 500 s overrun as a failure |
| `sym-break` | the comparison uses (−F_∞, +C) | `symmetry` | classes differ, e.g. (0.5, −3000) F->0 against (−0.5, −3000) FLOOR |
| `bisect-end` | the upper end's final class compared with the lower class | `bisect` | the check fails for the brackets (its first form, a self-comparison, did not fire and was replaced in `dev_12`/`dev_13`) |
| `eta0-sign` | N(0) expected as 3 F′²(F² − 1)(FF″ + F′²) | `eta0_local` | the identity (a) is False |
| `fwd-class` | LOGLOG tested at q/p² = +sgn p | `forward` | the 30 LOGLOG walks become UNRESOLVED |
| `even-series` | the exact coefficient b₃ × 1.001 | `even_pm1` | N ≠ 0 at order 6, and the two starts disagree |

The run of record is `python3 notes/warp/conical_global.py --fresh` (the series is solved again, not read from the cache), stdout to
`run_01.log` here and to `notes/warp/conical_global_output.txt`.

## Runs

Branch `wip/i167-conical-global`, script at 3651f86 for the run of record. Every log is kept, including the failed and stopped ones.

| log | what | result |
|---|---|---|
| `dev_01_series_k13.log`, `dev_02_a2probe.log` | A2 as first worded at n ≤ 13 | 3.2e-19 at (1, 0), fails; A1 item 1 |
| `dev_03_scan_grid.log`, `dev_05_scan_grid_kinds.log` | the grid, first labels, then revised labels | no regular crossing; 58 start residuals above 1e-18 |
| `dev_04_forward.log`, `dev_09_forward.log` | the forward map from η = 0 | log-log regime found; criteria of E3 written after |
| `dev_06_orchestrator_crash1`, `dev_07_orchestrator_crash2` | orchestrator crashes (zero scale in `n_table`; the series command's parse) | fixed, logs kept |
| `dev_08_orchestrator.log`, `dev_10_orchestrator.log` | the 17 checks; the first has `scan` and `forward` failing, the second passes after the pass of record became R ≤ 1e-8 | A1 item 3 |
| `dev_11_full_stopped.*`, `dev_11_controls_stopped/` | the controls run stopped by hand (PIDs 62010, 73368) after a format error in `scan` | control logs of the 7 that ran are valid |
| `dev_12_full.log`, `dev_12_controls/` | checks and 13 controls; `indep-eq` crashed and `bisect-end` was silent | repaired in `dev_13_controls/` (the −5.99 try stopped after 19 min by PID 94686) |
| `run_01_stopped_in_controls.*`, `run_01_stopped_controls/` | first run of record, the 17 checks passed in 1015 s, stopped by hand (PIDs 24605, 49086) in the controls to add tables | superseded |
| `run_02.log`, `run_02.err`, `run_02.rc`, `run_02_controls/` | the run of record | exit 0, 17 of 17 checks, 13 of 13 controls on target only, 1334 s, peak 205 MB |
