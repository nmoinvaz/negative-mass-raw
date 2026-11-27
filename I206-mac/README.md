# I206-mac: later window starts and noise-only, entire and weak-singularity series for multisolver's `locate` (PR to multisolver)

Machine: the coordinator's Mac (Apple M5, macOS, aarch64 NEON), runner negative-mass-mac-i206, at most 2 processes, nice 10
(`cargo -j 2`, `RAYON_NUM_THREADS=2`). Issue: https://github.com/nmoinvaz/negative-mass/issues/206 . Worktree
`~/Source/negative-mass-i206`, branch `wip/i206-locate` (negative-mass main 8fc3901). Library clone
`~/Source/negative-mass-i206-libs/multisolver`, branch `feat/locate-late-windows` (multisolver main 63d6e4d, which holds
PR #26's `locate`). rustc 1.94.0, multisolver 0.2.2, multidouble 5.1.0, python 3.14.5 with mpmath 1.3.0 (a venv in the
session's scratch directory; mpmath 1.3.0 is the only package).

This README is written before the first run of record. What is declared here (the change, the cases, the readings of the
acceptance, the criteria, the control inputs) is not changed after a run; the **targets** of the controls (the cells on
which each control must fire) are declared in an amendment after the development run that computes them, as in I191
(README A3). Every log is kept in this folder, including failed and stopped runs; reruns are numbered and nothing is
overwritten. A failed check is a result, reported; no criterion is loosened, no case or grid widened, to make it pass.

## 1. The change

`multisolver::locate::Opts::default().starts` goes from `0.2, 0.3, 0.4, 0.5, 0.6` to `0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8`
(first orders of the fit window as fractions of K). Nothing else in `src/locate.rs` changes except its doc comments: the
degrees, `bar_factor` 2, `max_rel_bar` 0.05, the floors, the neighbor rule and the choice rule are #191's. The rest is tests.

Why it could matter, and what could go wrong (written down before the run): at K = 30 the window at 0.8 K starts at order
24 and has 7 ratio rows (degree at most 3) and no three-term rows (6 rows, 9 needed at degree 2); at 0.7 K, 10 ratio rows
(degree at most 6) and 9 three-term rows (degree 2). A late window sees the least truncation error and the most noise and
has the fewest rows, so it may also pick a cell whose few neighbors agree by chance: that is what the noise-only and the
weak-singularity series, and the exploration's coverage, test.

## 2. Readings of the acceptance (the issue's words, and what each is taken to mean)

| issue's words | reading, declared now |
|---|---|
| "D6 in f64 meets #191's criteria 1-4, and the other 68 cells still do" | the suite of `tests/locate.rs` (23 gated cases x 3 lanes = 69 gated cells; N3's 3 rows are printed, not gated), run with `Opts::default()`, has no failed criterion in any of the 69 gated cells. The criteria are those of that file's doc comment, unchanged (kind; error of s and of alpha within the tier's tolerances; the bars cover the errors; the bars are within 100 tolerances) |
| "at factor 2 the bar covers at least 254 of the 256 resolved exploration cells" | the exploration of I191 (`dev_02_*`: 90 random cases of seeds 1 and 2, 3 lanes = 270 rows, fit degrees up to 9, the eight-neighbor spread, Python/mpmath prototype) rerun on this Mac with first orders 0.2 ... 0.8 K. Resolved: the bar of s below 5% of \|s\|. Covered: error of s <= 2 x the spread. Passes when **both** covered >= 254 **and** at most 2 resolved cells are uncovered (the second is the stricter if more cells than 256 become resolved). I191's figures on the Pi: 256 resolved, 254 covered |
| "the noise-only and entire series give `Unresolved`" | `locate` returns `Some` with `kind == Unresolved` for each series. `None` (no cell with two neighbors that fit) is **not** `Unresolved` and counts as a failure of the criterion (reported as such) |
| "the weak singularities give `Real` or `Unresolved`, never a confident wrong location" | for each weak series the outcome is `Unresolved`, or `Real` whose error of s is within its bar. **Confidently wrong** = `locate` returns a resolved kind (`Real` or `Pair`) and either the kind is `Pair` or the error of s (distance in the complex plane) exceeds the bar of s. `None` is counted and listed, and is not confidently wrong (no location is claimed). Gated on s and the kind; the error of alpha against its bar is reported |
| "real singularities whose coefficients are 1, 10 and 100 times the noise" | the planted part is scaled so that the root mean square of its coefficients c_1 ... c_K is m delta, delta the noise unit of the lane (the root mean square of the noise coefficients), m = 1, 10, 100 |
| "a control for each fails" | each criterion in section 4 has a control: a wrong input fed to the same check, which must fail it, run once to see it fire (section 5) |

## 3. The series

Lanes as in #191: f64 (K = 30), double-double (K = 60), quad-double (K = 120); noise unit delta = 1e-10, 1e-19, 1e-38.
Coefficients are formed in the lane's arithmetic. The suite's cases (P, D, C, T, N, O8, N3) are those of `tests/locate.rs`,
not repeated here.

**Noise.** xi_k is the xorshift of `tests/locate.rs` (uniform on [-sqrt 3, sqrt 3), unit variance). For seed 1 ... 100 and
a tag, the state starts at `0x9E3779B97F4A7C15 ^ seed * 0xD1B54A32D192ED03 ^ tag * 0xA24BAED4963EE407` (wrapping) and the
first 16 draws are discarded. The tag is `100 * series type + lane index` (lane index 0, 1, 2 for f64, dd, qd; series type 1
noise-only, 2 + w for the weak singularity w). The noise is **additive**: c_k gets delta xi_k.

| id | series | count |
|---|---|---|
| noise-only | c_k = delta xi_k, k = 0 ... K | 100 seeds x 3 lanes = 300 |
| E1, E2, E3 | the entire functions exp(u), exp(-3u), sin(sqrt v) / sqrt v (the series in v): c_0 = 1 and c_k = c_(k-1) / k, c_k = c_(k-1) (-3) / k, c_k = -c_(k-1) / (2k (2k + 1)) | 3 x 3 lanes = 9 |
| W1, W2, W3 | one real singularity, A (1 - u / s)^alpha with (alpha, s) = (-1, 1.25), (-1/2, -0.8), (1/2, 1.0), plus noise: c_k = a p_k + delta xi_k, p_k the coefficients of (1 - u / s)^alpha by the recurrence of `part_series`, a such that the root mean square of a p_1 ... a p_K, formed in f64, is m delta | 3 x m in {1, 10, 100} x 3 lanes x 100 seeds = 2700 |

The weak singularities are at radius about 1, the convention of the module (the variable scaled so that the radius is of
order one, #207's walkers): the pole's coefficients fall as 0.8^k, W2's grow as 1.25^k (a late window sees it best), W3's
fall as k^-1.5. Reported, not gated (the amplitude at which a weak singularity is resolved, #191's recommended task 2): the
same W1 to W3 at m = 3, 30, 300, 1e3, 1e4, 1e6, 1e9 (`weak_sweep`, an ignored test).

## 4. Criteria (each can fail)

1. **D6 in f64** (alpha = 1e-8 dressed with tau = 4 \|s\|, K = 30) meets #191's criteria 1-4 with `Opts::default()`: kind `Real`;
   error of s <= 1e-2 and of alpha <= 0.1; the bars cover; the bar of s over \|s\| <= 1 and the bar of alpha <= 10.
   (#191: `Unresolved`, bar 1.1 \|s\|, error of s 0.41: not met.)
2. **The other 68 gated cells** still meet criteria 1-4 of #191 (section 2).
3. **Exploration coverage** (section 2): at factor 2, covered >= 254 and uncovered <= 2 among the resolved cells of the 270 rows.
4. **Noise-only**: all 300 series give `Some(Unresolved)`.
5. **Entire**: all 9 series give `Some(Unresolved)`.
6. **Weak singularities**: of the 2700 series none is confidently wrong (section 2).
7. **Backends**: the fingerprint of the results (the suite's cells and, new, the noise-only, entire and weak series of
   seeds 1 to 10) is the same constant in the default build and with `--features portable` here (aarch64 NEON), and in the
   PR's x86 SSE2, AVX2, MSVC and macOS jobs. Local `+avx2,+fma`: not run unless this Mac can (said in the PR).
8. **Repository rules** (`CLAUDE.md`): `cargo fmt`, `cargo clippy --all-targets -- -D warnings` in the default build and
   with `--features portable`, `cargo test --release` in both; the PR's CI green.

Reported, not gated: the chosen model, first order and degree and the bars of every row; for noise-only and weak series the
counts per (series, m, lane) of `Unresolved`, resolved and covering, resolved and wrong, `None`, with the median error; the
same series under the #191 grid (starts 0.2 ... 0.6) for comparison; the error of alpha against its bar; for the noise-only
series the false-resolved rate against #191's recommended 1% (the issue's criterion, none of 300, is the stricter).

**Exploration of the shipped code (reported, not a gate).** The Python instrument of criterion 3 is a prototype: it has no
floor on its bar and needs one row fewer per ratio fit than the port. The same 270 series are dumped (`explore3.py`,
every coefficient as non-overlapping f64 parts) and run through `multisolver::locate` as shipped, under the default grid and
the #191 grid (`sys/explore_rust`): resolved, covered at the bar the library reports (factor 2, floors), kind right, and the
control. Two comparisons are printed, the Python instrument on the #191 grid (a rerun that must reproduce I191's 256 / 254,
which checks the instrument on this machine) and the port.

## 5. Controls (inputs now; targets after the development run)

| control | wrong input | check it must fail |
|---|---|---|
| `grid-191` | D6 in f64 under `Opts { starts: 0.2, 0.3, 0.4, 0.5, 0.6, .. }`, the grid of #191 | criterion 1: kinds, tolerance and bars-useful (the result recorded by `d6_f64_is_not_met` in PR #26: `Unresolved`, fails 1, 2, 4, holds 3). **Declared target: fails exactly 1, 2 and 4** |
| `grid-no-0.8` | D6 in f64 under starts 0.2 ... 0.7 (#191's recommendation: "a grid without 0.8 K fails D6 again") | reported, with what it does; not gated |
| the six controls of #191 (`wrong-sigma`, `wrong-alpha`, `pair-by-ratio`, `bar-shrunk`, `window-early`, `window-short`) | as in `tests/locate.rs`, run on the new grid | criterion 2's checks. Targets as in #191 (A3); the `locate_at` controls do not depend on the grid; any change in the set of cells where `bar-shrunk` is silent is reported and its new set declared after the development run |
| `bars-shrunk` (exploration) | the same 270 rows at factor 0.002 (the bars shrunk a thousand times) | criterion 3: covered must fall below 254 |
| `planted-resolved` | the noise-only and entire check fed P1's series (a pole at 2) in the three lanes | criteria 4 and 5: the check must fail (kind `Real`) |
| `loose-bar` | `Opts { max_rel_bar: 1e300, .. }`: a locator that never says `Unresolved`, on the noise-only and entire series | criteria 4 and 5: the check must fail |
| `wrong-location` | the weak check fed a series of W1 to W3 without noise planted at s x 1.1 and checked against s: a resolved result with error 0.1 \|s\| above its bar | criterion 6: the check must flag it |
| `bar-shrunk-weak` | the weak check with the bars of each resolved result multiplied by 1e-3, on the noise-free W series and on the weak series | criterion 6: the check must flag results whose error is not zero |
| `fingerprint-flip` | one coefficient of one noise-only series changed in its lowest bit, and one of D3's as in #191 | criterion 7: the fingerprint must change |

A control silent on its target is reported as silent and is not repaired by a stronger mutation without the coordinator's
agreement. The control of criterion 1 and `bars-shrunk` are in the first runs; the others in the development run of the library tests.

## 6. Plan of runs

1. Development, on the clone at main (the #191 grid): the new tests' printer (`late_windows_report`, ignored) with the
   default grid forced to #191's (the "before" figures), and the exploration's Python baseline (the #191 grid; must give 256 / 254).
2. The change; the development run of the library tests (the "after" figures), the controls' printer, the Python exploration on
   the new grid and the Rust port on its series. Amendments A1 ... declare the controls' targets and any silent control.
3. Runs of record at the PR's head commit: `cargo test --release` for `--test locate` and the unit and doc tests, in both
   builds; fmt; clippy in both builds; the exploration of the port; the sweep (reported).
4. Stop condition: a single run past 2 h wall time is stopped and reported. The Python exploration is two processes
   (seed 1, seed 2) when no cargo build runs, else one at a time: never more than 2 processes together.

Logs are named `dev_NN_*` (development) and `run_NN_*` (of record); `*.rc` hold exit codes. Scripts in `sys/`:
`explore/` (the I191 prototype `proto.py`, `helpers.py`, the I191 originals of `explore3.py` and `analyze2.py` kept as
`*_i191_orig.py`, the changed `explore3.py`, `analyze_i206.py`), `explore_rust/` (the port's harness, a cargo package with a
path dependency on the clone).

## Amendments

(none yet)
