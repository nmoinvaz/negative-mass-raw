# I274-mac: the 35 winding2 boxes of #126 and #117 recounted with the crate's complex lane (f64) as a second evaluator

Machine: mac, the coordinator's Mac (Apple M5, macOS), shared with other sessions; runner negative-mass-mac-i274 (Claude Code, account claude-me2).
Issue: https://github.com/nmoinvaz/negative-mass/issues/274 (depends on #188).
Code: worktree `~/Source/negative-mass-i274`, branch `wip/i274-crate-recount` from main 04c8407, pushed by `git push origin HEAD:refs/heads/wip/i274-crate-recount`.
Driver: `phase2/nonradial/recount_i274.py` (beside `taylor_polar.py`, which it imports for the counter, the `dserve` client and the stored-value counter; `taylor_polar.py` is not edited).
Crate: `taylor_polar` at main 04c8407, `cargo build --release -j 2 --features complex --target-dir target/complex` (`build_complex.log`) and the default build (`build_default.log`).
Python `~/Source/negative-mass/.venv/bin/python` (3.14), at most two processes, nice 10, one thread each. Lane: the crate's f64 `Cx<f64>`.

`dev_NN_*` are development runs (`devrun.sh`), `run_NN_*` the runs of record (`runrec.sh`: log, `/usr/bin/time -l` in the `.err`, exit code in `.rc`).
A failed run keeps its log; a rerun gets the next number. `results/record/<box>.json` holds every number of a box's record, `results/<control>/<box>.json` a
control's; `jsonl_rec/` the crate's evaluations of the runs of record (one JSON line per D, from which a stopped run resumes).

## What is recounted

