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

Controls' targets and effects: Amendment A2, after the control development runs.
