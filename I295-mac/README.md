# I295-mac: a frozen refit of family G's settled-mass relation over fifteen points, tested blind on a third route to the member (D = 4, δ = 1e-8)

Machine: the coordinator's Mac (Apple M5, macOS, shared and heavily loaded), Python 3.14.7, numpy 2.5.4, scipy 1.18.1, numba 0.68.1, one thread per process (`NUMBA_NUM_THREADS=1`), `nice -n 10`, at most 2 processes.
Runner negative-mass-mac-i295 on the claude-me2 account. Issue https://github.com/nmoinvaz/negative-mass/issues/295 ("Test a frozen refit of G's settled-mass relation on a third route, blind").
Worktree `~/Source/negative-mass-i295`, branch `wip/i295-third-route` from main (5796a03). Code: `notes/wormhole_evolution/settled_mass_route3.py` (a thin driver over #283's `settled_mass_route.py`,
which imports #266's `settled_mass_b.py` and #267's `settled_mass_member.py` and everything below them unchanged). Status words as in AGENTS.md: every mass and every member parameter here is *numerical evidence*.

This file is written in stages. **Stage 1 (this commit, before any run of the third route, development included): the refit, frozen.** Stages 2 and 3 (the route, the criteria, the planted cases, the mutations) are
appended below it before the runs of record; nothing in stage 1 is edited after it is committed.

## Stage 1: the refit, frozen

**What.** Plain least squares over the fifteen members at h = 0.005, y = M/r_th − M₀ = a γ₁ + b γ₁² + c ṙ_th, M₀ = 0.223086 (the coordinator's ruling; B = 0's plateau is 0.2230862), no intercept, no weights.
M is the plateau mean of M_AH over the last 1.0 of x⁺ (`summary_g`, `plat1`); γ₁, r_th are the member at departure (ε = 1e-3, #266's `member_at`) and ṙ_th = dr_th/dτ there (#267's `speed_at`); all read
from the stored runs with #283's code (`settled_mass_route3.py refit`, log `refit_frozen.log` in this folder, exit 0; the raw repository was at 9f25c3e8, `I266-mac`, `I267-mac`, `I283-mac` last changed at 4df36dd4).
The fifteen points are the four B of #266 (δ = 1e-8), the five δ = 1e-7, 1e-9 … 1e-12 of #267 (B = 0.1; δ = 1e-8 is #266's B = 0.1) and the six of #283 (route W: w = 1.0 at centre 3; route C: centre 4.0 at w = 0.5).

| point | route | γ₁ | r_th | ṙ_th | M | y = M/r_th − M₀ |
|---|---|---|---|---|---|---|
| B0.025 | B | 0.002936 | 0.999446 | −9.6904e-05 | 0.22356345 | +0.00060127 |
| B0.05 | B | 0.011844 | 0.998356 | −3.0256e-04 | 0.22523526 | +0.00252006 |
| B0.1 | B | 0.048316 | 1.002878 | +6.5048e-05 | 0.23554841 | +0.01178634 |
| B0.125 | B | 0.075449 | 1.015883 | +1.5945e-03 | 0.24710048 | +0.02015113 |
| e7 | δ | 0.048511 | 1.003370 | −6.3158e-04 | 0.23519848 | +0.01132250 |
| e9 | δ | 0.048159 | 1.003477 | +5.0940e-04 | 0.23599108 | +0.01208746 |
| e10 | δ | 0.048013 | 1.004787 | +8.0517e-04 | 0.23649657 | +0.01228378 |
| e11 | δ | 0.047870 | 1.006583 | +1.0109e-03 | 0.23705124 | +0.01241501 |
| e12 | δ | 0.047732 | 1.008642 | +1.0957e-03 | 0.23762213 | +0.01250014 |
| W1 | W | 0.012003 | 0.994956 | −5.0483e-04 | 0.22436705 | +0.00241847 |
| W2 | W | 0.047982 | 0.989179 | −6.6526e-04 | 0.23174045 | +0.01118956 |
| W3 | W | 0.075022 | 0.993634 | +4.9885e-04 | 0.24079399 | +0.01925067 |
| C1 | C | 0.011989 | 0.999623 | −3.8877e-04 | 0.22548919 | +0.00248812 |
| C2 | C | 0.048006 | 1.006321 | −2.9163e-04 | 0.23599547 | +0.01142704 |
| C3 | C | 0.074833 | 1.019366 | +9.9490e-04 | 0.24727837 | +0.01949453 |

**The frozen coefficients (P4).** M_pred = r_th (M₀ + a γ₁ + b γ₁² + c ṙ_th), h = 0.005, M₀ = 0.223086:

| a | b | c |
|---|---|---|
| +0.2296318924 | +0.2834170383 | +0.7657657062 |

(#267's post hoc fit over nine points: 0.2300, 0.2724, 0.7835; #283's over ten: 0.2269, 0.3294, 0.7096. Design's singular values 0.190, 3.1e-3, 1.9e-3.) They are not refitted after any run of the third route.

**Errors of the refit, M − predicted (frozen with the coefficients).**

| point | in-sample | leave-one-out |
|---|---|---|
| B0.025 | −1.12e-06 | −1.13e-06 |
| B0.05 | −7.69e-06 | −8.14e-06 |
| B0.1 | −2.01e-05 | −2.27e-05 |
| B0.125 | −8.86e-06 | −1.44e-05 |
| e7 | −5.97e-07 | −8.06e-07 |
| e9 | −1.89e-05 | −2.19e-05 |
| e10 | −1.15e-05 | −1.44e-05 |
| e11 | −1.13e-06 | −1.54e-06 |
| e12 | +5.51e-05 | **+7.90e-05** |
| W1 | +7.99e-06 | +8.69e-06 |
| W2 | +2.79e-05 | +3.81e-05 |
| W3 | +4.57e-05 | **+7.53e-05** |
| C1 | −7.87e-06 | −8.41e-06 |
| C2 | −2.65e-05 | −3.16e-05 |
| C3 | −3.93e-05 | −5.72e-05 |
| max \|·\| | 5.51e-05 | 7.90e-05 |

Leave-one-out in y (`refit_frozen.log`) differs from these by at most 2e-6 (the factor r_th); the closed form e_k/(1 − H_kk) agrees with the explicit leave-one-out to 1.2e-17.
**What the frozen errors say about the test, written before it is run:** the bar of the issue, 6e-5, is exceeded by two of the fifteen leave-one-out errors (e12, W3: the points at the largest |ṙ_th| or γ₁ of their group) and
is 76 % of the largest leave-one-out error. A held-out point is expected to miss by about the leave-one-out size, 1e-6 to 8e-5: a miss of the new member at γ₁ = 0.075 is not surprising, and is not a ground to move the bar.
For context (form without the speed, refit over the same fifteen points, **P2'**: y = 0.2177664539 γ₁ + 0.5888595816 γ₁²): in-sample residual up to 7.7e-04, leave-one-out up to 8.7e-04. P2' gates nothing.

## Stage 1: the route, its selection rule and the development procedure (declared before any run of the third route)

The third route changes both the normal pulse's width and its centre (family G with its ghost pulse unchanged, as #283's `route_family`). The member parameters of each route are
read at h = 0.02 in development; the rule below uses (γ₁, r_th, ṙ_th) only, and **P4 and the frozen errors are not evaluated on any development point** (the coefficients are for h = 0.005, and the development runs are at 0.02).

- **Candidates** (x_c, w): (3.5, 0.75) (the issue's example), (4.0, 0.7), (4.0, 0.35), (3.5, 0.35), (2.5, 0.35), (3.5, 1.0), (2.5, 0.7), (4.5, 0.7). Each differs from family B (3.0, 0.5), route W (3.0, 1.0) and route C (4.0, 0.5) in both its width and its centre
  from at least two of the three. At most these eight are tried; the selection below is applied to those that stall.
- **Tuning**: B per candidate by #283's secant iteration in (ln B, ln γ₁) at h = 0.02 to within 1 % of each of γ₁ = 0.012, 0.048, 0.075 (the targets of the issue; `dev/devtune.py`-style, a copy of #283's with this folder's driver).
- **Stall filter**: a candidate counts only if all three targets stall at h = 0.02 (T gains ≥ 2.0 per side from 1e-6 to 1e-8) and have a member.
- **Rule**: among the candidates that stall at all three targets, the one with the largest D = min over the three γ₁ and over the three reference curves (family B, route W, route C; each at h = 0.02, interpolated in γ₁ to the candidate's γ₁ by a piecewise-linear and by a PCHIP curve, the smaller
  difference) of sqrt((Δr_th/1e-3)² + (Δṙ_th/1e-4)²). The scales 1e-3 and 1e-4 are the separations #283's smallest accepted point had (C1: Δr_th 1.3e-3, Δṙ_th −8.8e-5). Route W and C's h = 0.02 members are #283's `dev/logs/tune_*.log` TUNED lines.
- The runs of record are at h = 0.01 and 0.005 for each of the three tuned points, p*ₕ bisected, chain at p*ₕ − 1e-8, the pair p*ₕ ∓ 1e-8, member and ṙ_th as #283.

*Stages 2 and 3 (criteria, planted cases, mutations with their computed effects, run procedure) follow below, before the runs of record.*


## Stage 2: the route, the criteria, the planted cases and the mutations (written after the development runs, before any run of record)

Code at negative-mass `bf82f25` (`settled_mass_route3.py`; `scripts/` here). The development runs are in `dev/`.

### The route (selected by the stage 1 rule, `dev/devselect.1.log`, h = 0.02)

Eight candidates were tuned (`dev/logs/tune_*`, 4 to 7 runs each, 11 to 25 s per run). All stall at all three targets but (2.5, 0.7), which has a member at γ₁ = 0.012 only (no stall at 0.048 and 0.075).
D of each candidate (smallest normalized distance from family B, route W, route C over the three γ₁): (3.5, 0.75) **1.598**, (4.5, 0.7) 1.563, (4.0, 0.7) 1.415, (3.5, 1.0) 1.057, (4.0, 0.35) 0.847,
(3.5, 0.35) 0.808, (2.5, 0.35) 0.600, (2.5, 0.7) rejected. **Selected: x_c = 3.5, w = 0.75** (the issue's example; the rule picked it, it was not put in).

| point | target γ₁ | B | x_c | w | γ₁ (h = 0.02) | r_th | ṙ_th |
|---|---|---|---|---|---|---|---|
| N1 | 0.012 | 0.05648 | 3.5 | 0.75 | 0.011994 | 0.99746 | −4.35e-04 |
| N2 | 0.048 | 0.1101 | 3.5 | 0.75 | 0.047988 | 0.99872 | −4.19e-04 |
| N3 | 0.075 | 0.136 | 3.5 | 0.75 | 0.075015 | 1.00854 | +8.63e-04 |

At h = 0.02 the three points differ from route B, W and C at the same γ₁ by at least D = 1.6 in the rule's units (9e-4 in r_th, 1.3e-4 in ṙ_th at N1 against family B; 2.5e-3, 7e-5 against route W; 2.2e-3, 4.6e-5 against route C).
The rule used (γ₁, r_th, ṙ_th) only. P4 was not evaluated at h = 0.02. The candidate (3.5, 0.75) is the midpoint of routes W (3.0, 1.0) and C (4.0, 0.5) in the pulse's (x_c, w) plane;
in the member's space it also lies between them: at the same γ₁ its r_th sits at 0.54, 0.56, 0.58 of the way from W's to C's and its ṙ_th at 0.60, 0.66, 0.74 (N1, N2, N3; post hoc, from the development set at h = 0.005), i.e. close to the chord of the two routes.

### What the development set at h = 0.01 and 0.005 found (`dev/set_a`, `dev/ana_dev2.log`; the runs of record take its brackets and are expected to equal it bit for bit)

Seven jobs (the three points at both h, and #283's W3 at h = 0.005), 22 to 82 s each, all exit 0. The analysis (`dev/ana_dev1.log`, `dev/ana_dev2.log`): 26 checks, 0 gating fail (after the correction below).

| point | γ₁ (h = 0.005) | r_th | ṙ_th | M | M − P4 | (comparison) M − P3 of #267 | (comparison) M − P2' |
|---|---|---|---|---|---|---|---|
| N1 | 0.011993 | 0.997459 | −4.348e-04 | 0.224974 | −4.8e-07 | +4.4e-06 | −2.3e-04 |
| N2 | 0.047988 | 0.998724 | −4.177e-04 | 0.234137 | −2.2e-06 | +1.3e-05 | −4.6e-04 |
| N3 | 0.075017 | 1.008541 | +8.649e-04 | 0.244642 | +1.2e-06 | +2.0e-05 | −1.7e-04 |

**These residuals are seen before the runs of record; they do not change a criterion.** They are smaller than the leave-one-out errors frozen in stage 1 (up to 7.9e-5) and than the roundoff realization of the plateau (up to 2.1e-6 in #283).
The reason is the position of the new points in the fitted cloud, stated here so the result is read as what it is (post hoc statistics of the development set, printed by the analysis): leverage of N1, N2, N3 in the fit's design is 0.070, 0.189, 0.328
(the fitted points' maximum is 0.393 at W3), and the nearest fitted point is B0.05 (1.6 units of 1e-3 in γ₁, 1e-3 in r_th, 1e-4 in ṙ_th), e7 (5.1) and B0.125 (10.4). **The third route is an interpolation inside the fitted data
in (γ₁, r_th, ṙ_th) (near the chord of W and C), not an extrapolation**; a route that leaves the fitted cloud would be the harder test (a recommended task).
SEP: all three points are informative against all three curves (r_th separations 9.0e-4 (N1, route B) to 1.5e-2, at least 7e3 times the point's own h difference; ṙ_th separations 4.6e-5 (N1, route C) to 7.0e-4, at least 3e2 times).
HST: γ₁ 3.3e-5, 7.8e-6, 5.4e-6; r_th ≤ 6.5e-7; ṙ_th ≤ 4.0e-7. RH: 1.0e-5, 1.0e-5, 1.2e-5. REP3: bit for bit (after the correction below).

Changes made to my own checks after the development data and before this README (the issue's four bars are untouched):

1. **REP3** compared the whole of `member.json`, which holds the job's wall time (`secs`: 15.2 against 20.9). The first analysis (`dev/ana_dev1.log`) failed REP3 for that field alone (p*ₕ, series, locus, plateau, γ₁, r_th, ṙ_th, t_dep all equal). The comparison now excludes `secs`; nothing else.
2. The mutation script `run_muts.sh` first listed #283's 26 mutation names (a `sed` that did not rewrite the module name); the four others (`drop_point`, `frz_a`, `frz_m0`, `loo_off`) were run on their own (`dev/mut_a_lane2.log`, `dev/mut_a_lane3.log`).

### The issue's four acceptance bars, as I read them (mine to be overruled)

| bar | id | reading | gating |
|---|---|---|---|
| every new member within 6e-5 of the frozen refit | **P4** | \|M − M_pred\| ≤ 6e-5 at all three new points, h = 0.005, plateau mean over the last 1.0 of x⁺, M_pred = r_th (M₀ + a γ₁ + b γ₁² + c ṙ_th) with the stage 1 constants. A point that fails SEP is still tested (no exclusion) | yes |
| SEP against both earlier routes | **SEPW**, **SEPC**; **SEPB** | for each new point and route, r_th or ṙ_th at departure differs from the route's curve at the same γ₁ by more than 5 times the new point's own h difference (\|x(0.01) − x(0.005)\|). A route's curve is B = 0's member (γ₁ = 0) plus the route's three points of #283 (family B: its five points), interpolated by piecewise-linear and PCHIP, the smaller difference; γ₁ up to 3 % beyond a curve's last point is extrapolated (linearly, PCHIP's own extension), beyond that the point is not informative. SEPB is family B (#283's SEP; the issue says "both earlier routes": W and C), stricter | all three |
| the member at the two h agrees as in #283 | **HST** | γ₁, r_th to 1e-4 relative, ṙ_th to 2e-5 absolute, h = 0.01 against 0.005 | yes |
| reproduction of one stored #283 point bit for bit | **REP3** | W3 = (B, x_c, w) = (0.1909, 3.0, 1.0) at h = 0.005 from #283's stored bracket (0.0256, 0.0512): p*ₕ, the chain's series, the locus, the member rows (all but the job's wall time), the plateau and (γ₁, r_th, ṙ_th, t_dep) equal #283's stored run exactly | yes |

Other checks (as #283, same bars; all gating): **CFG, FAM0, RUNS, BR, STL, EVT, RC5, RC4, RC8, RH (5e-5), TGT (within 3 % of the target), FITQ**, and the planted cases below.
**FRZ** (new, gating): the refit recomputed from the stored fifteen points equals the stage 1 constants to 1e-9, M₀ equals B = 0's plateau to 1e-6, and the largest leave-one-out and in-sample errors equal 7.90e-5 and 5.51e-5 to 1e-7.
Post hoc (gate nothing): **P4-ph** (the frozen (a, b, c) at h = 0.01 with M₀(0.01) = 0.223095, not frozen at that h), the comparison columns (M − P3 of #267, M − P2'), leverage and the nearest fitted point, a refit over eighteen points, and `--rn` (the three points at h = 0.005 again from another bracket of the bisection: a second roundoff realization of the chain).
RC4 cannot see the normal field (#283: its flux is 1e-8 of dM; the mutation `normal_drop` fires nothing here too).

Planted cases (before real data, the same code path): **PMEM, PDEP, PTD** (#283's: the extraction, the departure time and the speed, with known answers; observed max errors γ₁ 5.8e-7, r_th 3.5e-9, m± 6.7e-7; t_dep 6.3e-6; speed 1.4e-6);
**PFIT** (planted data that follow the frozen refit on the fifteen real (γ₁, r_th, ṙ_th) return (a, b, c) to 2e-15 and zero leave-one-out errors; one point displaced by 1e-4 has a leave-one-out error equal to the displacement; the explicit and the hat-matrix leave-one-out agree to 1e-12);
**PPRED4** (planted data that follow P4 pass it at 1e-12; the same with a × 1.05 misses by 8.7e-4, with c × 0.8 by 1.9e-4, against the bar 6e-5);
**PSEP3** (planted points at known separations from three planted route curves: far, on one curve, 2 % and 10 % beyond the last point, 3e-6 and 6e-6 in r_th against an h difference of 1e-6: informative or not as planted).

### Mutations (each `--mutate=NAME`, 30; the effect was computed on the development set before being declared; "newly fires" = fails with the mutation and not without)

The baseline (`dev/ana_dev2.log`) fails nothing, so every check can newly fire. The mutations that act on the extraction (`asym_sign`, `dep_eps`, `eps_h`, `rdot_nolapse`) also change the fifteen stored points the refit is recomputed from, so FRZ fires with them.
P4 can fail on these data: it newly fires under `coef_a`, `coef_c`, `no_rscale`, the chain-rerun mutations and the extraction mutations.

| mutation | what it does | newly fires (declared) |
|---|---|---|
| asym_sign | #225's `fit_asym` with the sides swapped | FRZ, P4, P4-ph, PMEM, PTD, SEPC, SEPW, TGT |
| bisect_early | the bracket replayed after 30 steps | BR |
| coef_a | a × 1.05 in the predictions | P4, P4-ph, PPRED4 |
| coef_c | c × 0.8 in the predictions | P4, P4-ph, PPRED4 |
| crit_dm | `settled_mass.CRIT["dm"] = 2.0` | CFG |
| dep_eps | ε × 10 in `departure_time` | FITQ, FRZ, P4, P4-ph, PDEP, PTD |
| drop_point | the refit over 14 points (W3 dropped) | FRZ |
| eps_h | ε × 100 at h = 0.005 only | FITQ, FRZ, HST, P4, PTD, SEPB, SEPC, SEPW |
| evt_side | the pair's expansion-side event in place of the collapse-side one | EVT |
| fitq_scale | the fit rms × 10 | FITQ |
| flux_sign | the horizon flux with the wrong sign | RC4 |
| frz_a | the frozen a × (1 + 1e-3) in the comparison with the recomputed refit | FRZ |
| frz_m0 | M₀ = 0.223095 in the refit and the predictions | FRZ, PPRED4 |
| loo_off | the leave-one-out errors replaced by the in-sample ones | FRZ |
| mass_exponent | M = r^n/2 (chain rerun) | P4, P4-ph, RC4, REP3 |
| no_rscale | the prediction without the r_th factor | P4, P4-ph, PPRED4 |
| no_run | N1's h = 0.005 member output treated as missing | HST, P4, RH, RUNS, SEPB, SEPC, SEPW, TGT |
| no_settle | the series truncated 3.0 before its end | P4, P4-ph, RC5, RC8, REP3 |
| normal_drop | the normal field dropped from the flux (#283's blind spot: it is 1e-8 of the flux) | **nothing** (blind spot) |
| rdot_nolapse | τ = t in the speed | FRZ, PTD |
| rep_off | the reproduction compared with the stored W2 | REP3 |
| rh_swap | the plateau at h = 0.005 of the next point | RH |
| sep_k | the factor 5 → 0.005 in the separation test | PSEP3 |
| sep_self | the three reference curves replaced by the new member's own values | SEPB, SEPC, SEPW |
| short_limit | K = 12 (chain rerun) | P4, P4-ph, RC5, RC8, REP3 |
| spec_w | the declared w × 1.1 | CFG |
| stl_flat | the lifetimes at 1e-6 and 1e-8 taken equal | STL |
| tgt_scale | the targets × 1.1 | TGT |
| w_scale | the normal pulse's width × 1.1 in `set_route` (the chain is rerun from the stored p*ₕ) | FAM0, HST, P4, REP3, RH, RUNS, SEPB, SEPC, SEPW, TGT |
| xc_offset | the normal pulse's centre + 0.1 (chain rerun) | FAM0, HST, P4, REP3, RH, RUNS, SEPB, SEPC, SEPW, TGT |

### Run procedure (the runs of record)

`scripts/make_jobs.py dev/set_a jobs_rec.txt jobs_rep.txt` (6 lines "B XC W H LO HI" for the three points at both h, brackets from the development set's `points.jsonl`; 1 line for W3); `scripts/run_jobs.sh RAW/runs jobs_rec.txt LANE 2` and `scripts/run_jobs.sh RAW/runs_rep jobs_rep.txt 0 1`
(two lanes, nice 10, `NUMBA_NUM_THREADS=1`, `scripts/run_one.sh`: pstar, chain, member; logs never overwritten, reruns numbered);
`python settled_mass_route3.py analyze --raw=RAW [--rn=RAW/runs_rn]`; `scripts/run_muts.sh RAW RAW/mut LANE 2 RAW/analyze_record.log`. Stop condition: a single run not finished in 2 h of wall time is stopped and reported (development: 22 to 82 s).
A check that fails on the runs of record is reported as not met. Nothing above is changed after the first run of record.

## Changes made after the criteria (stage 2 stands as committed, 6bdd3c69; nothing in the bars, the points, the frozen constants or the declared mutation sets was changed after the first run of record)

1. A post hoc block was added to `settled_mass_route3.py` after the first analysis of record (`analyze_record.1.log`): #283's description of P3's residual (M − P3 = K (r_th − family B's), K = −3.365e-3 from its six points)
   evaluated on the new members. It gates nothing. The mutation run on the records that was in progress was stopped (my two lane scripts and their two child processes, by PID) and set aside in `mut_aborted_1/`; the analysis of record was rerun
   (`analyze_record.log`, final; `analyze_record.1.log` is the first, identical but for the block) and all 30 mutations were run again (`mut/`). The code is negative-mass `f058afd`.
2. `settled_mass_route3_graph.py` and the figure (`settled_mass_route3.svg`) were added; they read the raw folder and gate nothing.

## Results (the runs of record)

- 6 jobs (`jobs_rec.txt`, `rec_lane0.log`, `rec_lane1.log`), all exit 0, 22 to 73 s each, `runs/`; the W3 reproduction (`jobs_rep.txt`, `rep_lane0.log`, `runs_rep/`, exit 0, 83 s); the second realization (`jobs_rn.txt`, `rn_lane0.log`, `runs_rn/`, 3 jobs exit 0, 63 to 75 s).
  The runs of record equal the development set (`dev/set_a`) bit for bit in every printed number (`diff` of `dev/ana_dev2.log` and `analyze_record.1.log`: the second-realization block only).
- The analysis of record: `analyze_record.log` (= the repository's `settled_mass_route3_output.txt`), exit 0: **26 checks (1 post hoc), 0 gating checks fail**. P4: M − P4 = −4.8e-07, −2.2e-06, +1.2e-06 (N1, N2, N3; bar 6e-5). SEPW, SEPC, SEPB, HST, REP3 (bit for bit), FRZ, TGT, RH, RC4, RC5, RC8, BR, STL, EVT, FITQ, CFG, FAM0, RUNS and
  the six planted cases pass.
- The 30 mutations on the runs of record: `mut/<name>.log` (+ `.err`, `.rc`; `mut_lane*.log` the progress), `--baseline=analyze_record.log` (no check fails): **30 of 30 MATCH their declared sets**.
- The second realization (`--rn`): p*ₕ differs by at most 4.3e-15, M by +1.8e-07, +1.6e-06, −1.0e-06, M − P4 becomes −3.0e-07, −5.9e-07, +2.0e-07.
- Figure: `settled_mass_route3.svg`, drawn by `notes/wormhole_evolution/settled_mass_route3_graph.py` of the repository from this folder.