The winding2 (D) boxes of #126's `jobs.txt` (31; `I126-rpi5/jobs.txt` without the control `w_mut_reverse`) and the four D boxes of #117 (`I117-rpi5/jobs.txt`).
The Zerilli (Z) boxes need Z itself (#188's recommended task 3) and are not run. Each box is counted as winding2.py counted it at `--guard=all`: its eps, omega, l,
region, `--y0`, `--rsmult`, `--zfac` and planted zero, the scalar plane started at winding2's fixed R_s = r_m + rsmult / (min Re k over the contour, 200 points per edge),
the phase strip applied in double precision, and the counter of `taylor_polar.py --complex` (a copy of winding2's `count()` and `--plant`). F(s) is the crate's `dserve`
(`Cx<f64>`, one star and one J table per process) with the star's central data (`pc`, `zc`) from the crate's own `star` shooting, and **r_m from the scipy path's
`PolarProblem(...).rm`** (the first radius with phi < 1e-9: a definition of the problem, not a result; `stars.json`). The star of each (omega, eps) is compared with
the scipy path's in `run_01_stars` and in `dev_01_probe_stars` (central values agree to 1e-7 at r0 = 1e-3 and 1e-9; the crate's star has the same r_m).
The stored values are the caches of `I126-rpi5/cache/` and `I117-rpi5/cache/` (winding2's own, rtol 1e-8, grown by the guard-all runs) and its logs.

| box | source | l | eps, omega | region | extra options | R_s (log) | stored winding | max step | min abs D | planted (stored) |
|---|---|---|---|---|---|---|---|---|---|---|
| p7603_l2 | #126 | 2 | -1, 0.7603 | Re s [0.1, 2.0], abs(Im s) ≤ 2.5 | - | 404.9 | +0.0000 | 0.39 | 6.70e-04 | +2.0000 of 2 at 0.3,1.76 |
| p7603_l3 | #126 | 3 | -1, 0.7603 | Re s [0.1, 2.0], abs(Im s) ≤ 2.5 | - | 404.9 | +0.0000 | 0.40 | 1.68e-03 | +2.0000 of 2 at 0.3,1.76 |
| c075_l2 | #126 | 2 | 1, 0.75 | Re s [0.1, 2.0], abs(Im s) ≤ 2.5 | - | 404.4 | +0.0000 | 0.40 | 6.88e-04 | +2.0000 of 2 at 0.3,1.76 |
| p070_l2 | #126 | 2 | -1, 0.70 | Re s [0.1, 2.0], abs(Im s) ≤ 2.5 | - | 403.0 | +0.0000 | 0.40 | 7.45e-04 | +2.0000 of 2 at 0.3,1.76 |
| p070_l3 | #126 | 3 | -1, 0.70 | Re s [0.1, 2.0], abs(Im s) ≤ 2.5 | - | 403.0 | +0.0000 | 0.40 | 1.86e-03 | +2.0000 of 2 at 0.3,1.76 |
| p085_l2 | #126 | 2 | -1, 0.85 | Re s [0.1, 2.0], abs(Im s) ≤ 2.5 | - | 409.7 | -0.0000 | 0.40 | 4.93e-04 | +2.0000 of 2 at 0.3,1.76 |
| p085_l3 | #126 | 3 | -1, 0.85 | Re s [0.1, 2.0], abs(Im s) ≤ 2.5 | - | 409.7 | +0.0000 | 0.40 | 1.23e-03 | +2.0000 of 2 at 0.3,1.76 |
| n1_l2 | #126 | 2 | -1, 0.7603 | Re s [0.0001, 0.1], abs(Im s) ≤ 0.23 | - | 312.0 | -0.0000 | 0.33 | 2.82e-03 | +2.0000 of 2 at 0.0005,0.12 |
| n1_l3 | #126 | 3 | -1, 0.7603 | Re s [0.0001, 0.1], abs(Im s) ≤ 0.23 | - | 312.0 | +0.0000 | 0.35 | 3.16e-02 | +2.0000 of 2 at 0.0005,0.12 |
| n3_l2 | #126 | 2 | -1, 0.7603 | Re s [-0.001, 0.0001], Im s [0.01, 0.23] | --y0=0.01 | 312.0 | +0.0000 | 0.39 | 2.75e-03 | +1.0000 of 1 at -0.0005,0.12 |
| n3_l3 | #126 | 3 | -1, 0.7603 | Re s [-0.001, 0.0001], Im s [0.01, 0.23] | --y0=0.01 | 312.0 | -0.0000 | 0.38 | 3.66e-02 | +1.0000 of 1 at -0.0005,0.12 |
| s1_l2 | #126 | 2 | -1, 0.7603 | Re s [0.03, 0.1], abs(Im s) ≤ 2.5 | - | 1293.2 | +0.0000 | 0.40 | 1.00e-03 | +2.0000 of 2 at 0.04,0.25 |
| s1_l3 | #126 | 3 | -1, 0.7603 | Re s [0.03, 0.1], abs(Im s) ≤ 2.5 | - | 1293.2 | +0.0000 | 0.40 | 2.49e-03 | +2.0000 of 2 at 0.04,0.25 |
| h1_l2 | #126 | 2 | -1, 0.7603 | Re s [0.1, 2.0], Im s [2.5, 6.0] | --y0=2.5 | 419.7 | +0.0000 | 0.38 | 1.05e-04 | +1.0000 of 1 at 0.3,2.7 |
| h1_l3 | #126 | 3 | -1, 0.7603 | Re s [0.1, 2.0], Im s [2.5, 6.0] | --y0=2.5 | 419.7 | -0.0000 | 0.38 | 2.63e-04 | +1.0000 of 1 at 0.3,2.7 |
| t1_r40 | #126 | 2 | -1, 0.7603 | Re s [0.02, 0.1], Im s [0.15, 0.33] | --y0=0.15 | 825.5 | +0.0000 | 0.38 | 3.73e-03 | +1.0000 of 1 at 0.03,0.25 |
| t1_r80 | #126 | 2 | -1, 0.7603 | Re s [0.02, 0.1], Im s [0.15, 0.33] | --y0=0.15 --rsmult=80 --zfac=2 | 1626.8 | -0.0000 | 0.39 | 3.73e-03 | +1.0000 of 1 at 0.03,0.25 |
| t2_r40 | #126 | 2 | -1, 0.7603 | Re s [0.02, 0.1], Im s [1.68, 1.84] | --y0=1.68 | 1870.3 | +0.0000 | 0.40 | 9.30e-04 | +1.0000 of 1 at 0.03,1.77 |
| t2_r80 | #126 | 2 | -1, 0.7603 | Re s [0.02, 0.1], Im s [1.68, 1.84] | --y0=1.68 --rsmult=80 --zfac=2 | 3716.5 | +0.0000 | 0.35 | 9.30e-04 | +1.0000 of 1 at 0.03,1.77 |
| s2_l2 | #126 | 2 | -1, 0.7603 | Re s [0.01, 0.03], abs(Im s) ≤ 2.5 | - | 3831.3 | +0.0000 | 0.40 | 5.30e-04 | +2.0000 of 2 at 0.015,0.25 |
| h2_l2 | #126 | 2 | -1, 0.7603 | Re s [0.1, 2.0], Im s [6.0, 10.0] | --y0=6.0 | 422.4 | -0.0000 | 0.31 | 2.57e-05 | +1.0000 of 1 at 0.3,6.2 |
| s3_l2 | #126 | 2 | -1, 0.7603 | Re s [0.03, 0.1], Im s [2.5, 6.0] | --y0=2.5 | 1342.8 | -0.0000 | 0.39 | 9.90e-05 | +1.0000 of 1 at 0.05,3.0 |
| s3_l3 | #126 | 3 | -1, 0.7603 | Re s [0.03, 0.1], Im s [2.5, 6.0] | --y0=2.5 | 1342.8 | -0.0000 | 0.38 | 2.71e-04 | +1.0000 of 1 at 0.05,3.0 |
| rep_l4 | #126 | 4 | -1, 0.7603 | Re s [0.1, 2.0], abs(Im s) ≤ 2.5 | - | 404.9 | -0.0000 | 0.40 | 3.02e-03 | +2.0000 of 2 at 0.3,1.76 |
| s1_l4 | #126 | 4 | -1, 0.7603 | Re s [0.03, 0.1], abs(Im s) ≤ 2.5 | - | 1293.2 | +0.0000 | 0.40 | 4.43e-03 | +2.0000 of 2 at 0.04,0.25 |
| n1_l4 | #126 | 4 | -1, 0.7603 | Re s [0.0001, 0.1], abs(Im s) ≤ 0.23 | - | 312.0 | +0.0000 | 0.40 | 4.17e-02 | +2.0000 of 2 at 0.0005,0.12 |
| rep_l5 | #126 | 5 | -1, 0.7603 | Re s [0.1, 2.0], abs(Im s) ≤ 2.5 | - | 404.9 | -0.0000 | 0.40 | 4.70e-03 | +2.0000 of 2 at 0.3,1.76 |
| n1_l5 | #126 | 5 | -1, 0.7603 | Re s [0.0001, 0.1], abs(Im s) ≤ 0.23 | - | 312.0 | -0.0000 | 0.40 | 7.17e-02 | +2.0000 of 2 at 0.0005,0.12 |
| rep_l6 | #126 | 6 | -1, 0.7603 | Re s [0.1, 2.0], abs(Im s) ≤ 2.5 | - | 404.9 | -0.0000 | 0.40 | 6.71e-03 | +2.0000 of 2 at 0.3,1.76 |
| s1_l6 | #126 | 6 | -1, 0.7603 | Re s [0.03, 0.1], abs(Im s) ≤ 2.5 | - | 1293.2 | +0.0000 | 0.40 | 8.69e-03 | +2.0000 of 2 at 0.04,0.25 |
| n1_l6 | #126 | 6 | -1, 0.7603 | Re s [0.0001, 0.1], abs(Im s) ≤ 0.23 | - | 312.0 | +0.0000 | 0.39 | 1.35e-01 | +2.0000 of 2 at 0.0005,0.12 |
| b25_l2 | #117 | 2 | -1, 0.7603 | Re s [2.0, 5.0], abs(Im s) ≤ 10.0 | - | 44.0 | +0.0000 | 0.39 | 1.95e-05 | +2.0000 of 2 at 2.5,1.0 |
| b25_l3 | #117 | 3 | -1, 0.7603 | Re s [2.0, 5.0], abs(Im s) ≤ 10.0 | - | 44.0 | -0.0000 | 0.40 | 4.87e-05 | +2.0000 of 2 at 2.5,1.0 |
| h2_l3 | #117 | 3 | -1, 0.7603 | Re s [0.1, 2.0], Im s [6.0, 10.0] | --y0=6.0 | 422.4 | +0.0000 | 0.38 | 6.43e-05 | +1.0000 of 1 at 0.3,6.2 |
| h3_l2 | #117 | 2 | -1, 0.7603 | Re s [0.1, 2.0], Im s [10.0, 20.0] | --y0=10.0 | 423.6 | -0.0000 | 0.28 | 3.38e-06 | +1.0000 of 1 at 0.3,10.5 |

All 35 stored windings are 0 (zeros of D minus poles of D in the box, the sign of zero is not significant) and every stored planted check passed. The other D box of
#115, s1 at l = 5, is not in #126's list (it was counted at `--guard=all` in #115) and is not recounted here.

## Criteria (declared before any run of record other than `run_01_stars`; the development runs `dev_01`–`dev_05` and the first box in `dev_03` are in this folder)

Each check can fail; the box's verdict is OK only if all four pass, otherwise REPORT with the failing checks; a box that cannot be evaluated is NOT RUN with the reason.

- **INPUT.** The R_s and r_m computed for the crate equal those in winding2's log (1 and 2 decimals). (A crate told another R_s or r_m is not winding2's box.)
- **STORED.** The counter on the stored cache alone (no crate) reproduces winding2's log: winding within 0.05 of the logged one, the planted difference within 0.05 of the
  logged one and the check passing, max steps equal at 2 decimals, min abs D equal at 3 digits, and no point asked that the cache lacks. (The counter's port is faithful on this box.)
- **COUNT.** The counter with the crate: winding within 0.05 of the stored one, the planted difference within 0.05 of the stored expectation (+2 symmetric, +1 upper box),
  every phase step (with and without the plant) under 0.45 rad.
- **MARGIN.** The smallest distance of any compared quantity from its threshold (0.4, 0.4, 0.1 rad: the step, the half step, the sum of the half steps against the step),
  without the plant and with it (as W0 of #188), is at least 10 E, where E = max(3.1e-6 rad, the largest |arg(crate / stored)| over the points both have). 3.1e-6 is the largest
  phase error of the stored caches measured in #188 (l = 6; 9.8e-7 at l = 2). A box below this is reported, with its margin and E.
- **Recorded, not checked:** whether the points the counter asks are exactly the stored cache's (asked, stored, asked not stored, stored not asked), min abs D and
  max step of both, the wall time per D, the setup time, the evaluations made.
- **Not run.** Where the crate cannot evaluate a box (the star does not solve, or an l or R_s it does not support) the box is reported NOT RUN with the reason and the others go on.
  A box not finished in 1 h of wall time is stopped (`BoxTimeout`) and reported, and the rest go on.
- A failed check is a result to report. A count that differs from the stored one is reported with the box, both counts and the margins; no cause is guessed here.
  No criterion is changed after seeing data.

## Controls (`--mutate=`, each run alone on every box; exit 1 when it fired on every box it applies to)

| control | target | what it breaks | fires when |
|---|---|---|---|
| `reverse`, `wrongdouble`, `misplant`, `onesided` | STORED and COUNT | the counter's own (winding2's): clockwise contour, doubling wrong, planted zero moved out of the box, one-sided factor (the identity in an upper box: n/a there) | the planted check fails in both the stored-value and the crate counts |
| `jsign`, `star_eps` | MARGIN | the crate's J entry sign; the star solved with the sign of eps flipped (#186's controls), 8 stored points per box | 10 E exceeds the margin of the counter on the stored values |
| `rs_shift`, `strip_off` | MARGIN | the scalar plane started at R_s + 1 with the strip at R_s; winding2's phase strip left out (#188's), same 8 points | same |
| `kmin_shift` | INPUT | the min Re k 1 percent off, so R_s is 1 percent of a few hundred off | R_s differs from the log's |

