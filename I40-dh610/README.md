# I40-dh610: lifetime law at the Ellis threshold, D = 4, 5, 6 (bisection to p*_h, T against ln|p - p*_h|, slope against 1/W)

Machine: dh610-fedora (Fedora 45, Linux 7.3.3, Intel i7-12700, 20 threads, 62 GB), shared with choptuik-large-d (load average 14 to 22 of 20
during the development runs). At most 4 processes, one thread each, `nice -n 10`. Issues: https://github.com/nmoinvaz/negative-mass/issues/40
(and #150, whose acceptance is covered here).
Worktree `~/Source/negative-mass-i40`, branch `wip/i40-ellis-threshold`, base 3a233b6 (#39's head). Python
`~/Source/negative-mass-venv314/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, numba 0.68.1). The evolution is #39's `dn.py` and `checks.py`, unchanged
(3a233b6). The driver is `notes/wormhole_evolution/threshold.py` at **13a1301**, committed and pushed before this README and before any run of record.

**This README was written after the development runs `dev/dev_01` to `dev/dev_17` listed below and before the first run of record.** Everything under
"Declared" is the `CRIT` and `MUTATIONS` tables of `threshold.py` at 13a1301, in words. Nothing there is changed after a run of record has been
seen. A criterion that is not met is reported as not met. A control that fires on real data stops the work until the cause is known.

## Contents

```
I40-dh610/
├── README.md
├── scripts/                  make_queue.py (writes runs/queue.txt), lane.sh (one lane of the queue)
├── dev/                      development runs (kept, none edited): logs, .time (/usr/bin/time -v), .rc, scripts dev_NN_*.py
└── runs/                     runs of record
    ├── queue.txt             the queue as written (lines are removed as lanes take them; the order is in scripts/make_queue.py)
    ├── g6/                   D = 6 growth control (g6.json, job.*)
    ├── D<D>_<family>_h<h>/   one job: points.jsonl (every evolution run: phase, A, fate, T, event cell), summary.json, constraints.json,
    │                         stall.json, job.{start,log,err,time,rc,lane}
    └── mut/<name>/           the mutation runs (D = 4, family S, three h) and the mutated D = 6 growth control
```

## Rulings received (coordinator, over hc)

1. D = 6 resolutions: in the coordinator's review of #39 the growth fit at h = 0.0058 was meaningless and h <= about 0.003 worked.
2. One-sided family: option 2, **S + O + G**. S symmetric, as briefed. O pure-ghost one-sided, as briefed, reported as it is: its threshold data are the
   static wormhole to O(h^2), so it is not a generic family. **G is added by this ruling**: a one-sided ghost pulse A (tuned) plus a fixed normal pulse
   B = 0.1 on the same ray, eps = (-1, +1), at D = 4, 5, 6, with the same events, windows and bars as S. B is not tuned; a difference from 1/W is a result.
   Development findings at D = 4 are reported marked as development runs (B = 0.04: slope 0.843; B = 0.1: 0.883; B = 0.2 and 0.5: T saturates at
   5.30 and 12.20 for d <= 1e-4, "observed only, no reading").
3. **Constraint diagnostic, added by the coordinator's message** (reported, not gated, no bar, changes no declared check): for each family, D and h, max |C++| and
   max |C--| along the two runs that bracket p*_h at the end of the bisection, over the event cell's past, with the sum of the absolute values of the terms as
   the scale, and its change between h and h/2 beside the change of p*_h and of the slope. Background: C++ = r++ + f+ r+ + (r/n) sum eps phi+^2, and
   d- C++ = -(n-1)(r-/r) C++ on the evolution equations (the coordinator's sympy check), so the violation is truncation error carried along the rays.
   *Disagreement with the text:* the message says "scaled by the size of their terms as #39's C1 does"; `checks.check_C` takes max |C| unscaled. Both are reported:
   the unscaled max as C1 does, and max |C| divided by the largest sum of |terms| in the region.
4. Defaults accepted (no waiver of the 2 h stop): window [1e-11, 1e-3] (still 8 decades); G's departure from 1/W is reported as a result; at D = 6 G runs at two
   h and the third is reported as not run; **D = 6 conclusions are drawn from the h <= 0.0025 runs and the h = 0.005 runs are reported as the coarse member; if
   its p*_h or slope breaks the three-h convergence, that is reported, not fixed**.

## Development runs (kept, none edited; `dev/`)

| id | what | outcome |
|---|---|---|
| dev_01 | D = 4, h = 0.02. S: bisect to 1e-12, series p* -/+ 10^-e. O: fate scan in A | S: p*_h = 4.753e-5; T linear in ln(1/d) from d <= 1e-3.5, slopes 0.8475 (collapse), 0.8435 (expansion) against 1/W = 0.846; the bisection ended "static through X" at X = 20 with a 1.2e-11 bracket, so X must be larger. O: A = 0 collapses (T = 7.62), the fate flips between A = 0 and 0.002: **O's threshold is the static wormhole to O(h^2)** |
| dev_02 | fate scan, ghost A plus normal B on one ray, B = 0 to 0.5 | one flip each, in A between 0.0022 and 0.0032 (B = 0.04), 0.0147 and 0.0215 (0.1), 0.068 and 0.1 (0.2), 0.147 and 0.215 (0.3), 0.316 and 0.464 (0.5); the bisected A*_h at h = 0.02 (dev_03): 0.00236 (0.04), 0.01495 (0.1), 0.0683 (0.2), 0.3845 (0.5) |
| dev_03 | bisect those, D = 4, h = 0.02, series to e = 11 | B = 0.04: slope 0.843; B = 0.1: 0.883, event cell 91 cells (x+ 1.8) off the diagonal; B = 0.2, 0.5: T saturates at 5.30 and 12.20 for d <= 1e-4 (observed only) |
| dev_04 | S at D = 6, h = 0.005, 0.0025, X = 12 | rectangle too short for the series (static through X); slopes at h = 0.005 are 0.5 to 1.6 % below 1/W, at 0.0025 about 0.2 % below |
| dev_05 | S, bracket 5.7e-16, series to e = 14.5: D = 4 h = 0.02, D = 5 h = 0.00707, 0.00354, D = 6 h = 0.005, 0.0025 | **roundoff floor**: T(p) is a log law for d >= 1e-11 (D = 5, 6; 1e-12 at D = 4); below it T jitters by about 0.1 and points land on the wrong side. D = 6 collapse side is not linear above d = 1e-5. Windows set from this |
| dev_06 | planted series | first version (envelope = min to max of the fits): the truth sat on the envelope's edge; envelope widened by 2 OLS SE and the control run over 40 noise seeds |
| dev_07 | fate scan of G at D = 5, 6 | one flip between A = 0.01 and 0.0178 in both |
| dev_08, dev_09 | job pipeline, D = 4 h = 0.02, S and G, with --ed --stall --cons | G needs X > 24; the analysis runs end to end; G's series is noisy (rms 0.18 against 0.012 for S) |
| dev_10 | G at D = 5 (h = 0.00707, X = 18), D = 6 (h = 0.005, X = 15); O at D = 6 | G: X too short, slopes far above 1/W; O at D = 6 is S (steps 0.52 to 0.55 against 0.532) |
| dev_11 | S, D = 4, three h, all flags | all checks pass; slopes 0.84664, 0.84652, 0.84652 against 0.846045 (+7.1e-4, +5.6e-4, +5.6e-4); p*_h order 2.000; max C ratio 3.998, 3.941. The slopes at h = 0.01 and 0.005 agree to 1e-12 because event rows agree within one coarse row and the slope lives on a lattice of spacing about 3e-5 (checked: perturbing T by 0.003 moves the slope in the 5th digit) |
| dev_12 | G with large X: D = 5 X = 30, D = 6 X = 40 | G reaches e = 12; lifetimes at e = 12: D = 5: 20.1 (collapse), 26.5 (expansion); D = 6: 23.5, 31.2; steps per half-decade 0.82 to 1.17 (D = 5; 1/W step 0.666) and 1.2 to 1.7 (D = 6; 0.532), rising with ln(1/d). Cost: third h of G at D = 6 about 4 h |
| dev_13 | D = 6 growth control (G1 protocol at n = 4), h = 0.00289, 0.00144, X = 12 | passes: W_fit 2.160530, 2.162551 against 2.164860 (-2.0e-3, -1.07e-3), A*_h ratio 4.005 |
| dev_14 | mutations at D = 4, S, three h: theta_coef, ghost_sign, no_corrector, finder_sign, ed_event (first run unregistered, kept as `_run1_unregistered`; rerun silent: the slope does not depend on the event, kept as `_run2_silent`), bisect_loose (run 1 unregistered, kept) | theta_coef, ghost_sign, finder_sign: the bracket does not straddle, JOB fires; no_corrector fires SL at h = 0.02 and 0.01; bisect_loose fires BR, FM, RA |
| dev_15 | analyses of dev_11 and dev_14, dev_17 under their mutation, and the analysis-only mutations time_unit, pstar_off, pstar_h1 | targets below |
| dev_16 | D = 6 growth control under time_unit | G1[D=6] fails, W_fit 1.5277, 1.5292 (-29.4 % = 1/sqrt2 - 1) |
| dev_17 | ed_unit, ellis_charge, scalar_coef, data_constraint_sign at D = 4, S | ed_unit fires ED; the other three: JOB only |

Units used in development: `nm-i40-dev05-*`, `dev10-*`, `dev11-d4s`, `dev12-*`, `dev13-g6`, `dev14-*`, `dev14b-*`, `dev16-g6-time_unit`, `dev17-*` (one thread each, nice 10).

## Declared

### Families (D = n + 2, n = 2, 3, 4; a = 1, 8 pi G = 1; the static Ellis wormhole of `dn.ellis_rays`, field 0 the ghost)

| family | pulses (Gaussian in phi, kind 'phi', centre xc = 3.0, width w = 0.5, on ray '+') | eps | fate bracket for the bisection |
|---|---|---|---|
| S | ghost, amplitude p, mirrored onto ray '-' with the parity of the field | (-1) | [-0.01, 0.01] |
| O | ghost, amplitude p, ray '+' only | (-1) | [-0.01, 0.01] |
| G (added by ruling 2) | ghost, amplitude p; and a normal field (field 1) with fixed amplitude B = **0.1**, same centre, width and ray | (-1, +1) | [0.005, 0.03] |

Collapse for p < p*_h and expansion for p > p*_h (as `checks.bisect_A`). Both brackets were found in development; a bracket that does not straddle is a failed job (JOB).

### Events, the lifetime, its start and end

- Events as `dn.evolve(stop=True)`, tolerance 1e-2: **collapse** = the first row j of the x- sweep that contains a cell with r+ < -tol and r- < -tol (cell-centred);
  **expansion** = the first row whose diagonal cell has r+ > tol and r- > tol and r >= 2 (rexp). Excision r_cut = 0.05, F_cut = 25 (#39).
- **T = t = (x+ + x-)/sqrt2 at the event cell's centre.** The start is t = 0, the corner S where the data begin (the throat sphere); the pulses cross the diagonal
  at t = sqrt2 xc = 4.24 for every p, so the start only enters the constants T0 of each side. For a static throat on the diagonal t is the proper time at
  the throat. A slope in x- would be 1/(sqrt2 W) ([SH02]'s unit); the prediction tested is Paper III's slope 1/W in t.
- Alternative events for the sensitivity check ED: tol = 0.1 (rexp 2), and rexp = 3 (tol 1e-2).
- The event cell's offset from the diagonal (cells of x+, and in l = (x+ - x-)/sqrt2) is recorded for every run (`points.jsonl`: j, i) and at p*_h -/+ 1e-8
  (`stall.json`).

### Grid, bisection, series

| D | h (coarse, middle, fine) | X, family S and O | X, family G | N = X/h at the finest h |
|---|---|---|---|---|
| 4 | 0.02, 0.01, 0.005 | 28 | 28 | 5600 |
| 5 | 0.00707107 (0.01/sqrt2), 0.00353553, 0.00176777 | 18 | 22 | 10182 (S, O), 12446 (G) |
| 6 | 0.005, 0.0025, 0.00125 | 15 | 28 | 12000 (S, O); **G: the two coarsest h only** (N = 11200 at 0.0025) |

- **Not run:** G at D = 6, h = 0.00125 (X = 28 would be N = 22400; estimated 4 h, over the 2 h stop; accepted by the coordinator). Its absence is reported, and
  the p*_h order there is not computed (two h: the ratio is printed).
- h at D = 6 per ruling 4: conclusions from h <= 0.0025; h = 0.005 is the coarse member.
- Bisection to hi - lo <= **1e-14** (the brief asks for 1e-10; the roundoff floor is about 1e-12, so p*_h is meaningful to that level). p*_h = midpoint of the last bracket.
- Series: p = p*_h -/+ 10^-e, e = 3, 3.5, ..., 12 (19 values per side). Points with e > 11 are run to document the floor and are not fitted.
- Every run stops at its event (`stop=True, store=False`); the stored runs (constraints, stall, formation values) use `store=True, stop=True` and read nothing outside the event cell's past.

### Fit, error bar, criteria

- Model: T = c_side + s ln(1/|p - p*_h|), one intercept per side (collapse, expansion), a common slope s: the joint fit. Units of t.
- Windows in d = |p - p*_h|: **primary [1e-11, 1e-3] (8 decades)**, then [1e-11, 1e-4], [1e-11, 1e-5], [1e-10, 1e-3], [1e-10, 1e-4]. Fit choices = each window x {joint, collapse side alone, expansion side alone}: 15.
- **What the error bar is:** the *fit spread* is the envelope [min(s_k - 2 SE_k), max(s_k + 2 SE_k)] over the 15 fit choices, where SE_k is the OLS standard error of that fit
  (it assumes independent residuals; the residuals are the event-row quantization sqrt2 h/sqrt12 and, at the small-d end, the roundoff floor). It is a spread over
  fit choices plus a statistical term, not a resolution difference and not a rigorous enclosure. The OLS SE of the primary fit and the per-side slopes are printed.
  The resolution difference is RA.
- **SL**: 1/W lies inside the fit spread, at each D, family and h. 1/W from #195: W^2 a^2 = 1.39705243433350684, 2.98495893035176025, 4.68662054311946479 (1/W = 0.846045, 0.578803, 0.461924).
- **RA**: the primary slopes at the two finest h run agree within 0.5 % (as #39's G1).
- **PS**: p*_h at three h: Richardson order (p1 - p2)/(p2 - p3) = 2^q with q in [1.75, 2.25] (#39's band); for S also the orders from p*_h(h)/p*_h(h/2) with the continuum
  p* = 0 (the unperturbed static wormhole is exactly critical by the symmetry).
- **BR**: the bisection ended with hi - lo <= 1e-14 and no run static through X. **FM**: every series point with d >= 1e-11 ends in an event on its own side of p*_h.
- **ED**: at the middle h of each (D, family), the joint slope over [1e-11, 1e-4] for each alternative event lies inside the primary fit spread.
- **JOB**: the job finished (status done).
- Reported, not gated: the primary slope's relative deviation from 1/W, OLS SE, residual rms, the per-side slopes; formation values; stall values; constraint diagnostic; the roundoff-floor points.
- No sentence will claim novelty. Status words: the slopes and p*_h are *numerical evidence*. The prediction tested is Paper III's (notes/wormhole_largeD/README.md,
  "A prediction for threshold evolutions"); [SH02] and [ST17] made the earlier runs.

### Planted series (#150) and the sqrt2 control

- **PL**: an oracle with a known law (fate = side of p* = 4.7e-5; T = c_side + (1/W) ln(1/|p - p*|) + Gaussian noise sigma = 0.01, c = (-0.79 collapse, +4.05 expansion) from dev_01,
  rounded to the quantum q = sqrt2 h_mid of the event row) goes through the **same** `bisect`, `series`, `fit_set` and `verdict_inside` as the evolution, at each D (h_mid = 0.01, 0.00354, 0.0025).
  Noise at the level the runs show: their residual rms is the quantization q/sqrt12 = 0.0082 (D = 4, h = 0.02) to 0.0095; the plant adds sigma = 0.01 on top of the quantization.
  Pass: p* recovered to 2e-14 in all 40 noise seeds and 1/W inside the fit spread in at least 90 % of them.
- **PX**: the same series planted with slope 1/(sqrt2 W) (the time unit scaled by sqrt2, [SH02]'s x- = (t - l)/sqrt2) must be **rejected** by the comparison with 1/W (1/W outside the spread) in every seed.
- Dev result: 40 of 40 inside, p* recovered 40 of 40, rejected 40 of 40, at D = 4, 5, 6.

### D = 6 growth control (G6)

`checks.check_G1` at n = 4, before any D = 6 bisection of record: h = 0.005/sqrt3, 0.0025/sqrt3 (0.0028868, 0.0014434), X = 12, bracket 0.01, tolerance 1e-10, window |H|/W in [1e-3, 1e-2], bar 1 %
against W, the two resolutions agreeing within 0.5 % (all as #39's G1). The D = 6 jobs start only if it exits 0 (barrier in `lane.sh`). Dev: passes (dev_13).

### Mutations (`--mutate=NAME`), targets computed in dev_11 to dev_17 at D = 4, family S, three h

| mutation | what it breaks | checks that must fire (computed) |
|---|---|---|
| time_unit | T scaled by sqrt2 in the fits (and in `checks.fit_growth`) | PL, PX, SL, G6 (G6 from the mutated growth control, dev_16) |
| pstar_off | p*_h shifted by 1e-9 in the fits | FM, PL, PX, RA, SL |
| bisect_loose | bisection stopped at 1e-9 | BR, FM, RA |
| ed_unit | the alternative events timed in x- units (T/sqrt2) | ED |
| pstar_h1 | p*_h replaced by p*_h h_1/h (a first-order seed) | PS |
| no_corrector | #39: predictor-only update | SL (at h = 0.02 and 0.01; silent at 0.005) |
| theta_coef, ghost_sign, finder_sign, ellis_charge, scalar_coef, data_constraint_sign | #39's input mutations | JOB (the bracket does not straddle) |

Silent by design: the constraint diagnostic and the formation and stall tables are reports, not checks, and have no mutation. `ed_event` (the alternative event
with rexp 0.5) is not declared: its slope is the same as the primary's by design (dev_14, `_run2_silent`).

### Runs of record

- Queue `runs/queue.txt` (26 jobs plus G6 and a barrier), four lanes `nm-i40-lane1` to `lane4` (systemd user units, nice 10, one thread each), each job under `timeout 7200` (rc 124 = stopped by the 2 h limit, reported with what finished).
  Flags: all jobs `--cons --stall`; `--ed` at the middle h of each (D, family). No lane edits code while it runs.
- Estimate (dev timings at load 14 to 22): about 8 CPU-h, about 2.5 h wall at four lanes (the brief's 1 h was too short: the rectangles of G and the floor-limited series lengthen the runs).
- After the runs: mutation runs (`runs/mut/`), the analysis `threshold.py analyze --raw=runs` into `notes/wormhole_evolution/threshold_output.txt`, the note.
- Memory is only reported (`/usr/bin/time -v` in `job.time`). Nothing stops a process because of its memory.

## Expectations written before the runs of record (so that they can be wrong)

S and O at D = 4, 5: slope within about 1e-3 relative of 1/W (dev: +7e-4, +5.6e-4 at D = 4; -3e-4 to -9e-4 at D = 5, h = 0.00707). D = 6: slopes below 1/W by about 1e-3 to 3e-3 at h = 0.0025
(dev: collapse -3e-3, expansion +1e-3 in [1e-11, 1e-4]) and more at h = 0.005. p*_h of S: order 2.000. O: p*_h within a factor of a few of S's. G: slopes above 1/W by about +6 % (D = 4), +50 % (D = 5), more at D = 6, with
event cells off the diagonal; no tuning of B.

## Runs of record (appended after the runs; the text above is unchanged)

Started 2026-11-26 23:23 (four lanes `nm-i40-lane1` to `lane4`, systemd user units, `nice -n 10`, one thread each, `timeout 7200` per job), last of the 26 jobs ended 2026-11-27 01:09.
Code `threshold.py` at 13a1301, `dn.py` and `checks.py` at 3a233b6 (unchanged); the note and `threshold_output.txt` are at 2e97643 on `wip/i40-ellis-threshold`.
The queue was `scripts/queue_as_written.txt`. Every job exited 0; none reached the 2 h limit (longest 52:47). Memory is reported only: peak 10.03 GB (D = 5 G h = 0.00177).
Load average at job start 16 to 22 of 20 (shared with choptuik-large-d). G6 (`runs/g6`): rc 0, 12:34.17.

| job | rc | start | wall | cpu s | peak GB | load at start | lane | status |
|---|---|---|---|---|---|---|---|---|
| D4_G_h0.005 | rc=0 | 23:57:33 | 9:40.34 | 545 | 2.21 | 22.92 | lane4 | done |
| D4_G_h0.01 | rc=0 | 00:12:22 | 3:08.01 | 185 | 0.73 | 18.24 | lane4 | done |
| D4_G_h0.02 | rc=0 | 00:15:52 | 0:46.36 | 44 | 0.38 | 17.42 | lane1 | done |
| D4_O_h0.005 | rc=0 | 23:57:20 | 8:13.59 | 461 | 1.69 | 22.90 | lane3 | done |
| D4_O_h0.01 | rc=0 | 00:10:53 | 2:40.85 | 156 | 0.63 | 15.84 | lane1 | done |
| D4_O_h0.02 | rc=0 | 00:15:30 | 0:41.01 | 40 | 0.35 | 17.60 | lane4 | done |
| D4_S_h0.005 | rc=0 | 23:50:40 | 10:29.61 | 561 | 1.69 | 16.25 | lane1 | done |
| D4_S_h0.01 | rc=0 | 00:09:48 | 2:34.33 | 151 | 0.65 | 17.14 | lane4 | done |
| D4_S_h0.02 | rc=0 | 00:15:23 | 0:29.07 | 28 | 0.35 | 17.99 | lane1 | done |
| D5_G_h0.00176777 | rc=0 | 23:23:14 | 51:25.01 | 2860 | 10.03 | 18.39 | lane2 | done |
| D5_G_h0.00353553 | rc=0 | 23:35:47 | 14:52.55 | 852 | 2.65 | 20.27 | lane1 | done |
| D5_G_h0.00707107 | rc=0 | 00:07:13 | 2:35.01 | 152 | 0.86 | 18.22 | lane4 | done |
| D5_O_h0.00176777 | rc=0 | 23:23:16 | 34:16.15 | 1880 | 5.16 | 18.39 | lane4 | done |
| D5_O_h0.00353553 | rc=0 | 00:05:34 | 10:25.96 | 613 | 1.46 | 20.98 | lane3 | done |
| D5_O_h0.00707107 | rc=0 | 00:14:39 | 2:15.41 | 132 | 0.59 | 17.19 | lane2 | done |
| D5_S_h0.00176777 | rc=0 | 23:23:15 | 34:04.84 | 1880 | 5.16 | 18.39 | lane3 | done |
| D5_S_h0.00353553 | rc=0 | 00:01:10 | 9:43.17 | 561 | 1.43 | 20.50 | lane1 | done |
| D5_S_h0.00707107 | rc=0 | 00:13:34 | 1:48.85 | 107 | 0.60 | 19.21 | lane1 | done |
| D6_G_h0.0025 | rc=0 | 00:16:38 | 52:46.62 | 2914 | 8.19 | 17.50 | lane1 | done |
| D6_G_h0.005 | rc=0 | 00:46:59 | 9:43.07 | 537 | 2.21 | 13.55 | lane2 | done |
| D6_O_h0.00125 | rc=0 | 00:16:12 | 49:54.79 | 2750 | 7.09 | 17.57 | lane4 | done |
| D6_O_h0.0025 | rc=0 | 00:32:33 | 14:25.99 | 817 | 1.91 | 22.84 | lane2 | done |
| D6_O_h0.005 | rc=0 | 01:00:19 | 3:45.18 | 200 | 0.72 | 23.34 | lane2 | done |
| D6_S_h0.00125 | rc=0 | 00:16:00 | 47:21.62 | 2605 | 7.09 | 17.05 | lane3 | done |
| D6_S_h0.0025 | rc=0 | 00:16:55 | 15:38.72 | 864 | 1.92 | 16.79 | lane2 | done |
| D6_S_h0.005 | rc=0 | 00:56:43 | 3:36.50 | 191 | 0.71 | 22.99 | lane2 | done |

Total CPU of the 26 jobs 6.1 h (the estimate above said about 8 CPU-h; the wall time was about 1 h 46 min against 2.5 h).

- Analysis of record: `threshold_output.txt` (copy `runs/analyze_record.log`, `.time`, `.err`): **100 of 111 checks pass; 11 fail**: SL for G at every D and h run (D = 4: 3, D = 5: 3, D = 6: 2); ED for G at D = 4;
  BR for D = 5 G h = 0.00707107 (X = 22 too short, bisection ended at 2.9e-12 with "static through X"; dev_12 at X = 30 reached 5.7e-15); SL for S at D = 6, h = 0.005 (the coarse member).
  Nothing was changed after seeing them.
- Mutation runs: `runs/mut/<name>/` (D = 4, S, three h; `scripts/mut.sh`, `scripts/mut_all.sh`, units `nm-i40-mut1`, `nm-i40-mut2-g6`) and their analyses `runs/mut/analysis_*.log` (`scripts/analyze_mut.sh`):
  every mutation fires exactly its declared set (time_unit in two analyses: PL, PX, SL on the stored runs; G6 in the mutated growth control).
- Disagreements with the briefs and texts, all reported in `notes/wormhole_evolution/threshold.md`: O is not a generic family (the brief said it was); the brief's 1e-10 bisection tolerance is above the
  roundoff floor (1e-11 in |p - p*_h|); the constraint maximum stops falling at the finest h at D = 5 and 6 while p*_h and the slope keep converging; #39's `check_C` does not scale by the terms as the coordinator's
  message said; D = 6 slopes of S and O sit 0.3 to 0.5 % below 1/W at h <= 0.0025 and do not tighten between the two finest h.
- Rerun of a failed job: none. Logs of the development runs that failed or were silent are kept (`dev_14/*_run1_unregistered`, `dev_14/ed_event_run2_silent`).
