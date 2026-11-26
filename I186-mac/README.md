# I186-mac: the polar matching determinant D(γ) by a Rust Taylor integrator

Machine: mac, the coordinator's Mac (Apple M5, 10 cores, 32 GB, macOS), shared with other sessions; runner
negative-mass-mac-i186 (Claude Code, Opus 5.5 account claude-me2). Issue: https://github.com/nmoinvaz/negative-mass/issues/186
Code: worktree `~/Source/negative-mass-i186`, branch `wip/i186-taylor-polar`. Pushes: `git push origin HEAD:refs/heads/wip/i186-taylor-polar`.
Written before the first run of record (`run_*`), after the development runs `dev_01` to `dev_44` that sit in this folder.
Amendments, if any, are numbered and dated at the end. Every number below that came from a development run says so.

## What is built

`phase2/nonradial/taylor_polar/` (Rust crate) computes D(γ) of `polar_solver.py` for real γ, with the same construction:
the interior 3-plane from r0 with the flat data r^l, the decaying Zerilli solution through the Riccati variable q = f Z′/Z
(from r_m + 40/γ + 20 l/γ + 50), the Moncrief map, the two decaying free-KG solutions from the contracting eigenspace of
the scalar block at R_s = r_m + 40/Re k, and D = det of the orthonormalized planes at r_m. Orientation is kept: the
orthonormalization is Gram-Schmidt with positive R diagonal (one reorthogonalization), which gives the same real D as the
LAPACK QR with its phase product (see `plane.rs`).

- **Integrator.** One Taylor step of order 30 for y′ = J y per step, from the jets of J's entries about the step start;
  the step is the largest whose last two terms (orders 29 and 30) are below `tol` (multishoot's `plan_path` rule, written
  out here); the plane is orthonormalized after every step. Reciprocals 1/k are formed in the lane (`plane::recips`).
- **Lanes.** f64, double-double (dd), quad-double (qd), octo-double (od): multidouble's scalar types behind one trait
  (`num.rs`). The lane's `tol` defaults to 100 u: 1.1e-14 (f64), 1.2e-30 (dd), 1.5e-62 (qd), 2.3e-126 (od).
- **J.** `taylor_polar.py --gen` writes `src/jgen.rs` from `polar_matrix_generated.py` by walking its syntax tree: every
  statement becomes a Rust operation on truncated power series. That file was written by `reduce_polar.py` (the
  issue and the brief name `gen_matrix2.py`, which is not in the repository: noted as a discrepancy). **The symbolic
  source is shared with `polar_solver.py`, not independent.**
- **The star.** Newton shooting in the crate, nothing from scipy's mesh: the Taylor recursion of `background.odes` in the
  variables (P, u, m, Z) = (φ0², φ0′/φ0, m, α⁻²) (polynomial/rational, only Cauchy sums and one reciprocal), started at
  r_s = 1e-8 from the leading-order regular series, P_c by bisection on the shot's class (u turns up or u → −∞) to the
  last bit, Z_c by the secant method on Z (1 − 2m/r) − 1 at r = 32. It is the star's own Taylor series, stored by step.
- **J's table.** J is linear in s² (checked in the table build at s = 1.5), so J = J0(r) + s² J1(r) is stored per l as
  Taylor coefficients (30 per entry) along the star, in steps cut by J's own radius of convergence. A plane step takes the
  jets of each entry about its start by shifting the table series (`ser::taylor_shift`). The exterior's vacuum J is
  evaluated directly at each step.
- **multishoot, multidouble.** `Cargo.toml` pins multidouble to main `ba0ad101ce76` (the series module, unreleased) with
  `[patch.crates-io]`; multishoot 4.2.0 requires `multidouble = "5.1.0"`, a caret requirement, which that revision
  satisfies, so no multishoot change is needed (the brief's "exact pin =5.1.0" is a caret in multishoot's Cargo.toml). The
  crate uses multidouble's DD, QD and OD scalars and calls multishoot's `Plan::optimal_kt` to print the order its cost
  model prefers (42 at 1.2e-30, 22 at 1.1e-14; the crate stops at 30). **It does not use multishoot's `Equations`,
  `Shooting` or lanes**: those solve boundary-value problems with 8-lane double-double fields and have no place for the
  orthonormalization between steps; the planner's rule is rewritten in `plane.rs`. Whether multishoot's `Shooting` should
  solve the star's boundary-value problem as an independent check is a recommended task, not done.