Effects of the controls, computed in development runs before the runs of record: see the section at the end of this file (added before the runs of record).

## Runs of record

Two lanes of one process each: lane A the odd-numbered boxes of the table above, lane B the even-numbered, then the controls. Order in `runs.txt`.

## Effects of the controls, computed in development runs before the runs of record (declared after them)

`dev_06_ctl_counter` (log, 167 s) and `dev_07_ctl_eval` (152 s) ran each control on five boxes: p7603_l2 and c075_l2 (symmetric, eps = -1 and +1), n3_l2 and h1_l2
(upper boxes), s1_l6 (l = 6, R_s 1293). Each box's unmutated numbers are in the same logs (the crate evaluations are the same). Every control fired on every box it applies to.

| control | effect on the five dev boxes (p7603_l2, c075_l2, n3_l2, h1_l2, s1_l6) |
|---|---|
| `reverse` | planted difference -2.0000, -2.0000, -1.0000, -1.0000, -2.0000 against +2, +2, +1, +1, +2 (crate and stored counts alike); windings stay 0 |
| `wrongdouble` | +1.0000, +1.0000, +2.0000, +2.0000, +1.0000 against +2, +2, +1, +1, +2 |
| `misplant` | 0.0000 (the planted zero outside the box) on all five, against the expectation; the counter asks 2 to 32 points the stored cache lacks |
| `onesided` | symmetric boxes +1.7195, +1.7195, +1.9123 (p7603_l2, c075_l2, s1_l6) against +2; **identity in an upper box** (n3_l2, h1_l2 unchanged, n/a) |
| `jsign` | phase against the stored values 2.30, 2.08, 3.14, 2.58, 3.12 rad (modulus 0.97, 0.97, 2.3, 0.33, 1.3): 10 E of 21 to 31 against margins of 5.2e-5 to 6.8e-3 |
| `star_eps` | phase 2.63, (c075_l2: the crate stops, the flipped-eps star does not solve: "more than 200000 Taylor steps"; counted as fired), 2.89, 2.98, 3.11 rad |
| `rs_shift` | phase 2.92, 2.64, **6.1e-3**, 1.97, 3.06 rad (modulus at most 2e-8): on n3_l2 the effect is 6.1e-3 rad against that box's margin 6.8e-3 (10 E = 6.1e-2), so the control fires there by a factor 9 only |
| `strip_off` | phase 2.71, 2.80, 2.95, 2.50, 1.97 rad (modulus 4e-10 to 2e-8 unchanged) |
| `kmin_shift` | R_s 401.1, 400.6, 309.1, 415.8, 1280.6 against the logs' 404.9, 404.4, 312.0, 419.7, 1293.2 |

