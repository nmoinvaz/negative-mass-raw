# I314-mac: independent readings of the throat speed and the member on #305's route, with their criteria (stored runs only)

Machine: the coordinator's Mac (Apple M5), runner negative-mass-mac-i314. Issue: https://github.com/nmoinvaz/negative-mass/issues/314 (from #305's recommended task 2).
Worktree `~/Source/negative-mass-i314`, branch `wip/i314-speed-estimators`; script `notes/wormhole_evolution/settled_mass_speed.py` (commit named in stage 1 below).
No new evolution is run: every number is read from the stored runs of #266 (`I266-mac`), #267 (`I267-mac`), #283 (`I283-mac`), #295 (`I295-mac`) and #305 (`I305-mac`), h = 0.005, delta = 1e-8, D = 4.

Status words as in AGENTS.md: every number is *numerical evidence*.

## Stage 1: what is declared before X1 to X3 are read by any new estimator

### The question and what the test can and cannot see

#305: the refit frozen in #295, (a, b, c) = (0.2296318924, 0.2834170383, 0.7657657062) on y = M / r_th - M_0 = a gamma_1 + b gamma_1^2 + c rdot_th (M_0 = 0.223086), misses the settled mass of
X1, X2, X3 (the Gaussian normal pulse x_c = 4.0, w = 1.5) by M - P4 = +9.00e-05, +2.13e-04, +1.98e-04 (bar 6e-5). The miss equals a coefficient of rdot_th 10.5 % below c on that route. A speed read
about 12 % too large in magnitude on that route would give the same miss. This issue reads rdot_th (and the member) again, by readings that share no code with `speed_at`, refits the fifteen with each
reading and predicts N1 to N3 (#295, held out there) and X1 to X3.

What a refit can see: it frees (a, b, c) over the fifteen, so a change of the reading that is the same for every point (a scale of rdot_th on all 21 points, an additive constant) is absorbed by the refit
(c changes by the inverse scale) and moves no prediction. Only a change that differs between the fifteen and X moves X1 to X3. This is why a uniform 12 % scale of rdot_th does not fire any prediction check
(mutation `n_speed` below acts on N only for that reason).

### The 21 stored points (h = 0.005)

| group | points | stored in |
|---|---|---|
| B | B0.025, B0.05, B0.1, B0.125 | `I266-mac/runs/G_B*/h0.005` |
| D | e7, e9, e10, e11, e12 (delta = 1e-e at B = 0.1) | `I267-mac/runs/G_B0.1/h0.005/e*` |
| W | W1, W2, W3 | `I283-mac/runs/R_B*_xc3_w1/h0.005` |
| C | C1, C2, C3 | `I283-mac/runs/R_B*_xc4_w0.5/h0.005` |
| N | N1, N2, N3 (held out in #295) | `I295-mac/runs/R_B*_xc3.5_w0.75/h0.005` |
| X | X1, X2, X3 (held out in #305) | `I305-mac/runs/R_B*_xc4_w1.5/h0.005` |

The fifteen are B, D, W, C. The settled mass M (plateau of M_AH over the last 1.0 of x+), the frozen M_0 = 0.223086, the departure criterion |odd|/r_tuned = 1e-3 (the definition of departure, #266's epsilon) and
the member's slice interpolation in t are shared with the reference reading and not varied here (the definition of departure is #296's, not this issue's).

### The readings

Every reading acts on the pair's mean r(tau) (the mean of the two runs A = p* -/+ 1e-8 on the slices both have; tau the stored proper time of the locus; t the stored coordinate time), with the departure time
t_dep recomputed in this script (|odd|/r = 1e-3, linear interpolation of ln(|odd|/r) between the two bracketing slices; #266's linear interpolation differs by at most 1.8e-6 in t) and tau_dep = tau(t_dep).
None calls `speed_at`, `pair_arrays`, `rdot_local` or `departure_time`; the reference reading is #267's `speed_at` and #266's `member_at`, taken from the stored runs as in #295 and #305.

| reading | what it reads | window / weights | variable |
|---|---|---|---|
| REF | reference: `speed_at` (local linear fit of r against tau over +-0.5, on every 14th slice, interpolated in t), `member_at` | | rdot_th = dr/dtau |
| S1 | local linear least-squares slope in **coordinate time**: dr/dt over |t - t_dep| <= 0.5, divided by the same-window slope dtau/dt (the lapse at the throat), evaluated exactly at t_dep | +-0.5 in t | dr/dtau |
| S1r | the same dr/dt without the division by dtau/dt | +-0.5 in t | dr/dt (the refit has its own coefficients) |
| S2 | local linear least-squares slope of r against tau over **twice the window** | +-1.0 in tau | dr/dtau |
| S3 | derivative at tau_dep of a **fitted model of r(tau) over the stall**: a quintic polynomial in tau - tau_dep fitted to r over tau_dep - 2.0 <= tau <= tau_dep + 0.5 | 2.5 in tau, degree 5 | dr/dtau |
| WA | member: s_th from M_+(r) - M_-(r) with **weights (r_th / r)^2** (inner radii emphasised), r_th the locus's | r = 1.25, 1.5, 2, 3, 4 r_th | gamma_1 |
| WJ | member: (r_th, s_th) **jointly** from M_+(r) and M_-(r), equal weights, starting at the locus's r_th | same radii (absolute) | gamma_1, r_th |
| WJi | member: (r_th, s_th) jointly from M_+ and M_-, weights (r_th / r)^2 with the locus's r_th fixed | same | gamma_1, r_th |

The reference member fits only s_th (the asymmetry) of the static member to M_+ - M_- with equal weights, at the locus's r_th. WA changes the weights; WJ and WJi also free r_th. The weights (r_th/r)^2 emphasise the radii
nearest the throat, where a static member should describe the state best. Each speed estimator is used with the reference member, and each member reading with the reference speed (supplementary, declared, gating
nothing: S1, S2, S3 each with WA, WJ, WJi).

Why these windows: r(tau) is smooth at departure (a degree-7 fit over [-2.5, +0.6] leaves sd 1.2e-9, the noise of the stored locus), so noise is not the issue; each estimator's error is its bias in curvature,
which for a local linear fit of half-width w is q w^2 / 10 for r''' = q, with q up to -1.9e-4 on the 18 development points (so 4.8e-6 for S1 and 1.9e-5 for S2). S3's degree-5 fit over 2.5 has no curvature bias at this order.

### The refit and the predictions

For each reading rho in {REF, S1, S1r, S2, S3, WA, WJ, WJi}: plain least squares for (a, b, c) of y = M / r_th - 0.223086 over the fifteen with that reading's (gamma_1, r_th, rdot_th) (no intercept, no weights, as #295);
prediction r_th (M_0 + a gamma_1 + b gamma_1^2 + c rdot_th) with the reading's values at the held-out points; residual M - prediction at N1 to N3 and at X1 to X3.

### Gating checks and bars (the bars are the issue's or #283's / #295's; none is moved)

| id | check | bar |
|---|---|---|
| PN_rho | N1 to N3 within the bar of the refit under reading rho (rho = REF, S1, S1r, S2, S3, WA, WJ, WJi) | 6e-5 |
| PX_rho | X1 to X3 within the bar of the refit under reading rho | 6e-5 |
| FRZ | the refit over the fifteen read here with REF equals the frozen (a, b, c) | 1e-9 |
| REFN, REFX | REF's residuals M - P4 equal the printed values of #295 (-4.77e-07, -2.15e-06, +1.21e-06) and #305 (+9.00e-05, +2.13e-04, +1.98e-04) | 1e-8, 6e-8 |
| DEP | recomputed t_dep equals #266's | 3e-6 (the interpolation convention; 1e-6 first written, corrected in development, below) |
| PAIR | the pair mean written here equals `pair_arrays` (t, tau, r, odd) | 1e-12 |
| SPD0 | #267's estimator (linear, +-0.5 in tau) written here and evaluated exactly at t_dep equals `speed_at` | 5e-6 |
| MEMREF | the member's fit written here with unit weights equals the stored fit (every third stored slice) | 1e-7 |
| PSPD_S1, S1r, S3 | each recovers a planted speed (below) | 1e-5 |
| PSPD_S2 | S2 recovers a planted speed | 3e-5 (bias q w^2/10 with w = 1.0) |
| PMEM | planted static members: WJ, WJi recover (r_th, s_th); WA and the unit-weight fit equal a grid search of their objective | 1e-7; 1e-6 |
| PPRED | planted data that follow the refit: coefficients, prediction (1e-12), failure with c x 0.8, leave-one-out of a displaced point | as stated |

PX_REF fails without a mutation (the #305 result), so no mutation can newly fire it; PPRED shows the prediction test can fail. A check that fails on the real data is reported as failed and not changed.

### The verdict map per speed estimator (from #305's task 2; defined before the record)

D15 = max over the fifteen of |rdot_rho - rdot_REF|, 'small' if at most 2 % of the rms of the fifteen's reference speeds (7.46e-4, so 1.49e-5); DX = |change| / |rdot_REF| at each of X1, X2, X3, 'large' if all three are at least 10 %.
- **reading**: PX_rho passes and D15 is small: the miss belonged to the reading;
- **reading, fifteen also change**: PX_rho passes and D15 is not small;
- **route-dependent reading**: PX_rho fails, DX is large and D15 is small;
- **form**: otherwise (the miss survives this reading).
The member readings WA, WJ, WJi have no map; they are judged by PX_rho.

The record also prints (declared here, gating nothing): each reading's speed and member at every point; the refit coefficients, in-sample and leave-one-out errors of the fifteen; the speed shift that would close each
miss under the reference refit, -(M - P4)/(r_th c), against each estimator's shift at X1, X2, X3; the supplementary combinations.

### Planted cases (through the same code path)

PSPD: for each of the 18 development points, a planted pair mean on the stored slice grid within |t - t_dep| <= 3: r(tau) the point's own degree-7 model over [tau_dep - 2.5, tau_dep + 1.2], tau(t) its cubic model of the lapse,
Gaussian noise of sd 1.24e-9 (the median over the points of the residual sd of a degree-9 fit; largest 1.86e-9), seed 314; truth dr/dtau = the model's linear coefficient (dr/dt = that times the lapse slope for S1r).
Also reported, gating nothing: the same with the curvature coefficients multiplied by 2. PMEM: exact static members (tl.member_M) of gamma_1 = 0.003, 0.012, 0.048, 0.075 with r_th = 1 + 0.005 z, at the stored radii built on a locus r_th 3e-4 above the true one.

### Development before this README

Stored runs only, so the development set is the eighteen points (the fifteen and N1 to N3); `--part=dev` of the script does not load X1 to X3 and raises if a new reading would touch them. In development I
(1) read the stored loci of the eighteen (r(tau) smoothness, noise, the lapse dtau/dt of 0.95 to 0.999, r'', r''', r'''' at t_dep) to choose the windows; (2) read the member rows' residuals by radius;
(3) tested WA, WJ, WJi on the eighteen (gamma_1 changes up to 1.6e-4, r_th up to 1.8e-4); (4) ran the whole analysis on the dev partition. Disclosed: a cache key of the member fits first collided across points
(the dev log showed gamma_1 changes of 4e-2; fixed before any log counted); the DEP bar was first 1e-6 and the dev data showed 1.8e-6 for the interpolation convention (changed to 3e-6 before this README, 1.8e-6 is the
analytic size (a/2) w (1 - w) dt of linear against exponential interpolation); the speed window of S3 and the weights of WA were written before looking at the refit's residuals under them (dev log
`dev/analyze_dev.1.log`). X1 to X3 have been read by the reference (`speed_at`, `member_at`) only, in #305; the numbers of #305 are known to me.
The mutation effects below were computed on the dev partition (checks on X are not in it).

**Expected before the record, stated so a wrong expectation is visible:** on the eighteen the four speed estimators differ from `speed_at` by at most 1.4e-5 (S2), 4.8e-6 (S3), 8e-7 (S1) and the member readings
move N1 to N3 by at most 4e-6; I therefore expect every reading to leave X1 to X3 near +9e-5 to +2e-4 (the form verdict). That is an expectation, not a criterion.

### Mutations and their effects (computed on the dev partition, `dev/mut/`, before this was written)

Each mutation breaks one input; "newly fires" is the set of checks that fail with the mutation and not without it (`--baseline` = the unmutated dev log `dev/analyze_dev.1.log`, which passes 20 of 20; `dev/analyze_dev.2.log`
is the same after the declared sets were written into the script). The code is commit 80856bd of `wip/i314-speed-estimators`; `scripts/run_muts.sh OUT LANE NLANES BASELOG PART` runs them.

| mutation | what it breaks | newly fires (dev) |
|---|---|---|
| `s1_win` | S1's window +-1.0 in t instead of +-0.5 (S1r shares it) | PSPD_S1, PSPD_S1r |
| `s1_nolapse` | S1 without the division by dtau/dt | PSPD_S1 |
| `s1_lapse_inv` | S1 multiplies by dtau/dt instead of dividing | PSPD_S1 |
| `s1r_tau` | S1r reads the slope against tau (= dr/dtau) | PSPD_S1r |
| `s2_win3` | S2's window +-3.0 in tau | PSPD_S2 |
| `s3_deg2` | S3 fits a quadratic | PSPD_S3 |
| `spd0_win` | SPD0's window +-1.0 | SPD0 |
| `tau_unit` | tau x sqrt(2) in the pair mean | PAIR, SPD0 |
| `dep_eps` | departure criterion 1e-2 in the departure time written here | DEP, SPD0, PN_S1, PN_S1r, PN_S2, PN_S3, PSPD_S1, PSPD_S1r, PSPD_S2 |
| `m0_shift` | M_0 = 0.223095 (h = 0.01's) in the refit and the prediction | FRZ, REFN, PPRED |
| `drop_pt` | e12 dropped from the fifteen | FRZ, REFN |
| `coef_c` | predictions with c x 0.8 | PN_REF, PN_S1, PN_S1r, PN_S2, PN_S3, PN_WA, PN_WJ, PN_WJi, REFN, PPRED |
| `n_speed` | N1 to N3's speeds x 1.3 (a route-dependent speed error: the refit cannot absorb it) | PN_REF, PN_S1, PN_S1r, PN_S2, PN_S3, PN_WA, PN_WJ, PN_WJi, REFN |
| `n_g1` | N1 to N3's gamma_1 x 1.05 | the same nine |
| `wa_outer` | WA with weights (r / r_th)^2 | PMEM |
| `wj_swap` | WJ, WJi fit M_- where M_+ is | PMEM |
| `memref_w` | the unit-weight fit uses (r_th / r)^2 | MEMREF, PMEM |
| `x_speed` | X1 to X3's speeds x 0.895 (record only; #305's post hoc c_eff / c) | nothing newly; every PX_rho that fails in the baseline is expected to pass |

Notes on the table. PX_rho and REFX are not in the dev partition, so no mutation's effect on them was computed before the record; on the record they are listed apart ("X-checks newly fired") and are not part of MATCH.
PX_REF fails without a mutation (#305). `x_speed` is the positive control for PX: if the speed of X1 to X3 were read 10.5 % smaller in magnitude (the hypothesis of the issue), the refit would predict them; the factor is
#305's published c_eff / c (0.895, 0.897, 0.892; 0.895 is the first), so the expected effect is computable without reading X1 to X3 with a new estimator. `n_speed` and `n_g1` fire PN for the same reason a reading
that differs between the fifteen and the held-out points would. `wa_outer` and `wj_swap` do not fire PN_WA, PN_WJ, PN_WJi (the dev run shows N1 to N3 within 6e-5 of the refit under them as well as under the declared
weights: the check on N does not distinguish the weightings; PMEM does).

### Stage 1 is closed here

Commands of the record (after this README is committed): `settled_mass_speed.py analyze` (all 21 points) to `record/analyze_record.log`, then every mutation with `--part=all` and the record log as baseline to `record/mut/`.

## Stage 2: the record

Script `settled_mass_speed.py`: record 1 at 80856bd (as declared above), record 2 at a0bc2f2 (the output of record). Commands from `notes/wormhole_evolution`: `python3 settled_mass_speed.py analyze` to `record/analyze_record.log`
(exit 1, 75 s; `record/analyze_record.1.log` is record 1), then `scripts/run_muts.sh record/mut LANE 2 record/analyze_record.log all` (18 mutations, `record/mut/`).

What changed between the records, all disclosed: (1) REFX failed in record 1 and fails in record 2 as declared: its bar (6e-8) is below half a unit of the printed last digit of #305's +2.13e-04 and +1.98e-04 (5e-7); a post hoc `REFX-ph`
with half a unit of each printed digit was added in record 2 (passes: differences +9.2e-09, -2.0e-07, -3.4e-08), REFX itself is unchanged; (2) the print of the shift that would close the miss had the wrong sign in record 1
(`-(M - P4)/(r_th c)`, written so in stage 1); record 2 prints `+(M - P4)/(r_th c)`; (3) record 2 adds a post hoc print of the fraction of the reference miss each reading closes. Every gating number of record 1 equals record 2's.

### Result

Residuals M - predicted after refitting the fifteen with each reading (bar 6e-5), `record/analyze_record.log`:

| reading | X1 | X2 | X3 | N1 to N3, largest |
|---|---|---|---|---|
| REF | +9.00e-05 | +2.13e-04 | +1.98e-04 | 2.2e-06 |
| S1 | +9.03e-05 | +2.12e-04 | +1.96e-04 | 1.9e-06 |
| S1r | +1.05e-04 | +1.78e-04 | +1.14e-04 | 8.0e-06 |
| S2 | +9.25e-05 | +2.20e-04 | +2.10e-04 | 2.3e-06 |
| S3 | +8.93e-05 | +2.11e-04 | +1.96e-04 | 2.1e-06 |
| WA | +1.00e-04 | +2.18e-04 | +2.06e-04 | 4.2e-06 |
| WJ | +3.92e-05 | +1.43e-04 | +1.83e-04 | 2.6e-06 |
| WJi | +9.02e-05 | +2.35e-04 | +2.72e-04 | 3.3e-06 |

Gating checks: 29; PN_rho pass for all 8 readings; PX_rho fail for all 8 (X1 to X3 within 6e-5: none; WJ at X1 only); REFX fails (above); every other check passes; PSPD errors 4.3e-06 (S1), 4.1e-06 (S1r), 1.9e-05 (S2), 9.0e-08 (S3).
The speed would have to shift by +1.18e-04, +2.83e-04, +2.63e-04 (10.5, 10.3, 10.8 % of |rdot_th|); S1, S2, S3 move it by at most 3.1e-06, 4.0e-05, 1.1e-05 (0.13, 1.65, 0.45 %). The map: all four speed estimators are "form (neither)".
My stage 1 expectation (every reading near +9e-5 to +2e-4) held for the speed estimators, WA and WJi; WJ at X1 (+3.9e-05) did not.

## Stage 3: amendment, Y1 to Y3 added to the held-out set (declared before any new reading touches them)

The coordinator (hc, and #314's comment "Added from #313") adds #313's three members Y1 to Y3 to the held-out set beside N1 to N3 and X1 to X3. Written after record 2 and before any reading of mine is applied to Y;
stages 1 and 2 are not edited. Y1, Y2, Y3 are the Gaussian normal pulse (x_c, w) = (5.0, 0.7) at B = 0.0394, 0.0768, 0.09431 (`I313-mac/runs/R_B*_xc5_w0.7/h0.005`), the route of #313 at leverage 0.4 to 1.0.
They do not enter the fit: the fifteen's refit under every reading is unchanged, so the residuals at N and X of record 2 must reappear bit for bit in record 3 (checked by diff).

What is added, identical in kind to the N and X checks:
- PY_rho, rho = REF, S1, S1r, S2, S3, WA, WJ, WJi: Y1 to Y3 within 6e-5 of the refit over the fifteen under reading rho (gating).
- REFY: the reference reading's residuals M - P4 at Y1 to Y3 equal #313's printed values +2.9e-05, +5.3e-05, +1.8e-05 (as quoted in #314's comment) to half a unit of the last printed digit, 5e-7 for each (two significant digits, unit 1e-6; I got this wrong for X, stage 2). Gating.
- The dev partition does not load Y (it raises as for X); the Y-checks (PY_*, REFY) join the X-checks in the list that is printed apart in the mutation runs and is not part of MATCH. The mutation effects of stage 1 are unchanged (dev partition unchanged).
- REFX-ph, which record 2 added and mutation runs counted as a newly fired check, is added to the list of X-checks that are printed apart (my omission; it made `coef_c`, `drop_pt`, `m0_shift` and `x_speed` read DIFFERENT in record 2's mutations, whose other newly fired sets match the declared ones).
- The figure carries Y1 to Y3.
No criterion, bar, reading or window changes. The verdict map stays defined for X only.

Known to me when this is written: the reference's residuals at Y (+2.9e-05, +5.3e-05, +1.8e-05, within the bar, Y2 at 88 % of it) and the whole of record 2.
**Expected before the run, stated so a wrong expectation is visible:** the speed estimators agree with `speed_at` to 1 % or better wherever the curvature of r(tau) is not far beyond the fitted points', so S1, S3 should leave Y within 6e-5 as REF does; Y2 sits 0.7e-5 from the bar, so a reading that raises its residual by more than that fails there by that margin
alone (not a statement about the reading); readings that change the member (WA, WJ, WJi) can move Y by up to a few 1e-5 (their shifts at N, at the same leverage, are 4e-6 at most).

Commands of record 3: `settled_mass_speed.py analyze` to `record/analyze_record.3.log`, then the 18 mutations with that log as baseline to `record/mut_3/` (record 2's files stay).

### Record 3 (with Y1 to Y3, stage 3), result

Script at dae4fee. `record/analyze_record.3.log` (exit 1, 56 s; 39 checks, 1 post hoc, 9 gating fail: PX_rho for the eight readings and REFX, as record 2); `dev/analyze_dev.3.log` equals `dev/analyze_dev.2.log` apart from its header. The residuals at N and X are identical to record 2's (the PN and PX lines hash equal).
REFY passes (+2.87e-05, +5.28e-05, +1.83e-05). PY_rho pass for all 8 readings, M - predicted at Y1, Y2, Y3:

| reading | Y1 | Y2 | Y3 |
|---|---|---|---|
| REF | +2.87e-05 | +5.28e-05 | +1.83e-05 |
| S1 | +2.88e-05 | +5.31e-05 | +1.89e-05 |
| S1r | +4.03e-05 | +5.31e-05 | +2.96e-06 |
| S2 | +3.03e-05 | +5.68e-05 | +2.35e-05 |
| S3 | +2.83e-05 | +5.19e-05 | +1.70e-05 |
| WA | +2.98e-05 | +4.22e-05 | +1.00e-06 |
| WJ | +9.54e-06 | +2.51e-05 | +1.26e-05 |
| WJi | +2.64e-05 | +5.11e-05 | +3.25e-05 |

My stage 3 expectation (S1, S3 within 6e-5 as REF) held; Y2 is the point nearest the bar under every reading but WJ (S2 +5.68e-05, 95 % of the bar), and no reading crosses it.
Mutations of record 3 (`record/mut_3/`, with the script of record 3): 17 of 18 newly fire exactly their declared sets; `x_speed` newly fires nothing as declared, but REFX-ph fires (an X-check, listed apart) and its stage 1 expectation (every PX_rho that fails in the baseline passes) is not met: PX_REF, PX_S1, PX_S2, PX_S3, PX_WA pass
(largest residual 1.5e-05), PX_S1r (X3 -7.1e-05), PX_WJ (X1 -5.1e-05, X2 -7.4e-05) and PX_WJi (X3 +7.8e-05) do not; the script's MATCH rule for it also required REFX (printed-value comparison) to flip, which it cannot. The X- and Y-checks that fire beside the declared sets are listed in the log lines and in the note.
Record 2's mutations (`record/mut/`) had four DIFFERENT because REFX-ph was missing from the list of X-checks printed apart (my omission, fixed in record 3). Record 2's PX/PN residuals, and the post hoc print of the closed fraction, are unchanged.

Correction: the stage 2 result table gave S3's largest N residual as 1.1e-06; the record's PN_S3 line has -6.06e-07, -2.09e-06, +1.08e-06, so it is 2.1e-06 (corrected above; the first result post on #314 repeated the 1.1e-06).