- **multidouble's series module (`mullow`, `Relaxed`).** Not used in the integrator. Its crossovers (512 in double-double,
  64 in quad-double, 16 in octo-double, README of multidouble) lie above the 30 coefficients of every product here, and
  the engine's products are scalar, not on lanes.

## What is shared with the scipy path, and what is not

| Shared (so not independent) | Not shared |
|---|---|
| the symbolic J (`reduce_polar.py` output), the problem's construction (r0, r_m, flat start data, Riccati start, Moncrief map, scalar-plane start columns, orientation), the model constants | the integrator, the orthonormalization, the star solver and its boundary treatment, the table, the lane arithmetic |

The stored rows (`convergence_l*_output.txt`) are scipy's DOP853 on a `solve_bvp` mesh star. Planted systems are compared
with mpmath, which shares no code with the crate. The mpmath evaluation of the generated function (T1, T2) shares the
symbolic J and no arithmetic.

## Discrepancies and answers (coordinator t2x)

- **Eight l = 2 rows, not nine.** `convergence_l2_output.txt` has γ = 1e-3 to 137. The script's list also has 300. The file
  and the script entered in one commit (81cc13d, 2026-10-22), the script already listing 300, and the file has no note of a
  stopped run; I cannot tell why the row is absent. The coordinator confirmed the "nine" was an error. A fresh scipy value at
  (l = 2, γ = 300) is part of the timing run (TS) and is compared as the ninth point.
- **S3.** The coordinator approved the bar 1e-16 on the central data's change with the start radius, and added the scaling
  test below (set after a dev probe that measured 8.6e-18).
- **T3, wording and bar.** First wording: each entry's error relative to itself, bar 1e-20, set from one dev point (s = 1,
  l = 2, 4.6e-23). Its first dev run at s = 0.3 gave 4.0e-17 at J[0][0] = 5.5e-5 (r = 1.3e-3); a normwise rewording gave
  4.0e-20. Both failures came from my check harness, which formed s² as an f64 product while the direct J used the exact
  double-double square; the integrator squares γ in the lane and was never affected. With the harness fixed the
  entrywise worst is 4.6e-23 and the worst relative to the largest |J| entry 8.6e-27. The coordinator's ruling: gate on the
  first wording (entrywise, 1e-20), print the normwise value. (I had first explained the 4.0e-17 as cancellation in
  J[0][0]; that explanation is withdrawn.)
- **Timings** are quoted only from the run of record, with the machine's load and the thread count.

## Defects found in development (kept as findings)

1. **J's table steps (D1).** The first table cut the star's Taylor steps only where the star's series needed it. The star's
   functions are regular at r = 0 and its steps near the centre are long; J has 1/r and 1/r² terms, so its series about a
   step start has radius about r. A plane step shifted J's series by up to a whole star step, past that radius. Near
   r = 2e-3 the shifted jets were wrong by up to 560 % and the sign of D flipped with the star's step structure: the same
   physics, a different `startol`, gave D of either sign at the same |D| to 1e-14. I found it in unlogged interactive
   probes; the mutation `wide_table` restores the defect, and `dev_40` to `dev_44` reproduce it as logged runs: table
   against direct J, relative error 9e-5 at r = 1e-3, 5.9e-2 at 2.1e-3, **5.6 at 2.25e-3**, 22 at 2.3e-3, back to 1e-15
   at 3e-3; D(l = 2, γ = 1, f64) = +6.00220e-3, −6.00220e-3, −6.00220e-3 for `startol` 1e-30, 1e-27, 1e-20 (`dev_41`–`dev_43`)
   against −6.00220e-3 with the fix (`dev_44`). The earlier matches with the stored rows at rs = 1e-6 were partly luck.
   Fix: a table step is at most 0.3 of the width at which J's series has converged to 1e-25 (last two coefficients against
   the sum). T3 and the control `wide_table` catch it (T3 26, A2 sign flipped, `dev_27`). The other findings below were also
   made in interactive probes before the logged development runs, and are re-run by the checks themselves.
