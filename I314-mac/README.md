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
