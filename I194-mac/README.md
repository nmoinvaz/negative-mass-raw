# I194-mac: the radial boson-star modes and the phantom family on multishoot and multisolver

Machine: mac, the coordinator's Mac (Apple M5, 10 cores, 32 GB, macOS), shared with other sessions; runner
negative-mass-mac-i194 (Claude Code, account claude-me2). Issue: https://github.com/nmoinvaz/negative-mass/issues/194
Code: worktree `~/Source/negative-mass-i194`, branch `wip/i194-radial-crate`, crate `phase2/radial/taylor_radial/`.
Pushes: `git push origin HEAD:refs/heads/wip/i194-radial-crate`.
Written before the first run of record (`run_*`). Development runs are `dev_*`; amendments are numbered and dated at the
end. Everything below that came from a development run says so.

## What is built

The radial (l = 0) system of `phase2/radial/radial_modes.py` and the boson-star family of `background.py` and
`phantom_follow.py`, in Rust, in f64, double-double (dd, the default) and quad-double (qd, the check lane).

- **Star.** The background (P, u, m, Z) = (φ0², φ0′/φ0, m, α⁻²) of `background.odes`, both signs of ε, as a multiple-shooting
  boundary-value problem on multishoot 4.2.0's `Shooting` (its `Equations` trait, exact dual Jacobians, `newton`): the
  regular start at r_s = 1e-8 from the leading-order series (its error feeds the singular solution at O(r_s⁵)), nodes
  every few units, the decaying tail condition u(R) = −k − 1/R, Z(R)(1 − 2m(R)/R) = 1, with k = √(1 − ω²) the global (ω² = 1 − k²
  keeps every equation polynomial). Newton starts from the crate's own shot (P_c bisected on the class of the shot,
  as `taylor_polar`'s `star.rs`) and a Yukawa tail. The α_c-pinned form (k a constant field, Z_c = α_c⁻² the global)
  is the family of the continuation.
- **Perturbation.** y = (A, A′, G̃, χ), y′ = J(r; σ²) y, with J = J0 + σ² J1 from `radial_rhs_generated.py` by walking its
  syntax tree (`taylor_radial.py --gen`, as `taylor_polar.py` does for `polar_matrix_generated.py`). **The symbolic source is shared
  with `radial_modes.py`; it is not independent.** J's entries are Taylor tables along the star's steps; a plane step takes the
  jets of each entry from the table (series shift), as #186.
- **D(σ²).** The regular 2-plane from r_s (A0, G0 free, χ = O(r³), leading order) integrated outward to r_m, and the decaying 2-plane
  integrated inward from R to r_m **from an arbitrary start plane**: the inward flow contracts every plane onto the pair that
  grows inward (the two decaying solutions) by e^{−(κ₁+κ₂)(R − r)}, so no far-field matrix or eigenvector enters (`radial_modes.py`
  starts from the frozen-coefficient projector instead; that is the one construction here that is not the same). R is
  r_m + 40/κ_min or more (below). Both planes are orthonormalized after every Taylor step (Gram-Schmidt, positive diagonal, twice),
  D = det[Y Z], bounded by 1, no poles. A zero of D is an eigenvalue; σ² < 0 is unstable.
- **Roots.** Sign changes of D on a fixed grid of σ², refined by Brent's method in the lane, then a Newton polish. Grids are declared
  below and printed.
