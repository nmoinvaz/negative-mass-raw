# I318-mac: the second-order part of the departure reading across members, and e12's first-order mode

Machine: the coordinator's Mac (Apple M5, macOS, shared and heavily loaded). Issue: https://github.com/nmoinvaz/negative-mass/issues/318
Checkout: ~/Source/negative-mass-i318, branch wip/i318-second-order. Threads: at most 2 processes, nice 10, `NUMBA_NUM_THREADS=1`.
Script: `notes/wormhole_evolution/settled_mass_second.py` (a driver over #296's `settled_mass_eps.py` and #305's `settled_mass_route4.py`, unchanged).
D = 4, h = 0.005, delta = 1e-8 (stored pairs), 1e-9 (new pairs). Status words as in AGENTS.md: every number is numerical evidence.

## Stage 1: method, members, predictors and criteria (written before any Part 1 or Part 2 number was computed)

### What I knew before writing this

Read from #296's note and output: e12's in-sample error at eps = 1e-2 is +374e-6 (the fit of the nine); the delta scan's same-moment pair differences
(r_th +1.36e-4 to +1.42e-4, rdot_th +3.21e-4 to +3.28e-4 at gamma_1 = 0.048; e11 vs e12 +5.5e-5, +2.6e-4); B = 0's r_th - 1 = -1.41e-4 and rdot_th = -3.24e-4 at eps = 1e-2.
Read from #317's note: V3 residuals at X1-X3 (+3.35e-5, +7.32e-5, +7.73e-5) and the ratios that would close them (1.19, 1.41, 1.44 in rdot_th; 2.05, 3.2, 3.3 in r_th).
Looked up before declaring (two files, no analysis): the stored bisections of B = 0.1 at h = 0.005 exist from two machines, the Mac (#266, #267, #283's REP, I40-mac-review's rerun, all the same lo, hi)
and dh610 (#253, `I253-rpi5/runs/pstar_G_h0.005.json`), and their p*_h differ by about 4e-14, with brackets 5.7e-15 wide that do not overlap.
By hand, from the printed e12 numbers, the e12 reading looks like a first-order mode of about -5 % of the odd part (negative sign) and the machines' centre gives a positive one,
so **I expect the signed Part 1 prediction (P1G below) to fail on the sign**. This is a prior, not a criterion. No Part 1 predicted shift and no difference of a new pair was computed before this stage.

### The model of the first-order mode in the pair's mean (part 1)

The pair is p*_h -/+ delta. If p*_h = p_c + D, where p_c is the pair's own critical value, the unstable mode in the pair's mean has amplitude m1 = D/delta in units of the odd part
(odd = (r_b - r_a)/2, b the expansion side), because the runs carry k (D -/+ delta) e^{lambda t}. The odd part itself is insensitive to D to first order.
Effect on the reading at the departure time t_dep (|odd|/r_tuned = eps) of a pair with mean-mode amplitude m1:

- d r_th = m1 odd(t_dep) (the mean locus's throat radius carries m1 odd),
- d rdot_th = m1 rdot_local(odd)(t_dep), the same local slope in proper time that `speed_at` applies to the mean locus,
- d gamma_1 = m1 (gamma_1 of the mean profile - gamma_1 of the collapse-side run alone) at the same eps (the stored `a` and `m` readings of #266's `member_at`; first order).

Effect on the form's residual (the fit of #296 at eps = 1e-2 over its nine members, M_0 = 0.223086; y = M/r_th - M_0 = a g + b g^2 + c rdot_th):
S = -[(M_0 + a g + b g^2 + c rdot) d r_th + r_th (a + 2 b g) d gamma_1 + r_th c d rdot_th], the change of M - predicted.
The model of the effect is validated against the real reader on a planted pair (PL2). The origin of D is not in the model.

### Predictors of D from the stored bisections of one point (B = 0.1, h = 0.005)

Each bisection ends in a bracket [lo, hi] (fate -1 at lo, +1 at hi). Stored: the Mac path (`I267-mac/runs/G_B0.1/h0.005/pstar/summary.json`), the dh610 path (`I253-rpi5/runs/pstar_G_h0.005.json`).
The fate sign changes within the union of the brackets, [min lo, max hi] (the zone).

- **PA1** (the issue's words, literal): |D| <= (hi - lo)/2 of the Mac bracket. Magnitude only.
- **PA2s** (the zone, signed): D = p*_Mac - (the zone's centre), the best estimate of the Mac pair's offset from p_c if both machines' p*_h scatter about p_c equally. Signed. **This is the gating predictor.**
- **PA2b** (the zone, bound): |D| <= max(p*_Mac - min lo, max hi - p*_Mac). Magnitude only, reported.

For each of the pairs e7, B0.1 (= e8), e9, e10, e11, e12 (all share the Mac p*_h): m1 = D/delta, then the effects above at eps = 1e-3 and 1e-2.
Also reported: the m1* that reproduces e12's +374e-6 exactly, in units of PA1's, PA2s's and PA2b's D.

### Criteria, part 1

- **P1G (gating):** S(e12, PA2s, eps = 1e-2) / (+374e-6) is within [0.5, 2] (sign included). +374e-6 is the issue's number and is reproduced from the stored runs (NINE) before it is used.
- Not gating, reported: the same ratio for PA1 and PA2b (magnitude), the predicted shifts at e9, e10, e11 beside the nine's in-sample errors there, and the shifts of r_th and rdot_th.
- Not a gate: whether the first-order mode in the mean explains e12 (the model's m1* is reported; its origin is not in the data of this issue).

### Part 2: the same moment from two pairs

For each member: S = the stored pair at delta = 1e-8 (I266, I283, I295, I305, read only), N = the new pair at delta = 1e-9, **centred on the stored p*_h** (the stored `pstar/summary.json` is copied under `pstar_store/`, sha256 in `pstar_store.sha256`;
re-bisecting from the stored bracket reproduces it to the bit by #305's REP4, so the stored value is used directly). N is run by #266's `member` (`settled_mass_second.py pair`) at e = 9.
Reading: `member_at(.., eps, "m")` and `speed_at` (#266, #267, through #296's driver). Difference at the same moment:
d = reading(N, eps = 1e-3) - reading(S, eps = 1e-2), for r_th, rdot_th, gamma_1 and t_dep. B = 0's d0 is the same difference of the two readings of the stored B = 0 pair (r_th and rdot_th).
The ratios rho_r = d_r/d0_r and rho_v = d_v/d0_v. (#296 compared the delta scan's differences to B = 0's part at eps = 1e-2 (4 %); here the denominator is B = 0's d0, which is 1 % smaller.)

The seven pairs: W3 (0.1909, 3, 1), C3 (0.09576, 4, 0.5), N3 (0.136, 3.5, 0.75), B0.125 (0.125, 3, 0.5), X1 (0.09112, 4, 1.5), X2 (0.1695, 4, 1.5), X3 (0.2044, 4, 1.5), as (B, x_c, w); gamma_1 = 0.075 (W3, C3, N3, B0.125, X3), 0.048 (X2), 0.012 (X1).

### Criteria, part 2

- **PD2 (gating):** |rho_r - 1| <= 0.10 and |rho_v - 1| <= 0.10 at every one of the seven. Every ratio is printed; a ratio outside is the result "differences reported".
- **SAME (gating):** |t_dep(N, 1e-3) - t_dep(S, 1e-2)| <= 0.01 at every member (the delta scan agrees to 0.002 away from the floor).
- Reported, not gating, at X1, X2, X3: rho_v and rho_r against the ratios that would close #317's miss (1.19, 1.41, 1.44 in rdot_th; 2.05, 3.2, 3.3 in r_th), computed live from the frozen V3 fit (`I317-mac/frozen_v3.json`) and checked against those printed numbers.
- Reported, not gating: X's own part (rho_r, rho_v times B = 0's r_th - 1 and rdot_th at eps = 1e-2) subtracted in place of B = 0's, in V3's frozen fit, and the change of the residual against V3's (+3.35e-5, +7.32e-5, +7.73e-5; reproduced first, REPV3). A variant that also subtracts gamma_1's part.

### Controls (gating unless noted) and planted cases

- **CFG**: the stored runs, the copied p*_h, the new pairs' p*_h equal to the stored one bit for bit, e = 9.
- **REP318**: the stored delta = 1e-8 pairs of X1 and B0.125 rerun through `pair` (dev/rep, e = 8) equal the stored locus arrays bit for bit and the member rows (the member.json differs in its `B` field (a route tuple) and `secs`). Done in development: **equal** (X1 locus and member; B0.125 locus and rows).
- **REP296**: the delta scan's four pair differences (e7 vs B0.1, B0.1 vs e9, e9 vs e10, e10 vs e11), computed by the Part 2 code, equal #296's printed ones to the half unit of the last printed digit. B0REF: B = 0's d0 equals #296's printed readings of B = 0.
- **NINE**: e12's in-sample error at eps = 1e-2 of the nine's fit equals +374e-6 (#296's printed one, to 0.5e-6); REPV3: V3's frozen fit with B = 0's offsets reproduces #317's printed X residuals to the half unit of their last digit.
- **PL1 (planted second-order part)**: a planted pair (a throat locus r_t(t) -/+ q, odd q = Q0 delta e^{lambda t} r_t, plus a planted second-order part K_r (q/r_t)^2 in the mean, whose speed is the exact derivative, rows every 0.5 in t from the exact static member)
  for delta and delta/10, and a planted static B = 0 with K_B0, through the Part 2 code: rho_r, rho_v are recovered to 2e-3 for planted ratios 1.0, 0.7, 1.3; the ratio 1.15 fires PD2's test, 1.05 does not.
- **PL2 (planted first-order mode)**: the planted pair with a first-order mode m1 = +/-0.05 in the mean: the shifts of the real reader's r_th and rdot_th (`member_at`, `speed_at`) equal the model's to 5 % of the shift.
  gamma_1 is not planted (the planted rows come from the exact static member), so the model's d gamma_1 is not validated by PL2.

### Mutations

Each check gets a `--mutate=` whose effect is computed in a development run (the stored delta scan standing for the seven pairs; the Part 1 data are all stored) and declared in stage 2 below, before the new pairs are run.
A check that fails without a mutation cannot be newly fired. Failing checks are not edited and no bar is moved after a number is read.

### Stop and run rules

New pairs run at nice 10, one or two at a time; a run not finished in 2 h of wall time is stopped and reported. Logs are kept and never overwritten (reruns are numbered).

## Stage 1b: two corrections to stage 1, written before any analysis code was run

Both came from reading the code and the printed outputs while designing the planted cases (hand arithmetic; no number of record, and no Part 1 or Part 2 number, had been computed).

1. **The +374e-6 is the fifteen's, not the nine's.** #296's output prints e12's in-sample error +374 in the line "fifteen at eps = 0.01: (a, b, c) = +0.240502, +0.034453, +0.510037"
   (the nine of T1 and the six of #283: B 0.025, 0.05, 0.1, 0.125, e7, e9 to e12, W1-W3, C1-C3). Stage 1 said "nine". S (the shift of the form's residual) uses the fifteen's fit at eps = 1e-2,
   and NINE parses that line. Nothing else in the criteria changes (the gate is S within [0.5, 2] of +374e-6).
2. **The reading of r_th has a position-dependent interpolation artifact.** `member_at` interpolates the throat radius linearly in t between the stored rows 0.5 apart. The second-order term grows as e^{2 lambda t} (about a factor 3.2 per cell),
   so linear interpolation overestimates it by 17 % at the middle of a cell and 0 on a row, whatever the member. At eps = 1e-2 the cell position x of the departure time is 0.47 (B = 0, t = 15.234), 0.62 (W3), 0.9 (C3), 0.83 (N3, B0.125), 0.66, 0.27, 0.82 (X1-X3):
   the factors are about 1.17 (B = 0), 1.15, 1.07, 1.09, 1.13, 1.16, 1.08, so a ratio of readings differs from the ratio of parts by up to -9 %. The speed is read on a fine grid (`rdot_local` on every k/10-th slice, window +-0.5 in proper time), whose window bias (about +9.5 % for a term growing as e^{2 lambda t}) is common to every member and cancels in the ratio.
   Therefore two readings of r_th are carried, the rest being unchanged:
   - **A (the reader as is)**: `member_at`'s r_th, the one the fits and V3 use. **PD2 gates on A** for r_th (and on `speed_at` for rdot_th), as declared in stage 1. V3's own-part variant subtracts A's offsets, to be consistent with the frozen fit.
   - **B (fine)**: the mean locus's throat radius interpolated on the stored locus (every slice, spacing 0.0035 in t) at the same t_dep. Same test (|rho_r - 1| <= 0.10), **reported, not gating**: it is the physical ratio of the parts.
   - The diagnostic "interpolation factor of A at t_dep" is printed for B = 0 and the seven members (computed for the law K e^{2 lambda t} with lambda from the stored odd part; a description, not a correction).
   - PL1 is run on both: B recovers the planted ratios to 2e-3; A recovers them times the planted law's own interpolation factor, which is computed by an independent evaluation of the two bracketing planted rows (agreement to 1e-9).

## Stage 2: the development set, what it showed, a correction to my own planted check, a post hoc addition, the mutations (written before the runs of record)

**Development set.** The seven new pairs (e = 9) were run once into `dev/runs_dev/runs` (`scripts/run_pairs.sh`, exit 0 for all; the driver's `wait` returned before X3 finished, X3's own rc file is complete: fixed in the script for the record).
The analysis on it (`dev/analyze_dev.4.log`, 29 checks) therefore showed me the Part 2 and Part 1 results **before** this stage was written. The criteria of stages 1 and 1b were not changed after seeing them. The runs of record will be compared with this set bit for bit (as #305 did).
What the development set showed: SAME met (<= 0.0003); rho_v = 1.002 (X1) to 1.009 (W3, X3) at all seven, rho_r (A) 0.891 (X3) to 0.965 and (B) 0.975 to 1.029; PD2 **fails at X3 only, on r_th (A)**; B-reading inside at all seven; P1G **fails** (predicted S at e12 -172.6e-6, ratio -0.46: the sign, as I expected); PA2b's magnitude is 0.99 of +374e-6, PA1's 0.07.
REPV3 and NEED reproduce #317's printed residuals and ratios. This is the baseline against which mutations are computed; the checks that fail on it (PD2, P1G, P1A) cannot be newly fired and show that they can fail by failing.

**A mistake in my planted check, corrected before the record (the bar is unchanged).** PL1 first failed (r_th and rdot_th recovered to 7.2e-3 against the 2e-3 bar) because the planted law is K eps^2 r_t, so the ratio to B = 0's (r_t = 1) is rho r_t at the moment (r_t = 1.0058 there), not rho. The expected value now carries r_t(t_dep), and the
independent A expectation solves the departure time exactly (the reader divides by the mean's throat radius, which carries the planted part; my first expectation used r_t alone and missed by 9.4e-8 against the 1e-8 bar). The bars 2e-3 and 1e-8 are as declared; both passed after the correction. (`dev/analyze_dev.1.log` is the stage-1 partition run on the stored delta scan, kept.)

**Post hoc, added after the first development run on the seven pairs (non-gating; check LIFE).** The stored pair also carries the two runs' crossing times (`cross_a`: r = 0.75, 0.5 on the collapse side; `cross_b`: r = 2.0, 3.0 on the expansion side). With amplitudes k (delta + D) and k (delta - D) the difference
dT = T_b - T_a = const - (1/lambda) ln((delta + D)/(delta - D)), so m1 = D/delta = -tanh(lambda dev / 2), dev the deviation of dT from the linear trend over log10 delta of e7, B0.1, e9, e10, lambda = ln 10 / (T gain per decade). It does not use the departure reading.
The check LIFE (S within a factor 2 of +374e-6 for both crossing pairs) is a description on the scan, post hoc.

**Mutations and their effects, computed on the development set** (`dev/mut/`; run 4 with the sets undeclared, run 5 with the declared sets: **16 of 16 MATCH** on the second pass; the effect of `lam_off` on LIFE was first tried at lambda x 0.5 and fired nothing (the factor-2 bar is wide), so it is x 0.25).
A mutation's "newly fired" excludes the three checks that fail on the baseline (PD2, P1G, P1A).

| mutation | what it changes | newly fires |
|---|---|---|
| eps_swap | the two eps (1e-3, 1e-2) swapped in every reading | B0REF, NEED, PD2B, PL1, PL2, REP296, REPV3, SAME |
| d_sign | difference taken as S - N | B0REF, REP296 |
| b0_scale | B = 0's d0 x 1.2 | B0REF, PD2B |
| same_moment_off | the new pair read at eps = 2e-3 | B0REF, PD2B, PL1, REP296, SAME |
| plant_ratio | planted ratio x 1.15 on the X side | PL1 |
| m1_sign | the model's m1 sign flipped | LIFE, PL2 |
| dv_scale | the model's rdot_th shift x 1.2 | PL2 |
| rep_off | the REP318 locus comparison forced to fail | REP318 |
| m0_shift | M_0 + 1e-4 in the fit | NINE |
| bis_off | the rerun's lo + 1e-16 | BIS |
| zone_one_path | the zone is the Mac bracket alone | P1B |
| run_miss | W3 treated as missing | RUNS |
| cfg_e | the expected e of the new pair 8 | CFG |
| v3_coef | V3's c x 1.05 | NEED, REPV3 |
| dep_eps | #266's departure eps x 10 | B0REF, NEED, NINE, PL1, PL2, REP296, REPV3, SAME |
| lam_off | lambda x 0.25 in LIFE | LIFE |

PD2, P1G and P1A fail on the baseline, so no mutation can newly fire them; that PD2's test can fire is shown by PL1's flags (1.15 outside, 1.05 inside) and by PD2 failing at X3, and that P1G's can pass by P1B (the same code, magnitude) passing.

**Runs of record.** After this stage is committed: `scripts/run_pairs.sh <RAW>` into `runs/` (two at a time), then `analyze --raw=<RAW>` (the log `record/analyze_record.1.log`), the 16 mutations on it (`record/mut/`), the comparison of `runs/` with `dev/runs_dev/runs` (bit for bit), the figure and the note.

## Stage 3: the runs of record and their verdicts

- The seven pairs of record: `runs/<member>/h0.005/e9/member/` (`scripts/run_pairs.sh <RAW>`, exit 0 for all, 25 s each); each equals the development pair in `dev/runs_dev/runs/` bit for bit (locus arrays and member.json apart from `secs`).
- Script at negative-mass commit 19e5d18 (branch wip/i318-second-order). `record/analyze_record.1.log` is the output of record: **18 checks, 14 gating, 4 non-gating; two gating checks fail, PD2 (X3, r_th as the reader reads it, ρ_r = 0.891) and P1G (S = -172.6e-6 against +374e-6)**; P1A (non-gating) fails.
  Correction to stage 2: the development baseline had 18 checks, not 29 (`dev/analyze_dev.4.log`, `.5.log`).
- The 16 mutations on the record (`record/mut/`, `scripts/run_muts.sh`): 16 of 16 MATCH their declared sets, exit 0 (`record/mut/summary.1.txt`). `dev/mut_run1_stopped/` is a development sweep stopped when the script changed (kept, not used).
- Figure: `record/graph.2.log` (`.1` a first drawing with labels that overlapped). Note: `notes/wormhole_evolution/settled_mass_second.md`.
- Results (the note has the tables): ρ_ṙ 1.002 to 1.009 at the seven members; ρ_r on the locus's grid 0.975 to 1.029, the reader's 0.891 to 0.965; X's own part changes V3's residuals by +1.1e-6, +2.5e-7, +2.1e-6; the ratios that would close #317's miss (1.19, 1.41, 1.44) are not met.
  Part 1: PA1 -24.7e-6, PA2s -172.6e-6, PA2b -370.0e-6 against +374e-6; post hoc (crossing times) +387e-6, +427e-6.
