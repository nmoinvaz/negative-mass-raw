# I313-mac: the frozen refit of family G's settled-mass relation tested blind on a route of leverage 0.4 to 1.0 (D = 4, δ = 1e-8)

Machine: the coordinator's Mac (Apple M5, macOS, shared and heavily loaded), numba one thread per process (`NUMBA_NUM_THREADS=1`), `nice -n 10`, at most 2 processes; Python `~/Source/negative-mass/.venv/bin/python`.
Runner negative-mass-mac-i313 on the claude-me2 account. Issue https://github.com/nmoinvaz/negative-mass/issues/313 ("Test the frozen settled-mass refit on a route of leverage 0.4 to 1.0").
Worktree `~/Source/negative-mass-i313`, branch `wip/i313-moderate-route` from main (d799aa0). Code: `notes/wormhole_evolution/settled_mass_route5.py` (to be written; a driver over #305's `settled_mass_route4.py`, #295's `settled_mass_route3.py`,
#283's `settled_mass_route.py` and everything below them, all unchanged). Status words as in AGENTS.md: every mass and every member parameter here is *numerical evidence*.

This file is written in stages. **Stage 1 (this commit, before any run of #313, the development scan and the retune included): the frozen refit restated, what was known before the rule, the choice rule, the bars, the planted cases and the post hoc readings.**
Stage 2 (the route chosen by the rule, the mutations with their computed effects) is appended after the development set and before the runs of record. Nothing in stage 1 is edited after it is committed.
Every bar below is written before any member of the new route is run at h = 0.01 or 0.005, so no bar is written after P4 or FITQ has been seen on the new route.

## Stage 1: the frozen refit (#295's; not refitted here)

M_pred = r_th (M₀ + a γ₁ + b γ₁² + c ṙ_th) at h = 0.005, M₀ = 0.223086, **(a, b, c) = (0.2296318924, 0.2834170383, 0.7657657062)** (#295's raw README stage 1, `I295-mac` 305e5fee, over the fifteen members of routes B, δ, W, C).
The driver recomputes the coefficients from the stored fifteen points and compares them with the frozen ones (the check FRZ); they are not refitted after any run of this issue.
Errors of the refit on its fifteen (frozen in #295): in-sample up to 5.51e-5, leave-one-out up to 7.90e-5, the bar 6e-5.
The design of the fit is A = (γ₁, γ₁², ṙ_th) of the fifteen at h = 0.005; the leverage of a point is L = aᵀ(AᵀA)⁻¹a (largest of the fifteen 0.3932, W3; mean 0.2000; γ₁ in [0.00294, 0.07545]; ṙ_th in [−6.65e-4, +1.59e-3]).
#305 (route X, normal pulse width 1.5 at centre 4.0; leverage 0.27, 1.98, 3.06; ṙ_th −1.1e-3 to −2.7e-3): M − P4 = +9.00e-5, +2.13e-4, +1.98e-4 and the static-member fit's rms 6.5e-5, 1.46e-4, 2.09e-4 (bar 1e-4).
#295 (route N, width 0.75 at centre 3.5; leverage 0.07 to 0.33, inside the data): M − P4 = −4.8e-7, −2.2e-6, +1.2e-6. **Between the two the relation has not been tested; this issue tests it.**

## Stage 1: what was known before the rule below was written

1. I read `notes/wormhole_evolution/settled_mass_route4.md` (#305) before this README. Its recommended task 1 lists the stored h = 0.02 candidates with their leverage, and says that the rule as worded **selects (5.0, 0.7)** from the stored table (S 1.397, largest leverage 0.773), whose ṙ_th at γ₁ = 0.048 (−1.2e-3) is outside the fitted range.
2. The rule below is the issue's, word for word. What I added: the candidate set (the sixteen scanned in #295 and #305, fixed here; **no new candidate is tuned**, because a larger set would be a larger choice made by me), the leverage definition (#305's), and the reading of "ties within 0.01".
3. So the selection by the rule is known to me in advance; this README says so rather than presenting the scan as blind. The bars of stage 1 do not depend on which route is selected.

## Stage 1: the choice rule (the issue's; the scan is the stored tuning at h = 0.02, read by `scripts/devselect5.py`)

**Tuning.** A Gaussian normal pulse (x_c, w) (family G, ghost pulse unchanged, as #283's `route_family`) with B tuned to within 1 % of γ₁ = 0.012, 0.048 and 0.075 at h = 0.02 by #295's secant iteration (`devtune.py`; a point counts only if it stalls and has a member).
The tunings are the TUNED lines of `I295-mac/dev/logs/tune_xc*_h0.02*.log` and `I305-mac/dev/logs/tune_xc*_h0.02*.log`, read as stored. (3.5, 0.75) is #295's route N and is a reference, not a candidate.

**A candidate counts only if**
- (a) all three targets stall and have a member;
- (b) every one of its three leverages (at h = 0.02, in the frozen design) is at most 1.0, and the largest is at least 0.43 (10 % above the fitted maximum 0.393, the margin for the change from h = 0.02 to 0.005 and the tuning's 1 % in γ₁).

**Selected:** the counting candidate with the largest S = L₁ + L₂ + L₃; candidates whose S is within 0.01 of the largest are ordered by the smaller largest |ṙ_th| of their three points.
No condition on ṙ_th and no separation guard. D (distance from the reference curves B, W, C, N, X) and the position of ṙ_th against the fitted range are printed for information only. If no candidate counts, I stop and report instead of relaxing (a) or (b).
Leverage uses γ₁ and ṙ_th of the member at h = 0.02 only (r_th and M are not used, and the frozen refit is not evaluated at h = 0.02 or on any development point).

**After the selection.** The three points are retuned at h = 0.02 (`devtune.py`, a reproduction check of the stored B, expected equal; the stored B are used regardless), then run at h = 0.01 and 0.005 (the development set, bracket scan inside `devpoint.py`), plus one stored #305 point at h = 0.005 from its stored bracket (the reproduction point).

## Stage 1: the bars (all written before any new member is run at h = 0.01 or 0.005; mine to be overruled)

Gating checks of the analysis (`settled_mass_route5.py analyze`); a failure is reported as *not met* with its numbers, and no bar is changed after the first run of record.

| id | bar |
|---|---|
| **P4** | \|M − M_pred\| ≤ 6e-5 at all three new members, h = 0.005, M_pred the frozen refit. A failure is reported with each residual beside the member's leverage, ṙ_th and FITQ's rms (the issue's first two acceptance lines) |
| **FITQ** | the rms of the member's static-profile fit of M(r) at the slices within 0.5 of departure is ≤ 1e-4 (#283's bar), reported beside each P4 residual |
| **LEVB** | at h = 0.005, in the frozen design: every new member's leverage ≤ 1.0 and the largest ≥ 0.40 (the issue's 0.4 to 1.0; the fitted maximum is 0.3932) |
| **SEPB, SEPW, SEPC, SEPN, SEPX** | against family B (#266), routes W and C (#283), N (#295) and X (#305): the new members' r_th or ṙ_th at departure differs from the route's curve (B = 0's member plus the route's points, piecewise-linear and PCHIP, the smaller difference) at the same γ₁ by more than 5 times the point's own h difference; all three points |
| **HST** | the member at h = 0.01 and 0.005: γ₁ and r_th to 1e-4 relative, ṙ_th to 2e-5 absolute (#283's) |
| **REP5** | #305's X2 = (B, x_c, w) = (0.1695, 4.0, 1.5) at h = 0.005 from #305's stored bracket reproduces #305's stored run bit for bit: p*ₕ, the chain's series, the locus, the member rows (all but the wall time), the plateau and (γ₁, r_th, ṙ_th, t_dep) |
| inherited, as #305 | CFG, FAM0, RUNS, BR (hi − lo ≤ 1e-14), STL (T gains ≥ 2.0 per side), EVT, RC5, RC4 (first law), RC8, RH (\|plat(0.01) − plat(0.005)\| ≤ 5e-5), TGT (γ₁ within 3 % of its target), FRZ |

REP5 uses X2 (the middle point of #305's route) in place of #305's choice of #295's N3; any stored point serves, X2 is fixed here before its timing is known to me.
Not gating, printed for information: whether each ṙ_th is inside [−6.7e-4, +1.6e-3] (OUTR of #305 is not a bar of this issue, whose rule has no ṙ_th condition).

**Planted cases (before real data, the same code path; all gating):** PMEM, PDEP, PTD, PFIT, PPRED4, PSEP3 (#295's six) and PLEV (#305's), and **PBAND** (new): the LEVB decision on planted leverage triples ((0.1, 0.2, 0.39) false: largest below 0.40; (0.1, 0.2, 0.41) true; (0.2, 0.5, 1.0) true; (0.2, 0.5, 1.01) false; (0.45, 0.2, 0.1) true).
**Mutations:** each check can be broken with `--mutate=NAME`; their effects are computed on the development set and declared in stage 2.

## Stage 1: post hoc readings, declared now so that the runs of record do not change (they gate nothing)

- *Table of the nine held-out members* N1 to N3, X1 to X3, Y1 to Y3 (Y the new route): leverage in the fifteen's design, γ₁, r_th, ṙ_th, M − P4, the static fit's rms, |M − P4|/rms, and the position of ṙ_th against the fitted range.
- *M1 as in #305*: the correlation of the static fit's rms with |ṙ_th|, |r_th − 1| and |γ₁| over the stored members (the 22 of #305 plus the three new).
- *#305's post hoc description* (M − P4 = k ṙ_th with k the mean of X's three (M − P4)/ṙ_th = −0.0796) applied to Y without refitting k: the predicted and the observed miss; it is "better than no correction" if |observed − k ṙ_th| < |observed| at all three. A description of one route tested on another, not a bar.
- *Refits including the new points* (post hoc; descriptions, not tests) over the fifteen and Y, the eighteen of #295 and Y, and all twenty-one with Y.
- *#283's description of P3's residual* (K = −3.365e-3 × (r_th − family B's)) on Y, not refitted.
- *P4-ph*: the frozen constants at h = 0.01 with M₀(0.01) = 0.223095 (as #305).
- *The second roundoff realization* (`--rn`): p*ₕ bisected from another bracket (0.98 and 1.02 p*ₕ), M and M − P4 compared.

## Stage 1: procedure and stop condition

1. Scan: `scripts/devselect5.py` (the rule, the stored tunings) → `dev/devselect.1.log`; retune of the selected route at h = 0.02 (`scripts/dev_retune.sh`).
2. Driver `settled_mass_route5.py` (commands `tag`, `bracket`, `pstar`, `job`, `member`, `planted`, `analyze`; `--mutate=`, `--baseline=`, `--rn=`) written and its planted cases run before any run of the new route.
3. Development set at h = 0.01 and 0.005 (`scripts/dev_set.sh`), its analysis, the mutations on it; then stage 2; then the runs of record from the development set's brackets (expected equal to it bit for bit), the analysis of record, the mutations on the runs of record.
4. A single run not finished in 2 h of wall time is stopped and reported. Logs are never overwritten; reruns are numbered. Processes are stopped only by PID.

## Stage 1b: the scan, the selection and the retune (commit of stage 1: 6b3e0f6e; the rule of stage 1 applied unchanged)

`scripts/devselect5.py` (exit 0, `dev/devselect.1.log`; its source label prints "dev" for every candidate, cosmetic): of the sixteen stored candidates thirteen stall at all three targets and have a member, and six of those pass (b):

| (x_c, w) | leverage at γ₁ = 0.012, 0.048, 0.075 (h = 0.02) | S | largest \|ṙ_th\| | counts |
|---|---|---|---|---|
| **(5.0, 0.7)** | 0.103, 0.521, 0.773 | **1.397** | 1.18e-3 | yes, selected |
| (4.0, 1.0) | 0.109, 0.518, 0.714 | 1.341 | 1.18e-3 | yes |
| (4.5, 0.7) | 0.086, 0.342, 0.514 | 0.942 | 8.45e-4 | yes |
| (3.5, 1.0) | 0.092, 0.358, 0.490 | 0.941 | 8.80e-4 | yes |
| (2.5, 0.25) | 0.051, 0.117, 0.497 | 0.665 | 1.98e-3 | yes |
| (2.5, 0.35) | 0.052, 0.114, 0.452 | 0.618 | 1.88e-3 | yes |

Not counting: (4.5, 1.0), (5.0, 1.0), (4.0, 1.5) (largest leverage 1.13, 1.85, 3.06 above 1.0); (3.0, 0.25), (3.5, 0.35), (4.0, 0.35), (4.0, 0.7) (largest leverage 0.426, 0.358, 0.344, 0.367 below 0.43); (2.5, 0.7), (2.0, 0.35), (2.0, 0.25) (no stall at all three).
**Selected: (x_c, w) = (5.0, 0.7), S = 1.397**; the runner-up's S is 0.056 lower, so no tie. As written in stage 1, this is the selection the stored table gave before the rule was written. B = 0.0394, 0.0768, 0.09431.

**The retune** (`scripts/dev_retune.sh`, `dev/logs/tune_xc5.0_w0.7_h0.02.log`, exit 0): the three TUNED lines equal I305-mac's stored ones in every printed digit (γ₁ 0.011967, 0.047990, 0.074394; r_th, ṙ_th, M and p*ₕ at h = 0.02 equal): the tuning reproduces. The stored B are used.

## Stage 2: the route, the development set, the mutations (written after the development set and its mutations, before the runs of record)

Code at negative-mass `19866b3` (`settled_mass_route5.py`, branch `wip/i313-moderate-route`; `scripts/` here). Planted cases (`dev/planted_1.log`, exit 0): PMEM, PDEP, PTD, PFIT, PPRED4, PSEP3, PLEV and PBAND all pass, run before any run of the route. Development runs in `dev/`: the set `dev/set_a`, the analysis `dev/ana_dev2.log` (final; `ana_dev1.log` is the same without three post hoc prints added after it), the mutations `dev/mut_a/`.

### The route (selected by the stage 1 rule, stage 1b)

Family G, ghost pulse unchanged, normal pulse a Gaussian of centre x_c = 5.0 and width w = 0.7, B tuned at h = 0.02 to within 1 % of the targets:

| point | target γ₁ | B | γ₁ (h = 0.02) | r_th | ṙ_th | leverage (h = 0.02) |
|---|---|---|---|---|---|---|
| Y1 | 0.012 | 0.0394 | 0.011967 | 0.99976 | −6.22e-04 | 0.103 |
| Y2 | 0.048 | 0.0768 | 0.047990 | 1.00509 | −1.18e-03 | 0.521 |
| Y3 | 0.075 | 0.09431 | 0.074394 | 1.01502 | −4.06e-04 | 0.773 |

### What the development set found (`dev/set_a`, `dev/ana_dev2.log`; the runs of record take its brackets and are expected to equal it bit for bit)

Seven jobs (the three points at both h, 25 to 78 s each; #305's X2 at h = 0.005 from its stored bracket, 80 s), all exit 0. 31 checks (1 post hoc), **1 gating check fails (FITQ)**. **These results are seen after the bars of stage 1 were committed; they change no bar.**

| point | γ₁ (h = 0.005) | r_th | ṙ_th | leverage | M | M − P4 | static-fit rms |
|---|---|---|---|---|---|---|---|
| Y1 | 0.011968 | 0.999756 | −6.21e-04 | 0.103 | 0.225373 | +2.87e-05 | 6.86e-05 |
| Y2 | 0.047984 | 1.005090 | −1.183e-03 | 0.521 | 0.235094 | +5.28e-05 | **1.50e-04** |
| Y3 | 0.074387 | 1.015009 | −4.05e-04 | 0.771 | 0.245068 | +1.83e-05 | **2.33e-04** |

- **P4 passes** (bar 6e-5), largest +5.28e-5 (Y2): all three misses are positive. The margin of Y2 (7e-6) is smaller than M's change between h = 0.01 and 0.005 at Y2 (1.4e-5); P4-ph at h = 0.01 also passes (+2.9e-5, +5.7e-5, +1.9e-5).
- **FITQ fails** at Y2 and Y3 (bar 1e-4). Y3 has the largest rms of all 25 stored members (2.33e-4) with a small speed (ṙ_th = −4.05e-4) and a small miss; over the 25 the rms correlates with |ṙ_th| at +0.669 (+0.952 over the 22 without Y, as #305's note: reproduced).
- LEVB passes (0.103, 0.521, 0.771), SEPB, SEPW, SEPC, SEPN, SEPX pass, HST passes, RH passes, TGT passes (γ₁ within 0.8 % of its target), REP5 passes bit for bit.
- Post hoc: (M − P4)/ṙ_th is −0.0462, −0.0446, −0.0453 on Y (spread 3.4 %) against −0.0796 on X (#305): #305's description, applied to Y without refitting k, predicts misses of +4.9e-5, +9.4e-5, +3.2e-5 against the observed +2.9e-5, +5.3e-5, +1.8e-5 (better than no correction at all three; Y's own constant is 0.57 times X's).

### Changes made after stage 1 and before this section (no bar was touched)

1. The driver and the planted case PBAND were written after stage 1. OUTR (#305's), LEV and PBEL are not in this driver: the issue's rule has no ṙ_th condition, LEV is replaced by LEVB, and the verdict map of #305 is not asked for here.
2. Three post hoc prints were added to the driver after `ana_dev1.log` (the correlation over the 22 members without Y, rms against γ₁ on each route, (M − P4)/ṙ_th per route); `ana_dev2.log` has them and is otherwise equal to `ana_dev1.log`.

### Mutations (each `--mutate=NAME`, 35; the effect computed on the development set before being declared; "newly fires" = fails with the mutation and not without)

The baseline (`dev/ana_dev2.log`) fails FITQ, so FITQ cannot newly fire: it shows that it can fail by failing on the data. P4 passes at baseline, so the mutations that move the prediction fire it (and P4-ph, a post hoc check, where the h = 0.01 members are affected too).

| mutation | what it does | newly fires (declared) |
|---|---|---|
| asym_sign | #225's `fit_asym` with the sides swapped | FRZ, P4, P4-ph, PMEM, PTD, SEPC, SEPN, SEPW, SEPX, TGT |
| bisect_early | the bracket replayed after 30 steps | BR |
| coef_a | a × 1.05 in the predictions | P4, P4-ph, PPRED4 |
| coef_c | c × 0.8 in the predictions | P4, P4-ph, PPRED4 |
| crit_dm | `settled_mass.CRIT["dm"] = 2.0` | CFG |
| dep_eps | ε × 10 in `departure_time` | FRZ, P4, P4-ph, PDEP, PTD |
| drop_point | the refit over 14 points (W3 dropped) | FRZ |
| eps_h | ε × 100 at h = 0.005 only | FRZ, HST, LEVB, P4, PLEV, PTD, SEPB, SEPC, SEPN, SEPW, SEPX |
| evt_side | the pair's expansion-side event in place of the collapse-side one | EVT |
| fitq_scale | the fit rms × 10 | **nothing** (FITQ fails without a mutation) |
| flux_sign | the horizon flux with the wrong sign | RC4 |
| frz_a | the frozen a × (1 + 1e-3) in the comparison with the recomputed refit | FRZ |
| frz_m0 | M₀ = 0.223095 in the refit and the predictions | FRZ, PPRED4 |
| lev_design | the leverage computed in the design without the γ₁² column | PLEV |
| lev_hi | LEVB's upper bound 1.0 → 0.5 (shared with PBAND's decision function) | LEVB, PBAND |
| lev_lo | LEVB's lower bound 0.40 → 1.0 (shared with PBAND's decision function) | LEVB, PBAND |
| lev_rdot | ṙ_th set to 0 in the new members' leverage row | **nothing** (with ṙ_th = 0 the leverages are 0.052, 0.118, 0.546, and LEVB still passes) |
| loo_off | the leave-one-out errors replaced by the in-sample ones | FRZ |
| mass_exponent | M = r^n/2 (chain rerun) | P4, P4-ph, RC4, REP5 |
| no_rscale | the prediction without the r_th factor | P4, P4-ph, PPRED4 |
| no_run | Y1's h = 0.005 member output treated as missing | HST, LEVB, P4, RH, RUNS, SEPB, SEPC, SEPN, SEPW, SEPX, TGT |
| no_settle | the series truncated 3.0 before its end | P4, P4-ph, RC5, RC8, REP5 |
| normal_drop | the normal field dropped from the flux (#283's blind spot: it is 1e-8 of the flux) | **nothing** (blind spot) |
| rdot_nolapse | τ = t in the speed | FRZ, PTD |
| rep_off | the reproduction compared with the stored X1 | REP5 |
| rh_swap | the plateau at h = 0.005 of the next point | RH |
| sep_k | the factor 5 → 0.005 in the separation test | PSEP3 |
| sep_self | the five reference curves replaced by the new member's own values | SEPB, SEPC, SEPN, SEPW, SEPX |
| sepx_self | only route X's curve replaced by the new member's own values | SEPX |
| short_limit | K = 12 (chain rerun) | P4, P4-ph, RC5, RC8, REP5 |
| spec_w | the declared w × 1.1 | CFG |
| stl_flat | the lifetimes at 1e-6 and 1e-8 taken equal | STL |
| tgt_scale | the targets × 1.1 | TGT |
| w_scale | the normal pulse's width × 1.1 in `set_route` (the chain is rerun from the stored p*ₕ) | FAM0, HST, LEVB, P4, REP5, RH, RUNS, SEPB, SEPC, SEPN, SEPW, SEPX, TGT |
| xc_offset | the normal pulse's centre + 0.1 (chain rerun) | FAM0, HST, LEVB, P4, REP5, RH, RUNS, SEPB, SEPC, SEPN, SEPW, SEPX, TGT |

### Run procedure (the runs of record)

`scripts/make_jobs.py dev/set_a jobs_rec.txt jobs_rep.txt` (6 lines "B XC W H LO HI" for the three points at both h, brackets from the development set's `points.jsonl`; 1 line for #305's X2 at h = 0.005 from its stored bracket); `scripts/run_jobs.sh RAW/runs jobs_rec.txt LANE 2` and `scripts/run_jobs.sh RAW/runs_rep jobs_rep.txt 0 1`
(two lanes, nice 10, `NUMBA_NUM_THREADS=1`, `scripts/run_one.sh`: pstar, chain, member; logs never overwritten, reruns numbered); `python settled_mass_route5.py analyze --raw=RAW [--rn=RAW/runs_rn]`; `scripts/run_muts.sh RAW RAW/mut LANE 2 RAW/analyze_record.log`.
Second realization (post hoc): the three points at h = 0.005 with the bracket (0.98 p*ₕ, 1.02 p*ₕ) in `runs_rn/runs`.
Stop condition: a single run not finished in 2 h of wall time is stopped and reported (development: 25 to 80 s). A check that fails on the runs of record is reported as not met. Nothing above is changed after the first run of record.

## Changes made after the criteria (stage 2 stands as committed, d9fb2fc0; nothing in the bars, the route, the frozen constants or the declared mutation sets was changed after the first run of record)

1. `scripts/make_jobs_rn.py` (the second realization's brackets, 0.98 and 1.02 p*ₕ of the records), `settled_mass_route5_post.py` (post hoc: Spearman rank correlations of the miss, geometric means of |M − P4|/rms per route, margins to the bar against the changes of M, the separation in units of the point's own h difference) were written after the analysis of record;
   they read the stored runs and change none of them (`post_hoc_1.log`; `post_hoc_2.log` is the same with two header lines reworded, final). The driver was not edited after the runs of record began (negative-mass `19866b3`).
2. `settled_mass_route5_graph.py` and the figure were added after the records; they read the raw folder and gate nothing (`graph_1.log`). The note and its proposed text are in negative-mass `779a6ba`.
3. The analysis of record was run once, with `--rn` (`analyze_record.log`); the development analysis `dev/ana_dev2.log` differs from it in the path line and the second-realization block only.

## Results (the runs of record)

- 6 jobs (`jobs_rec.txt`, `rec_lane0.log`, `rec_lane1.log`), all exit 0, 24 to 78 s each, `runs/`; the X2 reproduction (`jobs_rep.txt`, `rep_lane0.log`, `runs_rep/`, exit 0, 81 s); the second realization (`jobs_rn.txt`, `rn_lane0.log`, `rn_lane1.log`, `runs_rn/`, 3 jobs exit 0, 75 to 85 s; bracket 0.98 and 1.02 times p*ₕ).
  The runs of record equal the development set (`dev/set_a`) in every printed number.
- The analysis of record: `analyze_record.log` (= the repository's `settled_mass_route5_output.txt`), exit 1: **31 checks (1 post hoc), 30 gating, 1 gating check fails: FITQ**. P4 passes: **M − P4 = +2.87e-05, +5.28e-05, +1.83e-05 (bar 6e-5)** at leverage 0.103, 0.521, 0.771; P4-ph passes too.
  LEVB, SEPB, SEPW, SEPC, SEPN, SEPX, HST, RH, REP5 (bit for bit), FRZ, TGT, RC4, RC5, RC8, BR, STL, EVT, CFG, FAM0, RUNS and the eight planted cases pass. **FITQ: rms 6.86e-05, 1.50e-04, 2.33e-04 (bar 1e-4).**
- The 35 mutations on the runs of record: `mut/<name>.log` (+ `.err`, `.rc`; `mut_lane*.log` the progress), `--baseline=analyze_record.log` (FITQ fails): **35 of 35 MATCH their declared sets**, all exit 0.
- The second realization (`--rn`): p*ₕ differs by at most 5.0e-14, M by −5.7e-07, −9.8e-07, +1.3e-06, M − P4 stays +2.81e-05, +5.18e-05, +1.96e-05.
- Post hoc (`post_hoc_2.log`): the miss is not ordered by leverage (Spearman +0.68 over nine, +0.54 over X and Y) and is ordered by |ṙ_th| over X and Y (+0.94); (M − P4)/ṙ_th is −0.0454 on Y against −0.0796 on X; |M − P4|/rms geometric means 0.055 (N), 0.226 (Y), 1.244 (X); the margin of Y2 to the bar (7.2e-6) is 0.54 of M's change between h = 0.01 and 0.005.
- Figure: `settled_mass_route5.svg`, drawn by `notes/wormhole_evolution/settled_mass_route5_graph.py` of the repository from this folder.
