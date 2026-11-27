# I191-rpi5: a singularity locator from Taylor coefficients, planted suite, controls and the #183 comparison (PR to multisolver)

Machine: rpi5-ubuntu (Raspberry Pi 5, 4 cores, 8 GB, aarch64), runner negative-mass-rpi5-i191, at most 2 threads, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/191 . Worktree `~/Source/negative-mass-i191`, branch
`wip/i191-singularity-locator` (base 9debda2, #183's head). Library clone `~/Source/negative-mass-i191-libs/multisolver`, branch
`feat/locate-singularity` (base main 8e699ab). Rust 1.100.0, multisolver 0.2.2, multishoot 4.2.0, multidouble 5.1.0.

This README is written before the first run of the library's tests. What is declared here (cases, orders, tolerances, criteria,
bar definition, control names and mutations) is not changed after a development run without the coordinator's agreement; the
**targets** of the controls are declared in an amendment after the development run that computes them (see "Controls").
Every log is kept in this folder, including the failed and stopped ones; reruns are numbered.

## 1. Library: multisolver, a new module `locate`

| reason | multisolver | multishoot |
|---|---|---|
| what the locator reads | a coefficient slice, nothing of a problem | same |
| the code it generalizes | `singularity` holds the root test, an f64 ratio fit without a bar and a pair recurrence of constant coefficients: the locator belongs beside them | none (`taylor` only steps) |
| dependency direction | multishoot depends on multisolver, so its Taylor stepping (#192's radius cut) can call the locator | multisolver cannot call it |
| precision | multidouble's scalars are already its dependency | same |
| CLAUDE.md | planted truth, a control per accuracy check (a test that asserts the failure), `cargo fmt`, `cargo clippy --all-targets -- -D warnings` and once with `--features portable`, bitwise across backends | the same, with the `mutate` feature |

multisolver has no `mutate` feature: its CLAUDE.md asks for controls as tests that assert the failure. The coordinator's
"with and without `mutate`" is the multishoot rule; for multisolver the commands are the ones in its CLAUDE.md. Not run on this
Pi: the `+avx2,+fma` build (said in the PR and the note). `singularity` keeps its functions (no API removed).

## 2. API

```rust
pub trait Real { const UNIT: f64; fn from_f64(f64) -> Self; fn to_f64(self) -> f64; fn sqrt(self) -> Self; /* + - * / neg */ }
// implemented for f64, DD, QD, OD (the Scalar of Double, Quad, Octo)
pub struct Opts { starts: Vec<f64>, ratio_degrees: Vec<usize>, three_term_degrees: Vec<usize>, bar_factor: f64, max_rel_bar: f64 }
pub enum Model { Ratio, ThreeTerm }          pub enum Kind { Real, Pair, Unresolved }
pub struct Singularity<T> { re: T, im: T, alpha: T, bar: f64, alpha_bar: f64 }
pub struct Location<T> { kind, model, nearest: Singularity<T>, farther: Option<Singularity<T>>, first, degree, rel_bar, skew }
pub fn locate<T: Real>(c: &[T], opts: &Opts) -> Option<Location<T>>
pub fn locate_at<T: Real>(c: &[T], model: Model, first: usize, degree: usize, opts: &Opts) -> Option<Location<T>>   // one cell, for controls
```

`c` is c_0 ... c_K of a series about u = 0 in a variable scaled so that the radius is of order one; `s = re + i im` is the
singularity in that variable, Im s >= 0, the exponent `alpha` is that of (1 - u/s)^alpha (a pole: -1, a square root: 1/2).

## 3. Method

Near the nearest singularity f ~ A (1 - u/s)^alpha, so c_k ~ s^-k k^(-alpha-1).

- **Ratio** (Domb and Sykes 1957): r_k = c_k/c_(k-1) = b_0 + b_1/k + ... + b_d/k^d, least squares over k = first ... K
  (Householder QR in the arithmetic of the coefficients). s = 1/b_0, alpha = -1 - b_1/b_0. Exact at d = 1 for a pure
  branch point or pole; real s only.
- **Three-term** (the recurrence of a conjugate pair with 1/k terms; **not** the method of Mercer and Roberts): (1 + 1/k) c_(k+1) =
  (pi_0 + ... + pi_d/k^d) c_k - (theta_0 + ... + theta_d/k^d) c_(k-1), rows scaled by their largest |c|, d >= 2. For two
  singularities of one exponent (a pair s, conj(s), or two real) the recurrence is exact with 1/s_1 + 1/s_2 = pi_0, 1/(s_1 s_2) =
  theta_0, pi_1 = -alpha pi_0, theta_1 = -(1 + 2 alpha) theta_0. The roots of z^2 - P_0 z + Q_0 (P_0 = pi_0, Q_0 = theta_0) are 1/s: complex
  roots are a pair, real roots the nearest of two real singularities and the farther one. The exponents come from the
  first-order terms (P_1 = pi_1 - pi_0, Q_1 = theta_1 - theta_0): P_1 - Q_1 z_j = g_j (z_j - z_other), alpha_j = -1 - g_j; for a pair alpha = -1 - Q_1/(2 Q_0)
  and `skew` is |Im g|, which is 0 for a pair of one exponent. A single real singularity makes it rank deficient (the fit
  returns no cell) and the ratio model serves.
- **Cells.** A cell is (first order, degree). The default grid: first = round(phi K) with phi = 0.2, 0.3, 0.4, 0.5, 0.6
  (at least 2), ratio degrees 1 ... DMAX and three-term degrees 2 ... DMAX (DMAX: see Amendment A0), a cell needs at least
  (unknowns + 3) rows.
- **Choice.** The cell whose (up to eight) neighbors in the grid, one step in first and in degree, differ least from it in s
  (relative to |s|), per model; of the two models, the smaller difference wins (the ratio model on a tie).
- **Error bar** (what it is): `bar_factor` = 2 times the largest difference of s (complex distance) or of alpha between the chosen
  cell and its neighbors, floored at 8 u |s| (alpha: 64 u max(1, |alpha|)), u = 2^(-52 parts). **It is a range of the estimator
  over its fit choices (window and degree), not an enclosure and not a bound.** It can miss where all neighboring cells share
  an error (a contamination that the windows do not reveal); the planted suite measures how often. A singularity whose bar is
  above 5% of |s| is `Kind::Unresolved` (an entire function, or no cell that fits).
- `locate_at` takes the cell by hand, its neighbors being first -+ K/10 and degree -+ 1.

### Design exploration (before the criteria)

Python and mpmath at 53, 106 and 212 bits (the lanes' precisions), scripts in `sys/explore/`. It was done on cases that are **not**
the suite below (other alphas, singularities, dressings), and chose the grid, the two models, the neighborhood rule,
`bar_factor` = 2 and the tolerances' scales. The library is a Rust port of the prototype `proto.py`; the suite runs the port.

| run | what | parameters | finding |
|---|---|---|---|
| `dev_00_explore1`, `_explore2`, `_probe` | single cases: pole, branch points, pairs (also at 1 to 11 degrees from the real axis), two real singularities, entire exp(u), log, geometric | K = 30, 60, 120; dressings exp(beta u) and 1/(1 + (u/tau)^2), tau = 3 to 6 abs(s) | exp(beta u) dressing keeps the three-term recurrence exact (a holonomic series), so the suite dresses by poles; the ratio model fails for a pair (bar 0.3 to 1), the three-term fit resolves a pair at 1 degree; an entire function has bar 1 (unresolved) |
| `dev_00_explore3` seeds 1, 2 | 90 random cases x 3 lanes (kind, alpha in -2 ... 1.5 and 1e-6, tau in 0, 3, 4, 6, sums with a farther singularity), every third noisy at delta = u^0.6 | degrees up to 5 | coverage of s 250/256 resolved cells at factor 1, 254/256 at factor 2; 14 unresolved (bar >= 5%), 13 of them f64 or alpha ~ 1e-6 with a dressing; kind right in 256/256 |
| `dev_01_degrees` | dressed cases, dd and qd, degrees up to 5, 7, 9 | tau = 3 to 6 abs(s) | error falls with the degree (see A0) |
| `dev_02_*` | the 90 cases of dev_00 again, degrees up to 9 | | A0 |
| `dev_03_noise_dressed_stopped` | noise amplification, four cases W1 to W4: reals (alpha, s, c) = (0.45, 2.2, 1.4), (-0.6, -1.9, 0.7), (2e-8, 1.8, 1), a pair (0.4, 1.0 + 1.3 i, 1.2), **dressed with tau = 1000 abs(s)**, delta = 1e-10, 1e-19, 1e-38, seeds 1, 2, 3, degrees up to 9 | stopped during W4 by the runner | **truncation, not noise:** the quad-double errors are identical for the three seeds (s 4e-21 to 1e-20, alpha 1e-19 to 1e-18, against delta 1e-38): the algebraic correction of the dressing, relative q^2 = 1e-6, is fitted to degree 9 in 1/k at k >= 24 with an error of about 1e-6 x (1/24)^10 = 1e-20; the double-double errors are 1e-14 to 1e-13 and f64's are 1e-9 to 1e-8, also above delta. A dressed case with noise cannot test noise: the weak tier of the first plan (N1, N2, O8 dressed at 1000 abs(s)) was **changed to pure plus noise, with the coordinator's agreement (hc, A2)** |
| `dev_03b_noise` | the same four cases W1 to W4, **pure** (no dressing), same noise, seeds, degrees | | error of s at most 0.14 delta (singles) and 2.5 delta (the pair), of alpha at most 6.6 delta and 127 delta, in every lane and seed (the chosen cell is a low-degree one at the window's start) |

At factor 1 the bar's misses had a bar of exactly 0 (a rounding-level error that all neighbors reproduce), which the floor of the bar
prevents (8 u abs(s), 64 u max(1, abs(alpha))).

## 4. Planted suite

Lanes (f64, double-double, quad-double): orders K = 30, 60, 120; u = 2^-52, 2^-104, 2^-208; noise delta = 1e-10, 1e-19, 1e-38.
A part is c (1 - u/s)^alpha (a conjugate pair of parts, 2 Re of one, when Im s > 0), coefficients from c_k = c_(k-1)(k-1-alpha)/(k s) in the
lane's arithmetic. Dressed: multiplied by 1/(1 + (u/tau)^2) (poles at +- i tau), tau = 4|s| or 1000|s| (weak). The alphas
1/3 and 1e-8 are the f64 numbers nearest to them, in every lane. The nearest singularity is the first part.

| case | parts (c, alpha, s) | dressing | noise | kind |
|---|---|---|---|---|
| P1 to P6 | (1.7, -1, 2), (-0.8, -2, -1.5), (1.3, 1/2, 2.5), (0.9, -1/2, -1.75), (2.2, 1/3, 1.25), (1.1, 1e-8, 2) | none | none | Real |
| D1 to D6 | the six of P | tau = 4 abs(s) | none | Real |
| C1, C2, C3 | pairs (1.7, -1, 1+1.25i), (1.3, 1/2, 0.9+1.4i), (1.1, -1/2, 1.59+0.16i) (C3 at 5.7 degrees from the real axis) | none | none | Pair |
| C4, C5 | C1, C2 | tau = 4 abs(s) | none | Pair |
| T1 | (1, 1/2, 2) and (1, -1/2, -2.8) | none | none | Real |
| T2 | (1, 1/2, 2) and (1, -1/2, 2.8) | none | none | Real |
| T3 | (1, -1, 2) and (1, -1, 3) | none | none | Real |
| N1 | the part of P3 | none | delta | Real |
| N2 | the pair of C2 | none | delta | Pair |
| O8 | the part of P6, (1.1, 1e-8, 2) | none | delta in dd and qd, none in f64 | Real |
| N3 (reported, not gated) | the part of D3 | tau = 4 abs(s) | delta | Real |

23 gated cases x 3 lanes = 69 gated cells, and N3's 3 rows printed (the interplay of truncation and noise; coordinator's condition, A2). The cases P, D, C, T, N, O8 cover: the pole and the double pole, branch points of alpha 1/2, -1/2, 1/3 and
1e-8 (the regime of #183's O8), a conjugate pair (also near the real axis), a nearest singularity with a farther one of equal
amplitude behind it (on the other side, on the same side, and two poles), the coefficient noise of #634's question.
The orders are the same in every cell of a lane; no cell is run at another K.

**Criteria** (the doc comment of `tests/locate.rs` states them in the same words; each cell). Errors: s relative to |s|, alpha absolute.

1. the kind is the table's;
2. error of s <= `tol_s` and of alpha <= `tol_alpha`:

| tier | cases | tol_s | tol_alpha |
|---|---|---|---|
| pure single | P1-P6 | 1e4 u | 1e6 u |
| pure pair, two poles | C1-C3, T3 | 1e5 u | 1e7 u |
| dressed (and the two-singularity sums T1, T2) | D1-D6, C4, C5, T1, T2 | 1e-2 (f64), 1e-6 (dd), 1e-9 (qd) | 0.1, 1e-4, 1e-7 |
| noisy, single | N1, O8 | max(2 delta, 1e4 u) | max(70 delta, 1e6 u) |
| noisy, pair | N2 | max(30 delta, 1e5 u) | max(1300 delta, 1e7 u) |

   (delta = 0 where a cell has no noise); and for O8 the error of alpha <= 1e-9 (a tenth of alpha) in every lane;
3. the error of s <= its bar and the error of alpha <= its bar (**coverage**, factor 1);
4. the bar of s over |s| <= 100 tol_s and the bar of alpha <= 100 tol_alpha (**useful**, not vacuous: within two orders of the tolerance).

Where the tolerances come from: the pure ones are about 1e4 to 1e6 above the rounding errors of the pure planted cells in the exploration
(f64: s 2e-16 and alpha 2e-15); the dressed ones are 10 to 100 times the worst errors of the exploration's product-dressed
cases at q = |s|/tau = 0.25 to 0.43 (f64: s 1e-3, alpha 5e-2; dd: s 1.4e-8, alpha 3.7e-6; qd: s 2e-15 with degrees up to 9);
the noisy ones are **ten times the largest amplification of the noise measured in dev_03b** (below), rounded up:
single singularity, s 0.14 delta and alpha 6.6 delta, so 2 delta and 70 delta; pair, s 2.5 delta and alpha 127 delta, so 30 delta
and 1300 delta (a priori: the relative error of a ratio is the difference of two noises of the neighboring orders, so
the low-frequency content that the intercept of the fit reads is small, of the order of delta over the window's length; the
slope, which carries alpha, reads K/sqrt(n) times more). The measured numbers are not the tolerances. A cell that
fails is a result: reported, the criterion not loosened.

Reported, not gated, in every cell: the chosen model, first order and degree, `skew`, and for T1 to T3 the farther singularity's
error and bar.

## 5. Controls (names and mutations now; targets after the development run)

Each control feeds a check of the table a wrong input and the check must fail; each runs on every cell it names after its effect
was computed in a development run (CLAUDE.md of multisolver: "run once to see it fire"; "a control silent on its named target is a result").

| control | wrong input | check it must fail |
|---|---|---|
| `wrong-sigma` | the nearest singularity planted at s (1 + 10 tol_s) (the pair at the modulus scaled alike) and checked against s | 2 |
| `wrong-alpha` | the nearest singularity planted at alpha + 10 tol_alpha, checked against alpha | 2 |
| `pair-by-ratio` | a pair's series fed to the ratio model by `locate_at(Model::Ratio, ...)` | 1 and 2 |
| `bar-shrunk` | the bars multiplied by 1e-3 | 3 |
| `window-early` | `locate_at` with first = 2, degree 2, ratio model, on a case with a farther singularity | 2 |
| `window-short` | `locate_at` with the last 8 orders (first = K - 7), degree 2, ratio model, on a noisy case | 2 |

The window controls name their planted cases after the development run computes them (a window that is "too early" or "too short"
must fail on a stated planted case); the cases are chosen among those of the table, and the choice, with the numbers that led to it,
is declared in the amendment. A control that is silent on its target is reported as silent and not repaired by a stronger mutation
without the coordinator's agreement. The unit tests of the arithmetic (`lstsq` on a planted polynomial) each have one control.
The bitwise check across backends (a fingerprint of the result bits of the suite) has a control that flips one input ulp.

## 6. Comparison with #183 (reported, not gated)

#183's raw folder keeps no Taylor coefficients: its records (`dump_run_03a/offgrid_*.jsonl`) keep the last step's x and state in
double-double (`x_last`, `s_last`), `xstar`, `bar`, the fitted `est` and `alpha_pred` = 2/(eta*^2 + 4). The series is regenerated by
#183's `hp::taylor_p` in double-double (`kt` = 30, as the walk) about `x_last` from `s_last`, in the step variable s = (x - x_last)/l,
l = 2^round(log2 est.r): the series #183's locator read at its last step. A harness outside the repository (`sys/compare183/`, a cargo
package with path dependencies on the worktree's `conical_global` and on the multisolver branch; nothing in #183's crate is edited)
runs the new locator on each of the three fields (F, F', F'': field f has exponent alpha - f) at: the 20 points of O8's failure in
`dev_07` (all `F->0`, eta* >= 5.7e3, alpha ~ 1e-8), ten other `F->0` points over eta* from 1 to 100, and six `a3->0` points
(the kappa-curve stops, which #183's A1 read as a complex pair near the real axis). Per point: eta* = x_last + l Re s (and
Im s), the exponent alpha (F) = alpha_field + f with its bar, the kind, against #183's `xstar`, its bar, its fitted exponent and
`alpha_pred`. The driver is `notes/warp/singularity_locator.py`, its output `notes/warp/singularity_locator_output.txt`.

## 7. Runs

Units (systemd, nice 10, one at a time): `nm-i191-dev00` (exploration rerun), `nm-i191-dev02` (degrees up to 9), `nm-i191-dev03` (stopped,
A2), `nm-i191-dev03b`, `nm-i191-build183`, `-build183b`, `-build183c` (the harness's builds). Tests and clippy ran in the terminal (each test run under 10 s,
builds up to 2 min). Logs in this folder, none overwritten:

| log | what |
|---|---|
| `dev_00_*`, `dev_01_degrees`, `dev_02_*`, `dev_03_noise_dressed_stopped`, `dev_03b_noise` | design exploration (section 3); scripts in `sys/explore/`, launchers `sys/run_dev0*.sh` |
| `dev_04_build_compare183`, `dev_05_*` | the harness's first build, its first probe (the id collision of A1) and the check of one record |
| `dev_10_planted_first.log`, `dev_10_lstsq_unit.log` | the first run of the suite (68 of 69 gated cells meet 1 to 4; D6 f64 not met, A4) and of the `lstsq` unit test |
| `dev_11_controls.log` | the controls' development run (A3) |
| `dev_12_locate_*`, `dev_13_locate_*` | the fingerprint's first run (control silent, A5) and its rerun, default and portable |
| `dev_14_clippy_*`, `dev_14b_clippy_*` | clippy before and after the fixes (A6) |
| `dev_15`, `dev_16`, `dev_17` | the harness's rebuild and two driver runs before the record (a crash on a missing `alpha_pred`, then the ulp column) |
| **`run_01_*`** | **run of record** of the library at multisolver 0db3966 (`run_01_commit.txt`): the locate tests, the unit test and the doc test in the default build and with `--features portable` (exit 0, the same fingerprint 0xa5113e9ccb6776c8), and the controls' development printer again (identical to dev_11) |
| **`run_02_*`** | **run of record** of the comparison with #183: the harness built at 0db3966 (`run_02_build_compare183.log`), the driver's stdout (`run_02_compare183.log`, the same as `notes/warp/singularity_locator_output.txt`), its exit code |

Scripts in `sys/`: `explore/` (the python prototype and the exploration), `compare183/` (the harness, a cargo package), `build_compare183.sh`, `run_dev0*.sh`.

## Amendments

**A0 (before any run of the library's tests): DMAX = 9** (the default grid: ratio degrees 1 to 9, three-term degrees 2 to 9, in every
lane). `dev_01_degrees.log`: on the exploration's product-dressed cases the error of s falls with the degree in double-double (the
three-term pair X6: 1.4e-8 at degree 5, 4.1e-10 at 7, 8.8e-12 at 9) and in quad-double (the ratio case X1: 1.8e-10, 1.2e-13, 1.9e-15).
`dev_02_*` (the 90 random cells of dev_00 again, degrees up to 9; `dev_02_analyze2.log`): at `bar_factor` 2 the bar covers 254 of the
256 resolved cells for s (the two misses have a bar of exactly 0; the floor of the bar is the cure) and 256 for alpha, the kind is
right in 256 of 256, the median error is 5.8e-14 in double-double (3.4e-11 at degree 5) and 2.7e-21 in quad-double (2.1e-16).
The tolerances above were written with these figures in view.

**A1 (before any run of the library's tests): the driver's id.** `notes/warp/singularity_locator.py` keyed its results by
(F_inf, C) and #183's dump holds four to eight records of one point (first pass, pass of record, double- and quad-double runs), so
a result could be shown beside another record's #183 values; the first probe (`dev_05_compare183_probe.log`) showed 20% off in eta* on
one record. The id now carries the file and the line. Checked directly on that record (the first pass, R = 1.1e-4, `dev_05_firstpass_record.out`):
the locator gives s = -0.9015624526 on all three fields, eta* = 11547.002498558373, the value #183 stored, and alpha(F) = 1.500000704606e-8
against alpha_pred 1.5000007046060564e-8.

**A2 (before any run of the library's tests): the noise tier.** dev_03 (the weak tier of the first plan, dressed at 1000 abs(s), plus
noise) showed truncation, not noise, in every lane (table above). The coordinator agreed (hc, 2026-11-26) that N1, N2 and O8 become the
pure series P3, C2 and P6 plus noise, and set three conditions, all met here: (1) the tolerances are set before the first library
run, from an a-priori argument where one exists and else from dev_03b with a margin of 10 over the measured amplification, never at
the measured value (section 4, "Where the tolerances come from"); (2) one dressed case with noise, N3 = D3 plus noise, is printed and
**not gated**; (3) dev_03 and dev_03b are recorded above, with their parameters, before the criteria. D1 to D6, C4 and C5 are unchanged.

**A3 (after dev_11, `dev_11_controls.log`; before the run of record): the controls' targets**, computed from the development run and declared
here (`controls_fire` in `tests/locate.rs` asserts them):

| control | check | target | development run |
|---|---|---|---|
| `wrong-sigma` | 2 | all 72 cells (24 cases x 3 lanes) | fires in 72 of 72 |
| `wrong-alpha` | 2 | all 72 cells | fires in 72 of 72 |
| `pair-by-ratio` | 1 and 2 | the 18 cells of C1 to C5 and N2 | fires in 18 of 18 (kind Unresolved, s off by 0.7 to 2.6) |
| `bar-shrunk` (bars x 1e-3) | 3 | every cell except ten | **silent in ten cells**, reported as silent: P1 in f64 and double-double (the error is 0), D1, D2, C4 in double-double and quad-double, T1 and T2 in quad-double (the error is at least a thousand times below the bar); fires in the other 62 |
| `window-early` (ratio model, first order 2, degree 2) | 2 | **T1, T2 and T3 in the three lanes** (9 cells), cases with a farther singularity | fires on them; also on C1 to C5, N2, N3, D1, D3 to D6 in every lane and on D2 in dd and qd (47 of 72); silent on P1 to P6, N1, O8 (the ratio model is exact there) and on D2 in f64 |
| `window-short` (ratio model, the last 8 orders, degree 2) | 2 | **N1, N2 and T3 in the three lanes** (9 cells): the noisy and the two-pole cases | fires on them; also on C1 to C5, D6 and in places on D2 to D5, N3, O8, T1, T2 (42 of 72); silent on P1 to P6 and D1 |

A window that starts too early (first order 2) fails on the planted two-singularity cases and one that is too short (8 orders) fails
on the noisy ones, as the issue asks.

**A4 (after dev_10, `dev_10_planted_first.log`): D6 in f64 is NOT MET.** The first run of the suite: 68 of the 69 gated cells meet criteria 1 to 4.
D6 (alpha = 1e-8, s = 2, dressed with poles at +-8i) in f64 (K = 30) does not meet criteria 1, 2 and 4: kind `Unresolved` (bar 1.1 of |s|), error of s
0.41, error of alpha 12; criterion 3 **holds**: the bar covers the errors, and the locator says `Unresolved`, so it gives no confident wrong
answer. Cause: the dressing's coefficients (1/64)^(k/2) swamp the alpha-sized coefficients of the singular part (1e-8 2^-k/k) up to order about 16; the
contamination decays like 4^-k, and the default windows start at 0.2 to 0.6 K = 6 to 18, so none starts where the data are clean (about order 24 of 30, i.e. 0.8 K, with 7
rows and degree at most 3), which the default grid does not contain. A window starting near 0.8 K would resolve this regime; it is not implemented. D6 in dd and qd
meet all four criteria. The coordinator (hc, 2026-11-26): leave it NOT MET, change neither the cases nor the tolerances nor the grid, report it with the cause. The test
`planted_suite` asserts the 68 cells and names D6 f64 as excepted; `d6_f64_is_not_met` records what the locator does there (the failures 1, 2 and 4, the kind
`Unresolved`, the bar above 5%); neither makes the cell meet its criteria.

**A5 (after dev_12): the fingerprint control.** The bitwise check across backends (`bitwise_across_backends`: FNV-1a of the results of every cell,
constant 0xa5113e9ccb6776c8 from the default build on aarch64) has the control "one f64 coefficient changed in its lowest bit changes the fingerprint". As first coded
(coefficient 10 of P1) it was **silent** (`dev_12_locate_default.log`, "control did not fire": a pure pole's results do not move by one ulp of one coefficient). The same
one-ulp mutation at coefficient 20 of D3 (f64) fires, and is the control of record. The check (the fingerprint against the constant) did not change. Both
backends gave the constant: default 0xa5113e9ccb6776c8, `--features portable` 0xa5113e9ccb6776c8 (`dev_13_locate_*.log`).

**A6 (tooling): rustfmt and clippy.** The Pi's stable toolchain had neither. The coordinator allowed (hc, 2026-11-26) `rustup component add rustfmt clippy`
(toolchain components, nothing else); run as `rustup component add rustfmt clippy --toolchain stable`; versions: rustfmt 1.11.0-stable (0ef1bc3860 2026-11-09), clippy
0.1.100 (0ef1bc3860 2026-11-09), rustc 1.100.0. `cargo fmt` (width 120) then `cargo clippy --all-targets -j 1 -- -D warnings` in the default build and with `--features portable`:
the first pass (`dev_14_clippy_*.log`) reported one lint in `src/locate.rs` (an indexed loop in `spread`) and two kinds in the tests (negated float comparisons,
a lazy `then`), all fixed without changing a result; the second pass (`dev_14b_clippy_*.log`) is clean in both builds. The `+avx2,+fma` build was **not run** (no x86 here); the
default build is aarch64 NEON, and `--features portable` was run. multisolver has no `mutate` feature.

**A7 (the pull request).** https://github.com/nmoinvaz/multisolver/pull/26 (branch `feat/locate-singularity`, commits a2d767e and 0db3966 on main 8e699ab, label
`enhancement`). Its CI (x86 SSE2, AVX2, portable and MSRV 1.89 on Ubuntu, NEON on Ubuntu and macOS, Windows MSVC, rustfmt, clippy on SSE2, portable and NEON, docs, coverage) passed at
the time of the closing comment; the fingerprint test (`bitwise_across_backends`) is asserted in each test job, so the x86 and Windows jobs agree with the Pi's constant
0xa5113e9ccb6776c8: the `+avx2,+fma` build was not run on the Pi, and was run by the PR's AVX2 job.