Observed in the same development runs, before any run of record: the unmutated crate on these five boxes asks exactly the stored points (n3_l2 and h1_l2 as well), and the smallest margin
of the five is 5.15e-5 rad (s1_l6), against 10 E >= 3.1e-5.

## Results (the output file is `phase2/nonradial/i274_recount_output.txt` of the code branch, a copy is `i274_recount_output.txt` here)

- **35 of 35 boxes OK** (`run_02`, `run_03`, f64 lane, one process each, 483 s and 506 s of wall time; crate time 835 s for 6811 evaluations incl. the extra box, 0.07 s per D median,
  0.8 s at most). Crate winding 0 and planted pair +2 (22 symmetric boxes) or +1 (13 upper boxes) in every box, equal to the stored count and planted check; every max step
  and min abs D equal to the log's as printed; the counter asks **exactly winding2's stored points** in all 35 (0 asked not stored, 0 stored not asked).
- **MARGIN.** The smallest distance of any compared quantity from its threshold is 5.15e-5 rad (s1 at l = 6), then 7.33e-5 (s1 at l = 3, with the plant), 1.39e-4 (rep at l = 4),
  3.72e-4 (n1 at l = 5, with the plant), 3.80e-4 (c075 at l = 2); the other 30 boxes are above 6e-4. E (the stored phase error used) is the floor 3.1e-6 except in the 11 boxes with
  larger crate-against-stored phase: 3.13e-6 to 3.27e-6 (s1, s3, R_s 1293 to 1343), 3.78e-6 (t2_r40, R_s 1870), 7.51e-6 (t2_r80, 3717), 9.60e-6 (s2_l2, 3831), 2.51e-6 (h3_l2) is below the floor.
  The least margin / (10 E) is 1.63 (s1 at l = 6); no box is reported.
