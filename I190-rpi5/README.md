# I190-rpi5: implicit-ODE Taylor facility for multishoot (PR), planted checks, #167's crate switched to it

Machine: rpi5-ubuntu (Raspberry Pi 5, 4 cores, 8 GB, aarch64, shared with choptuik-large-d). Issue: https://github.com/nmoinvaz/negative-mass/issues/190

Written before the first run of any test. Amendments, if any, are listed at the end with their reason and the coordinator's
answer; nothing above them is edited.

## Where

| what | where |
|---|---|
| worktree (the crate, the note) | `~/Source/negative-mass-i190`, branch `wip/i190-implicit-taylor`, base 9debda2 (#183's head) |
| multishoot clone | `~/Source/negative-mass-i190-libs/multishoot`, branch `feat/implicit-taylor` from main 70fac93 |
| raw | this folder; logs `dev_NN_*.log` (development), `run_NN_*.log` (of record), every rerun numbered, none overwritten |
| toolchain | rustc 1.100.0, cargo 1.100.0, rustfmt 1.11.0, clippy 0.1.100; multishoot 4.2.0, multisolver 0.2.2, multidouble 5.1.0 |
| budget | 2 threads, `nice -n 10`, one build or run at a time; runs over a few minutes as `systemd-run --user --unit=nm-i190-<name>` |

## The facility (module `multishoot::implicit`)

The equation is N(x, y, y', y'') = sum_g A_g(x) y^a y'^b y''^c = 0, a polynomial in y'' of any degree. The caller supplies the
pattern (a, b, c) of the monomials and, at each step's start x0, the Taylor coefficients of every A_g about x0 (a jet). The
library knows nothing of any one problem.

```text
Scalar            + - * /, neg, zero, one, from_f64, from_dd, mulf   (f64, DD, QD, OD, and Fl<T, 1> for any lane T)
Real: Scalar      to_f64, EPS                                         (f64, DD, QD, OD)
Coefficients<T>   pattern() -> Vec<(a, b, c)>;  jets(x0, n, out)      the caller's side: A_g(x0 + h) = sum_j out[g][j] h^j
taylor_shift      the jet of a polynomial in x about x0, in the scalar's precision
Recursion<T>      new(pattern, kt); form(jets, l, y0, ..) -> Series; a0_series(n)
Series<T>         c[f][k] (f = y, y', y''; k = 0..=kt) in s = (x - x0)/l, l a power of two; a0 = dN/dy'' at order 0
WalkOpts          plan (kt, tol, hmax), branch Project | Conserve, norm Rel | Abs, h_scale, tiny, max_steps, pivot_abs, drift_tol
Walker<T, S>      new(src, x0, y0, opts); form(); planned(); advance(h, target); run(x1, checkpoints) -> WalkOut<T>
WalkOut<T>        x, y, steps, stop, checkpoints, crossings, zero, n_rel_max
Stop              End | Pivot | ZeroPivot | Drift | NonFinite | Tiny | StepLimit
```

What it does, in the words of the issue:

- **Order by order.** Order k of N is set to zero and solved for y''_k, which enters linearly with the factor
  A0 = dN/dy'' at the step's start: one division per step. Order 0 of N is not imposed, so N is constant along the flow.
- **Branch by continuity.** The branch is chosen once, by the data (y, y', y'') at the start. After that the state is carried
  and never re-selected by an order among the roots. `Project` makes one Newton correction of y'' at each step's start;
  `Conserve` makes none. `Drift` stops a walk whose |N| / sum |terms| at a step's start exceeds `drift_tol`.
- **Where dN/dy'' vanishes.** `ZeroPivot`: A0 = 0 at a step's start (no division by zero). `Pivot`: |A0| <= `pivot_abs`, with
  an estimate of the zero: for A0 ~ c (x* - x)^beta, beta = 1 / (1 - rho), rho = A0 A0'' / A0'^2, x* = x - beta A0 / A0' from
  orders 0 to 2 of A0's series (exact for a pure power; an estimate otherwise, and the planted cases below are pure powers).
  `crossings`: a sign change of A0 between two step starts means the branch passes a double root with its analytic
  continuation intact; the zero of A0's series inside the step is reported.
- **Step.** `taylor::step_from_norms` (the planner of PR #70's refactor, copied verbatim, `step_size` unchanged in bits)
  on the largest coefficient of orders kt - 1 and kt; `Rel` divides each field by |c_0| (1 if zero), as #184's walker does.
  The step variable s = (x - x0)/l with l a power of two near the last step (as #184), so coefficients do not overflow.
- **Controls** (feature `mutate`, `control::ImplicitControl`): `SkipOrder(k)`, `RecipDD`, `NoPivotCheck`, `NoCrossing`,
  `ExponentHalf`, `NoPivotStop`; and, in the tests without a hook, `wrong_start` and `switch_mid`.

Scalar overlap with PR #70 (`plane::Real`): this module has its own small trait; unify after #70 merges (reported to the
coordinator).

## Planted cases (`tests/implicit.rs`; criteria written here first)

Settings for every case: Taylor order and tolerance per lane, `Plan { kt, tol, hmax }`, `Rel`, from x = 0 unless stated.

| lane | eps (unit roundoff) | tol | kt = `Plan::optimal_kt(tol)` | bar = 1e6 eps |
|---|---|---|---|---|
| f64 | 1.1e-16 | 1e-14 | 22 | 1.1e-10 |
| dd | 1.2e-32 | 1e-30 | 42 | 1.2e-26 |
| qd | 1.5e-64 | 1e-62 | 80 | 1.5e-58 |

Each case runs in each lane and in both branch modes (`Project`, `Conserve`).

**The equations and their closed forms** (all share no code with the recursion; closed forms use multidouble's `exp`, `sqrt`,
`sin`, `cos` in the lane, `f64` std for f64). With E = exp(x^2/2), E' = exp(-x^2/2), s = y + x y':

- **Q** (quadratic): N1 = y''^2 - s^2 = y''^2 - y^2 - 2 x y y' - x^2 y'^2. Data y(0) = 1, y'(0) = 0.
  - Q-A: y''(0) = +1, y = E, y' = x E, y'' = (1 + x^2) E. A0 = 2 y'' > 0: no zero.
  - Q-B: y''(0) = -1, y = E', y' = -x E', y'' = (x^2 - 1) E'. A0 = 2 y'' vanishes at x = 1: a double root, the branch continues.
- **K** (cubic, three real roots +-s, 2y): N3 = N1 (y'' - 2 y), eight monomials. Branches Q-A, Q-B and
  K-C: y''(0) = +2, y = cosh(sqrt2 x), y' = sqrt2 sinh(sqrt2 x), y'' = 2 cosh(sqrt2 x). Roots meet on the branch at
  K-A: x = 1; K-B: x = 1 and sqrt3; K-C: the root of u tanh u = 1, u = sqrt2 x (found in the test by Newton in the lane).
- **R** (quartic, four real roots +-s, +-2y): N4 = N1 (y''^2 - 4 y^2), seven monomials. Branches R-A, R-B, R-C as K-A, K-B, K-C and R-D:
  y''(0) = -2, y = cos(sqrt2 x), y' = -sqrt2 sin(sqrt2 x), y'' = -2 cos(sqrt2 x). Only the trajectory of R-D is checked.
- **F1** (a fold, exponent 1/2): N = 16 y''^2 + 4 y'^2 + 225 x + 25 x^3, from x0 = -1 with (y, y', y'') = (1, -5/2, 15/4):
  y = (-x)^(5/2), y'' = (15/4) (-x)^(1/2), A0 = 32 y'' = 120 (-x)^(1/2) vanishes at x* = 0.
- **F2** (a fold, exponent 1): N = 3 y' + 2 y''^3, from x0 = -1 with (y, y', y'') = (4/15, -2/3, 1): y = (4/15) (-x)^(5/2),
  y' = -(2/3) (-x)^(3/2), y'' = (-x)^(1/2), A0 = 6 y''^2 = 6 (-x) vanishes at x* = 0 (data formed in the lane from integers).
- **Z** (zero pivot): N1 from x0 = 1 with (1, -1, 0), where y'' = 0 = s and A0 = 0 exactly.

**Checks** (each is a pass criterion; err = max_f |computed_f - exact_f| / max_f |exact_f| over (y, y', y'')):

| name | what | cases | criterion |
|---|---|---|---|
| `coeffs` | the series' coefficients c_k, k <= kt, against the Taylor coefficients of the closed form about x0 = 0.7 (the product of the series of exp(x0 h) and exp(h^2/2) etc.), unscaled | Q-A | relative error of every c_k, f in (y, y', y''): <= bar |
| `closed_form` | the walk to x = 3, landing on 0.5, 1.5 and 3, hmax 0.3 | Q-A, Q-B, K-A, K-B, K-C, R-A, R-B, R-C, R-D | err <= bar at every landing, and n_rel_max <= bar |
| `crossings` | the sign changes of A0 and where the series puts the zero | Q-B {1}; K-A {1}; K-B {1, sqrt3}; K-C {x_C}; R-A {1}; R-B {1, sqrt3}; R-C {x_C} | the count equals the list's, and every position within bar of the exact one |
| `fold` | the walk stops at `Stop::Pivot` with `pivot_abs` = 1e-4 (F1) and 1e-9 (F2), from x0 = -1, planner-limited (hmax 1), and the estimate of x* = 0 | F1, F2 | stop is Pivot, x_last < 0, and \|x_zero\| <= 1e-3 (-x_last) (a trivial estimate x_zero = x_last misses by the full distance) |
| `zero_pivot` | `form` at (1, -1, 0) | Z | `Stop::ZeroPivot` at x = 1, no NaN in the output |
| `planner` | `planned()` equals `h_scale l step_from_norms(...)` from the formed series, at five steps of F1 | F1 | bitwise |
| `lanes` | the series of `Recursion<Fl<DV, 1>>` against `Recursion<DD>` at Q-A and K-C from x0 = 0.7; a dual lane (`Fl<Du, 1>`) value part equals the DV lane's | Q-A, K-C | every coefficient within 1e2 eps_dd; the dual lane's value part within 1e2 eps_dd |

The nine closed-form cases x 3 lanes x 2 modes are 54 cells of `closed_form`. A cell that is not met is a result.

**Controls**, each run once on the cells it names (declared in an amendment after the development run, with what each does
computed first; the names and the predicted target are fixed here):

| control | what it changes | predicted target |
|---|---|---|
| `SkipOrder(3)` | y''_3 left zero (N then drifts) | `coeffs`, `closed_form` in every lane |
| `RecipDD` | 1/k and 1/A0 rounded to double-double | `coeffs` and `closed_form` in qd only (a no-op in f64 and dd) |
| `NoPivotCheck` | A0 = 0 not tested before the division | `zero_pivot` |
| `NoCrossing` | A0's sign not compared | `crossings` |
| `ExponentHalf` | the zero estimate with beta = 1/2 fixed | `fold` on F2 only |
| `NoPivotStop` | `pivot_abs` ignored | `fold` |
| `wrong_start` (test) | K-A with the start y''(0) = -1 (K-B's root) | `closed_form` on K-A |
| `switch_mid` (test) | K-A walked to x = 0.6, then y'' replaced by 2y (K-C's root), walked on | `closed_form` on K-A |
| `skip_landing` (test) | the closed form compared at x = 1.5 with y'' of the other root | the comparison itself (the check can fail) |

## The crate switch (#167's `notes/warp/conical_global/`)

- Cargo feature `implicit_lib` (default off). With it, `poly::implicit_taylor` (lane `Fl<T, 1>`, used by `walk` and by the
  matching with duals) and `hp::taylor_p` and `hp::hp_walk` (scalar `Sc<P>`, with the locator's hooks) call
  `multishoot::implicit`; without it the code is #183's, byte for byte. `Cargo.toml` takes multishoot from the PR branch by
  a git `rev` (on the remote, never a local path); the lock file is committed.
- **Criteria**, each for the feature on, against the feature off (both built here, same machine, `--bin` forwarded):
  1. both build; no absolute path in `Cargo.toml`.
  2. `python3 notes/warp/conical_global.py` (checks and controls, default): same exit code 0, same label of each check
     (PASS, NOT MET as in #183), every control FIRED on the same targets.
  3. `python3 notes/warp/conical_loglog.py` (default): 20 of 20 checks, 17 of 17 controls on target only.
  4. `python3 notes/warp/conical_offgrid.py --grid=ctl --no-controls --dump=DIR` (all 16 checks on the `ctl` grid: 31 points
     F_inf in {0.01, 0.1, 1, 4, 16} x C in {-1e8, -1e5, -1e4, 0, 1e4, 1e5, 1e8} with |C| <= 1e8 |F_inf| or |F_inf| >= 0.25, the
     mirrors, and the line of F_inf = 0.1): 16 of 16; and `--controls=n-drift,recip-dd` (the two that touch the recursion).
  5. **Same eta* and kinds to the printed digits**: in the `ctl` verdict records (`dump`), every class and kind equal and every
     eta* equal as printed (the output prints 10 significant digits); in the two other outputs, every eta*, class and kind
     printed on a line equal as a string. Numbers that measure an error (a residual, a difference, a bar) are not compared as
     strings: each is held to its own check's bar. Step counts, timings and error sizes that differ are listed, not gated.
     A difference in any eta*, class or kind is reported as not met with the line, the cause not guessed.
- The baseline (feature off) is run first and kept; the comparison script `compare_outputs.py` (in this folder) is written
  after the baseline and before the first run with the feature on, from the baseline's lines.
- Timings are reported with the machine, load and thread count (2 threads, nice 10, load at the start).

## Run protocol

- `cargo build -j 2`, `cargo test --release -j 2 -- --test-threads=2`, one at a time, logs `dev_NN_*` and `run_NN_*`.
- Backends: default (aarch64 NEON) and `--features portable`: the same tests, and a digest of every planted result (printed
  bits) compared across the two. `+avx2,+fma` was not run (no x86 machine).
- `cargo fmt` (max width 120), `cargo clippy --all-targets --features mutate -- -D warnings` and with `portable,mutate`.
- Stop condition: any single run not finished in 1 h of wall time is stopped and reported with what finished.

## Development log and amendments

Nothing above this heading has been edited. The development runs are `dev_01_implicit` (the first run of
`tests/implicit.rs`; its tests stopped at the first unmet cell) and `dev_02_implicit` (every cell run before the assertion;
the same code). Both are kept; both were run with `--features mutate` at multishoot's working tree on `feat/implicit-taylor`
(uncommitted at the time), release build, 2 threads, nice 10, load 0.6.

### D1 What the development run shows (reported to the coordinator before any change)

| cell | verdict | number |
|---|---|---|
| `closed_form`, branch mode `Project`, all 9 branches, 3 lanes (27 cells) | met | worst err 1.9e-31 dd, 2.2e-15 f64, 1.1e-63 qd (bars 1.2e-26, 1.1e-10, 1.5e-58) |
| `crossings`, `Project`, 7 branches, 3 lanes (21 cells) | met | worst position error 7.8e-14 f64, 2.3e-30 dd, 2.3e-62 qd |
| `fold` F1, F2, `Project`, 3 lanes (6 cells) | met | \|x_zero\| / (-x_last) <= 2.5e-33 dd, F2 1e-22 (the estimate is exact for a pure power) |
| `closed_form`, `Conserve`: Q-A, Q-B, K-A, K-C, R-A, R-C | met | worst 3.5e-14 f64, 4.1e-30 dd, 6.1e-63 qd |
| `closed_form` and `crossings`, `Conserve`: **K-B, R-B, R-D**, every lane | **NOT MET** (9 cells each) | stop `Tiny` after 26 to 115 steps; err 7.4e-8 f64, 1.6e-18 dd, 3.2e-50 qd on K-B; one of two crossings found |
| `fold` F1 `Conserve`, f64 | **NOT MET** | \|x_zero\| 5.7e-15 against 1e-3 (-x_last) = 6.3e-16 (dd, qd met) |
| `coeffs` (l = 1 and 1/4), every lane | **NOT MET as worded** | relative error of c_k 4.9e-8 f64 (k <= 22), 1.5e-11 dd (k <= 42), 1.5e-14 qd (k <= 80) |
| `zero_pivot`, `planner`, `lanes`, the three hook-free controls | met | `planner` bitwise at 5 steps; `lanes` equal to dd bit for bit (0.0 difference) |

Causes (computed, not assumed):

- `coeffs`: the relative error of c_k grows by a factor 2 to 5 per order (`dbg_coeffs`, f64: 1.5e-16 at k = 3, 5.8e-14 at
  k = 9, 3e-11 at k = 17, 4.9e-8 at k = 22). Order k of N is s^2_k minus a convolution of the y'' coefficients, and for a
  function whose coefficients fall off super-exponentially the convolution terms exceed c_k (by about C(k, k/2)^(1/2)), so
  c_k has an absolute error of about eps |c_0| and a relative one that grows. The check as worded asks for what the
  recursion cannot give. The error that enters a step is |dc_k| |s|^k <= eps |c_0| at |s| <= 1, and the walks' errors
  (closed_form) are at roundoff.
- `Conserve` through a double root (K-B at x = 1 and sqrt 3, R-B likewise, R-D at y = 0): N is conserved at its start
  value, a rounding eps, not at 0. For N = eps the double root is two roots, at distance sqrt(eps) from the crossing the
  analytic branch of N = 0 becomes an avoided crossing (or a fold), and the Taylor series about a point at distance d has
  radius about d: the planner's steps shrink to the crossing and the walk stops with `Tiny`. `Project` sets N = 0 at each
  step's start and crosses freely. Q-B, K-A, R-A, K-C, R-C meet it in `Conserve` (the sign of the start residual is
  favorable, or the crossing is with a root that N = eps does not avoid).
- f64 F1 `Conserve`: N drifts by about eps (sum of |terms| = 250) per step over 84 steps, and a drift dN moves the fold of
  N = const by dN / (dN/dx) = dN / 225; 5.7e-15 is that shift.

Proposals made to the coordinator (not applied): `coeffs` reworded to |dc_fk| <= 1e6 eps max_g |c_g0| for all k and f;
the `Conserve` cells of K-B, R-B, R-D and f64 F1 reported as NOT MET, the criteria left as written, and a documented
statement that `Conserve` is not for branches that meet a double root (K-B stays in the table).

### A1 Rulings of the coordinator on D1 (hc, t2x, after `dev_01` and `dev_02`; the text above D1 is not changed)

1. **`coeffs` stays as worded and is NOT MET in every lane.** The growth of the relative error of c_k by a factor of
   about 3 per order is a finding (cancellation in the convolution of N_k). A criterion that measures what a step uses is
   added, declared after this development run and before its first run: **`step_sum`**, at each planted path's planned
   step h, `sum_k |dc_k| h^k <= 1e6 eps sum_k |c_k| h^k` for each of y, y', y'' (k = 0..kt, the sums in the step variable
   with s = h / l; dc_k = the recursion's c_k minus the closed form's Taylor coefficient). The recursion is started from
   the closed form's state at the step's start, so that the path's accumulated error does not enter. The paths and steps:
   the nine branches of `closed_form` in `Project` mode (steps as the walk takes them, h = `planned()` before the landing
   rule, hmax 0.3) and F1 and F2 from x = -1 (hmax 1, pivot_abs 1e-4 and 1e-9, until the stop). The bar is not "versus
   max |c_0|": that is loose for the high orders, whose c_k are small. Gated.
2. **The double-root criterion stays as written.** `Conserve` on K-B, R-B and R-D (9 cells over the lanes; also their
   `crossings` cells) is NOT MET: `Conserve` turns a crossing into an avoided crossing, because N = eps splits the double
   root, and `Project` crosses. Not restricted. The library's docs and the PR state it as a property of the mode (use
   `Project` near a double root of N in y''). The test file prints these cells as `(recorded, not gated)` with
   `[NOT MET]` or `[met]`; the passing cells of the other branches are gated.
3. **f64 F1 `Conserve` fold estimate is NOT MET** (5.7e-15 against 6.3e-16), N's drift moving the fold; dd and qd stand.
   Printed as recorded, not gated.

Controls: the targets are declared after the development run that has `step_sum` (`dev_03_implicit`), from its table.
`coeffs` is no target of any control (it is NOT MET without one).

### A2 Control targets, declared after `dev_03_implicit` (the run that has `step_sum`) and before the next run

`dev_03_implicit` ran every check once with each control (the table in its log: `control ... FIRED/SILENT`); from it the
targets below are declared. They are asserted by `controls_f64`, `controls_dd`, `controls_qd` in `tests/implicit.rs`
(a control must fail exactly its row and no other check). The checks of a row: `step_sum` K-A, `closed_form` K-A and R-D
on `Project`, `crossings` K-B `Project`, `fold` F1 and F2 `Project`, `zero_pivot`. `coeffs` is no target (NOT MET without a
control). The first table of `dev_01` used R-D `Conserve` among its cells, a recorded NOT MET cell, so its "FIRED" lines
for the controls that change nothing there were not controls' effects; this table uses gated cells only.

| control | fails (every lane unless stated) | silent on | what dev_03 showed |
|---|---|---|---|
| `SkipOrder(3)` | step_sum, closed_form, crossings, fold F1, fold F2 | zero_pivot | step_sum ratio 8.1e31 dd, 9.0e15 f64, 6.7e63 qd (bar 1e6) |
| `RecipDD` | in quad-double: step_sum, closed_form, crossings | fold F1, F2, zero_pivot; in f64 and dd everything | step_sum ratio 2.5e33 qd, against 4.9e2 (dd) and 6.2e2 (f64) with it |
| `NoPivotCheck` | zero_pivot (stop `NonFinite` in place of `ZeroPivot`) | the rest | |
| `NoCrossing` | crossings (0 of 2 found) | the rest | |
| `ExponentHalf` | fold F2 (estimate off by R / 2 at exponent 1) | fold F1 (exponent 1/2 is the mutated value), the rest | |
| `NoPivotStop` | fold F1, fold F2 (walk ends `Tiny`, no estimate) | the rest | |
| `wrong_start`, `switch_mid`, `WrongForm` (no hook) | closed_form K-A | | err 1.5, 0.94 and 1e4 against a bar of 1.2e-26 (dd) |

A prediction of the README that `dev_03` did not confirm: none. A prediction that was too narrow: `SkipOrder(3)` also
fails `crossings` and the folds (N drifts, so every check that depends on the path does).