2. **Planted harness.** Decimal inputs (0.3, 0.1) are not the same number in Rust and mpmath: the first planted comparison had
   a 4e-17 floor until the matrix and starts were made dyadic. mpmath's `expm` loses the sub-dominant directions at
   ‖A‖ L ≈ 2e5 (90 digits), and `eig` leaves a complex phase on a real eigenvector: the long-L reference is now closed
   form from the invariant subspaces, with the orientation sign det M, and a transient case at γ L = 40 uses `expm` at 140
   digits. The crate printed 40 digits, which hid quad-double (1e-64): it prints each lane's full digits.
3. **S3's first bar** (1e-18) was a guess before any run; see above.
4. **Controls.** In dev, `jsign` on J[1][4] left D unchanged at 4e-7 (D is nearly independent of that coupling): the
   mutation now negates J[3][2], the largest entry. `dropterm` (the order-30 term of the Taylor sum, about 1e-30) fired
   nowhere: replaced by `lowsum`. `noqr` and `zc1` ran away (one evaluation over 12 minutes, one star shot through a zero
   of φ): both runs were stopped by their PIDs, their logs kept (`dev_22`, `dev_24`), and the crate now carries a step cap
   in the star shooting and a wall-clock cap (`TP_MAX_SECONDS`, 60 s under a mutation) in `integrate`.

## Criteria (each can fail; `taylor_polar.py` codes them exactly so)

Reference for D: the stored base-variant rows `convergence_l{2,4,5,6}_output.txt` ("stored"), 7 printed digits. "Spread" is
the file's 2.1e-4, the largest relative spread of D between the variants in any row. Lane dd unless named.

