# I207-mac: multisolver's locate in the conical walkers (feature `locate_lib`), against #183's 818 verdicts and the default checks of #167 and #184

Machine: the coordinator's Mac (Apple M5, 10 cores, macOS, arm64 NEON, shared with other agents; load average 2 to 9 during development). Issue: https://github.com/nmoinvaz/negative-mass/issues/207

The criteria below are written before the first run of record (`run_NN`); the development runs (`dev_NN`) came first and are
described at the end of this file, with what they showed. Amendments, if any, are listed after them with their reason; nothing
above the heading "Development log" is edited.

## Where

| what | where |
|---|---|
| worktree (the crate) | `~/Source/negative-mass-i207`, branch `wip/i207-locate-walkers` from main 62ebb47 (#216 merged), crate `notes/warp/conical_global/` |
| code under test | commits c70867f (`locate_lib`) and 2abf1ee (controls and the ungated arm) of that branch; the runs of record build from the clean tree at 2abf1ee or a later commit named in the run's log header |
| build outputs | `~/Source/negative-mass-i207-target/<arm>` (`off`, `on`, `early`, `late`, `ungated`), copied to the crate's `target/release` by `sys/arm.sh` before a run, their sha256 in `arm_<job>.sha256` |
| raw | this folder: `run_NN_<what>.log` (stdout), `.err`, `.rc` (exit code), `.time` (`/usr/bin/time -l`); every rerun numbered, none overwritten |
| toolchain | rustc 1.94.0, Python 3.14.7 (`~/Source/negative-mass/.venv`), multishoot =5.0.0, multisolver =0.3.0, multidouble =6.1.0 (unchanged by this task) |
| budget | at most 2 processes (`cargo -j 2`, `RAYON_NUM_THREADS=2`), `nice -n 10`, one job at a time; a job not finished in 2 h of wall time is stopped (rc 124) and reported |

## The work

`multisolver::locate` (#191, #206, in multisolver 0.3.0) replaces the f64 Domb-Sykes fit of `walk.rs` (#167's walker, in
double-double) and `hp.rs` (#183's walker, double-, quad- and octo-double) behind the cargo feature `locate_lib`. The window and
degree are the library's (`Opts::default()`); the series is read in the lane's own precision (`W<P>` implements the library's
`Real`). The fixed design, written here before the runs of record (module doc of `src/loc.rs`):

- **Scale.** Each field's coefficients are multiplied by r^k, r a power of two nearest |c_(K-1)/c_K| (exact; the library expects a
  radius of order one).
- **Estimate of a step.** The three fields are read separately. A field that reads `Kind::Real` gives R = |s| r l (x units), the side
  from the sign of s, gamma = 1 + alpha of the field, and the library's bar of s over |s| in the place of the fit residual; of the
  fields the smallest bar wins. A field that reads a pair, `Unresolved` or nothing gives no estimate, as a field with a sign change
  of its ratios did for the f64 fit. The stop rule (five consecutive real estimates ahead, the last R at most the stop radius, bar =
  spread of the last five eta*) and the labels of `conical_kind` are unchanged.
- **Gate.** `locate` costs about 1 ms (double-double, K = 30), 16 ms (quad-double, K = 60) and 0.3 s (octo-double, K = 120) per field
  and step on this Mac (`dev_12_bench_locate.log`, source in `sys/bench_locate/`; a first run under a higher load gave 1.2 ms, 21 ms and
  430 ms, which the first commit's comment quoted). It runs only at the steps where the
  planner's step h is at most 16 stop radii. h is about 0.09 times the radius (the planner's tolerance to the power 1/K), so the
  gate is open from R of about 180 stop radii inward, which contains the five steps the rule needs. Outside it the step has no
  estimate. The ungated arm (`locate_ungated`) checks this (criterion C8).
- **Shadow.** On the same steps the f64 fit runs beside `locate` with its own five-step rule; `LocStats` (written to the verdict
  JSON, key `loc`, with the feature only) keeps, per walk, the counts of what `locate` said at the gated steps (real, behind, pair,
  Unresolved, nothing), the steps where the old fit was a real singularity ahead and `locate` was not, and the step and eta* at
  which the old rule would have stopped. The steps of a walk do not depend on the locator, so this is what the f64 walker would
  have done. Feature off: no `loc` key, the output is the same as before.

## Baselines (all feature off; multishoot 4.2.0, multisolver 0.2.2, multidouble 5.1.0; Raspberry Pi 5, aarch64 NEON)

| for | log | dump or controls |
|---|---|---|
| 818 verdicts, stage a (15 checks, full grid) | `I183-rpi5/run_04a.log` | `I183-rpi5/dump_run_04a/` (241 files) |
| 818 verdicts, stage b (`dd_qd`) | `I183-rpi5/run_03b.log` | `I183-rpi5/dump_run_03b/` |
| controls of `conical_offgrid.py` | `I183-rpi5/ctl_run_03/ctl_<name>.log` | |
| `ctl` grid, 16 checks | `I190-rpi5/run_06_base_offgrid_ctl.log` | `I190-rpi5/dump_base_ctl/` (79 files) |
| `conical_global.py` (#167) | `I190-rpi5/run_11_base_global.log` | `I190-rpi5/ctl_base_global/` |
| `conical_loglog.py` (#184) | `I190-rpi5/run_09_base_loglog.log` | `I190-rpi5/ctl_base_loglog/` |

The commands of #183's run of record (`I183-rpi5/sys/run_record.sh`): stage a is `conical_offgrid.py --nobuild --no-controls
--dump=D --only=n_table,series_hp,plant_167,plant_far,regress167,scan,spread,modes,symmetry,n4_factor,closed_form,bisect,independent,recip_check,step_halving`,
stage b is `--no-controls --dump=D --only=dd_qd`. The Mac's feature-off arm runs them too: it separates what the platform and the
script's later changes do from what the feature does.

## Criteria (each can fail; verdicts are given as worded here)

The comparator is #190's `compare_outputs.py`, unchanged (sha256 341f60b737719ab2366664e5299b3dfc84d99a0ee7c2e5b68e98f4b584c0fa6f,
the same file as `I190-rpi5/sys/compare_outputs.py`), through `sys/compare_run.py` (#216's wrapper, adds listings) and
`sys/classify_diff.py` and `sys/compare_eta.py` (new, below). A difference in any eta*, verdict, class or kind is reported as not
met, with its line, and its cause is not guessed. No criterion is loosened after a run of record.

| id | criterion | gated |
|---|---|---|
| C0 | the five arms build (exit 0, no warning); `cargo clippy --all-targets -- -D warnings` is clean with default features and with `--features=locate_lib` (and each of the other three); `cargo test --release --lib --features=locate_lib`: 3 of 3 | yes |
| C1 | feature off is unchanged: the `off` arm's `ctl` run (all 16 checks, dump) against `I190-rpi5`: `compare_run.py` no gated difference, `compare_eta.py` 0 differing eta* at 1e-15 max(1, eta*); its stage a and stage b runs on the full grid against `I183-rpi5`: the same comparator, every difference listed | yes |
| C2 | the 818 verdicts with the feature on: stage a and stage b of the `on` arm exit 0 and every check passes (15 of 15 and 1 of 1) | yes |
| C3 | the same runs, labels: every class, kind, stop, tiny_kind, through and converged string of every dump record equals the baseline's, and `classify_diff.py` finds no line of kind (ii) in the logs (kinds below) | yes, every difference reported with its record |
| C4 | the same runs, eta*: every `xstar` of the dump, in the records whose class and kind equal the baseline's, within 1e-10 max(1, eta*) of the baseline's (`compare_eta.py`). 1e-10 is the bar #183 uses to compare the same point under two formulations of the walk (O9 `modes`, O10 `symmetry`, O16 `step_halving`); the tighter 1e-12 of O8 (`dd_qd`, two lanes) is listed (count above it) | yes at 1e-10 |
| C5 | #167's and #184's default checks, feature off and on: `conical_global.py` (17 of 17 checks, 13 of 13 controls on target only) and `conical_loglog.py` (20 of 20, 17 of 17), exit 0, on both arms | yes |
| C6 | the logs of C5 against #190's baseline: no line of kind (ii), each control's own log and exit code equal | yes, every difference reported |
| C7 | a control on the window fails: the `early` arm (first order 2, degree 2, through `locate_at`) on the `ctl` grid fails a check that the `on` arm passes (declared: `scan`), and `classify_diff.py` finds more lines of kind (ii) than for the `on` arm. The `late` arm (last 10 orders, degree 2) is reported, no target declared | yes for `early` |
| C8 | the gate changes nothing: the `ungated` arm's `ctl` run against the `on` arm's: every string of the log (kinds (i) and (iii) aside) and of the dump equal, every `xstar` bit for bit, every step count equal | yes |
| C9 | where `locate` says `Unresolved`, the records and what the old fit said there are reported: `loc_report.py` on every on-arm dump gives, per record, the counts of Unresolved, nothing and pair steps, the steps where the old fit was a real singularity ahead and `locate` was not, the stop step and eta* of the old rule beside the new ones; the counts of table 1 equal the counts of the records listed | yes (the report is complete) |
| C10 | the script controls that touch the locator, on the `on` arm: `conical_offgrid.py --grid=ctl --controls-only --controls=locator-side,plant-locator,n-drift,recip-dd`, each control fires its declared targets (#183's list) and no check outside them, except `regress167` where it fails without any control (declared below) | yes |

**Kinds of a differing log line** (`classify_diff.py`; the rules are written from the baseline's lines and the development runs
before the runs of record):
(i) zero-token: equal once `0.0e+00` is read as `<err>`. The comparator replaces numbers in scientific notation with an exponent of
-6 or smaller by `<err>` and leaves an exact zero as it is, so an error or bar that is exactly zero in one run and rounding-sized in
the other differs for it (the five-step spread of eta* is 0.0 where the estimates agree to the last bit). Listed.
(ii) every other difference: a label, a count, a class, a kind, an eta* printed to 10 digits, a pass or a fail, a line count.
(iii) fitted exponent: equal once the fitted exponent and its ratio to 2/(eta*^2 + 4) are masked in the two places the baseline prints
them (the closing line of the scan summary, "measured exponent ... worst relative difference X", and the `dd_qd` note, "double-double X
(R) F->0; quad-double X (R) F->0"). The exponent is what the feature changes (#183's fit was off by up to 6% in the O8 regime), so
it is listed, not gated; the eta*, the kinds and every other number on those lines stay compared.

**`regress167` in C10.** `regress167` fails in every `on` run in the development log (two points, below), with or without a
control. For a control whose targets do not include it (`plant-locator`, `recip-dd`) a failure of `regress167` is therefore read as
the feature's, not the control's, and listed; the control's own targets are still required.

**The tools can fail** (`sys/selftest_tools.py`, `selftest_01.log`): on copies of the baseline, an unchanged copy gives no
difference; a number printed as 0.0e+00 gives kind (i); a changed fitted exponent kind (iii); a changed label and a changed 10th
digit of an eta* in a label line kind (ii); an eta* of the dump moved by 5e-11 max(1, eta*) passes at 1e-10 and fails at 1e-12; one
moved by 1e-9 fails at 1e-10; a changed class makes `compare_eta.py` skip the record and count it. `--mutate=NAME` runs one case.

## The controls and their computed effects (development runs on the `ctl` grid, all 16 checks)

| control (cargo feature) | change | effect in development |
|---|---|---|
| `locate_mut_early` | `locate_at(c, Ratio, first = 2, degree = 2)` in place of `locate` | `dev_07`: 14 of 16 checks pass; `scan` fails (the point (F_inf, C) = (16, 1e8) ends `TINYSTEP`), `regress167` fails at 3 points ((0.75, 300) `FLOOR:log` against `NONFINITE`, (1, 3000) and (-1, -3000) `S:F->0` against `NONFINITE`); 48 lines of kind (ii) against #190's baseline; 13 dump records differ in class or kind |
| `locate_mut_late` | `locate_at(c, Ratio, first = K - 9, degree = 2)`: the last 10 orders as the f64 fit, in the lane's precision | `dev_08`: 16 of 16 pass; no record differs in class or kind; every eta* within 7.5e-12 of the baseline's. **Silent on this grid**: no check fails, which includes `dd_qd` at the points of the O8 regime that the grid holds ((+-1, +-1e8)), and it reads no pair (the ratio model has none). Reported, no target |

## Run plan

One queue, one job at a time, in this order (the first of each line is the run's name stem): `run_01..05` builds; `run_06` `on` ctl
(sanity); `run_07`, `run_08` `on` stage a, b; `run_09`, `run_10` `off` stage a, b; `run_11`, `run_12` `off`, `on` global;
`run_13`, `run_14` `off`, `on` loglog; `run_15` `off` ctl; `run_16`, `run_17`, `run_18` `early`, `late`, `ungated` ctl; `run_19`
`on` script controls; `run_20`, `run_21` clippy off, on (and the other three arms); `run_22` unit tests. A job over 2 h of wall
time is stopped and reported. The pilot of the hardest case (a quad-double walk of the O8 point, 5.5 s per walk, `dev_` log
in the development section) ran before.

## Development log

Nothing above this heading has been edited.

### D1 First on-arm run of the `ctl` grid (`dev_04`, tree of the working copy before the commits c70867f and 2abf1ee)

15 of 16 checks pass, 633 s (the first 5 min build the series pickle); `regress167` fails: `offgrid` gives `S:F->0` and #167's binary `NONFINITE` at (F_inf, C) = (2, 3000)
and (-2, -3000) (`conical_global scan --rstop=1e-8`: the f64 walker with the locator reads no real singularity ahead, passes R = 1e-8
and ends at a planned step h = 0). Against #190's baseline (`compare_run.py`): 8 gated log lines, of which 5 zero-token, 1 fitted
exponent, 2 other (`regress167` and the checks count); the dump has 4 records of another class or kind (the two points in `offgrid`
change `a3->0` to `F->0` at eta* 1.2014264 instead of 1.7085396; in #167's binary `SINGULAR` to `NONFINITE`), 16 eta* that differ in
the 10 printed digits, 19 records with another step count. `compare_eta.py`: 533 eta* compared, largest difference 7.5e-12, 5 above
1e-12, none above 1e-10. The four largest are the planted blow-ups of `plant_167` (truth 0.7321): the baseline's f64 fit has
0.7321000000074667 (error 7.5e-12), the library 0.7321000000000001. This is why C4's bar is 1e-10 and not O8's 1e-12: the
baseline's own estimator is off by more than 1e-12 there.

What the library reads at (2, 3000), traced with a temporary print (not committed): up to R of about 1e-8 a real singularity with
alpha(F) = 1.94 to 2.0; from there on a conjugate pair, in the three fields, with Im s = 1.4e-11 to 1.8e-11 (rising slowly over the last 50
steps) and alpha(F) = 2.5 (alpha of the three fields 2.50, 1.50, 0.50 at R = 1.7e-10, bars 3e-7 to 1.5e-5 of |s|). #183 inferred such
a pair for its first-pass versus pass-of-record points (conical_offgrid.md section 4). The cause of the difference with the f64 fit
is not decided here.

### D2 Controls (`dev_07` early, `dev_08` late), see the table above; `dev_09` ungated `ctl` run (the gate check, C8)

`dev_09` was stopped at 23 min by the agent (its own PID, `dev_09_ungated_offgrid_ctl.stopped`), in the `dd_qd` check, to free the
queue: checks 1 to 7 were done, and its 50 dump files (560 records) equal `dev_04`'s (the gated arm) outside the `loc` key, parsed
and compared as JSON. C8 is checked again in full by `run_18`.

### D3 Pilot of the hardest case

A quad-double walk of the O8 point (F_inf, C) = (2, -1e8) with the `on` arm: 5.5 s, 390 steps, 68 calls of `locate`, class `F->0`,
eta* 7071.061147280221 (the f64 fit: the same), alpha(F) = 4.000007214e-8 against 2/(eta*^2 + 4) = 4.000007220e-8 (the f64 fit in
double-double: 4.0166e-8). The same point in double-double: 0.2 s.

### D4 Tools

`sys/classify_diff.py`, `sys/compare_eta.py`, `sys/loc_report.py`, `sys/selftest_tools.py` written after D1 (the zero-token and
fitted-exponent kinds and C4's bar come from it). `dev_10`, `dev_11`: clippy clean off and on (before the final edits; C0 reruns it).
`dev_10_clippy_on_failed1_shellsplit.log` is a failed command line (zsh did not split `--features locate_lib`), kept.

## Amendments

### A1 The lint and test runs are numbered `run_20` to `run_25` (not `run_20`, `run_21`)

The run plan said "`run_20`, `run_21` clippy off, on (and the other three arms); `run_22` unit tests". As queued
(`sys/jobs_record.txt`, `sys/jobs_lint.txt`, `sys/run_all.sh`): `run_20` to `run_24` clippy of the arms off, on, early, late, ungated;
`run_25` `cargo test --release --lib --features=locate_lib`. The script controls are `run_19` as planned. No criterion changes.
The queue started 2026-11-28 04:58 UTC (the log headers hold the exact times), from the clean tree at 2abf1ee.

### A2 `classify_diff.py` aligns the log lines (a change of the listing, not of a criterion)

`classify_diff.py` paired the lines of the two logs by position, like `compare_outputs.py`. In `run_07` the new run lists 46 points
of the NOTE `scan_first_pass` where the baseline lists 44, so every line after the first inserted one was shifted and 340 of 349 lines
were reported as differing. It now aligns the normalized lines with `difflib.SequenceMatcher` first, pairs the lines of a replaced
block of equal length, and counts an inserted or deleted line as kind (ii). The comparator itself, the kinds (i), (ii), (iii) and C3's
rule ("no line of kind (ii)") are as declared; only the count of lines of kind (ii) changes (338 positional, 64 aligned for `run_07`).
`selftest_tools.py` passes with it. The positional listing is kept as `classify_run_07_on_stage_a.v1_positional.txt`.

### A3 The first lint and test jobs failed in the queue (mine); reruns `run_26` to `run_31`

`run_20` to `run_25` exited 2 within a second: `run_queue.sh` creates `NAME.log` before it starts the job, and `clippy.sh` and `test.sh`
refuse to overwrite a log of that name. Their logs are kept. `run_26` to `run_31` are the same six jobs (clippy of the arms off, on,
early, late, ungated, and `cargo test --release --lib --features=locate_lib`) started by hand, `clippy.sh` and `test.sh` writing their
own logs. No code changed between the queue's start and these runs except the comment of `src/loc.rs` (commit 9a9fa74, after the runs of
the arms); the arms of the runs of record were built at 2abf1ee.

## Results of the runs of record

Table of all runs: `results_table.md` (`sys/summarize_i207.py`). Per run, `cmp_<run>.txt` (the comparator through `compare_run.py`),
`classify_<run>.txt` (kinds (i), (iii), (ii)), `eta_<run>.txt` (C4), `loc_<run>.md` (the Unresolved and pair tables, C9).
The code of the runs: `wip/i207-locate-walkers`, arms built at 2abf1ee (`run_01` to `run_05`, all exit 0, no warning).

| id | verdict | numbers |
|---|---|---|
| C0 | met | five builds exit 0 with no warning; `cargo clippy --all-targets -- -D warnings` exit 0 on the five arms (`run_26` to `run_30`); `cargo test --release --lib --features=locate_lib` 3 of 3 (`run_31`) |
| C1 | **comparator met, eta* bar not met as declared** | feature off against the baselines: `ctl` (`run_15`) 0 of 68 gated lines, 537 eta* (largest difference 1.33e-15 max(1, eta*), **1 record above the declared 1e-15**, F_inf 1.5, C 1000; 10 records with another step count); stage a (`run_09`) 0 of 349 gated lines, 4034 eta*, largest 1.33e-15, 102 records with another step count; stage b (`run_10`) 9 of 25 lines differ, all of kind (iii) (the f64 fit's exponent in the `dd_qd` note, Pi against Mac), 727 eta* equal. The size is #216's one-path difference (2.45e-15 there); the feature's code is compiled out in this arm |
| C2 | **not met** | on arm, full grid: stage a (`run_07`, 1861 s, exit 1) 10 of 15 checks pass, failed `regress167`, `scan`, `spread`, `modes`, `bisect`; stage b (`run_08`, 1221 s, exit 1) 0 of 1, failed `dd_qd` |
| C3 | **not met** | stage a: 59 records of the dump of another class or kind (31 `a3->0` to `F->0`, 25 `a3->0` to `TINYSTEP`, 2 `a3->0` to `NONFINITE` in #167's binary, 1 `fold` to `F->0` in a first pass), 64 lines of kind (ii); stage b: 11 records, 2 lines of kind (ii). Of the 818 points 808 keep class and kind and 10 change (below) |
| C4 | met | stage a: 3971 eta* of records that keep class and kind, largest difference 1.945e-11 max(1, eta*), none above 1e-10, 89 above 1e-12; stage b: 716, largest 5.5e-15, none above 1e-12 |
| C5 | **not met on, met off** | off (`run_11`, `run_13`): `conical_global.py` 17 of 17 and 13 of 13 controls on target only, `conical_loglog.py` 20 of 20 and 17 of 17, exit 0. On (`run_12`, `run_14`): 16 of 17 (`scan`: 2 `NONFINITE`, (+-2, +-3000)) and 19 of 20 (`basin`: 9 of 100 labels `kappa@`, which the script prints for `NONFINITE`), controls 13 of 13 and 17 of 17 on target only, exit 1 each |
| C6 | **not met on, met off** | off: 0 gated lines of 126 and of 124, 13 and 17 control logs equal; on: 50 and 3 lines of kind (ii), 3 of 13 and 1 of 17 control logs differ (the exit codes of all equal) |
| C7 | met | `early` (`run_16`): 14 of 16, fails `scan` ((16, 1e8) `TINYSTEP`, which the `on` arm passes) and `regress167` (3 points); 11 lines of kind (ii) against 2 for `on`; 13 records of another class or kind. `late` (`run_17`): 16 of 16, 0 lines of kind (ii), no record of another class or kind (silent, as developed) |
| C8 | met | `ungated` (`run_18`, 2087 s against 570 s) against `on` (`run_06`): 79 files, 685 records equal outside the `loc` key, 535 eta* bit for bit, 0 differing lines of 68; `locate` was called 266,880 times against 67,088. `equal_outside_loc.py --mutate=eta` and `--mutate=count` fail it |
| C9 | met | `check_c9.py` on the six feature-on dumps: the counts of table 1 equal the rows of tables 2 and 3 and the counts made from the dump (`c9_all.txt`); `--mutate=drop` fails it. Stage a: 240 records with an Unresolved step (2940 of 101,143 gated steps), 318 with a pair step |
| C10 | met, with the declared exception | `run_19`, exit 1 (the script's own line: "SOME DID NOT FIRE ON TARGET ONLY"): `locator-side` fails exactly its targets; `n-drift` fails exactly its targets; `plant-locator` and `recip-dd` fail their targets and also `regress167`, which fails in every on-arm run (declared above), and the script prints them as `[EXTRA]` |

**The 10 points of the 818 whose class changes** (both from `a3->0` in #183): `TINYSTEP` at (F_inf, C) = (2, 1e4), (-2, -1e4), (4, 3e4),
(8, 1e5), (128, -1e6); `F->0` beyond the curve at (5, 3e4) eta* 4.6214 (was 4.8874), (12, 1e5) 11.8284 (11.9433), (24, 3e5) 23.9065
(23.9642), (64, 1e6) 63.9577 (63.9794), (128, -3e6) 127.9742 (127.9851). In #167's 187-point grid, (+-2, +-3000) `S:F->0` at 1.2014 in
`offgrid` (was `a3->0` at 1.7085) and `NONFINITE` in #167's binary. At (1.5, 1e4) the double-double lane reads a real singularity and ends
`a3->0` and the quad-double lane ends `TINYSTEP` (60 of 87 gated steps read a pair).

**What the old fit said** where `locate` said `Unresolved` (stage a, 240 records, 2940 Unresolved steps among their 101,143 gated steps):
at 217 of the records the f64 fit was a real singularity ahead on steps where `locate` was not; at 209 the stop step, class, kind and
eta* equal the baseline's and the old rule's shadow; at 31 the old rule would have stopped earlier than the walk with `locate` did (the
changed points above, their mirrors and repeats), at none later. Every record with its counts and the old rule's stop step and eta* is in
`loc_run_07_on_stage_a.md`, tables 2 to 4. At the 5 `TINYSTEP` points of the grid the old rule would have stopped 36 to 39 steps before the walk
ended, at the eta* where the walk stalls (to 5e-15), and `locate` read a pair at 38 to 55 of 73 to 79 gated steps.

Not run: `+avx2,+fma`, another machine or OS, `conical_offgrid.py` controls other than the four of `run_19`, the controls of #167's and #184's
scripts beyond their default target-only mode, octo-double walks with the feature.
