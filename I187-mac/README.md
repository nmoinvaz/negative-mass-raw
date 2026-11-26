# I187-mac: convergence.py's rows, and #114's two capped rows, from #186's Rust Taylor crate

Machine: mac, the coordinator's Mac (Apple M5, 10 cores, 32 GB, macOS), shared with other sessions; runner
negative-mass-mac-i187 (Claude Code, Sonnet 5.5, account claude-me2). Issue: https://github.com/nmoinvaz/negative-mass/issues/187
Code: worktree `~/Source/negative-mass-i187`, branch `wip/i187-taylor-rows` (from main 6dcbbb6). Pushes: `git push origin HEAD:refs/heads/wip/i187-taylor-rows`.
Written before the first run of record (`run_*`); the development runs `dev_NN_*` (made with `devrun.sh`, which keeps stdout,
stderr and the exit code) sit beside it. Amendments are numbered and dated at the end. A number below that came from a
development run says which.

## What is built

On top of #186's crate (`phase2/nonradial/taylor_polar/`, merged) and `taylor_polar.py`, behind a new mode `--rows`:

- **q_int** (`interior_q`): the interior Zerilli log-derivative f Z′/Z at r_m of `polar_solver.interior_zerilli`. There the null vector
  c of (I − S S⁺) Y[2:] (4 × 3) is the last right-singular vector of an SVD. Here it is the null vector of the 4 × 5 matrix
  [Y[2:] | −S] by signed 4 × 4 cofactors (n_j = (−1)^j det of M without column j) in the lane; (H1/s, K) = Y[:2] c; (Z, Z′) = T⁻¹ (H1/s, K)
  with T the Moncrief map; q_int = f Z′/Z. S is the exterior scalar plane (4 × 2) the D evaluation already builds. The method differs
  from the scipy path's (SVD against cofactors); the symbolic source, the planes and the Moncrief map are shared.
- **q_ext**: the crate's `q` (the Riccati variable of the decaying Zerilli solution at r_m), unchanged.
- **r_m by the grid rule of `PolarProblem`**: r_m = r_i for the first i with φ0(r_i) < φ_cut on r_i = linspace(r0, R, 20000) (numpy's
  formula i·step + start, step = (R − r0)/19999, last point R), φ0 from the crate's own star.