- **dd lane** (`run_07`, `dev_08_dd_vs_f64`): rep_l4, s1_l3 and s1_l6 give the same count, planted pair, margins and crate-against-stored phase (1.00e-6, 3.14e-6, 3.15e-6) in double-double; f64 against dd at
  the common points: phase 6e-13 rad, modulus 1.3e-13 at worst.
- **Controls** (`run_04`, `run_05`): `reverse`, `wrongdouble`, `misplant`, `jsign`, `star_eps`, `rs_shift`, `strip_off`, `kmin_shift` fire on 35 of 35 boxes (`star_eps` stops the crate on c075_l2:
  the flipped-eps star does not solve); **`onesided` fires on 21 of 22 symmetric boxes and does not fire on s2_l2** (planted difference +1.9746 against 2, within the 0.05 tolerance: the box is
  0.02 wide in Re s). The control is reported as not met there; nothing was changed. `reverse`, `wrongdouble` and `misplant` fire on s2_l2.
- **Extra box** (`run_06`, not in either list): #115's s1 at l = 5 (the box whose guard-1 count lost 2 pi): winding 0, planted +2, 387 points = the stored 387, margin 3.74e-4, phase 3.15e-6; OK.

## Notes

- The driver at 63fe72b ran every run of record. After them only `--collect` was edited (the extra box's rows, a numeric controls table, the result line); `run_box` is unchanged.
  `i274_recount_output.txt` is made by that collector from `results/`; `collect.rc` is 1 because of the `onesided` row; `dev_09_collect_mut_missing` shows `--collect --mutate=missing` exit 1.
- `dev_04_boxtable` failed (a `|` in the stored text broke a split) and was rerun as `dev_05`. Two redundant background waiters were started; they only waited for exit codes.
- `dev_01` to `dev_09`, `dev_launch_*.out` and `launch_*.out` are development and launcher output; `results_dev/`, `jsonl_dev/` hold the development counts (not records).
