# I323-mac: scan of the departure threshold eps for the 24 settled-mass members (stored runs only)

Machine: the coordinator's Mac (Apple M5, macOS, shared), one process at a time, `NUMBA_NUM_THREADS=1 nice -n 10`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/323 (from #314's recommended task 1; related #296, #305, #313).
Code: negative-mass branch `wip/i323-eps-scan`, `notes/wormhole_evolution/settled_mass_eps_scan.py` at 1dea30a (imports `settled_mass_speed.py` (#314) and
`settled_mass_eps.py` (#296) unchanged). Nothing is evolved; every number is read from the stored runs of #266, #267, #283, #295, #305, #313.

## Stage 1: criteria, written before the scan of record

The held-out nine (N1 to N3, X1 to X3, Y1 to Y3) were not read at any eps by any code of this issue before this file was committed. Development
(`dev/`) read the fifteen and B0 only (`--part=dev` does not load the nine; a guard raises if one is asked for). `dev/analyze_dryrun.1.log` runs the
record's code path with nine of the fifteen carrying the held-out names (in-sample; a code test, its numbers mean nothing).

Seen before this file, and not used to choose any criterion or code: the auto-memory index of this machine lists a line for #317 ("V3 frozen over 14 points,
X1-X3 +3.35e-5/+7.32e-5/+7.73e-5"), a parallel runner's result that this issue does not depend on. Known beforehand from #296's printed output: at eps = 1e-2 the
reference reading's refit over the fifteen predicts N1 to N3 to +6.67e-05, -9.34e-05, +1.24e-05 (so N leaves the bar at 1e-2 under the reference reading;
CTRL296 reproduces it); at eps = 1e-3 #314's residuals are N <= 2.2e-6, X1 to X3 +9.00e-05, +2.13e-04, +1.98e-04, Y +2.87e-05, +5.28e-05, +1.83e-05.
What I expect (a prior, not a criterion): X1 to X3 stay beyond 6e-5 at every eps; Y1 to Y3 leave the bar by 5e-3 to 1e-2 under the reference reading.

### What is read

Per member and per eps of the grid, from the stored `member.json` rows and `locus.npz` (the pair p* -/+ 1e-8, h = 0.005, D = 4):

| reading | what |
|---|---|
| REF | #266's `member_at` at the departure of |odd|/r = eps (r_th and gamma_1 interpolated linearly in t between the two bracketing profile slices, 0.5 apart), #267's `speed_at` there |
| WJ | the same departure; (r_th, s_th) fitted jointly from M+ and M- with equal weights (#314's `member_read`, imported); the speed is REF's |
| REF-V3, WJ-V3 | REF or WJ with B0's reading at the same eps subtracted from every member: r_th - (r_th(B0) - 1) and rdot_th - rdot_th(B0) (#296's V3, which subtracts the static member's second-order part -1.41 eps^2, -3.24 eps^2) |

Fit and prediction: P4 of #295, y = M/r_th - M_0 = a gamma_1 + b gamma_1^2 + c rdot_th, M_0 = 0.223086 fixed, plain least squares, no intercept, no weights,
over the fifteen (B0.025, B0.05, B0.1, B0.125; delta = 1e-7, 1e-9 to 1e-12 at B = 0.1; W1 to W3; C1 to C3) read at the same eps; the nine are predicted,
residual M - r_th (M_0 + a gamma_1 + b gamma_1^2 + c rdot_th). Bar 6e-5.

Grid (gating): eps = 1e-3, 2e-3, 5e-3, 1e-2. Post hoc (declared here, gates nothing): the fine grid eps = 1e-3 x 10^(k/8), k = 0..8, and 2e-2, 5e-2
(the stored rows reach t_dep(1e-1) + 1, #296); the X residual tables and the speed the miss needs; #314's S1 and S3 speed estimators against REF at each eps;
a refit with the speed read by S3.

### Declared verdicts (each can fail; a failure is a result, not something to fix)

| id | statement | count |
|---|---|---|
| PN_r@e, PX_r@e, PY_r@e | reading r at eps e: the refit over the fifteen predicts N1 to N3 (X, Y) within 6e-5 | 3 x 4 readings x 4 eps = 48 |
| NOEXIT_r | reading r: N1 to N3 and Y1 to Y3 stay within 6e-5 at every eps of the grid (else the first eps of the grid at which one leaves is reported; the fine grid refines it post hoc) | 4 |
| XCLOSE_r | reading r: at some eps of the grid all nine are within 6e-5 and the fifteen's in-sample error is at most 6e-5 (#314's recommended acceptance) | 4 |

"X's miss moves with eps": the largest |M - predicted| over X1 to X3 at the four eps; it moves if any value differs from its value at 1e-3 by more than 25 % of that
value. Reported for REF and WJ (second-order part not subtracted) and for REF-V3 and WJ-V3 (subtracted). The 25 % is mine; the tables are in the output.

### Controls (reproduction; compared at half a unit of the last printed digit of the earlier output files, parsed at run time)

| id | what |
|---|---|
| CFG, RUNS, FRZ | M_0, P4, the fifteen, the grid and the bar as declared; every member and B0 reads at every eps; the refit at eps = 1e-3 returns #295's frozen (a, b, c) to 1e-9 |
| DEPX | `settled_mass_speed.dep_own` (ln-linear departure) equals #266's `departure_time` to 3e-6 at every member and eps (independent code) |
| MONO | t_dep rises with eps at every member; t_dep(1e-2) - t_dep(1e-3) within 1.9 to 2.4 |
| REFRD | REF's t_dep, gamma_1, r_th, rdot_th of every member at eps = 1e-3 and 1e-2 equal #296's printed member table |
| B0CTRL | B0's t_dep, r_th - 1, rdot_th at the four eps equal #296's printed B0 table |
| REF15 | the fifteen's in-sample and leave-one-out errors at 1e-3 and 1e-2 equal #296's printed values (x1e-6) |
| CTRL314 | at eps = 1e-3 the refit with REF and WJ has #314's printed (a, b, c) and maximal in-sample and leave-one-out errors |
| WJ314 | at eps = 1e-3 WJ's change of gamma_1 and r_th against REF equals #314's printed table |
| CTRL314R (record only) | at eps = 1e-3 REF and WJ reproduce #314's printed residuals at N1 to N3, X1 to X3, Y1 to Y3 (18 numbers); the issue's control |
| CTRL296 (record only) | REF's residuals at N1 to N3 at eps = 1e-3, 2e-3, 5e-3, 1e-2 equal #296's printed T2 residuals |

### Planted cases (pass criteria written first; bars of mine, measured in development, all on the fifteen's code path with synthetic data)

Planted pairs: #283's planted trajectory (known drift in r_th and gamma_1) plus a second-order part of the mean throat radius, alpha (q/r_th)^2 r_th with alpha = -1.41
(#296's value at B0), a locus with tau = 0.97 t, profile rows every 0.5 in t carrying the exact static member of the planted (r_th, gamma_1), delta = 1e-8.

| id | what | bar | measured in development |
|---|---|---|---|
| PRD_REF | four planted trajectories at h = 0.01, 0.005 through `member_at` and `speed_at` at the four eps; reading against the expected reading of an independent implementation (root-found departure, linear interpolation of the planted rows, #314's S0 estimator) | t_dep 2e-5, gamma_1 1e-5, r_th 1e-7, rdot_th 5e-6 | 7.2e-6, 4.8e-10, 1.6e-8, 2.0e-6 |
| PRD_WJ | the same through WJ | gamma_1 1e-5, r_th 1e-7 | 4.3e-10, 1.6e-8 |
| PL2 | 24 planted members (15 + 9, three of them X-like with large speeds) and a planted B0; M from P4's form at the true state at eps = 1e-3; the scan (reader, refit, prediction, V3 subtraction) at the four eps and four readings against the analytic expectation (normal equations, the planted B0's analytic offset); the expected misses reach 1.7e-4 so the bar 6e-5 can fire | 1e-6 | 6.6e-8 |
| PL3 | clean planted members, a known speed deformation per group and eps (largest misses N 1e-6, 2e-5, 5e-5, 9e-5; X 1e-5, 4e-5, 8e-5, 1.5e-4; Y 2e-5, 2.2e-5, 2.4e-5, 2.1e-5): the scan returns the table; first exits N 1e-2, X 5e-3, Y none; N and X move by more than 25 %, Y does not | 1e-9 on the table | 3.6e-17 |

Reported, not gated (PRD, planted exact values): the reader's r_th differs from the exact planted value by up to 2.6e-5 (linear interpolation of the rows every 0.5 in t, which
interpolates the growing second-order part and the drift) and its speed by up to 6.0e-5 at eps = 1e-2 (the ±0.5 window of `speed_at` on the second-order part, which grows as e^{2 lambda t}).
Both are properties of the readers shared by every earlier note; they are error bars of the reading at large eps, not defects of the scan.
A uniform scale of rdot_th on all members is absorbed by the refit (#314), so `rdot_nolapse` does not fire PL2.

### Mutations (effects computed in `dev/mut_final/` on the fifteen only, 4 stand-ins held out of an 11-point fit, before the nine were read)

Baseline `dev/analyze_dev.4.log` (30 checks; the only failures are the four stand-in outcome checks at eps = 1e-2). "Newly fires" excludes outcome checks (`PD_*`, `PN/PX/PY_*`, `NOEXIT_*`,
`XCLOSE_*`), which a mutation may flip and which are printed apart, and the two record-only controls, whose expected effects are declared below.

| mutation | what it breaks | newly fires (computed in development) | record-only controls expected (declared, not computed) |
|---|---|---|---|
| `eps_swap` | the reading at 1e-2 is the one at 1e-3 | B0CTRL, DEPX, MONO, PL2, PRD_REF, PRD_WJ, REF15, REFRD | CTRL296 |
| `dep_eps` | departure criterion x10 | B0CTRL, CTRL314, FRZ, PL2, PRD_REF, PRD_WJ, REF15, REFRD, WJ314 | CTRL296, CTRL314R |
| `rdot_nolapse` | speed against t, not tau | B0CTRL, CTRL314, FRZ, PRD_REF, REF15, REFRD | none declared (a nearly uniform scale is absorbed by the refit) |
| `speed_t1` | speed read at t_dep(1e-3), not t_dep(eps) | B0CTRL, PL2, PRD_REF, REF15, REFRD | CTRL296 |
| `wj_swap` | M+ and M- swapped in WJ | CTRL314, PRD_WJ, WJ314 | CTRL314R |
| `coef_c` | prediction with c x 0.8 | CTRL314, PL2, PL3, REF15 | CTRL296, CTRL314R |
| `m0_shift` | M_0 = 0.223095 | CTRL314, FRZ, PL2, PL3, REF15 | CTRL296, CTRL314R |
| `drop_pt` | e12 dropped from the fit | CTRL314, FRZ, REF15 | CTRL296, CTRL314R |
| `no_rscale` | prediction without the r_th factor | CTRL314, PL2, PL3, REF15 | CTRL296, CTRL314R |
| `v3_sign` | B0's offset added, not subtracted | PL2 | none |
| `b0_stale` | V3 uses B0 at eps = 1e-3 for every eps | PL2 | none |
| `exit_last` | the first-exit finder returns the last exit | PL3 | none |
| `moves_never` | the "moves" classifier returns False | PL3 | none |
| `grid_drop` | the grid loses 5e-3 | CFG, PL3 | none |

14 mutations; `run_muts.sh` runs them two at a time; the record's runs are in `record/mut/`.

### Stop conditions and logs

A single analysis not finished in 1 h of wall time is stopped and reported (the development run takes about 1 min). Every log is kept, reruns are numbered.
`dev/`: `analyze_dev.1..4.log` (1: bracket error of the root finder in the planted truth; 2: first complete run; 3: planted bars tightened (PRD r_th 1e-6 to 1e-7, PL2 5e-6 to 1e-6), mutations `moves_never`, `grid_drop` added; 4: final, after the dry-run and MONO edits), `analyze_dryrun.1.log`,
`mut/` (14 mutations before the `moves_never`/`grid_drop` and `finish` edits: grid_drop crashed on a hard-coded 3), `mut_final/` (the 14 of the table), `match_check_*.log`.

## Stage 2: the record (written after the runs)

Code: `settled_mass_eps_scan.py` at 454d7a2 (record 4); the note, output of record and figure at 23ca1e5 of `wip/i323-eps-scan`.

| log | what |
|---|---|
| `record/analyze_record.1.log` | crashed in REFRD after RUNS, DEPX, MONO (REFRD compared X1 to X3 and Y1 to Y3 with #296's table, which lacks them); no residual was printed |
| `record/analyze_record.2.log` | REFRD fixed (18 members); numbers of the scan as in 3 and 4; the post hoc X table's header listed the columns in a different order than its rows |
| `record/analyze_record.3.log` | header fixed (code 6834a63) |
| `record/analyze_record.4.log` | output of record (code 454d7a2: the two mutation-only paths below); equals 3 apart from the first line and the timing |
| `record/mut/` | the 14 mutations on the record with code 6834a63 (`exits.txt`); `dep_eps` and `grid_drop` crashed there (a mutated post hoc block at eps x 10 beyond the stored rows; CTRL296 indexing the dropped eps) |
| `record/mut_2/` | `dep_eps` and `grid_drop` rerun with code 454d7a2: both MATCH |
| `record/graph.1.log` | the figure's numbers |

Result: 72 checks, 26 fail, all outcome checks (PX 16, PN and PY at 1e-2 under REF and WJ 4, NOEXIT_REF, NOEXIT_WJ, XCLOSE x 4); the 16 controls and planted checks pass, CTRL314R and CTRL296 among them.
13 of 14 mutations of the record newly fire exactly their declared sets, including the record-only controls. `wj_swap` does not: its declared CTRL314R effect is wrong (the swap flips gamma_1's sign under WJ, which the refit absorbs); it fires CTRL314, WJ314 and PRD_WJ as declared.
`rdot_nolapse` had no record-only expectation and fires CTRL296 and CTRL314R. No criterion of stage 1 was moved.