- **The five variants** of `convergence.py` and their crate analogues. Each is one call of the same `d_eval` with different inputs:

  | convergence.py name | scipy variant | crate analogue (stated as what it is) |
  |---|---|---|
  | `base (rtol1e-10, phi_cut1e-9, R60)` | rtol 1e-10, φ_cut 1e-9, R = 60, r0 = 1e-3 | order 30, tol 1.2e-30 (dd), φ_cut 1e-9, grid R = 60, r0 = 1e-3, star shot with classification radius 60 |
  | `rtol 1e-12` | rtol 1e-12 | **no scipy rtol exists in the crate.** The analogue is a looser step control of the same integrator: order 30, tol 1e-12 (the bound on the last two Taylor terms), everything else as base. It measures the crate's sensitivity to its step control. The header line prints `rtol 1e-12 [crate: Taylor tol 1e-12]` |
  | `phi_cut 1e-12 (larger r_m)` | φ_cut 1e-12 (r_m ≈ 34.2) | as base with φ_cut 1e-12 |
  | `background R=90` | star solved on [1e-3, 90] | the star shot with classification radius 90 (its own pc, zc, J table), and the r_m grid over [r0, 90] |
  | `r0 = 3e-3` | interior start at 3e-3 | the interior start at r0 = 3e-3 and the r_m grid from 3e-3 |

  The row prints D of each, q_int and q_ext of the base variant only (as `convergence.py`'s task `q` does), and the spread over the
  names without `phi_cut` in them, which leaves base out (its name contains `phi_cut1e-9`; #114 found this, it is in main) and keeps
  rtol 1e-12, R = 90 and r0 = 3e-3. The driver keeps convergence.py's names and f-string so this quirk reproduces.
- **`rows` command, `--rows` mode.** One crate process per l: the star(s) and the J table are built once (≈ 3 + 3 s per l), then every
  (γ, variant) is a `d_eval`; each evaluation is one JSON line, flushed, so a stopped run resumes at the next γ. Everything is
  appended to a jsonl file in this folder. `python taylor_polar.py --rows --l=6 --jsonl=PATH` prints the rows in `convergence.py`'s
  format and runs the checks below. Lane dd (the row) unless named.
- **Reporting fix** (the coordinator's review of #186). A skipped check is `SKIPPED`, kept apart in the summary
  ("N passed, M failed, K skipped (names)"), and can never count as a control's fired target. Before the fix, in a development run:
  `--only=TS` printed `SUMMARY: 0 of 0 checks passed`, exit 0 (`dev_NN`, named in the amendments once made).

## What is shared with the scipy path, and what is not

| Shared (so not independent) | Not shared |
|---|---|
| the symbolic J, the problem's construction (r0, r_m rule, flat start data, Riccati start, Moncrief map, scalar-plane start columns), the model constants, the 20000-point grid rule | the integrator, the orthonormalization, the star solver, J's table, the lane arithmetic, the null-vector method of q_int |

Stored rows: scipy's DOP853 on a `solve_bvp` star (`convergence_l{2,4,5,6}_output.txt`, 7 printed digits). For l = 4, 5, 6 the
full-precision scipy values of every variant at every γ are in `negative-mass-raw/I4-win/convergence_l{4,5,6}_w0.7603.partial.csv`
(read only, used for differences that explain a token, not as a gate); for l = 5 γ = 6000 #114's finished rtol 1e-12 evaluation is in
`negative-mass-raw/I114-win/convergence_l5_w0.7603.partial.csv` (read only). #114's l = 6 run is still going on surface-laptop-4 and is
not touched.

## γ lists

| l | γ | stored file |
|---|---|---|
| 2 | 0.001, 0.03, 0.3, 1, 3, 10, 40, 137 and 300 | the file has the first 8; 300 is in `convergence.py`'s list and not in the file: printed, compared with #186's fresh scipy D (`I186-mac/scipy_timing.jsonl`) |
| 3 | 0.001, 0.03, 0.3, 1, 3, 10, 40, 137, 300, 1000 (the script's list) | none in the repository: rows printed, not compared |
| 4 | the 8 above, 300, 1000, 3000 | 11 rows |
| 5 | the 8 above, 300, 1000, 6000 | 11 rows (the 6000 row is #114's capped one) |
| 6 | the 8 above, 300, 1000, 12000 | 11 rows (the 12000 row is #114's capped one) |

## Criteria (each can fail; `taylor_polar.py --rows` codes them exactly as worded)

| ID | What is compared | Points | Bar |
|---|---|---|---|
| QP | planted q_int: dyadic planes Y (6 × 3) and S (4 × 2) built so that Y[2:] c0 ∈ span S with a known c0, dyadic r_m, M, l = 3; the exact q_int from sympy's rational null space and Fractions (no code shared with the crate), two cases: well conditioned, and near-degenerate (column 3 of Y = column 2 + 2⁻²⁷ w) | f64, dd, qd | well conditioned: 1e-12, 1e-28, 1e-60. Near-degenerate: 1e-5, 1e-20, 1e-50 (relative) |
| RP | planted r_m: φ0(r) = a e^{−κ r} through the crate's grid rule against numpy's `linspace` and `argmax`: the index and the float r_m, each equal | (φ_cut, R, r0) = (1e-9, 60, 1e-3), (1e-12, 60, 1e-3), (1e-9, 90, 1e-3), (1e-9, 60, 3e-3), with a = 0.02, κ = 0.65 | exact equality of the index and of r_m |
| RM | the crate's r_m of the five variants (from its own star) against `PolarProblem(...).rm` of the scipy path (scipy stars R = 60 and 90) | the 5 variants | exact equality of the float |
| RA2, RA4, RA5, RA6 | the printed rows against the stored file, token by token as strings: header lines (variant name, r_m `%.2f`) and each row's γ, `D_base` (`%+.6e`), `signs`, `rel.spread` (`%.1e`), `D(r_m~34)` (`%+.3e`), `q_int`, `q_ext` (`%+.6e`). The time column and the bracketed note of the two capped rows are not compared. The `rtol 1e-12` header's name differs by design; its r_m is compared | l = 2: 8 rows; 4, 5, 6: 11 rows each | every token equal as a string |
| RX | l = 2, γ = 300 (no stored row): the crate's `D_base` token against #186's fresh scipy D there (−1.0204252e-9, `I186-mac/scipy_timing.jsonl`) | 1 | string equality of the 8-digit token `%+.7e` |
| CAP5, CAP6 | the capped rows (l = 5, γ = 6000; l = 6, γ = 12000): (a) D < 0 in each of the five variants; (b) \|D_tol1e-12 / D_base − 1\| ≤ 2.1e-4 (#114's acceptance, applied to the crate's analogue); (c) for l = 5 only, the five crate D against #114's five scipy values, each relative difference ≤ 1e-8 (2 × the worst crate-vs-scipy 4.5e-9 of #186's TS, rounded up; set before any run) | 2 rows | as listed. (d) printed, not gated: the error bars E1 to E4 below |

What the error bars of a capped row are (each named, none rigorous):
- **E1**: \|D(tol 1e-12)/D(tol 1.2e-30) − 1\|, a spread over two Taylor tolerances at order 30 (dd). An estimator range of the integration error of the looser setting.
- **E2**: \|D(order 24, tol 1e-22)/D(order 30, tol 1.2e-30) − 1\|, a spread over order and tolerance (dd). An estimator range.
- **E3**: \|D(f64)/D(dd) − 1\|, a spread over two lanes: the roundoff scale of the f64 lane. Not an error bar of dd, whose roundoff is smaller by about 1e-16.
- **E4** (l = 5 only): the crate's D against an independent scipy evaluation of the same (l, γ, variant): a spread over two solvers. It contains scipy's own integration error, which #114 measures as 2.33e-9 between its rtol 1e-10 and 1e-12 evaluations at this point.
- The 2.1e-4 spread between the variants is **not** an error bar: #186's V4 showed it is the shift of r_m between the variants (24.1098, 24.1084, 24.1110), to which D, a normalized determinant, is sensitive.
- No quad-double evaluation at these γ is made (estimated 1.5 to 3 h each, past the 1 h cap). The dd-against-qd agreement 5.7e-26 and 5.4e-29 of #186's L1 at (2, 300) and (6, 137) is cited, not repeated.

The stored-row criterion is the strict reading, "agrees to its printed digits" = the same printed token. The stored tokens are scipy's, and #186 measured the crate's difference
to scipy at up to 4.5e-9 (TS); a token whose scipy value lies within a few 1e-9 of a rounding boundary can differ in its last digit
without any defect. Such a token is **reported as not met**, with the crate's unrounded value, scipy's full-precision value (l = 4, 5, 6) and the
distance to the boundary; it is not passed under another name and no bar is moved.

The acceptance of the issue maps as: every stored D and q agrees to its printed digits = RA2, RA4, RA5, RA6 (RX extra); the capped
rows with their error bars named = CAP5, CAP6; a control (a mutated variant) fails and each check has a `--mutate=` = the controls below.
QP, RP and RM come first: the new code (q_int, the r_m rule) is tested on planted truth before the real rows.

## Controls (`python taylor_polar.py --rows --mutate=NAME`: the checks named must fail; exit 1)

Names, the error each puts in, and the checks they target. **The measured values the targets reach in the development runs are
filled in at step 4 (amendment A1), before the run of record of the controls.**

| Control | The error | Targeted checks |
|---|---|---|
| `qint_sign` | +S instead of −S in M = [Y[2:] \| −S] (a wrong null vector) | QP, RA |
| `qint_f` | q_int formed as Z′/Z, without the factor f = 1 − 2M/r_m | QP, RA |
| `rm_off1` | the r_m grid index one too low | RP, RM, RA |
| `rm_cut` | the φ_cut variant's cut set to 1e-11 | RM, RA |
| `r0_grid` | the r0 = 3e-3 variant's r_m grid starts at 1e-3 | RM, RA |
| `tol_loose` | the rtol-analogue variant runs at tol 1e-3 | CAP |
| `qstart` (#186's) | the Riccati started at r_m + 1, which moves q_ext | RA |
| `moncrief` (#186's) | a sign in the Moncrief map, which moves D and q_int | RA, QP |

Each control is run alone; each must exit 1 with the targeted checks failing.

## Runs (planned; sizes from #186's timings, dd, one process, nice 10, one thread)

- Development: `devrun.sh NAME cmd`, each logged; none quoted as a result.
- Run of record, one process at a time: QP, RP, RM; RA2 + RX (seconds); the l = 3 rows (extra, printed, no stored file, no check); RA4; RA5 + CAP5; RA6 + CAP6
  (the 5-variant row at l = 6, γ = 12000 is about 6.5 min); then the default mode (#186's 22 checks, ≈ 13 min), then the controls.
- Stop condition: a single run not finished in 1 h of wall time is stopped by its PID and reported. Memory is reported
  (`/usr/bin/time -l`), nothing is stopped over it.
- Timings are reported with the machine, the load average at the run's start and the thread count (one).

## Amendments

**A1, 2026-11-26, after the development runs `dev_01` to `dev_21`, before any run of record.**

1. *Control `qint_sign` is replaced by `qint_cofsign`* (the cofactor signs of q_int's null vector not alternated). A sign of S in
   M = [Y[2:] | −S] does not change the null vector's c, so `qint_sign` could not fire (found by analysis, not by a run).
2. *The R = 90 analogue uses the same star.* The star's central data (P_c, Z_c) are the same 33 digits for the shooting's
   classification radius 60 and 90 (`dev_01`, `dev_02`), so a second star would be the same star: the variant differs from base by its
   r_m grid over [r0, 90] only (as #186's V4 found). The table in "What is built" row `background R=90` reads that way.
3. *Reporting names.* The clauses of CAP5 and CAP6 are reported as separate checks with the bars as worded above: `CAP5a`, `CAP5b`,
   `CAP5c` (l = 5) and `CAP6a`, `CAP6b` (l = 6), so that each clause can have a control. "CAP5 met" means all three are met.
4. *Development result for CAP5 (`dev_18`, dd, load 2.1)*: (a) and (b) hold (E1 = 1.4e-14); **(c) fails as declared**: crate D against #114's
   scipy D at l = 5, γ = 6000, bar 1e-8 per variant: base 5.4e-9, rtol analogue 3.1e-9, R = 90 8.0e-10, r0 = 3e-3 4.2e-9, **φ_cut 1e-12 4.7e-8**.
   Coordinator's ruling (hc, t2x): option (A), the bar stays 1e-8 and the run of record reports CAP5c not met for the φ_cut variant.
5. *New check `CAP5s`, added after that development result (coordinator's ruling).* The crate's star started as scipy's: the shooting
   from r_s = 1e-3 with scipy's leading-order boundary condition (#186's S1 "matched" start, which agrees with `solve_star` to 1e-10), at l = 5,
   γ = 6000, all five variants against #114's scipy D, bar **1e-8 per variant, the same as CAP5c, not to be tuned**. The change of the
   crate's own D from r_s = 1e-8 to 1e-3 is printed, not gated. A development run (`dev_20`, the script `diag_matched_star.py`, before this check was coded)
   gave the same five numbers as CAP5c to all printed digits, so CAP5s is expected to fail at the φ_cut entry in the run of record too; the note
   states CAP5c and CAP5s as measured. `dev_21` shows why the star start does not move D: D (l = 2, γ = 1, dd) changes by 5e-21 relative from r_s = 1e-8 to 1e-3, because the
   star beyond the centre is the same decaying solution (m(r_m) agrees to 5e-18).
6. *Control `tol_loose`*: its targeted check is `CAP5b` (the rtol analogue at tol 1e-3 must leave the 2.1e-4 bar). CAP5c and CAP5s fail on real data
   already, so a control cannot show them firing; their `tol` entries (3.1e-9 unmutated) are read in the control's log instead.

**A2, 2026-11-26, step 4: the controls' targets, from the development runs named (before the run of record of the controls).**
A control is `python taylor_polar.py --rows --mutate=NAME`; the targeted checks must fail, exit 1.

| Control | The error | Targeted checks and the development values (dd, one thread) |
|---|---|---|
| `qint_cofsign` | the cofactor signs of q_int's null vector not alternated | QP relative error 9.0 (well-conditioned), 0.61 (near-degenerate) against bars 1e-12 to 1e-60 and 1e-5 to 1e-50; RA2 63 of 66 tokens (the three q_int tokens at γ ≤ 0.3 differ; the others agree at 7 digits because q_int ≈ γ there) (`dev_26`) |
| `qint_f` | q_int without the factor f | QP 1.3e-3 in all six; RA2 58 of 66 (all eight q_int tokens) (`dev_27`) |
| `rm_off1` | the r_m grid index one too low | RP 4 of 4 cases differ; RM 5 of 5 variants differ; RA2 33 of 66 tokens (`dev_28`) |
| `rm_cut` | the φ_cut variant's cut at 1e-11 | RM: φ_cut r_m 30.821 against 34.205 (the other four equal); RA2 57 of 66 (its r_m header and the eight D(r_m~34) tokens) (`dev_29`) |
| `r0_grid` | the r0 variant's r_m grid from 1e-3 | RM: r0 variant 24.1098 against 24.1110; RA2 58 of 66 (the eight spread tokens, spread 1.1e-4 against 2.1e-4) (`dev_30`) |
| `qstart` (#186's) | the Riccati started at r_m + 1 | RA2 54 of 66 (D, spread, D(r_m~34), q_ext at small γ). **RX does not fire**: at γ = 300 the Riccati forgets its start, so RX is not a target (`dev_31`) |
| `moncrief` (#186's) | a sign in the Moncrief map | RA2 35 of 66; RX −3.7e-6 against −1.0e-9; QP 0.26 and 0.15 (`dev_32`) |
| `tol_loose` | the rtol analogue at tol 1e-1 | CAP5b: E1 = 1.4e-3 against the bar 2.1e-4; its `tol` entry of CAP5c reads 1.4e-3 against 3.1e-9 unmutated (`dev_35`). At first the control ran at tol 1e-3, which moved D by 3.9e-6 and did not fire (`dev_33`); the sweep `dev_34` gave E1 = 4.1e-4 at 1e-2, 1.4e-3 at 1e-1; its tol = 1 run did not finish (more than 8 min) and was stopped by its PID with the sweep script (rc 143), as was the tol = 10 process the script had started before it was stopped |
| `jsign` (#186's) | J[3][2] negated | CAP5a: D > 0 in base, tol and r0 (+8.47e-13, +8.47e-13, +1.28e-12), < 0 in φ_cut and R = 90 (`dev_36`) |

Each check of `--rows` has a control: QP (qint_cofsign, qint_f, moncrief), RP (rm_off1), RM (rm_off1, rm_cut, r0_grid), RA2 (all of the
above but jsign and tol_loose), RX (moncrief), CAP5a (jsign), CAP5b (tol_loose). RA4, RA5, RA6 and CAP6a, CAP6b are the same code at other l
and are controlled through RA2, CAP5a, CAP5b. CAP5c and CAP5s fail on real data already, so no control can show them firing; the tol_loose
control's `tol` entries of CAP5c (`dev_35`) and, in the run of record, of CAP5s are the evidence that they can fail per variant. CAP5s's control
run is `--mutate=tol_loose --only=CAP5s`.