- **Integrator.** One Taylor step of order 30 (jets of J's entries about the step start), the largest step whose last two terms
  are below `tol`: 1.1e-14 (f64), 1.2e-30 (dd), 1.5e-62 (qd). `plane.rs` is `taylor_polar`'s, adapted to a 4 × 2 plane.
- **multishoot, multisolver.** multishoot 4.2.0 (`Equations`, `Shooting`, `plan_segments`, `newton`, `in_global`) and multisolver
  0.2.2 (arclength continuation `arclength::continuation`, `locate_fold`) solve and follow the star. They do not enter D(σ²): its
  planes need the orthonormalization between steps that the layout has no place for (#186's finding), so D uses the crate's own
  integrator. A second eigenvalue solver on the layout (σ² the global, the mode normalized by an extra row) is run at the end as an
  independent check of σ₀² (it shares J and the star, and none of the planes, the matching or the root grid).
- **Versions.** Rust 1.94.0, multishoot 4.2.0, multisolver 0.2.2, multidouble 5.1.0 (the unreleased series module #186 patched in is not needed).

## What is shared with the stored scipy path and what is not

| Shared | Not shared |
|---|---|
| the symbolic radial system (`radial_rhs_generated.py`), the model constants (λ = 10240, μ = λ²/4.8), the regular start at r → 0 (leading order), the matching radius rule (r_m: φ0 = 1e-3 φ_c on the same 4000-point grid) | the integrator, the star solver and its boundary treatment (exact start, the node layout), the far-field start of the decaying plane, the lane arithmetic, the root finder |

## Declared criteria (before any run of record)

Nothing below is moved after a development run. A criterion that fails is reported as not met.

**Lanes and tolerances (G).** Taylor order 30; tol as above; R − r_m ≥ 40/κ_min in dd (19/κ_min in f64, 74/κ_min in qd), where κ_min is
the smaller of √(1 − (ω ± σ)²) at the largest σ² of the scan (so that the contamination of the decaying plane, e^{−2κ(R−r_m)}, is
below the lane's roundoff).

**P1, planted eigenproblem through the same code.** Two decoupled Pöschl–Teller radial problems in y = (u₁, u₁′, u₂, u₂′), mixed by a
fixed smooth invertible S(r) so that the planes mix (J = S J̃ S⁻¹ + S′S⁻¹), linear in the eigenvalue s:
u_i″ = [b_i − c_i s − λ_i(λ_i + 1) sech²r] u_i, u_i(0) = 0. The eigenvalues are s = (b_i − (λ_i − n)²)/c_i for odd n < λ_i
(the odd states of the line problem), exact in closed form; the regular plane starts exactly at r = 0 and the decaying plane from
an arbitrary plane at R, as for the star. The parameters (λ, b, c, S) are in `src/planted.rs` and `taylor_radial.py` and are listed
in the output. Criterion: every planted eigenvalue found by the same root finder (grid, Brent, polish) to relative **1e-10 (f64),
1e-24 (dd), 1e-50 (qd)**; and no root other than the planted ones on the grid. The control `plant_sign` (λ → −λ(λ+1)) must fail it.

**P2, planted D.** D(s) at five s that are not eigenvalues, against an independent mpmath evaluation (60 digits, `odefun`, planes
orthonormalized once at the matching point): relative 1e-9 (f64), 1e-24 (dd), 1e-48 (qd).

**P3, planted extremum.** The routine that finds dN/dω = 0 (polynomial fit of N(ω) on 9 points, degree 8, window ±1e-3) on a synthetic
N(ω) = N₀ + 3(ω − ω*)² − 40(ω − ω*)³ + 500(ω − ω*)⁴ at ω* = 0.92584444444444444…, recovers ω* to 1e-14 (dd inputs).

**G1, J.** The crate's J(r; σ²) against `radial_rhs_generated.py` evaluated in mpmath at 60 digits at 12 points (r, σ²) of the canonical
star (the star's values entering as given numbers): relative 1e-24 (dd). **G2**, the shifted table against the direct series: 1e-20.

**S, the star.** S1: the star's (α, a, φ0, u) at 10 radii against `background.solve_star` at ω = 0.75 (ε = +1) and ω = 0.7603 (ε = −1)
(scipy BVP, tol 1e-9): 1e-7 relative (scipy's own error). S2: the multishoot recursion against the crate's own Num-lane recursion
(`star_ref.rs`, the `taylor_polar` recursion) at one state: 1e-28. S3: dd against qd (central data and M): 1e-26. S4: the Newton residual
max |F| ≤ 1e-28 (scaled rows). S5: first law dM = ε ω dN on the continuation's rows: relative 1e-18 of |dM| from 4 consecutive rows at
spacing 1e-3 in ω by an exact polynomial rule (the rows themselves are ~1e-28).

**X1, the crossing (ε = +1).** On the ε = +1 family near ω = 0.9258: ω₀ (D(σ² = 0; ω) = 0 by the secant method on stars solved at each ω),
ω_N (dN/dω = 0), ω_M (dM/dω = 0) from the same fit as P3. **Tolerance, set before the run: |ω₀ − ω_N| ≤ 1e-12 and |ω_N − ω_M| ≤ 1e-12.**
Reported to the digits reached. Against the stored crossing table (ω₀ = 0.92584444, ω_N = ω_M = 0.92584446): within 3e-8 each (the stored
2e-8 mutual spread, set by polynomial fits to 17 stars at BVP tolerance 1e-9). The same for ε = −1 (stored 0.92890846, 0.92890838) with
tolerance 1e-12 and 3e-8. Error bars (named): E1 spread over fit window and degree (±1e-3 deg 8 against ±2e-3 deg 10), E2 spread over lanes
(dd against qd), E3 spread over R and Taylor order.

**A, the canonical scan table (§3).** At ω = 0.75, 0.80, 0.85, 0.88, 0.90, 0.91, 0.92, 0.925, 0.93, 0.935, 0.94, 0.95, 0.96 (ε = +1): the
crate's M and N rounded to the 7 decimals of the table, and the lowest σ² rounded to its 4 significant digits, each **equal to the stored
token**; the rows "none in [−4, (1−ω)²)" (ω ≤ 0.88) have no sign change of D on the crate's grid (60 points log-spaced on [−4, −1e-7], 0,
and 60 points on [1e-7, 0.995(1−ω)²], log-spaced then linear as `lowest_modes`). For each token the distance to its rounding boundary is
printed. Also against the stored full-precision values in `scan_eps+1.json` (their error is scipy's, about 1e-9 relative), reported not
judged.

**F, the phantom modes (§7).** At α₀ = 1.10, 1.20, 1.50, 2.00, 2.50, 3.00 the σ² roots (up to the three of the table) on [−0.2, (1−ω)²)
equal to the 5 significant digits of the table, and ω, N, M to their printed digits; at α₀ = 3.50, 3.90, 4.00, 4.015 no sign change of D on
the grid (24 points log-spaced on [−0.2, −1e-7], 0, 24 + 32 above as `lowest_modes` scaled, plus a 4× denser rerun). Against the full-precision
roots in `negative-mass-raw/I10-rpi5/modes.jsonl`, reported not judged.

**Z, σ₀² at α₀ = 2.0 and 3.0.** The lowest root to all dd digits reached. Error bars, named: E2 (dd against qd, criterion 1e-20), E3 (R − r_m
40/κ against 60/κ, order 30 tol 1e-30 against order 24 tol 1e-22, two node layouts of the star), and the independent multishoot eigenvalue
solver (criterion 1e-18). They are spreads over choices of the method, not rigorous enclosures. The phantom_fd.py extrapolations (6.0e-3
and 1.04e-2 off) are reported against the crate's value.

**C, the continuation.** The phantom family (ε = −1) in α_c by multisolver's pseudo-arclength continuation of the α_c-pinned family
(`Shooting::in_global`, `arclength::continuation`) from the weak-field star ω = 0.7603 (α_c < 1) up through α_c = 1.172 (the ω-fold of
`phantom_checks.py` C4) to 4.017906, and Newton at each stated α_c. Rows: α_c = 1.10, 1.15, 1.17, 1.20, 1.25, 1.30, 1.40, 1.50, …, 4.00
(0.1 steps), 4.015, 4.017906 (36 rows of `phantom_family.txt`). Criterion: ω to its 8 decimals, N to its 6 significant digits, M to its 5
decimals, **each equal to the stored token**; max |2m/r| and r_s (printed 4 and 2 decimals) reported. The stored rows are BVP solutions at
tolerance 1e-8 (§7), so a token of ω at its 8th decimal can differ from the true value; each difference is reported with the crate's value.
Information tier, declared now and not a criterion: |ω|, |N|, |M| each within 2e-8 relative of the stored value. The ω-fold: ω_min and its α_c by
`locate_fold` on the ω-pinned family (stored: ω_min = 0.42226358 at α_c = 1.172 from C4's fit), reported. The same continuation in ω
(k the global) passes the fold by arclength; the number of points it takes to cross it is reported.

**Controls.** Each check has a `--mutate=NAME`. The target of each mutation is computed in a development run (`dev_*`) and written in
Amendment A1 before the run of record, with the effect found. The names and the first guess of what each does:

| name | what it does | first guess of its targets |
|---|---|---|
| `jsign` | flips the sign of one J entry (the G̃ coupling to χ) | G1, A, X1, F |
| `jomega` | ω in J off by 1e-6 (not in the star) | A, X1, Z |
| `jmu` | μ in J scaled by 1 + 1e-6 (not in the star) | X1 (σ² = 0 leaves the extremum) |
| `eps` | ε = +1 in the phantom star | S1, F, C |
| `noqr` | no orthonormalization between steps | P1, P2, A |
| `lowsum` | Taylor sum cut at order 8 | every integrator check |
| `shortR` | R − r_m = 3/κ instead of 40/κ | P1 (qd), Z |
| `start` | wrong leading term of the regular start of χ | A, X1 |
| `plant_sign` | the planted well with the wrong sign | P1, P2 |
| `fit_deg` | the extremum fit at degree 3 | P3, X1 |
| `tailk` | the tail condition u(R) = −k + 1/R | S1, S4, C |
| `nonewton` | one Newton step instead of converging | S4, C |
| `arcfold` | arclength continuation with the tangent orientation flipped at the first point | C (does not cross the fold) |

## Plan of runs

1. dev: J, table, planted P1/P2 in the three lanes, then the star and D on the ω = 0.75 star (`dev_*`).
2. run: planted P1–P3, G1–G2, S1–S5, the scan A (step 2 post).
3. run: X1, F, Z (step 3 post).
4. run: C, the controls (step 4).
5. run: the driver `phase2/radial/taylor_radial.py` from scratch to `taylor_radial_output.txt` (step 5).

## Threads, stop condition

One process at a time, `nice -n 10`, `RAYON_NUM_THREADS=2`, `cargo build -j 2`. Any run not finished in 1 h of wall time is stopped by its
PID and reported with what finished. Memory is reported (`/usr/bin/time -l`) and never a reason to stop.

## Amendments

### A1 (2026-11-26, before any run of record; the development runs are dev_01 to dev_03 here)

Method and criteria changed after development runs, none after a run of record. Nothing below loosens a criterion on data.

1. **The decaying plane starts from the spectral projector, not an arbitrary plane.** The README's "from an arbitrary start plane" was
   wrong for the star. With an arbitrary plane, D(σ²) of the ε = +1 star at ω = 0.925 had a second sign change that moved with the far
   radius (σ² = 3.54e-3, 3.67e-3, 7.64e-3 at R scales 0.5, 1, 1.5) and had |D| = 1.7e-4 at its "root": the start plane's component along
   the decaying pair changes sign with σ², and D changes sign with it. The star now starts the plane from P e_A and P e_G̃, P the
   projector onto the contracting eigenspace of the frozen matrix in (A, A′, G̃, χ/r²), formed in the lane by the matrix sign function
   (`radial.rs: decaying_start`), as `radial_modes.py` does. The control `arbstart` puts the arbitrary plane back. The planted problem keeps
   its arbitrary plane; P1 requires the sign of det C (the plane's orientation against the decaying pair) to be constant on the grid, and P2's
   reference orients by it.
2. **S5** is 13 stars at ω = 0.93 spaced 1e-4 (degree 12), not four rows: the declared rule's truncation error would have exceeded 1e-18.
3. **The family has 35 stored rows**, not 36 (1.10, 1.15, 1.17, 1.20, 1.25, 1.30, 1.40 to 4.00 in steps of 0.1 (27), 4.015, 4.017906).
4. **The star's layout.** Outward segments are at most 2.5/k long (an outward shot amplifies roundoff by e^{2kΔ}: a residual floor of 4.8e-27
   at Δ = 10.5, k = 0.66 became 6.6e-30 at 3.5/k), the boundary-value problem ends at r_t = r_cut + 40/k where P < 1e-44 at r_cut, and the
   exterior r_cut to R is the vacuum chain (P = 0, m = M, u from the exterior Riccati equation integrated inward). Newton uses NLEQ-ERR's
   iterate scaling (`Scaling::Iterates`): without it Newton stalled at 2e-24 to 5e-18 scaled residual on tail unknowns of size 1e-70.
5. **G1's reference** evaluates `radial_rhs_generated.py` with exact rationals: the file writes 8/3 and the like as float divisions, which
   gave 4.6e-16 against the crate's exact constants (the crate is right; first run of G1).
6. **Controls.** `tailk` is silent by construction (the star does not feel its far condition; §7 of RESULTS.md found the same), replaced by
   `znorm` (Z(R) = 1: no α(∞) = 1 normalization). `start` changes the start of χ at r_s = 1e-8, an effect of order r_s³: expected silent.
7. **FOLD.** `locate_fold`'s corrector did not converge on the k-pinned family (message in the output); the fold is reported by the sign change
   of t_k (multisolver's detection) and ω_min and its α_c by the extremum of the interpolating polynomial of ω(α_c) (2 windows).
8. **Newton tolerance** for stars is 1e-28 (scaled rows); S4's limit 1e-28 is unchanged.


### A2 (2026-11-26, after dev_01 to dev_05 and the stopped run_03, on the coordinator's ruling; no run of record has produced a family row yet)

The one arclength run of the whole family (run_03, checks C, F, Z) was stopped at 2 h 29 min (rc 143) with nothing finished. The cost, measured:

| run | what | number |
|---|---|---|
| dev_02 (old Newton) | arclength from ω = 0.45 to α_c = 3.736 | 1370 points, 137 chunks, 2168 s, 1.6 s per point |
| dev_03 (new Newton) | to α_c = 2.02, four mode scans | 630 s |
| dev_05 (new Newton, load averages 23.5 / 17.5 / 12.1 on 10 cores, `par = false`) | chunks 1 to 10 | 3.0 s per point; 84 % and 80 % of busy samples in `bvp::recursion`, 1.1 of 2 threads busy |
| projection (not measured: the new code never ran beyond α_c = 2.02) | to 4.017906 | 1900 to 3600 points, 0.9 to 3 h, before rows and scans |

1. **C as worded is NOT MET.** The README's C asks for the pseudo-arclength continuation from the weak-field star to α_c = 4.017906. It is reported as not met
   (driver check `C2`), with the reason above. The stored rows are still compared (check `C1`) by the procedure below.
2. **Procedure.** (a) Stage `arc`: multisolver's arclength continuation of the α_c-pinned family from the weak-field star (ω = 0.66, continued to 0.45)
   through the ω-fold to α_c = 2.0, chunks of 10 points, rows at the 13 stored α_c ≤ 2.0 (1.10 to 2.0), mode scans at 1.10, 1.20, 1.50, 2.00, the
   variants at 2.00. (b) Stages `stepA`, `stepB`, `stepC`: rows at the 22 stored α_c > 2.0 (2.1 to 4.017906) by Newton at each α_c on the same multishoot
   layout (`solve_z`), α_c stepped up from the ω = 0.45 star: first step 0.01, at most 0.05, ×1.3 after a success, halved after a failure; a step is
   taken when Newton reaches a scaled residual ≤ 1e-24 and k changes by at most 25 % (|Δ ln k| ≤ 0.25, a guard against landing on another star); the
   step lands on every target. If the step falls below 1e-7 the stepping stops, the last α_c reached is reported and no other method is tried.
   Mode scans at 2.5, 3.0 (`stepB`, with the variants at 3.0), 3.5, 3.9, 4.0, 4.015 (`stepC`). Every bar of the row comparisons and of the mode
   scans is as declared above. Each stage is one child process of at most 3600 s of wall time, stopped by its PID at that limit.
3. **`par = true`.** The arclength corrector's Jacobian, LU and tangent run on rayon tasks (they ran serially in dev_01 to dev_05: `cont.rs` passed `par = false`),
   with `RAYON_NUM_THREADS=2`. multishoot documents that the result does not depend on `par`; dev_06 (`par=0`) and dev_07 (`par=1`) run one chunk of 10 points
   and are compared digit by digit: **all 7 JSON lines are identical** except their timing fields (the start star, both rows at α_c = 1.07 and 1.08 to 30 digits with their residual norms, the chunk's end point, the ten path points (α_c, ω) in full f64 representation). Chunk 1 took 16.5 s with `par=0` and 12.9 s with `par=1`, load averages 8 to 11 on 10 cores: one measurement, not a benchmark.
4. **Driver.** The child's output is streamed to the log and the JSON lines are written and flushed as they arrive (`--stage=NAME` runs one stage and writes
   RAW/NAME.jsonl; `--arc-log=a.jsonl,b.jsonl,...` evaluates C, F, Z from the stage logs). Each child is capped at 3600 s.
5. **A hypothesis, untested** (no run spent on it): the arclength step stays near 1e-3 in α_c because the scaled step norm (`Scaling::Iterates`, needed so that Newton
   sees the tail unknowns of size 1e-44 and below) lets the tail, ln P ≈ −2kr over 44 decades, set the step. dk/k per point was 6e-4 on the weak side and 1.6e-3 at k = 0.35.

**A2, development results (dev_08 to dev_11), written after them; nothing below moves a declared bar.**

- dev_08 failed in its first second (an empty `modes=` and the target 4.017906 formatted as 4.01791 by `:g`; run_03 had the second bug too). Fixed.
- dev_09 stalled at α_c = 3.4824498 (target 3.5) because `step_family` also required Newton's own flag `converged` (tolerance 1e-28), which A2 does not
  declare. dev_10 logged the reasons: at α_c = 3.0 every refused step had a scaled residual of 2.2e-27 to 3.0e-27 (bar 1e-24) with the flag false.
  The code now takes a step when the scaled residual is at most 1e-24 and |Δ ln k| ≤ 0.25, as A2 says.
- dev_11 (stage `stepA`, 1486 s, load averages 3 to 7 on 10 cores): rows 2.1 to 3.9 (19 rows), 362 solves, 106 refused; **stalled at α_c = 3.9935489**
  (k = 0.1038, ω = 0.99460), target 4.0, with the step below 1e-7: Newton's scaled residual stays at 2e-6 to 8e-6 for every step down to 1e-7 (its first
  iterate 1.5). Not a turning point in α_c (the stored family is smooth to 4.017906). By the ruling the stepping stops there and no other method is tried.
  The accepted rows' scaled residuals grow with α_c: 6.6e-29 (3.5), 2.7e-28 (3.6), 1.3e-27 (3.7), 5.5e-27 (3.8), 7.3e-27 (3.9).
  Against the stored table: 48 of 57 tokens equal; 9 differ by 1.0 to 1.5 half-units of the last printed digit (relative at most 5.0e-8; the stored rows are
  boundary-value solutions at 1e-8): ω at 2.3, 2.8, 3.9; N at 2.1, 2.4, 2.8, 3.5, 3.9; M at 2.4. Not equal as worded; reported, not loosened.

**A2, the coordinator's ruling S1 on the stall (2026-11-26, after dev_11).**

- The stall is accepted as A2's rule requires. Rows α_c = 4.0, 4.015 and 4.017906 (3 of the 35 stored rows) and the mode scans at 4.0 and 4.015 are
  **NOT COMPUTED**: Newton in α_c with halving stalled at α_c = 3.9935489 (k = 0.1038, ω = 0.99460) with a scaled residual of 2e-6 to 8e-6 at every step
  down to 1e-7, and the stored family has no turning point in α_c there. No other method is tried. The stage `stepC` therefore lists 3.5 and 3.9 only.
- Why this region can wait: RESULTS.md §7 says that the old solver stops near ω → 1 because of the boundary condition, not the star, and the star continues
  through ω = 1. `phantom_follow.py`'s outer radius grew as k fell (R = 1919 at k = 0.0109). The three end rows test the far boundary, not the physics.
  The coordinator files the endpoint as a follow-up; no run is spent on it here.
- The hypothesis about the floor, **untested**: the layout's outer radius r_t against the decay length 1/k = 9.6 at the stall, or the tail condition's
  accuracy at that radius. The layout is `bvp.rs: nodes_from_profile`: r_x is the first integer radius where P < 1e-9 P_c, r_cut = r_x + ln(P(r_x)/1e-44)/(2k),
  r_t = r_cut + 40/k; outward segments at most 2.5/k, tail segments at most 10/k. The tail condition at r_t is u = −k − 1/r_t (the Yukawa decay of
  φ ∝ e^{−kr}/r, without the O(1/r²) and gravitational corrections), m = m_R free, Z = 1/(1 − 2m_R/r_t), and k′ = 0. At k = 0.1038: 1/k = 9.6, outward segments
  at most 24, r_t − r_cut = 385.
- The two items the coordinator accepted, recorded here: (1) the `par = true` check passed (dev_06, dev_07, all 7 lines identical); (2) the fix of the extra
  `converged` condition of `step_family` back to A2's text (dev_09, dev_10).
- The 9 of 57 tokens of rows 2.1 to 3.9 that differ by 1.0 to 1.5 half-units of the last digit are reported with the criterion's own wording
  ("each equal to the stored token"): **NOT MET** for those tokens, with each token's crate and stored value in `taylor_radial.md`. The stored rows are
  boundary-value solutions at tolerance 1e-8 (RESULTS.md §7). The criterion is not reworded.

### A3 (2026-11-26, after run_07_stepC; the coordinator's ruling by hc; before any run it names)

1. **F at α₀ = 3.5 and 3.9 is NOT COMPUTED, under A1.8's gate as declared.** A1.8: stars are solved by Newton to 1e-28 (scaled rows). run_07_stepC's rows
   at 3.5 and 3.9 reached 1.02e-28 and 7.6e-27 (A2's row bar of 1e-24 governs the rows, not the scans' input); `family::prepare` refused them, as it refuses any star
   whose Newton flag is false (`mroots_error` in `run_07_stepC.jsonl`). The gate is not loosened. F at 4.0 and 4.015: NOT COMPUTED (A2, S1).
2. **A supplementary run, outside A1.8's gate.** Stage `stepS`: the scans at α₀ = 3.5 and 3.9 on the stars as Newton converged them. Its output lines carry
   `"ungated":true` and, beside each σ² root (or "none"), the star's scaled residual. Its numbers enter **no verdict**: C, F and Z are evaluated without it, and F
   at 3.5 and 3.9 stays NOT COMPUTED. It is labeled "supplementary, outside A1.8's gate" here and in the note.
3. **S3 and E2 are built and run** (declared above): S3 is dd against qd for the central data and M of one star; E2 is the lane spread of ω₀ (X1) and σ₀² (Z), for
   D in dd and D in qd on the same dd star. Their settings are written in an addendum after their development runs. The qd lane of the star beyond S3's one
   star, and so ω_N and ω_M in qd, are not built.
4. **The independent multishoot eigenvalue solver** (σ² the global, README "What is built"): **NOT DONE**; a recommended task. Criterion Z's third error bar is therefore not available.

### A4 (2026-11-27, after the control development runs `dev_ctl_*`, before the control runs of record `run_ctl_*`)

The targets and effects of the controls, from the development runs. "Fires" is a failing verdict of the named check under `--mutate=NAME`; "silent" is a
passing verdict, which is a result. `Cs` and `Fs` are `C1` and `F` restricted to α_c ≤ 1.30 and α₀ = 1.10 (stored tokens: 18 and 4), evaluated on the
stage `arcm` (the arclength continuation to α_c = 1.30 with one scan at 1.10) run under the mutation; the unmutated `arcm` passes both (`dev_ctl_base_*`).

| control | fires on | silent on | note |
|---|---|---|---|
| `jsign` | A, X1, Fs | G1, Cs | the entry is flipped in the table, not in `jeval`'s series: G1 does not see it |
| `jomega` | A, X1, Fs | Cs | |
| `jmu` | X1 | | |
| `eps` | S1, S5, Cs, Fs | S4 | with ε = +1 the arclength path stays on the canonical branch (α_c 0.99817 after 54 chunks) and never reaches 1.10: the stage run was stopped by me at 24.5 min |
| `noqr` | P1, P2, A in the f64 lane | | the dd and qd lanes never finish (`dev_ctl_noqr`, stopped at the 1800 s cap); the control runs with `--p-lanes=f64` |
| `lowsum` | P1, P2 in the f64 lane | G2, A | the same `--p-lanes=f64` (`dev_ctl_lowsum` was stopped by me) |
| `shortR` | P1 in the qd lane | Cs, Fs | silent on the scan at α₀ = 1.10; Z at 2.0 and 3.0 was not run under it |
| `start` | | A, X1 | silent (X1b of ε = −1 fails unmutated too): the wrong leading term of χ at r_s = 1e-8 acts at order r_s³ |
| `plant_sign` | P1, P2 | | |
| `fit_deg` | P3, X1a | X1b ε = +1 | |
| `tailk` | | S1, S4, S5, Cs, Fs | silent by construction (A1.6) |
| `znorm` | S1, S5, Cs, Fs | S4 | |
| `nonewton` | Cs, Fs | S4, S5 | |
| `arcfold` | Cs, Fs | | the tangent flipped at the first point does not cross the fold |
| `arbstart` | A | | 374.6 half-units at the worst token |
| `start_term` | | S1, S2, A | silent |
| `shift_off` | G2, A | | |
| `wide_table` | G2, A | | |
| `recip_dd` | P1 in the qd lane | | qd worst relative 1.14e-33 against 1e-50 |

The runs of record `run_ctl_*` run each control on the checks above (the silent ones too), with `--p-lanes=f64` for `noqr` and `lowsum`, `--p-lanes=qd` for `shortR` and
`recip_dd`, and a 600 s cap on the stage runs of the family controls (the unmutated `arcm` takes about 170 s). A control run that reaches its cap is reported
as stopped, with what it printed. Also added: the supplementary run of A3 (`run_11_stepS`), the reruns `run_09_arc` and `run_10_stepB` (the qd variant of σ₀²),
and the options `--p-lanes`, `--stage`, `--tag`, `--supp-log` of the driver.