| ID | What is compared | Points | Bar |
|---|---|---|---|
| T1 | J at order 0, crate (dd) against the generated function evaluated at 60 digits (mpmath), each entry relative to itself | 8 points (l = 2, 3, 4, 6; s = 0 to 12000), 36 entries | 1e-24 |
| T2 | J's 30 series coefficients (Horner at 0.1 of a star step) against the generated function at 60 digits, on the series' own background | 4 cases, 96 entries | 1e-24 |
| T3 | the table's order-0 jets against J evaluated directly from the star, each entry relative to itself; the error relative to the largest \|J\| entry is printed, not gated | 150 radii 1e-3 · 1.037^i < 23; l = 2 (s = 0.3), l = 6 (s = 300) | 1e-20 |
| R1 | \|k (1/k) − 1\| for k = 1..32, 1/k formed in the lane (the control of choptuik-large-d's `recip_check.py`), at 200 digits | qd, od | 8 u (1.2e-63, 1.8e-127) |
| P1 | planted y′ = A y, A = blockdiag([[0,1],[g²,0]]) + C, g = γ + (0, ½, ¾), C_ij = (((7i + 3j + 1) mod 11) − 5)/8, dyadic starts: D, the planes (projectors) and ln vol against the invariant subspaces at 90 digits, L = 24, Lz = 40 | γ = 3, 10, 300, 12000 (qd: 10, 300) | f64 1e-6, 1e-9, 1e-9; dd 1e-24; qd 1e-56 (D, planes, ln vol) |
| P0 | the same system in the transient (γ L = 40), mpmath `expm` at 140 digits, orientation included | γ = 3, 300, 12000; f64, dd | as P1 |
| P2 | A(r) = A0 + r A1, A1_ij = (((5i + 2j + 3) mod 7) − 3)/16, mpmath `odefun` at 60 digits | γ = 3, 6; L = 1; dd | 1e-28 |
| S1 | the star by shooting against `solve_star` at 10 radii (α, a, φ0, u, each relative): exact regular start; and the shooting started at r0 = 1e-3 with scipy's leading-order boundary condition | r = 0.002 … 24.10980364018201 | 1e-6; 1e-9 |
| S2 | the crate's star at r = 8 against DOP853 (rtol 1e-13) on `background.odes` started from the crate's state at r = 0.5 | one pair | 1e-9 |
| S3 | the central data (P_c, Z_c) against the start radius: rs = 1e-8 vs 1e-9; and the scaling: that difference over the rs = 1e-6 vs 1e-7 difference is 1e-4 within a factor of 3 (rs² law) | both | 1e-16; [3.3e-5, 3e-4] |
| A2, A4, A5, A6 | D against the stored rows, \|D/D_stored − 1\| at every stored γ | l = 2: 8 rows (1e-3 … 137); l = 4: 11 (… 3000); l = 5: 11 (… 6000); l = 6: 11 (… 1000, 12000) | spread 2.1e-4 |
| L1 | lanes: f64 against dd at (2, 300), (6, 1000), (6, 12000), gated at the spread; dd against qd at (2, 300), (6, 137) | as named | 2.1e-4; 1e-20 |
| V1 | the variant r0 = 3e-3 (r_m = 24.111) against the base, same code | (2, 1), (2, 137), (6, 1000) | 2.1e-4 |
| V2 | the variant r_m = 34.2051 against the stored D(r_m ~ 34) column (4 digits) | 7 points | 2.1e-4 + 0.5e-3 / mantissa |
| V3 | order 24 at tol 1e-22 against order 30 at 1.2e-30 (the analog of the rtol variant), measured at 60 digits | (2, 10), (6, 1000) | 1e-15 |
| V4 (amendment A1) | convergence.py's variants (R = 90, r0 = 3e-3, rtol 1e-12) through scipy here and through the crate at the same r0 and r_m (read from each scipy problem) | (2, 1), (2, 10), (6, 10), (2, 137) | 1e-7 |
| TS | the scipy path on this Mac (base variant): its D against the crate's dd, and both wall times | 11 points (l = 2: γ = 1, 10, 40, 137, 300; l = 6: 0.001, 1, 40, 137, 300, 1000) | 2.1e-4 on D; time reported |

The acceptance of the issue: A2 (l = 2) and A6 at γ = 1000 and 12000 against the stored rows; the planted case P1 with QR;
the star S1 (with S2, S3); the time TS; and a control for each. A6's other rows and A4, A5, L1, V1 to V3 are additional.
A miss at A2 or A6 is reported as it comes out; no bar is moved after a run of record.

## Controls (`python taylor_polar.py --mutate=NAME`: the checks named must fail; exit 1)

Targets are the values the targeted checks reach in the development runs named (before declared here).

| Control | The error | Targeted checks and the dev values |
|---|---|---|
| `jsign` | J[3][2] negated (jcheck, jjets, the table) | T1 2.0, T2 2.0, A2 1.64 (dev_32) |
| `lowsum` | the Taylor sum cut at order 8 | P0[f64] ln vol 2.6e-3, P0[dd] 1.2e-6, P1 2.5e-3 / 1.1e-6 / 4.2e-15 (f64 / dd / qd), P2 D 1.3e-5 (dev_33); A2 moves 2.3e-6 and is not a target |
| `lin_drop` | the planted matrix without its linear term | P2 D 1.2 (dev_20) |
| `recip_dd` | 1/k formed in dd and widened (qd, od) | R1 3.1e-33; P1[qd] ln vol 2.0e-36 (D and planes unchanged at 1.5e-63: a constant-coefficient system's invariant planes do not depend on the series coefficients, only its growth does) (dev_21) |
| `noqr` | no orthonormalization between steps (P1 at γ = 3, qd at γ = 10) | P1[f64] D 1.4e268, P1[dd] 7e236, qd and A2 abort (a non-finite coefficient or the 60 s cap) (dev_37) |
| `star_eps` | the star solved with ε of the wrong sign | S1 0.12, S2 8e12, A2 5.5e-3 (dev_23) |
| `zc1` | Z_c = 1 (lapse normalization skipped) | S1, A2 abort at the star's step cap (dev_34) |
| `start_term` | the start u = r c/2, not r c/3 | S1 (matched start) 6.3e-2 against 1e-9, S3 ratio 1.0e-6 against 1e-4 (dev_25); the exact-start part of S1 stays at 4.1e-8 |
| `shift_off` | the table's jets not shifted to the step start | T3 1.3 (entrywise; 7.0e-2 normwise), A2 4.3 (dev_26) |
| `wide_table` | table steps as wide as the star's (defect D1) | T3 26, A2 sign flipped (rel 2.0) (dev_27) |
| `moncrief` | one sign in the Moncrief map | A2 1.65e3 (dev_28) |
| `swapcols` | the scalar plane's two start columns swapped | A2 sign flipped (rel 2.0) (dev_29) |
| `mext0` | the exterior mass set to 0 | A2 0.996 (dev_30) |
| `qstart` | the Riccati started at r_m + 1 | A2 0.21 at γ = 0.001 (dev_31) |

## Amendments

- **A1 (2026-11-26, after run_04, before run_05).** Added V4 and put it among the targets of the control `moncrief`. Reason: a
  development probe (`dev_45`, `spread_probe.py`: scipy's D of each variant at (2, 1), (2, 10), (6, 10)) showed that the
  stored rows' variant spread of 2.1e-4 is the shift of r_m, not integration error: rtol 1e-12 moves D by at most 3.5e-12,
  R = 90 (r_m = 24.1084) by +1.13e-4 and r0 = 3e-3 (r_m = 24.1110) by −9.9e-5, against the base's r_m = 24.1098. The bar 1e-7
  is about 20 times the 4.5e-9 that TS gave for the base variant at (2, 300) in run_02. V4 is additional to the acceptance;
  no bar of run_02 or run_03 is touched. `run_05` is V4 alone, `run_06` the control `moncrief` again.

## Run plan

1. `run_01`: `python taylor_polar.py --scipy-timing scipy_timing.jsonl` first (one process, nice 10, 1 thread, each
   evaluation under a 1 h alarm; the l = 6, γ = 12000 evaluation (89 h) is not run: its stored row is the comparison).
2. `run_02`: `python taylor_polar.py --scipy-file=scipy_timing.jsonl` (every check, then TS).
3. `run_03`: every control, one after another.
4. The output of 2 and 3 goes to `phase2/nonradial/taylor_polar_output.txt` with the load average and the commit.
Limits: one process at a time, nice 10, RAYON_NUM_THREADS = 2 (the crate itself is single-threaded), a run over 1 h is stopped
by its PID. Memory is reported only.

## Files

`devrun.sh` runs a dev command and keeps `dev_NN_<name>.{log,err,rc}`; `run_controls_dev.sh` runs the controls in
development. `dev_01`–`dev_06` are the first D values (l = 2, 6) from the first crate; `dev_07`–`dev_17` the checks as they were
written (several failed, see above); `dev_14` onward use the fixed table.

## Outcome (the runs of record; the numbers are in `phase2/nonradial/taylor_polar_output.txt` of the code repository)

- `run_01` the scipy path, 11 points, 267 s in all, one process. `run_02` every check: 22 of 22 pass (779 s). `run_03` the
  14 controls: each fails its targeted checks. `run_04` the one-time costs (star shooting 2.7 s, table 3.2 s per l). `run_05`
  V4 passes (worst 8.5e-10). `run_06` the control `moncrief` again with V4 among its targets: fails both.
- Dev findings as listed above; the output file's first lines name the commit of the crate (b9da6ad for the V4 runs, ebd4cdc
  for run_01 to run_04, the first line of each log says which).
